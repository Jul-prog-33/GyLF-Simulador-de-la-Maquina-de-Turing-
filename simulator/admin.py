from django.contrib import admin

from .models import Execution, TuringMachine


@admin.register(TuringMachine)
class TuringMachineAdmin(admin.ModelAdmin):
    list_display = ["name", "initial_state", "blank_symbol", "created_at"]
    search_fields = ["name", "description"]


@admin.register(Execution)
class ExecutionAdmin(admin.ModelAdmin):
    list_display = ["machine", "input_string", "current_state", "steps", "status", "updated_at"]
    list_filter = ["status", "machine"]
