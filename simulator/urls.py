from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("machines/upload/", views.upload_machine, name="upload_machine"),
    path("machines/clear/", views.clear_machines, name="clear_machines"),
    path("machines/<int:pk>/", views.machine_detail, name="machine_detail"),
    path("machines/<int:pk>/delete/", views.delete_machine, name="delete_machine"),
    path("machines/<int:pk>/start/", views.start_execution, name="start_execution"),
    path("executions/clear/", views.clear_executions, name="clear_executions"),
    path("executions/<int:pk>/", views.execution_detail, name="execution_detail"),
    path("executions/<int:pk>/delete/", views.delete_execution, name="delete_execution"),
    path("executions/<int:pk>/step/", views.step_execution, name="step_execution"),
    path("executions/<int:pk>/run/", views.run_execution, name="run_execution"),
    path("executions/<int:pk>/reset/", views.reset_execution, name="reset_execution"),
]
