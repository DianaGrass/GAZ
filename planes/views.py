from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import (
    LoginForm,
    RegisterForm,
    ContractForm,
    SumsBYNForm,
    SumsRURForm,
    PlanningForm,
    YearForm,
    SumsBYNForm_economist,
    SumsBYNForm_lawyer,
    SumsBYNForm_asez
)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User, Permission
from django.core.mail import send_mail
from django.views import View
from datetime import date
from datetime import datetime as dt
from .models import (
    Contract,
    SumsBYN,
    SumsRUR,
    UserActivityJournal,
    Curator, 
    FinanceCosts, 
    Planning,
    ContractType,
    ContractMode,
    PurchaseType,
    StateASEZ,
    NumberPZTRU,
    ContractStatus,
    Counterpart
)
from django.urls import reverse
import json
from django.forms import formset_factory, modelformset_factory
from django.db.models import Q


def test(request):
    perm = Permission.objects.all()
    print(request.user.get_user_permissions())
    if request.user.has_perm('auth.add_group'):
        return HttpResponse('it can auth.add_group')



    return render(request, template_name='contracts/test.html', context={})


@login_required
def index(request):
    return render(request, 'planes/index.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')


def login_view(request,):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/plane/')
                else:
                    return HttpResponse('disable account')
            else:
                return redirect('/login/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def register_view(request):
    form = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        email = request.POST.get('email')
        username = request.POST.get('username')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким адресом уже существует')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = email
                password = User.objects.make_random_password(4)
                user = User.objects.create_user(
                    username,
                    email,
                    password
                )
                user.save()
                create_journal = UserActivityJournal.objects.create(user=user)
                create_journal.save()
                send_mail(
                    'Hello from GAZ',
                    'Ваш пароль: ' + str(password),
                    'gazprombelgaz@gmail.com',
                    [email],
                    fail_silently=False
                )
                return HttpResponse(("Регистрация прошла успешна, пароль отправлен на почту: %s") % str(email))
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


class ContractView(View):
    ''' render contracts register table and allow to search '''
    template_name = 'contracts/contract_main.html'
    today_year = date.today().year
    cont = {}
    cont['all_fin_costs'] = FinanceCosts.objects.all()
    cont['all_curators'] = Curator.objects.all()
    cont['all_contract_types'] = ContractType.objects.all()
    cont['all_contract_modes'] = ContractMode.objects.all()
    cont['all_purchase_types'] = PurchaseType.objects.all()
    cont['all_state_asez'] = StateASEZ.objects.all()
    cont['all_pztru'] = NumberPZTRU.objects.all()
    cont['all_cont_suatus'] = ContractStatus.objects.all()
    cont['all_counterparts'] = Counterpart.objects.all()

    def get(self, request):
        context = self.cont.copy()

        if request.GET.__contains__('search_name'):
            print(request.GET)
            contracts = self.search(request)

        else:  # if no search request:
            contracts = Contract.objects.filter(
                start_date__contains=self.today_year,
                contract_active=True).order_by('-id')

        contract_and_sum = self.make_table(contracts)

        context['contracts'] = contracts
        context['contract_and_sum'] = contract_and_sum
        return render(request,
                      template_name=self.template_name,
                      context=context)

    def search(self, request):
        if request.GET['search_name'] == '':  # search_header
            search_name = None
        else:
            search_name = request.GET['search_name']
        if request.GET['search_date1'] or request.GET['search_date2']:
            search_date1 = request.GET['search_date1']
            search_date2 = request.GET['search_date2']

        search_fin_cost = request.GET['search_fin_cost']  # search_bottom
        search_curator = request.GET['search_curator']
        search_type = request.GET['search_type']
        search_mode = request.GET['search_mode']
        search_purchase_type = request.GET['search_purchase_type']
        search_asez = request.GET['search_asez']
        search_pztru = request.GET['search_pztru']
        search_cont_suatus = request.GET['search_cont_suatus']
        search_counterpart = request.GET['search_counterpart']
        contracts = Contract.objects.filter(contract_active=True).order_by('-id')
        try:
            contracts = contracts.filter(start_date__range=(search_date1, search_date2))
        except:
            pass

        if request.GET['search_name'] != '':
            contracts = contracts.filter(Q(title__icontains=search_name) | Q(title__in=search_name.split()))
            return contracts

        contracts = contracts.filter(
            Q(finance_cost=search_fin_cost) |
            Q(curator=search_curator) |
            Q(contract_type=search_type) |
            Q(contract_mode=search_mode) |
            Q(purchase_type=search_purchase_type) |
            Q(stateASEZ=search_asez) |
            Q(number_PZTRU=search_pztru) |
            Q(contract_status=search_cont_suatus) |
            Q(counterpart=search_counterpart)
        ).order_by('-id')

        return contracts

    def make_table(self, contracts):
        contract_and_sum = []

        for contract in contracts:
            sums_byn = SumsBYN.objects.filter(contract=contract)
            sum_rur = SumsRUR.objects.get(contract=contract)

            period_byn = {}
            for sum in sums_byn:
                sum_dic = {'plan_sum_SAP': sum.plan_sum_SAP,
                           'contract_sum_without_NDS_BYN': sum.contract_sum_without_NDS_BYN,
                           'forecast_total': sum.forecast_total,
                           'economy_total': sum.economy_total,
                           'fact_total': sum.fact_total,
                           'economy_contract_result': sum.economy_contract_result}

                period_byn[sum.period] = sum_dic

            contract_and_sum.append(
                {
                    'contract': contract,
                    'sum_byn': period_byn,
                    'sum_rur': sum_rur,
                }
            )
        return contract_and_sum


class DeletedContracts(View):
    ''' render deleted contracts and allow to recover contract '''
    def get(self, request, contract_id=None):
        if contract_id:
            self.recovery(contract_id)
            return HttpResponse('just text!!')
        deleted_contracts = Contract.objects.filter(contract_active=False)
        return render(request,
                      template_name='contracts/deleted_contracts.html',
                      context={
                          'contracts':deleted_contracts,
                      })

    def post(self, request):
        return HttpResponse('post')

    def recovery(self, contract_id):
        contract_to_recover = Contract.objects.get(id=contract_id)
        contract_to_recover.contract_active = True
        contract_to_recover.save()
        return contract_to_recover


class ContractFabric(View):
    ''' allow to create, change, copy and delete (move to deleted) contracts '''
    create_or_add = 'contracts/add_new_contract.html'
    periods = [
        "year",
        "6months",
        "9months",
        "10months",
        "11months",
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]

    def get(self, request, contract_id=None):
        if request.GET.__contains__('from_ajax'):
            if request.GET['from_ajax'] == 'del_contract':
                contract_id_list = request.GET.getlist('choosed[]')
                Contract.objects.filter(id__in=contract_id_list).update(contract_active=False)
                return HttpResponse('this is delete contract')

        if request.GET.__contains__('pattern_contract_id'):
            contract_id = int(request.GET['pattern_contract_id'])



        if not contract_id:
            ''' Create new contract with initial sumBYN and sumRUR'''
            contract_form = ContractForm
            sum_rur_form = SumsRURForm
            SumBYNFormSet = formset_factory(SumsBYNForm, extra=0)  # создает НОВЫЕ
            formset = SumBYNFormSet(initial=[  # для создание нового договора
                {'period': '1quart'},
                {'period': '2quart'},
                {'period': '3quart'},
                {'period': '4quart'},
            ])
        else:
            # if request.user.has_perm('planes:change_contract'):
                # return HttpResponse(request.user.groups.all())
            if request.user.groups.filter(name='economists'):
                SumBYNFormSet = modelformset_factory(SumsBYN, SumsBYNForm_economist, extra=0)  # Берет ИЗ БД
                formset = SumBYNFormSet(
                    queryset=SumsBYN.objects.filter(contract__id=contract_id))  # для вызова из бд
                contract_form = ContractForm(instance=get_object_or_404(Contract, id=contract_id))
                sum_rur_form = SumsRURForm(instance=get_object_or_404(SumsRUR, contract__id=contract_id))

            elif request.user.groups.filter(name='lawyers'):
                SumBYNFormSet = modelformset_factory(SumsBYN, SumsBYNForm_lawyer, extra=0)  # Берет ИЗ БД
                formset = SumBYNFormSet(
                    queryset=SumsBYN.objects.filter(contract__id=contract_id))  # для вызова из бд
                contract_form = ContractForm(instance=get_object_or_404(Contract, id=contract_id))
                sum_rur_form = SumsRURForm(instance=get_object_or_404(SumsRUR, contract__id=contract_id))

            elif request.user.groups.filter(name='asez'):
                SumBYNFormSet = modelformset_factory(SumsBYN, SumsBYNForm_asez, extra=0)  # Берет ИЗ БД
                formset = SumBYNFormSet(
                    queryset=SumsBYN.objects.filter(contract__id=contract_id))  # для вызова из бд
                contract_form = ContractForm(instance=get_object_or_404(Contract, id=contract_id))
                sum_rur_form = SumsRURForm(instance=get_object_or_404(SumsRUR, contract__id=contract_id))

            else:
                SumBYNFormSet = modelformset_factory(SumsBYN, SumsBYNForm, extra=0)  # Берет ИЗ БД
                formset = SumBYNFormSet(
                    queryset=SumsBYN.objects.filter(contract__id=contract_id))  # для вызова из бд
                contract_form = ContractForm(instance=get_object_or_404(Contract, id=contract_id))
                sum_rur_form = SumsRURForm(instance=get_object_or_404(SumsRUR, contract__id=contract_id))

        return render(request,
                      template_name=self.create_or_add,
                      context={
                          'formset': formset,
                          'contract_form':contract_form,
                          'rur_form':sum_rur_form,
                      })

    def post(self, request, contract_id=None):
        if not contract_id:
            SumBYNFormSet = formset_factory(SumsBYNForm, extra=0)  # создает НОВЫЕ
            instance_contract = None
            instance_rur = None
            create_periods_flag = True
        else:
            SumBYNFormSet = modelformset_factory(SumsBYN, SumsBYNForm, extra=0)  # Берет ИЗ БД
            instance_contract = get_object_or_404(Contract, id=contract_id)
            instance_rur = get_object_or_404(SumsRUR, contract__id=contract_id)
            create_periods_flag = False

        contract_form = ContractForm(request.POST, instance=instance_contract)
        sum_rur_form = SumsRURForm(request.POST, instance=instance_rur)
        formset = SumBYNFormSet(request.POST)

        if sum_rur_form.is_valid() and contract_form.is_valid() and formset.is_valid():
            new_contract = contract_form.save()
            for form in formset:
                new_sum_byn = form.save(commit=False)
                new_sum_byn.contract = new_contract
                new_sum_byn.save()
            if create_periods_flag:
                for p in self.periods:
                    new_sum_byn = SumsBYN.objects.create(period=p, contract=new_contract)

            new_sum_rur = sum_rur_form.save(commit=False)
            new_sum_rur.contract = new_contract
            new_sum_rur.save()
            return redirect(reverse('planes:contracts'))
        else:
            print(formset.errors)
            return HttpResponse(formset.errors)


def adding_click_to_UserActivityJournal(request):
     counter = UserActivityJournal.objects.get(user=request.user)
     counter.clicks += 1
     counter.save()
     return HttpResponse('add_click')

@login_required
def plane(request,year=dt.now().year):
    finance_costs = FinanceCosts.objects.all()
    if request.method != 'POST':
        year_f = YearForm(initial={
            'year': year
        })
    if request.method == 'POST':
        year_f = YearForm(request.POST)
        if year_f.is_valid():
            year = year_f.cleaned_data['year']
            print(year_f.cleaned_data['year'])
    
    send_list = []
    money = None
    for item in finance_costs:
        try:
            money = item.with_planning.filter(year=str(year)).get(curator__title="ALL")
        except Planning.DoesNotExist:
            plan = Planning()
            plan.FinanceCosts = FinanceCosts.objects.get(pk = item.id)
            plan.curator = Curator.objects.get(title = "ALL")
            plan.q_1 = 0
            plan.q_2 = 0
            plan.q_3 = 0
            plan.q_4 = 0
            plan.year = year
            plan.save()
            money = item.with_planning.filter(year=str(year)).get(curator__title="ALL")
        send_list.append([item, money])

    response = {"finance_costs": finance_costs,
    'send_list':send_list,
     'year_f':year_f,
     'year': year
     }
    return render(request, './planes/plane.html', response)

@login_required
def curators(request, finance_cost_id, year):
    planning = Planning.objects.filter(FinanceCosts=finance_cost_id).filter(year=str(year)).exclude(curator__title='ALL')
    finance_cost_name = FinanceCosts.objects.get(pk=finance_cost_id).title
    response = {
        'planning': planning,
        'finance_cost_name': finance_cost_name,
        'finance_cost_id':finance_cost_id,
        'year' : year          
    }
    return render (request, './planes/curators.html', response)

  
def from_js(request):
    a = request.body.decode('utf-8')
    jsn = json.loads(a)
    try:
        result_curator = Curator.objects.get(title='ALL')
        id_result_curator = result_curator.id
    except Curator.DoesNotExist:
        print('error')
        result_curator = Curator()
        result_curator.title = 'ALL'
        result_curator.save()
        id_result_curator = result_curator.id


    finance_cost_title = jsn['cost_title']
    year = jsn['data_from_django']
    id_finance_cost = FinanceCosts.objects.get(title=finance_cost_title).id

    try:
        planing = Planning.objects.filter(FinanceCosts = id_finance_cost).filter(year = year)
        result_cur = planing.get(curator__title='ALL')
    except Planning.DoesNotExist:
        plan = Planning()
        plan.FinanceCosts = FinanceCosts.objects.get(pk = id_finance_cost)
        plan.curator = Curator.objects.get(pk = id_result_curator)
        plan.q_1 = jsn['result_money'][0]
        plan.q_2 = jsn['result_money'][1]
        plan.q_3 = jsn['result_money'][2]
        plan.q_4 = jsn['result_money'][3]
        plan.year = year
        plan.save()
        result_cur = planing.get(curator__title='ALL')
    
    if result_cur.q_1 != jsn['result_money'][0] : 
        result_cur.q_1 = jsn['result_money'][0]
    if result_cur.q_2 != jsn['result_money'][1]:
        result_cur.q_2 = jsn['result_money'][1]
    if result_cur.q_3 != jsn['result_money'][2]:
        result_cur.q_3 = jsn['result_money'][2]
    if result_cur.q_4 != jsn['result_money'][3]:
        result_cur.q_4 = jsn['result_money'][3]
    result_cur.save()
    return HttpResponse('123')

@login_required
def edit_plane(request, year, item_id):
    plan = Planning.objects.get(pk=item_id)
    plan_form = PlanningForm(instance=plan)
    response = {
        'plan_form':plan_form,
         'item_id':item_id,
         'year':year
         }
    if(request.method == 'POST'):
        plan_form = PlanningForm(request.POST, instance=plan)
        if plan_form.is_valid():
            if plan_form.cleaned_data.get('delete'):
                Planning.objects.get(pk=item_id).delete()
                return redirect('/plane/{0}/{1}/curators'.format(year, str(plan.FinanceCosts.id)) )
            plan_form.save()
            return redirect('/plane/{0}/{1}/curators'.format(year, str(plan.FinanceCosts.id)) )
        else:
            print('12324')
            print(plan_form._errors)
    return render(request, './planes/edit_plane.html', response)

@login_required 
def add(request, finance_cost_id, year):
    plane_form = PlanningForm(initial={
        'FinanceCosts': finance_cost_id,
        'year': year,
        })
    response = {
        'plane_form':plane_form,
        'finance_cost_id':finance_cost_id,
        'year': year
    }
    if(request.method == 'POST'):
        plane_form = PlanningForm(request.POST)
        if plane_form.is_valid():
            plane_form.save()
            return redirect('/plane/{0}/{1}/curators'.format(year, finance_cost_id) )

            # return reverse('planes', kwargs={'year': year})
    return render(request, './planes/add.html', response)
