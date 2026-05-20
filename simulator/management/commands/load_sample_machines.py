from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from simulator.models import TuringMachine
from simulator.parser import MachineParseError, parse_mt


class Command(BaseCommand):
    help = "Carga las máquinas de ejemplo desde la carpeta machines"

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parents[3]
        machines_dir = base_dir / "machines"
        if not machines_dir.exists():
            raise CommandError("No existe la carpeta machines")

        loaded = 0
        for path in sorted(machines_dir.glob("*.mt")):
            source = path.read_text(encoding="utf-8")
            try:
                parsed = parse_mt(source, name=path.stem.replace("_", " ").title())
            except MachineParseError as exc:
                raise CommandError(f"{path.name}: {exc}") from exc

            TuringMachine.objects.update_or_create(
                name=parsed.name,
                defaults={
                    "description": parsed.description,
                    "states": parsed.states,
                    "input_alphabet": parsed.input_alphabet,
                    "tape_alphabet": parsed.tape_alphabet,
                    "initial_state": parsed.initial_state,
                    "final_states": parsed.final_states,
                    "blank_symbol": parsed.blank_symbol,
                    "transitions": parsed.transitions,
                    "source": parsed.source,
                },
            )
            loaded += 1

        self.stdout.write(self.style.SUCCESS(f"Máquinas cargadas: {loaded}"))
