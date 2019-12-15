from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.shortcuts import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Warehouse
from .forms import WarehouseForm
import json
import math
import requests
from bs4 import BeautifulSoup
import re
from fpdf import FPDF
from datetime import date, datetime


def index(request):
    content = requests.get("https://www.defence24.pl/wiadomosci/")
    soup = BeautifulSoup(content.content, 'html.parser')
    results = soup.find('ul', class_='main-news-list mt-30')
    results = re.findall(r'<a href="(.*)" title="(.*)"><span.*', str(results))
    context = {
        "results": results[:6]
    }
    return render(request, 'militaria/index.html', context)


@login_required(login_url='/militaria/login/')
def dashboardView(request):
    warehouses = Warehouse.objects.filter(user=request.user)
    context = {
        "warehouses": warehouses,
    }
    return render(request, 'militaria/dashboard.html', context)


def registerView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, help_texts=None)
        if form.is_valid():
            form.save()
            return redirect('/militaria/login/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {"form": form})


def AddWarehouse(request):
    if request.method == "POST":
        form = WarehouseForm(request.POST)
        if form.is_valid():
            ware = form.save(commit=False)
            user = User.objects.get(username=request.user.username)
            ware.save()
            ware.user.add(user)
            ware.save()
            return redirect('/militaria/dashboard/')
    else:
        form = WarehouseForm()
    return render(request, 'militaria/add.html', {'form': form })


def Supply(request):
    all_warehouses = Warehouse.objects.filter(user=request.user)
    low_level = [x for x in all_warehouses if x.get_warehouse_fill_code() == '#ff153c']
    medium_level = [x for x in all_warehouses if x.get_warehouse_fill_code() == '#fffab7']
    high_level = [x for x in all_warehouses if x.get_warehouse_fill_code() == '#99dcbb']
    context = {
        "low_level": low_level,
        "medium_level": medium_level,
        "high_level": high_level
    }

    def get_ratio(high, priority):
        return (100 - high) * priority

    PLANE_MAX = 100
    necessary = 0

    for ware in all_warehouses:
        to_high = ware.max - ware.how_many
        necessary_weight = to_high * ware.weight
        necessary += necessary_weight

    all_warehouses = sorted(all_warehouses, key=lambda x: get_ratio(x.max, x.priority), reverse=True)
    for x in all_warehouses:
        x.how_many = x.max
        print(x.name, get_ratio(x.max, x.priority))
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 10, txt="Dostawa z dnia: {}".format(datetime.now().strftime("%d-%m-%Y, %H:%M")), ln=1, align="C")
    pdf.cell(200, 10, txt="", ln=1, align="C")
    pdf.cell(200, 10, txt="", ln=1, align="C")
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="pojemnosc samolotu: {}".format(PLANE_MAX), ln=1, align="L")
    pdf.cell(200, 10, txt="\ndostawa: {}".format(necessary), ln=1, align="L")
    planes = math.ceil(necessary / PLANE_MAX)
    MAX_WEIGHT = PLANE_MAX * planes - necessary
    pdf.cell(200, 10, txt="liczba potrzebnych samolotow: {}".format(planes), ln=1, align="L")
    pdf.cell(200, 10, txt="Maksymalny ciezar: {}".format(MAX_WEIGHT), ln=1, align="L")

    while True:
        idx = 0
        all_warehouses.sort(key=lambda x: get_ratio(x.how_many, x.priority), reverse=True)
        print("SORTED: ", all_warehouses[0])
        warehouse_biggest_prio = all_warehouses[idx]
        weight = warehouse_biggest_prio.weight
        if MAX_WEIGHT >= weight:
            warehouse_biggest_prio.how_many += 1
            MAX_WEIGHT -= warehouse_biggest_prio.weight
        else:
            print("RESZTA: ", MAX_WEIGHT)
            break
    for x in all_warehouses:
        print(x.name, x.how_many)
        x.save()
    pdf.cell(200, 10, txt="", ln=1, align="C")
    pdf.cell(200, 10, txt="", ln=1, align="C")
    for low in all_warehouses:
        res = "{}%, priorytet: {}, waga: {}, ponad stan: +{}%".format(low, low.weight, low.priority, low.how_many-low.max)
        pdf.cell(200, 10, txt=res, ln=1, align="L")
    pdf.cell(200, 10, txt="", ln=1, align="C")
    pdf.cell(200, 10, txt="", ln=1, align="C")
    pdf.cell(200, 10, txt="", ln=1, align="C")
    pdf.cell(200, 10, txt="........................................        ".format(MAX_WEIGHT), ln=1, align="R")
    pdf.set_font("Arial", size=8)
    pdf.cell(200, 10, txt="(podpis operatora)                ", ln=1, align="R")
    pdf.output("militaria/static/report.pdf")

    return render(request, 'militaria/supply.html', context)


def contactView(request):
    return render(request, 'militaria/contact.html')
