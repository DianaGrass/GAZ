from django.shortcuts import render
from planes.models import (
    FinanceCosts,
    ActivityForm,
    Curator,
    ContractType,
    ContractMode,
    PurchaseType,
    StateASEZ,
    Counterpart,
    ContractStatus,
    UserTypes,
    NumberPZTRU,
    Currency,
)
from . import forms
from django.forms import modelformset_factory

# Create your views here.
def index(request):
    context = {}
    return render(request, 'catalog/index.html', context)

def catalog_funding(request):
    obj_list = FinanceCosts.objects.all().order_by('title')
    name_list = []
    for obj in obj_list:
        name_list.append(obj.title)
    v_name = FinanceCosts._meta.get_field('title').verbose_name

    CatalogFormset = modelformset_factory(FinanceCosts, form=forms.CatalogFinanceCostsForm, extra=0)
    formset = CatalogFormset()
    title = 'Статьи финансирования'
    context = {'formset': formset, 'title': title, 'queryset': name_list, 'v_name': v_name}
    return render(request, 'catalog/article.html', context)

def catalog_activityform(request):
    obj_list = FinanceCosts.objects.all().order_by('title')
    name_list = []
    for obj in obj_list:
        name_list.append(obj.title)
    v_name = FinanceCosts._meta.get_field('title').verbose_name

    CatalogFormset = modelformset_factory(ActivityForm, form=forms.CatalogActivityFormForm, extra=0)
    formset = CatalogFormset()
    title = 'Виды деятельности'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_curator(request):
    CatalogFormset = modelformset_factory(Curator, form=forms.CatalogCuratorForm, extra=0)
    formset = CatalogFormset()
    title = 'Кураторы'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_contracttype(request):
    CatalogFormset = modelformset_factory(ContractType, form=forms.CatalogContractTypeForm, extra=0)
    formset = CatalogFormset()
    title = 'Типы договора'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_contractmode(request):
    CatalogFormset = modelformset_factory(ContractMode, form=forms.CatalogContractModeForm, extra=0)
    formset = CatalogFormset()
    title = 'Виды договора'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_purchasetype(request):
    CatalogFormset = modelformset_factory(PurchaseType, form=forms.CatalogPurchaseTypeForm, extra=0)
    formset = CatalogFormset()
    title = 'Типы закупки'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_stateasez(request):
    CatalogFormset = modelformset_factory(StateASEZ, form=forms.CatalogStateASEZForm, extra=0)
    formset = CatalogFormset()
    title = 'Состояния АСЭЗ'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_counterpart(request):
    CatalogFormset = modelformset_factory(Counterpart, form=forms.CatalogCounterpartForm, extra=0)
    formset = CatalogFormset()
    title = 'Контрагенты'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_contractstatus(request):
    CatalogFormset = modelformset_factory(ContractStatus, form=forms.CatalogContractStatusForm, extra=0)
    formset = CatalogFormset()
    title = 'Статусы договора'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_usertypes(request):
    CatalogFormset = modelformset_factory(UserTypes, form=forms.CatalogUserTypesForm, extra=0)
    formset = CatalogFormset()
    title = 'Типы пользователя'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_numberpztru(request):
    CatalogFormset = modelformset_factory(NumberPZTRU, form=forms.CatalogNumberPZTRUForm, extra=0)
    formset = CatalogFormset()
    title = 'Номер пункта Положения о закупках'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_currency(request):
    CatalogFormset = modelformset_factory(Currency, form=forms.CatalogCurrency, extra=0)
    formset = CatalogFormset()
    title = 'Валюта'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_report(request):
    return render(request, 'catalog/report.html')

