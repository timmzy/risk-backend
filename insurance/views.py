from django.shortcuts import render, HttpResponse, redirect, reverse
from django.db import connection
from django.db.utils import ProgrammingError
from .models import *


# Create your views here.

def handler404(request, exception):
    return redirect(reverse('admin:index'))


def handler500(request):
    response = render(request, '', {})
    response.status_code = 500
    return response
