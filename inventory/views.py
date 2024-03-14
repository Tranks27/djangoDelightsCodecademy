from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, TemplateView



class HomeView(TemplateView):
    template_name = "inventory/home.html"

    