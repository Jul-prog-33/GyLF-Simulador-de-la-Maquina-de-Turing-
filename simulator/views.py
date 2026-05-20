from pathlib import Path

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .engine import InvalidInputError, TuringMachineSimulator
from .forms import MachineUploadForm, SimulationForm
from .models import Execution, TuringMachine
from .parser import MachineParseError, parse_mt


def machine_diagnostics(machine):
    reachable_symbols = set(machine.input_alphabet) | {machine.blank_symbol}
    changed = True
    while changed:
        changed = False
        for rules in machine.transitions.values():
            for read_symbol, transition in rules.items():
                write_symbol = transition["write_symbol"]
                if read_symbol in reachable_symbols and write_symbol not in reachable_symbols:
                    reachable_symbols.add(write_symbol)
                    changed = True

    readable_symbols = {read_symbol for rules in machine.transitions.values() for read_symbol in rules}
    unreachable_read_symbols = sorted(readable_symbols - reachable_symbols)
    if not unreachable_read_symbols:
        return []
    symbols = ", ".join(unreachable_read_symbols)
    return [
        (
            f"La máquina lee {symbols}, pero esos símbolos no están en el alfabeto de entrada "
            "ni pueden generarse desde los símbolos iniciales. Con la cinta inicial actual, "
            "esas transiciones pueden ser inalcanzables."
        )
    ]


def home(request):
    return render(
        request,
        "simulator/home.html",
        {
            "machines": TuringMachine.objects.all(),
            "executions": Execution.objects.select_related("machine")[:8],
            "upload_form": MachineUploadForm(),
        },
    )


@require_POST
def upload_machine(request):
    form = MachineUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)
        return redirect("home")

    try:
        uploaded = form.cleaned_data["file"]
        source = uploaded.read().decode("utf-8")
        name = form.cleaned_data["name"] or Path(uploaded.name).stem.replace("_", " ").title()
        parsed = parse_mt(source, name=name, description=form.cleaned_data["description"])
    except UnicodeDecodeError:
        messages.error(request, "El archivo debe estar codificado en UTF-8")
        return redirect("home")
    except MachineParseError as exc:
        messages.error(request, str(exc))
        return redirect("home")

    machine = TuringMachine.objects.create(
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
    messages.success(request, "Máquina cargada correctamente")
    return redirect(machine)


def machine_detail(request, pk):
    machine = get_object_or_404(TuringMachine, pk=pk)
    return render(
        request,
        "simulator/machine_detail.html",
        {
            "machine": machine,
            "simulation_form": SimulationForm(),
            "executions": machine.executions.all()[:10],
            "diagnostics": machine_diagnostics(machine),
        },
    )


@require_POST
def delete_machine(request, pk):
    machine = get_object_or_404(TuringMachine, pk=pk)
    machine_name = machine.name
    machine.delete()
    messages.success(request, f"Máquina eliminada: {machine_name}")
    return redirect("home")


@require_POST
def clear_machines(request):
    deleted_count, _ = TuringMachine.objects.all().delete()
    if deleted_count:
        messages.success(request, "Máquinas cargadas eliminadas correctamente")
    else:
        messages.info(request, "No había máquinas cargadas para eliminar")
    return redirect("home")


@require_POST
def start_execution(request, pk):
    machine = get_object_or_404(TuringMachine, pk=pk)
    form = SimulationForm(request.POST)
    if not form.is_valid():
        messages.error(request, "La cadena o el límite de pasos no son válidos")
        return redirect(machine)
    try:
        execution = TuringMachineSimulator.create_execution(
            machine=machine,
            input_string=form.cleaned_data["input_string"],
            max_steps=form.cleaned_data["max_steps"],
        )
    except InvalidInputError as exc:
        messages.error(request, str(exc))
        return redirect(machine)
    return redirect(execution)


def execution_detail(request, pk):
    execution = get_object_or_404(Execution.objects.select_related("machine"), pk=pk)
    simulator = TuringMachineSimulator(execution)
    halt_reason = ""
    if execution.status == Execution.REJECTED and execution.history:
        last = execution.history[-1]
        if last.get("transition") is None:
            halt_reason = f"No existe transición para ({last.get('state')}, {last.get('read')})"
    elif execution.status == Execution.TIMEOUT:
        halt_reason = "Se alcanzó el límite máximo de pasos"
    elif execution.status == Execution.ACCEPTED:
        halt_reason = "La máquina alcanzó un estado final"
    return render(
        request,
        "simulator/execution_detail.html",
        {
            "execution": execution,
            "machine": execution.machine,
            "cells": simulator.visible_tape(),
            "final_tape": simulator.final_tape(),
            "recent_history": list(reversed(execution.history[-12:])),
            "halt_reason": halt_reason,
            "diagnostics": machine_diagnostics(execution.machine),
        },
    )


@require_POST
def delete_execution(request, pk):
    execution = get_object_or_404(Execution, pk=pk)
    execution.delete()
    messages.success(request, "Registro del historial eliminado")
    return redirect("home")


@require_POST
def clear_executions(request):
    deleted_count, _ = Execution.objects.all().delete()
    if deleted_count:
        messages.success(request, "Historial reciente eliminado correctamente")
    else:
        messages.info(request, "No había historial para eliminar")
    return redirect("home")


@require_POST
def step_execution(request, pk):
    execution = get_object_or_404(Execution.objects.select_related("machine"), pk=pk)
    TuringMachineSimulator(execution).step()
    return redirect(execution)


@require_POST
def run_execution(request, pk):
    execution = get_object_or_404(Execution.objects.select_related("machine"), pk=pk)
    TuringMachineSimulator(execution).run()
    return redirect(execution)


@require_POST
def reset_execution(request, pk):
    execution = get_object_or_404(Execution.objects.select_related("machine"), pk=pk)
    restarted = TuringMachineSimulator.create_execution(
        machine=execution.machine,
        input_string=execution.input_string,
        max_steps=execution.max_steps,
    )
    return redirect(restarted)
