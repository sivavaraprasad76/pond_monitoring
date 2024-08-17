from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import PondData
import json

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        dissolved_oxygen = request.POST.get('dissolved_oxygen')
        temperature = request.POST.get('temperature')
        turbidity = request.POST.get('turbidity')
        pH = request.POST.get('pH')
        TDS = request.POST.get('TDS')
        phone = "6304988175"
        
        if dissolved_oxygen and temperature and turbidity and pH and TDS:
            print(f"Received data - Dissolved Oxygen: {dissolved_oxygen}, Temperature: {temperature}, Turbidity: {turbidity}, pH: {pH}, TDS: {TDS}")
            
            # Create a new PondData instance
            PondData.objects.create(
                phone_number=phone,
                timestamp=timezone.now(),
                temperature=temperature,
                tds=TDS,
                turbidity=turbidity,
                ph=pH,
                dissolved_oxygen=dissolved_oxygen
            )
            
            print(f"Data inserted into database at {timezone.now()}")
            
            return HttpResponse("Data received", status=200)
        else:
            return HttpResponse("Invalid data", status=400)
    else:
        return HttpResponse("Method not allowed", status=405)