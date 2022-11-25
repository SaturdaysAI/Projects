from django.shortcuts import render
from django.views.generic import View, CreateView, ListView, TemplateView, UpdateView

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from unipath import Path
import random

# Create your views here.
class LandingPageView(ListView):
    # la nueva direccion de los template es Album/----.html
    template_name = 'landingPage.html'
    context_object_name = 'fx'
    def get_queryset(self):
        return random.randint(1, 20), random.randint(1, 20)

class Map1View(ListView):
    template_name = 'IAmap.html'
    context_object_name = 'maps'

    def get_queryset(self):
        dataAI = [
            ['2022', 'Septiembre', '1,0,1,0,0,1,0,0,0,1,0,0,1,0,1,1'],
            ['2022', 'Octubre', '0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1'],
            ['2022', 'Noviembre', '0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,1'],
        ]
        pkMonth = self.kwargs['month']
        pkYear = self.kwargs['year']
        month = ['Septiembre', 'Octubre', 'Noviembre']
        years = ['2022']
        # peticion o logica
        for x in dataAI:
            if x[0] == pkYear and x[1] == pkMonth:
                query = x[2].split(",")
        return query, month, years

def error_404_view(request, exception):
    return render(request, 'index/page404.html')