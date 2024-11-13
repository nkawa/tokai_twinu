from django.shortcuts import render, redirect

from django.template import loader
from django.http import HttpResponseRedirect
from django.http import HttpResponse
# Create your views here.



def index(request):
    user = request.user
#    return redirect(dashboard)
    print("Check Auth in Index",user)
#    if user.is_authenticated:
    return redirect(dashboard)
 #   else:
 #       return redirect("login")


#@login_required
def dashboard(request):
    user = request.user
   
    context = {}
    context['segment'] = 'dashboard'
   
    html_template =  loader.get_template( 'dashboard.html' )
    return HttpResponse(html_template.render(context, request))

def model(request):
    user = request.user
   
    context = {}
    context['segment'] = 'model'
   
    html_template =  loader.get_template( 'model.html' )
    return HttpResponse(html_template.render(context, request))


def first_floor(request):
    user = request.user
   
    context = {}
    context['segment'] = 'first_floor'
   
    html_template =  loader.get_template( 'first_floor.html' )
    return HttpResponse(html_template.render(context, request))

