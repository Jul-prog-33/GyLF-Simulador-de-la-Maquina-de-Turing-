from dataclasses import dataclass

from .models import Execution


class InvalidInputError(ValueError):
    pass


@dataclass
class TapeCell:
    index: int
    symbol: str
    display_symbol: str
    is_head: bool


class TuringMachineSimulator:
    def __init__(self, execution):
        self.execution = execution
        self.machine = execution.machine

    @classmethod
    def create_execution(cls, machine, input_string, max_steps=100):
        input_symbols = cls._tokenize_input(machine, input_string)
        tape = {str(index): symbol for index, symbol in enumerate(input_symbols)}
        execution = Execution.objects.create(
            machine=machine,
            input_string="".join(input_symbols),
            tape=tape,
            head_position=0,
            current_state=machine.initial_state,
            max_steps=max_steps,
            history=[],
        )
        if machine.initial_state in machine.final_states:
            execution.status = Execution.ACCEPTED
            execution.save(update_fields=["status", "updated_at"])
        return execution

    @staticmethod
    def _tokenize_input(machine, input_string):
        text = input_string.strip()
        if not text:
            return []
        if "," in text:
            symbols = [symbol.strip() for symbol in text.split(",") if symbol.strip()]
            invalid = [symbol for symbol in symbols if symbol not in machine.input_alphabet]
            if invalid:
                raise InvalidInputError(f"Símbolo fuera del alfabeto de entrada: {invalid[0]}")
            return symbols
        compact = "".join(text.split())
        symbols = []
        index = 0
        alphabet = sorted(machine.input_alphabet, key=len, reverse=True)
        while index < len(compact):
            match = next((symbol for symbol in alphabet if compact.startswith(symbol, index)), None)
            if match is None:
                raise InvalidInputError(f"Símbolo fuera del alfabeto de entrada: {compact[index]}")
            symbols.append(match)
            index += len(match)
        return symbols

    def step(self):
        e = self.execution
        if e.is_finished:
            return e
        if e.steps >= e.max_steps:
            e.status = Execution.TIMEOUT
            e.save(update_fields=["status", "updated_at"])
            return e
        if e.current_state in self.machine.final_states:
            e.status = Execution.ACCEPTED
            e.save(update_fields=["status", "updated_at"])
            return e

        symbol = self._read(e.head_position)
        state_before = e.current_state
        head_before = e.head_position
        transition = self.machine.transitions.get(e.current_state, {}).get(symbol)
        if transition is None:
            e.status = Execution.REJECTED
            self._append_history(state_before, head_before, symbol, None)
            e.save(update_fields=["status", "history", "updated_at"])
            return e

        next_state = transition["next_state"]
        write_symbol = transition["write_symbol"]
        direction = transition["direction"]

        self._write(e.head_position, write_symbol)
        if direction == "L":
            e.head_position -= 1
        elif direction == "R":
            e.head_position += 1
        e.current_state = next_state
        e.steps += 1
        self._append_history(state_before, head_before, symbol, transition)

        if e.current_state in self.machine.final_states:
            e.status = Execution.ACCEPTED
        elif e.steps >= e.max_steps:
            e.status = Execution.TIMEOUT

        e.save(update_fields=["tape", "head_position", "current_state", "steps", "status", "history", "updated_at"])
        return e

    def run(self):
        while not self.execution.is_finished:
            before = self.execution.steps
            self.step()
            if self.execution.steps == before and self.execution.is_finished:
                break
        return self.execution

    def visible_tape(self, padding=5):
        tape = self.execution.tape
        used_positions = [int(pos) for pos, symbol in tape.items() if symbol != self.machine.blank_symbol]
        used_positions.append(self.execution.head_position)
        start = min(used_positions) - padding
        end = max(used_positions) + padding
        return [
            TapeCell(
                index=i,
                symbol=self._read(i),
                display_symbol=(symbol := self._read(i)),
                is_head=i == self.execution.head_position,
            )
            for i in range(start, end + 1)
        ]

    def final_tape(self):
        tape = self.execution.tape
        positions = [int(pos) for pos, symbol in tape.items() if symbol != self.machine.blank_symbol]
        if not positions:
            return ""
        return "".join(
            symbol
            for index in range(min(positions), max(positions) + 1)
            if (symbol := self._read(index)) != self.machine.blank_symbol
        )

    def _read(self, position):
        return self.execution.tape.get(str(position), self.machine.blank_symbol)

    def _write(self, position, symbol):
        key = str(position)
        if symbol == self.machine.blank_symbol:
            self.execution.tape.pop(key, None)
        else:
            self.execution.tape[key] = symbol

    def _append_history(self, state, head, symbol, transition):
        item = {
            "step": self.execution.steps,
            "state": state,
            "head": head,
            "read": symbol,
            "transition": transition,
        }
        history = list(self.execution.history)
        history.append(item)
        self.execution.history = history[-100:]
