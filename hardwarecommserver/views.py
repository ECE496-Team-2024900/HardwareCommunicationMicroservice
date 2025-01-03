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
        treatment_information = requests.get(f"http://127.0.0.1:8000/treatment/parameters/get?id={treatment_id}")
        #packet_string = f"approval+{treatment_information['handshake_random_string']}+{treatment_information['handshake_counter']+1}"
        packet_string = "Approved"

        # Setting cache expiry to 5 minutes - approval shouldn't remain here indefinitely or for too long
        cache.set(f'treatment_approval_{treatment_id}', packet_string, timeout=300) 

        return JsonResponse({'message': 'Approval received'}, status=200)
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
            return JsonResponse({'packet': packet_string}, status=200)
        else:
            return JsonResponse({'packet':'Approval not recieved'}, status=204)
    except Exception as e:
        return JsonResponse({'message':str(e)}, status=500)
