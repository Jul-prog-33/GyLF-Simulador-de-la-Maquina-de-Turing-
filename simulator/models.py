from django.db import models
from django.urls import reverse


class TuringMachine(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    states = models.JSONField(default=list)
    input_alphabet = models.JSONField(default=list)
    tape_alphabet = models.JSONField(default=list)
    initial_state = models.CharField(max_length=80)
    final_states = models.JSONField(default=list)
    blank_symbol = models.CharField(max_length=20)
    transitions = models.JSONField(default=dict)
    source = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("machine_detail", args=[self.pk])


class Execution(models.Model):
    RUNNING = "RUNNING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    TIMEOUT = "TIMEOUT"

    STATUS_CHOICES = [
        (RUNNING, "En ejecución"),
        (ACCEPTED, "Aceptada"),
        (REJECTED, "Rechazada"),
        (TIMEOUT, "No termina"),
    ]

    machine = models.ForeignKey(TuringMachine, on_delete=models.CASCADE, related_name="executions")
    input_string = models.CharField(max_length=500, blank=True)
    tape = models.JSONField(default=dict)
    head_position = models.IntegerField(default=0)
    current_state = models.CharField(max_length=80)
    steps = models.PositiveIntegerField(default=0)
    max_steps = models.PositiveIntegerField(default=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=RUNNING)
    history = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return f"{self.machine.name} - {self.input_string or 'ε'}"

    @property
    def is_finished(self):
        return self.status in {self.ACCEPTED, self.REJECTED, self.TIMEOUT}

    def get_absolute_url(self):
        return reverse("execution_detail", args=[self.pk])
