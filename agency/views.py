import email
from datetime import datetime,timedelta
from os import stat
import re
from django.db.models import Q
import json
from unicodedata import name
from urllib import response
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from django.core.paginator import Paginator
from .models import *
# Create your views here.
@csrf_exempt
def registration(request):
    body = request.POST
    image =  request.FILES
    User.objects.create(full_name=body.get("full_name"),resume=image.get("images"),email=body.get("email"),role=body.get("role"))
    return HttpResponse("successfully registered.")
@csrf_exempt
def status(request):
    method = request.method
    #updating the status
    if method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user = User.objects.filter(email=body.get("email"))
        if not user:
            return JsonResponse({"Error Message":"User does not exist."})
        user = user[0]
        prev_status = user.status
        user.status= body.get("status")
        user.save()
        message_info = f"status changed to {user.status}" 
        Emails.objects.create(userid = user)
        print(f"status is updated from {prev_status} to {user.status}")
        return JsonResponse({"message":"succefully status is updated"})

    else:
        print("it's executed..")
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user = User.objects.filter(email=body.get("email"))
        print(len(user))    
        user = user[0]
        user = userResponse(user)
        return JsonResponse(user,safe=False)

    # users= User.objects.filter(full_name="srikanth")
    # al_users = []
    
    # for user in users:
    #     individual_user={}
    #     individual_user.update(name=user.full_name)
    #     al_users.append(individual_user)
    # return FileResponse(user.resume)
def filter(request):
    all_responses= []
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        page = body.get("page")
        print(page)
        if not page:
            page=0
        else:
            del body["page"]
        user = User.objects.filter(**body).order_by("date")[page:page+2]
        for ind_user in user:
            all_responses.append({"full name":ind_user.full_name,"email":ind_user.email,"role":ind_user.role,"status":ind_user.status})
        return JsonResponse({"users":all_responses})
@csrf_exempt
def interviewSchedule(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user = User.objects.get(email=body.get("email"))
        date_time_from = datetime.strptime(body.get("datetime_from"),'%Y-%m-%dT%H::%M::%S.%f')
        date_time_to = datetime.strptime(body.get("datetime_to"),'%Y-%m-%dT%H::%M::%S.%f')
        interviews = Interview.objects.filter(Q(schedule_time_from__range = (date_time_from,date_time_to)) | Q(schedule_time_to__range=(date_time_from,date_time_to)))
        status = False
        if not interviews:
            onehour_back = date_time_from- timedelta(hours=0, minutes=50)
            onehour_forward = date_time_to + timedelta(hours=0,minutes=50)
            interviews = Interview.objects.filter(Q(schedule_time_from__range=(date_time_to,onehour_forward)) | Q(schedule_time_to__range=(onehour_back,date_time_from)))
            if not interviews:
                status= True
                Interview.objects.create(schedule_time_from=date_time_from,schedule_time_to=date_time_to,userid=user)
        if status:
            return JsonResponse({"scheduled time from": body.get("datetime_from"),"scheduled time to": body.get("datetime_to"),"userid":body.get("email")})
        else:
            return JsonResponse({"Error Message":"slot is already booked."})
def filterSchedule(request):
    if request.method == "GET":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        page = body.get("page")
        if page:
            page = int(page)
            del body['page']
        else:
            page=0
        date = datetime.strptime(body.get("date"),'%Y-%m-%d')
        if date:
            del body['date']        
        result = Interview.objects.filter(Q(**body)).order_by("schedule_time_from")[page:page+2]
        al_responses =[]
        print(result)
        for interv in result:
            al_responses.append({"user email":interv.userid.email,"from":interv.schedule_time_from,"to":interv.schedule_time_to})
        print(al_responses)
        return JsonResponse({"interview schedules":al_responses})

def historyMails(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    page = body.get("page")
    if page:
        page = int(page)
        del body['page']
    else:
        page=0
    emails = Emails.objects.filter(userid=body.get("email")).order_by("date_created")
    al_responses = []
    for email in emails:
        al_responses.append({"email":email.userid.email,"message":email.message,"created":email.date_created})
    return JsonResponse({"all emails":al_responses})
def userResponse(user):
    return {"name":user.full_name,"status":user.status,"role":user.role,"email":user.email}