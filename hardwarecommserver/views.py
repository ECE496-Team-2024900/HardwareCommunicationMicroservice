from django.http import JsonResponse
import requests
from django.core.cache import cache
from rest_framework.decorators import api_view


def index(request):
    return JsonResponse({"message": "This is the hardware communication microservice"})

# Used for clinicians to sent their treatment approval
# Packet format: "approval+{random_number_R}+{counter}"
# TO-DO: Need keys to sign packet and update logic once handshake counter is implemented
@api_view(['GET'])
def treatment_approval(request):
    treatment_id = request.GET['id']
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        packet_string = "Approved"

        # Setting cache expiry to 5 minutes - approval shouldn't remain here indefinitely or for too long
        cache.set(f'treatment_approval_{treatment_id}', packet_string, timeout=300) 

        return JsonResponse({'message': 'Approval received'}, status=200)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)

# For testing!!!
@api_view(['GET'])
def remove_treatment_approval(request):
    treatment_id = request.GET['id']
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        cache.delete(f'treatment_approval_{treatment_id}') 

        return JsonResponse({'message': 'Approval removed'}, status=200)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)

@api_view(['GET'])
def remove_sensor_data(request):
    treatment_id = request.GET['id']
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        cache.delete(f'sensor_data_{treatment_id}') 

        return JsonResponse({'message': 'Sensor data removed'}, status=200)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)

# Used for patient's app to check if clinician has approved treatment
@api_view(['GET'])
def treatment_approval_status(request):
    treatment_id = request.GET['id']
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        # Checking if the approval exists in the cache
        packet_string = cache.get(f'treatment_approval_{treatment_id}')
        if packet_string:
            return JsonResponse({'message': packet_string}, status=200)
        return JsonResponse({'message':'Approval not recieved'}, status=200)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)

@api_view(['PUT'])
def set_sensor_data_updates(request):
    treatment_id = request.GET['id']
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        cache_value = json.loads(request.body).get("data")

        # Setting cache expiry to 5 minutes
        cache.set(f'sensor_data_{treatment_id}', cache_value, timeout=300) 

        return JsonResponse({'message': 'Sensor data received'}, status=200)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)

@api_view(['GET'])
def get_sensor_data_updates(request):
    treatment_id = request.GET['id']
    if treatment_id is None:
        return JsonResponse({'message':'Please provide a treatment ID'}, status=400)
    try:
        data = cache.get(f'sensor_data_{treatment_id}') 
        if packet_string:
            return JsonResponse({'message': data}, status=200)
        return JsonResponse({'message':'No data'}, status=200)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)

