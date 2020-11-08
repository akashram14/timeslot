from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect
from .forms import choosetime
from .models import Orders
import datetime, time
import pytz
from django.utils import timezone


def check(a, b, freetimes):
    now = timezone.localtime(timezone.now())
    a = timezone.localtime(a)
    b = timezone.localtime(b)
    print(now)
    if now >= a or now >= b:
        return False
    for i in freetimes:
        if i[0]<=a and b<=i[1]:
            print(i[0])
            print(i[1])
            return True
    return False

# Create your views here.
def book(request):
    if request.method == 'POST':
        form = choosetime(data = request.POST)
        if form.is_valid():
            today = form.cleaned_data['starttime'].date()
            times = Orders.objects.all().order_by('starttime').filter(starttime__date = today)
            freetimes = []
            openingtime = datetime.datetime.combine(today, datetime.time(8,00,00))
            openingtime = pytz.timezone('Asia/Kolkata').localize(openingtime, is_dst=None)
            closingtime = datetime.datetime.combine(today, datetime.time(21,00,00))
            closingtime = pytz.timezone('Asia/Kolkata').localize(closingtime, is_dst=None)
            temp = [[i.starttime,i.endtime] for i in times]
            if(len(temp) == 0):
                freetimes.append([openingtime, closingtime])
            else:
                for i in range(len(temp)):
                    if i == 0:
                        freetimes.append([openingtime,temp[i][0]])        
                    else:
                        freetimes.append([temp[i-1][1], temp[i][0]])  
                    if i == len(temp) - 1:
                        freetimes.append([temp[i][1], closingtime])
            for i in freetimes:
                print(i[0])
                print(i[1])
            if(check(form.cleaned_data['starttime'], form.cleaned_data['endtime'], freetimes)):
                form.save()
            else:
                return HttpResponse("<h1> Sorry no slots available </h1>")
    else:
        form = choosetime()
    return render(request, 'bookings/ordernow.html', {'form':form})
