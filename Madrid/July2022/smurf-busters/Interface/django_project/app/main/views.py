import json
import os

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
import hashlib
from functools import wraps

import logging
import copy
from django.template.loader import render_to_string
import pandas as pd
from demo import demo

def base(request, *args, **kwargs):
    return render(request, "base.html")

def calculate_table(request, *args, **kwargs):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        df_table = demo()
        df_table['percentage'] = df_table['percentage'].round(2)
        params = request.body.decode()
        if 'table1' in params:
            data = df_table.iloc[:5]
        else:
            data = df_table.iloc[-5:]
        response_dic = {'data': data}
        return HttpResponse(render_to_string("tables/team1.html", response_dic, request))



