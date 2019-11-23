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


def index(request):
    return render(request, 'militaria/index.html')


@login_required()
def dashboardView(request):
    warehouses = Warehouse.objects.filter(user=request.user)
    context = {
        "warehouses": warehouses,
    }
    return render(request, 'militaria/dashboard.html', context)


def registerView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
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

    # amunicja = Warehouse(name="amunicja", how_many=30, low=45, high=60, weight=5, priority=2)
    # jedzenie = Warehouse(name="jedzenie", how_many=50, low=60, high=72, weight=2, priority=3)
    # paliwo = Warehouse(name="paliwo", how_many=68, low=77, high=89, weight=3, priority=2)

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

    print("dostawa: {}".format(necessary))
    print("pojemność samolotu: {}".format(PLANE_MAX))
    planes = math.ceil(necessary / PLANE_MAX)
    print("liczba potrzebnych samolotów: {}".format(planes))
    MAX_WEIGHT = PLANE_MAX * planes - necessary
    print("maxWeight: {}".format(MAX_WEIGHT))

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
    return render(request, 'militaria/supply.html', context)
