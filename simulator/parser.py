from dataclasses import dataclass


class MachineParseError(ValueError):
    pass


@dataclass(frozen=True)
class ParsedMachine:
    name: str
    description: str
    states: list
    input_alphabet: list
    tape_alphabet: list
    initial_state: str
    final_states: list
    blank_symbol: str
    transitions: dict
    source: str


REQUIRED_KEYS = [
    "Estados",
    "Alfabeto_entrada",
    "Alfabeto_cinta",
    "Inicial",
    "Finales",
    "Blanco",
]


def parse_mt(source, name="Máquina cargada", description=""):
    sections = {}
    transitions_lines = []
    reading_transitions = False

    for raw_line in source.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "Transiciones:":
            reading_transitions = True
            continue
        if reading_transitions:
            transitions_lines.append(line)
            continue
        if ":" not in line:
            raise MachineParseError(f"Línea inválida: {raw_line}")
        key, value = line.split(":", 1)
        sections[key.strip()] = value.strip()

    missing = [key for key in REQUIRED_KEYS if key not in sections]
    if missing:
        raise MachineParseError(f"Faltan campos obligatorios: {', '.join(missing)}")
    if not transitions_lines:
        raise MachineParseError("La sección Transiciones no puede estar vacía")

    states = _split_csv(sections["Estados"])
    input_alphabet = _split_csv(sections["Alfabeto_entrada"])
    tape_alphabet = _split_csv(sections["Alfabeto_cinta"])
    final_states = _split_csv(sections["Finales"])
    initial_state = sections["Inicial"]
    blank_symbol = sections["Blanco"]

    _validate_non_empty("Estados", states)
    _validate_non_empty("Alfabeto_entrada", input_alphabet)
    _validate_non_empty("Alfabeto_cinta", tape_alphabet)
    _validate_non_empty("Finales", final_states)

    if initial_state not in states:
        raise MachineParseError("El estado inicial no pertenece al conjunto de estados")
    if any(state not in states for state in final_states):
        raise MachineParseError("Todos los estados finales deben pertenecer al conjunto de estados")
    if blank_symbol not in tape_alphabet:
        raise MachineParseError("El símbolo blanco debe pertenecer al alfabeto de cinta")
    if any(symbol not in tape_alphabet for symbol in input_alphabet):
        raise MachineParseError("El alfabeto de entrada debe estar contenido en el alfabeto de cinta")
    if blank_symbol in input_alphabet:
        raise MachineParseError("El símbolo blanco no puede pertenecer al alfabeto de entrada")

    transitions = {}
    seen = set()
    for line in transitions_lines:
        left, right = _split_transition(line)
        state, read_symbol = _parse_left(left)
        next_state, write_symbol, direction = _parse_right(right)
        if state not in states:
            raise MachineParseError(f"Estado no declarado en transición: {state}")
        if next_state not in states:
            raise MachineParseError(f"Estado destino no declarado en transición: {next_state}")
        if read_symbol not in tape_alphabet:
            raise MachineParseError(f"Símbolo leído fuera del alfabeto de cinta: {read_symbol}")
        if write_symbol not in tape_alphabet:
            raise MachineParseError(f"Símbolo escrito fuera del alfabeto de cinta: {write_symbol}")
        if direction not in {"L", "R", "S"}:
            raise MachineParseError(f"Dirección inválida: {direction}")
        key = (state, read_symbol)
        if key in seen:
            raise MachineParseError(f"Transición duplicada para ({state}, {read_symbol})")
        seen.add(key)
        transitions.setdefault(state, {})[read_symbol] = {
            "next_state": next_state,
            "write_symbol": write_symbol,
            "direction": direction,
        }

    return ParsedMachine(
        name=name,
        description=description,
        states=states,
        input_alphabet=input_alphabet,
        tape_alphabet=tape_alphabet,
        initial_state=initial_state,
        final_states=final_states,
        blank_symbol=blank_symbol,
        transitions=transitions,
        source=source,
    )


def _split_csv(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def _validate_non_empty(label, values):
    if not values:
        raise MachineParseError(f"{label} no puede estar vacío")
    if len(values) != len(set(values)):
        raise MachineParseError(f"{label} contiene valores repetidos")


def _split_transition(line):
    if "->" not in line:
        raise MachineParseError(f"Transición sin flecha: {line}")
    left, right = line.split("->", 1)
    return left.strip(), right.strip()


def _parse_left(left):
    parts = _split_csv(left)
    if len(parts) != 2:
        raise MachineParseError(f"Lado izquierdo inválido: {left}")
    return parts[0], parts[1]


def _parse_right(right):
    parts = _split_csv(right)
    if len(parts) != 3:
        raise MachineParseError(f"Lado derecho inválido: {right}")
    return parts[0], parts[1], parts[2]
