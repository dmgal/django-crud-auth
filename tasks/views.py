from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
# Para el acceso de usuarios
from django.contrib.auth.forms import UserCreationForm, User, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
# Control de errores - Integridad en BBDD de usuarios
from django.db import IntegrityError
# Formularios personalizados
from .forms import TaskForm
# Datos de nuestros modelos para poder consultar la BBDD
from .models import Task
# Tiempo
from django.utils import timezone
# Comprobar que están los usuarios logeatos y puedan acceder a las secciones
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        # Al llegar a la página web se le mostrará el formulario solamente
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        # Cando recibamos los datos del formulario (POST) tendremos que realizar comprobaciones
        if request.POST['password1'] == request.POST['password2']:
            # A pesar de los filtros que pongamos, la Propia BBDD tiene sus reglas y puede dar error, por eso usamos un try
            try:
                # Registramos el usuario
                # Recogemos los datos introducidos para el usuario
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()  # Salvamos en BBDD el usuario, el sistema se encarga de encriptar el password
                # antes de redireccionar, para que se cree la cookie con los datos del login necesitamos pasarle los datos
                login(request, user)
                return redirect('tasks')
            except IntegrityError:  # Controlamos la excepción de integridad de usaurios en la BBDD
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "El usuario ya existe."
                })
        # Formulario rellenado incorrectamente
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': "Las contraseñas no coinciden."
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
# Para evitar confusiones, el nombre de la función se llamará diferente
def signout(request):
    logout(request)  # Directamente cierra la sesión
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        # Toca comprboar posibles problemas
        if user is None:  # El usuario no existe en BBDD
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o contraseña son incorrectos.'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Por favor, introduzca datos válidos.'
            })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)  # Buscamos la tarea
        # Presentamos el formulario para poder modificar la tarea
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)  # Buscamos la tarea
            # Presentamos el formulario para poder modificar la tarea
            form = TaskForm(request.POST,instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error actualizando la tarea.'
            })

@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  # Buscamos la tarea
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required    
def delete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  # Buscamos la tarea
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required    
def activate_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  # Buscamos la tarea
    if request.method == 'POST':
        task.datecompleted = None
        task.save()
        return redirect('tasks')