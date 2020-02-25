from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings

class HomeView(View):
    def get(self, request) :
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal'   : islocal,
            'is_staff'  : (request.user.groups.filter(name="staff").count()>0),
            'meal_list' : [(i+1, m) for i, m in enumerate(Meal.objects.all().order_by("name"))]
        }
        return render(request, 'home/index.html', context)

