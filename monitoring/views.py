# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import User, PondData, AeratorStatus
from .forms import UserRegistrationForm, UserLoginForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend which doesn't require a GUI


import matplotlib.pyplot as plt
import io
import base64

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            AeratorStatus.objects.create(phone_number=user)
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'monitoring/register.html', {'form': form})




def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(phone_number=phone_number)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    print(user.id)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid credentials')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')
    else:
        form = UserLoginForm()
    return render(request, 'monitoring/login.html', {'form': form})


# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import User, PondData, AeratorStatus
from .forms import UserRegistrationForm, UserLoginForm

import matplotlib.pyplot as plt
import io
import base64

# ... (keep the register, login, and other existing functions as they are)

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user = User.objects.get(id=request.session['user_id'])
    print(user)
    print("IN dashboard view")
    # Fetch the latest 4000 records for graphs
    pond_data_graph = PondData.objects.filter(phone_number=user.phone_number).order_by('-timestamp')[:300]
    
    # Fetch the latest 24 records for current values and statistics
    pond_data_stats = PondData.objects.filter(phone_number=user.phone_number).order_by('-timestamp')[:24]

    latest_records = PondData.objects.filter(phone_number=user.phone_number).order_by('-timestamp')[:1200]
    context = {
        'do_graph': None,
        'temp_graph': None,
        'ph_graph': None,
        'turbidity_graph': None,
        'tds_graph': None,
        'do_temp_graph': None,
        'ph_temp_graph': None,
        'all_data_graph': None,
        'current_values': None,
        'avg_values': None,
        'min_max_values': None,
        'latest_records': latest_records,
    }

    if pond_data_graph.exists():
        # Generate graphs using the latest 4000 records
        context['do_graph'] = generate_graph(pond_data_graph, 'dissolved_oxygen', 'Dissolved Oxygen(mg/L)')
        context['temp_graph'] = generate_graph(pond_data_graph, 'temperature', 'Temperature(°C)')
        context['ph_graph'] = generate_graph(pond_data_graph, 'ph', 'pH')
        context['turbidity_graph'] = generate_graph(pond_data_graph, 'turbidity', 'Turbidity(NTU)')
        context['tds_graph'] = generate_graph(pond_data_graph, 'tds', 'TDS(ppm)')
        context['do_temp_graph'] = generate_xy_graph(pond_data_graph, 'temperature', 'dissolved_oxygen', 'DO vs Temperature')
        context['ph_temp_graph'] = generate_xy_graph(pond_data_graph, 'temperature', 'ph', 'pH vs Temperature')
        context['all_data_graph'] = generate_all_data_graph(pond_data_graph)
    
    if pond_data_stats.exists():
        # Calculate statistics using the latest 24 records
        context['current_values'] = pond_data_stats.first()
        context['avg_values'] = calculate_average(pond_data_stats[:5])  # Last 5 hours
        context['min_max_values'] = calculate_min_max(pond_data_stats)
    context['username'] = user.name
    context['aerator_status'] = AeratorStatus.objects.get_or_create(phone_number=user)[0]
    
    return render(request, 'monitoring/dashboard.html', context)

def Sample(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    user = User.objects.get(id=request.session['user_id'])
    print("In dashboard")
    print(user)
    # Fetch the latest 4000 records for graphs
    pond_data_graph = PondData.objects.filter(phone_number=user.phone_number).order_by('-timestamp')[:1200]
    print(pond_data_graph)
    # Fetch the latest 24 records for current values and statistics
    pond_data_stats = PondData.objects.filter(phone_number=user.phone_number).order_by('-timestamp')[:24]

    latest_records = PondData.objects.filter(phone_number=user.phone_number).order_by('-timestamp')[:310]
    context = {
        'do_graph': None,
        'temp_graph': None,
        'ph_graph': None,
        'turbidity_graph': None,
        'tds_graph': None,
        'do_temp_graph': None,
        'ph_temp_graph': None,
        'all_data_graph': None,
        'current_values': None,
        'avg_values': None,
        'min_max_values': None,
        'latest_records': latest_records,
    }

    if pond_data_graph.exists():
        # Generate graphs using the latest 4000 records
        context['do_graph'] = generate_graph(pond_data_graph, 'dissolved_oxygen', 'Dissolved Oxygen(mg/L)')
        context['temp_graph'] = generate_graph(pond_data_graph, 'temperature', 'Temperature(°C)')
        context['ph_graph'] = generate_graph(pond_data_graph, 'ph', 'pH')
        context['turbidity_graph'] = generate_graph(pond_data_graph, 'turbidity', 'Turbidity(NTU)')
        context['tds_graph'] = generate_graph(pond_data_graph, 'tds', 'TDS(ppm)')
        context['do_temp_graph'] = generate_xy_graph(pond_data_graph, 'temperature', 'dissolved_oxygen', 'DO vs Temperature')
        context['ph_temp_graph'] = generate_xy_graph(pond_data_graph, 'temperature', 'ph', 'pH vs Temperature')
        context['all_data_graph'] = generate_all_data_graph(pond_data_graph)
    
    if pond_data_stats.exists():
        # Calculate statistics using the latest 24 records
        context['current_values'] = pond_data_stats.first()
        context['avg_values'] = calculate_average(pond_data_stats[:5])  # Last 5 hours
        context['min_max_values'] = calculate_min_max(pond_data_stats)
    context['username'] = user.name
    context['aerator_status'] = AeratorStatus.objects.get_or_create(phone_number=user)[0]
    
    return render(request, 'monitoring/Sample.html',context)
# views.py

import matplotlib.pyplot as plt

import io
import base64


# ... (other imports and functions)
# views.py


# ... (other imports and functions)

from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def generate_graph(data, field, title):
    plt.figure(figsize=(10, 8))
    
    # Ensure timestamps are datetime objects
    timestamps = [d.timestamp if isinstance(d.timestamp, datetime) else datetime.fromisoformat(str(d.timestamp)) for d in data]
    values = [getattr(d, field) for d in data]
    
    plt.plot(timestamps, values)
    plt.title(f'{title} vs Time (Latest 5 hours records)',fontsize=20)
    plt.xlabel('Time',fontsize=20)
    plt.ylabel(title,fontsize=20)
    
    # Format x-axis to show date and time
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
     
    plt.xticks(rotation=45, ha='right',fontsize=19)
    plt.yticks(fontsize=19)
    plt.tight_layout()
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_edgecolor('black')  # Border color
        spine.set_linewidth(2)
    
    
    
    return save_plot_to_base64()

def generate_xy_graph(data, x_field, y_field, title):
    plt.figure(figsize=(10, 8))
    x_values = [getattr(d, x_field) for d in data]
    y_values = [getattr(d, y_field) for d in data]
    plt.scatter(x_values, y_values)
    plt.title(f'{title} (Latest 5 hours records)',fontsize=20)
    plt.xlabel(x_field.capitalize(),fontsize=20)
    plt.ylabel(y_field.capitalize(),fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.tight_layout()
    
    return save_plot_to_base64()

def generate_all_data_graph(data):                                                                                                                                                                                                                                     
    plt.figure(figsize=(10, 8))
    timestamps = [d.timestamp for d in data]
    plt.plot(timestamps, [d.dissolved_oxygen for d in data], label='DO')
    plt.plot(timestamps, [d.ph for d in data], label='pH')
    plt.plot(timestamps, [d.temperature for d in data], label='Temp')
    plt.plot(timestamps, [d.turbidity for d in data], label='Turbidity')
    plt.plot(timestamps, [d.tds for d in data], label='TDS')
    plt.title('All Data vs Time (Latest 5 hours records)',fontsize=20)
    plt.xlabel('Time',fontsize=30)
    plt.ylabel('Value',fontsize=30)
    
    plt.legend(fontsize=12                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         )
    plt.xticks(rotation=45, ha='right',fontsize=15)                                                                                                                                                         
    plt.yticks(fontsize=15)
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_edgecolor('black')  # Border color
        spine.set_linewidth(2)
    plt.tight_layout()
    
    return save_plot_to_base64() 

def save_plot_to_base64():
    buffer = io.BytesIO()                                                            
    plt.savefig(buffer, format='png', dpi=300)                                                                                                                                                                                                                                                                                                                                                                                                                                             
    buffer.seek(0)                 
    image_png = buffer.getvalue()                
    buffer.close()
    plt.close()  # Close the figure to free up memory
    
    graphic = base64.b64encode(image_png)
    return graphic.decode('utf-8')

# ... (rest of your code)

def calculate_average(data):
    if not data:
        return {
            'dissolved_oxygen': 0,
            'pH': 0,
            'temperature': 0,
            'turbidity': 0,
            'tds': 0,
        }
    return {
        'dissolved_oxygen': sum(d.dissolved_oxygen for d in data) / len(data),
        'pH': sum(d.ph for d in data) / len(data),
        'temperature': sum(d.temperature for d in data) / len(data),
        'turbidity': sum(d.turbidity for d in data) / len(data),
        'tds': sum(d.tds for d in data) / len(data),
    }

def calculate_min_max(data):
    if not data:
        return {
            'dissolved_oxygen': {'min': 0, 'max': 0},
            'pH': {'min': 0, 'max': 0},
            'temperature': {'min': 0, 'max': 0},
            'turbidity': {'min': 0, 'max': 0},
            'tds': {'min': 0, 'max': 0},
        }
    return {
        'dissolved_oxygen': {'min': min(d.dissolved_oxygen for d in data), 'max': max(d.dissolved_oxygen for d in data)},
        'pH': {'min': min(d.ph for d in data), 'max': max(d.ph for d in data)},
        'temperature': {'min': min(d.temperature for d in data), 'max': max(d.temperature for d in data)},
        'turbidity': {'min': min(d.turbidity for d in data), 'max': max(d.turbidity for d in data)},
        'tds': {'min': min(d.tds for d in data), 'max': max(d.tds for d in data)},
    }

def toggle_aerator(request):
    if request.method == 'POST' and 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        aerator_status = AeratorStatus.objects.get(phone_number=user)
        aerator_status.is_on = not aerator_status.is_on
        aerator_status.save()
        return redirect('dashboard')
    return redirect('login')


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')




import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PondData  # Import the PondData model

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            
            dissolved_oxygen = float(data.get('dissolved_oxygen', 0))
            temperature = float(data.get('temperature', 0))
            turbidity = float(data.get('turbidity', 0))
            pH = float(data.get('pH', 0))
            TDS = float(data.get('TDS', 0))
            phone = data.get('phonenumber',0)  # Replace with actual phone number if available

            print(f"Received data - Dissolved Oxygen: {dissolved_oxygen}, Temperature: {temperature}, Turbidity: {turbidity}, pH: {pH}, TDS: {TDS}")
            
            # Save the data to the database
            PondData.objects.create(
                phone_number=phone,
                dissolved_oxygen=dissolved_oxygen/1000,
                ph=pH,
                temperature=temperature,
                turbidity=turbidity,
                tds=TDS
            )
            
            return JsonResponse({'status': 'success'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid data type'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=405)
