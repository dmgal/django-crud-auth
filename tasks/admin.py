from django.contrib import admin
from .models import Task

# Para poder ver la fecha de creación de la tareas (se auto completa) - CAMPOS DE SOLO LECTURA A MOSTRAR EN EL ADMINISTRADOR
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.
admin.site.register(Task,TaskAdmin)