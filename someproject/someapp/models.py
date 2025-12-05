from django.db import models

# someapp/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client, Employee, Service, Appointment
from .forms import AppointmentForm, ClientForm
from django.http import HttpResponse

def home(request):
    """Главная страница"""
    services = Service.objects.all()
    employees = Employee.objects.all()
    
    context = {
        'services': services,
        'employees': employees,
        'title': 'Салон красоты "Элегант"'
    }
    return render(request, 'someapp/home.html', context)

def create_appointment(request):
    """Страница создания записи"""
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        appointment_form = AppointmentForm(request.POST)
        
        if client_form.is_valid() and appointment_form.is_valid():
            # Сохраняем клиента
            client = client_form.save()
            
            # Сохраняем запись с привязкой к клиенту
            appointment = appointment_form.save(commit=False)
            appointment.client = client
            appointment.save()
            
            messages.success(request, 'Запись успешно создана!')
            return redirect('home')
    else:
        client_form = ClientForm()
        appointment_form = AppointmentForm()
    
    services = Service.objects.all()
    employees = Employee.objects.all()
    
    context = {
        'client_form': client_form,
        'appointment_form': appointment_form,
        'services': services,
        'employees': employees,
        'title': 'Запись на услугу'
    }
    return render(request, 'someapp/appointment.html', context)

def appointments_list(request):
    """Список всех записей"""
    appointments = Appointment.objects.all().order_by('-appointment_date')
    
    context = {
        'appointments': appointments,
        'title': 'Все записи'
    }
    return render(request, 'someapp/appointments_list.html', context)

def someview(request):
    """Простой тестовый view"""
    return HttpResponse("Это тестовая страница")