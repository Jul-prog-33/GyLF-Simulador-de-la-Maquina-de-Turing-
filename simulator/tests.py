from pathlib import Path

from django.test import TestCase

from .engine import TuringMachineSimulator
from .models import Execution, TuringMachine
from .parser import MachineParseError, parse_mt
from .views import machine_diagnostics


BASE_DIR = Path(__file__).resolve().parent.parent


class MachineTestMixin:
    def load_machine(self, filename):
        source = (BASE_DIR / "machines" / filename).read_text(encoding="utf-8")
        parsed = parse_mt(source, name=filename)
        return TuringMachine.objects.create(
            name=parsed.name,
            description=parsed.description,
            states=parsed.states,
            input_alphabet=parsed.input_alphabet,
            tape_alphabet=parsed.tape_alphabet,
            initial_state=parsed.initial_state,
            final_states=parsed.final_states,
            blank_symbol=parsed.blank_symbol,
            transitions=parsed.transitions,
            source=parsed.source,
        )

    def run_machine(self, filename, input_string, max_steps=1000):
        machine = self.load_machine(filename)
        execution = TuringMachineSimulator.create_execution(machine, input_string, max_steps=max_steps)
        simulator = TuringMachineSimulator(execution)
        simulator.run()
        execution.refresh_from_db()
        return execution, simulator.final_tape()


class ParserTests(TestCase):
    def test_parser_reads_valid_machine(self):
        source = (BASE_DIR / "machines" / "0n1n.mt").read_text(encoding="utf-8")
        parsed = parse_mt(source, name="0n1n")
        self.assertEqual(parsed.initial_state, "q0")
        self.assertIn("qf", parsed.final_states)
        self.assertEqual(parsed.transitions["q0"]["0"]["next_state"], "q1")

    def test_parser_rejects_blank_outside_tape_alphabet(self):
        source = """Estados: q0,qf
Alfabeto_entrada: 0
Alfabeto_cinta: 0
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> qf,0,S
"""
        with self.assertRaises(MachineParseError):
            parse_mt(source)

    def test_parser_rejects_duplicate_transition(self):
        source = """Estados: q0,qf
Alfabeto_entrada: 0
Alfabeto_cinta: 0,B
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> qf,0,S
q0,0 -> q0,0,R
"""
        with self.assertRaises(MachineParseError):
            parse_mt(source)

    def test_parser_rejects_unknown_state(self):
        source = """Estados: q0,qf
Alfabeto_entrada: 0
Alfabeto_cinta: 0,B
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> qx,0,S
"""
        with self.assertRaises(MachineParseError):
            parse_mt(source)

    def test_parser_rejects_invalid_direction(self):
        source = """Estados: q0,qf
Alfabeto_entrada: 0
Alfabeto_cinta: 0,B
Inicial: q0
Finales: qf
Blanco: B
Transiciones:
q0,0 -> qf,0,X
"""
        with self.assertRaises(MachineParseError):
            parse_mt(source)


class SimulatorTests(MachineTestMixin, TestCase):
    def test_current_0n1n_machine_accepts_0011(self):
        execution, _ = self.run_machine("0n1n.mt", "0011")
        self.assertEqual(execution.status, Execution.ACCEPTED)

    def test_0n1n_rejects_011(self):
        execution, _ = self.run_machine("0n1n.mt", "011")
        self.assertEqual(execution.status, Execution.REJECTED)

    def test_binary_palindrome_accepts_101(self):
        execution, _ = self.run_machine("palindromo_binario.mt", "101")
        self.assertEqual(execution.status, Execution.ACCEPTED)

    def test_current_binary_palindrome_machine_rejects_10(self):
        execution, _ = self.run_machine("palindromo_binario.mt", "10")
        self.assertEqual(execution.status, Execution.REJECTED)

    def test_professor_unary_duplicator_doubles_ones(self):
        execution, final_tape = self.run_machine("duplica_unos.mt", "111")
        self.assertEqual(execution.status, Execution.ACCEPTED)
        self.assertEqual(final_tape, "111111")

    def test_ends_with_aa_accepts_baa(self):
        execution, _ = self.run_machine("termina_aa.mt", "baa")
        self.assertEqual(execution.status, Execution.ACCEPTED)

    def test_ends_with_aa_accepts_spaced_input(self):
        execution, _ = self.run_machine("termina_aa.mt", "b a a")
        self.assertEqual(execution.status, Execution.ACCEPTED)

    def test_ends_with_aa_accepts_comma_separated_input(self):
        execution, _ = self.run_machine("termina_aa.mt", "b,a,a")
        self.assertEqual(execution.status, Execution.ACCEPTED)

    def test_ends_with_aa_rejects_ba(self):
        execution, _ = self.run_machine("termina_aa.mt", "ba")
        self.assertEqual(execution.status, Execution.REJECTED)

    def test_professor_binary_duplicator_copies_input_with_separator(self):
        execution, final_tape = self.run_machine("duplica_binaria.mt", "01")
        self.assertEqual(execution.status, Execution.ACCEPTED)
        self.assertEqual(final_tape, "01#01")

    def test_diagnostics_warn_about_unreachable_separator(self):
        machine = self.load_machine("duplica_binaria.mt")

        diagnostics = machine_diagnostics(machine)

        self.assertEqual(diagnostics, [])

    def test_professor_unary_sum_leaves_current_machine_output(self):
        execution, final_tape = self.run_machine("suma_unaria.mt", "11#111")
        self.assertEqual(execution.status, Execution.ACCEPTED)
        self.assertEqual(final_tape, "11111")

    def test_infinite_loop_stops_by_step_limit(self):
        execution, _ = self.run_machine("bucle_infinito.mt", "no_termina", max_steps=20)
        self.assertEqual(execution.status, Execution.TIMEOUT)
        self.assertEqual(execution.steps, 20)

    def test_default_max_steps_is_100(self):
        machine = self.load_machine("palindromo_binario.mt")
        execution = TuringMachineSimulator.create_execution(machine, "101")
        self.assertEqual(execution.max_steps, 100)

    def test_infinite_tape_expands_without_index_errors(self):
        execution, _ = self.run_machine("bucle_infinito.mt", "no_termina", max_steps=120)
        self.assertEqual(execution.status, Execution.TIMEOUT)
        self.assertEqual(execution.head_position, 120)


class DeletionViewTests(MachineTestMixin, TestCase):
    def test_delete_execution_removes_history_item(self):
        machine = self.load_machine("palindromo_binario.mt")
        execution = TuringMachineSimulator.create_execution(machine, "101")

        response = self.client.post(f"/executions/{execution.pk}/delete/")

        self.assertRedirects(response, "/")
        self.assertFalse(Execution.objects.filter(pk=execution.pk).exists())

    def test_clear_executions_removes_recent_history(self):
        machine = self.load_machine("palindromo_binario.mt")
        TuringMachineSimulator.create_execution(machine, "101")
        TuringMachineSimulator.create_execution(machine, "11")

        response = self.client.post("/executions/clear/")

        self.assertRedirects(response, "/")
        self.assertEqual(Execution.objects.count(), 0)

    def test_delete_machine_removes_machine_and_executions(self):
        machine = self.load_machine("palindromo_binario.mt")
        TuringMachineSimulator.create_execution(machine, "101")

        response = self.client.post(f"/machines/{machine.pk}/delete/")

        self.assertRedirects(response, "/")
        self.assertFalse(TuringMachine.objects.filter(pk=machine.pk).exists())
        self.assertEqual(Execution.objects.count(), 0)

    def test_clear_machines_removes_loaded_machines(self):
        self.load_machine("palindromo_binario.mt")
        self.load_machine("termina_aa.mt")

        response = self.client.post("/machines/clear/")

        self.assertRedirects(response, "/")
        self.assertEqual(TuringMachine.objects.count(), 0)
