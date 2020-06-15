from planes.models import (
    SumsBYN,
    Contract,
    Planning,
    Curator,
    FinanceCosts,
    ContractType,
    ContractStatus
)
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.db.models import Avg, Count, Min, Sum, Q
from decimal import Decimal

def get_analytics_for_all_contracts(request):
    YEARS = [
        2018, 2019, 2020
    ]
    curators = Curator.objects.all()
    finance_costs = FinanceCosts.objects.all()
    contracts = Contract.objects.all()
    contract_types = ContractType.objects.all()
    contract_status = ContractStatus.objects.all()

    year = '2020'
    curator_id = 1
    finance_cost_id = 1
    contract_type_id = '1'
    contract_status_id = '0'

    if request.GET:
        year = request.GET['select_year']
        curator_id = request.GET['select_curator']
        finance_cost_id = request.GET['select_cost']
        contract_type_id = request.GET['select_contractType']
        contract_status_id = request.GET['select_contractStatus']

    finance_cost_title = FinanceCosts.objects.filter(id=finance_cost_id).values('title')[0]['title']
    curator_title = Curator.objects.filter(id=curator_id).values('title')[0]['title']

    if contract_type_id == '0':
        contract_types_ids = [value['id'] for value in contract_types.values('id')]
    else:
        contract_types_ids = list(contract_type_id)


    status_id = int(contract_status_id)

    contract_status_ids=['0']

    if contract_status_id == '0':
        contract_status_ids = [value['id'] for value in contract_status.values('id')]

    elif contract_status.values('id', 'title').filter(id=status_id)[0]['title']=='Заключен':
        ad =[i['id']  for i in contract_status.values('id', 'title') if i['title'] == 'Исполнен']
        contract_status_ids = list(contract_status_id) + ad

    elif contract_status.values('id', 'title').filter(id=status_id)[0]['title']=='Исполнен':
        ad =[i['id']  for i in contract_status.values('id', 'title') if i['title'] == 'Заключен']
        contract_status_ids = list(contract_status_id) + ad
    else:
        contract_status_ids = list(contract_status_id)

    planning = Planning.objects.filter(
        FinanceCosts_id = finance_cost_id,
        curator_id = curator_id,
        year = year
    ).values()

    if not planning:
        a = Planning(year=year, FinanceCosts_id=finance_cost_id, curator_id=curator_id)
        planning = [a]

    plan_sum_sap_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        plan_sum_sap_all = SumsBYN.objects.filter(
        period=period,
        year=year,
        contract__finance_cost_id = finance_cost_id,
        contract__curator_id = curator_id,
        contract__contract_type_id__in=contract_types_ids,

        contract__contract_status_id__in=contract_status_ids,
        contract__contract_active='True'

    ).aggregate(sum = Sum('plan_sum_SAP'))['sum']
        if not plan_sum_sap_all:
            plan_sum_sap_all='0'
        plan_sum_sap_dict[period] = plan_sum_sap_all

    contract_sum_without_NDS_BYN_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        contract_sum_without_NDS_BYN_all = SumsBYN.objects.filter(
            period=period,
            year=year,
            contract__finance_cost_id=finance_cost_id,
            contract__curator_id=curator_id,
            contract__contract_type_id__in=contract_types_ids,

            contract__contract_status_id__in=contract_status_ids,
            contract__contract_active='True'
        ).aggregate(sum=Sum('contract_sum_without_NDS_BYN'))['sum']
        if not contract_sum_without_NDS_BYN_all:
            contract_sum_without_NDS_BYN_all='0'
        contract_sum_without_NDS_BYN_dict[period] = contract_sum_without_NDS_BYN_all

    forecast_total_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        forecast_total_all = SumsBYN.objects.filter(
            period=period,
            year=year,
            contract__finance_cost_id=finance_cost_id,
            contract__curator_id=curator_id,
            contract__contract_type_id__in=contract_types_ids,

            contract__contract_status_id__in=contract_status_ids,
            contract__contract_active='True'

        ).aggregate(sum=Sum('forecast_total'))['sum']
        if not forecast_total_all:
            forecast_total_all='0'
        forecast_total_dict[period] = forecast_total_all

    fact_total_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        fact_total_all = SumsBYN.objects.filter(
            period=period,
            year=year,
            contract__finance_cost_id=finance_cost_id,
            contract__curator_id=curator_id,
            contract__contract_type_id__in=contract_types_ids,
            contract__contract_status_id__in=contract_status_ids,
            contract__contract_active='True'

        ).aggregate(sum=Sum('fact_total'))['sum']
        if not fact_total_all:
            fact_total_all='0'
        fact_total_dict[period] = fact_total_all


    contracts_count_plan = {}

    contracts_count_plan['Все'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,

        contract_status__title__in=['Запланирован'],
        contract_active='True'


    ).count()

    contracts_count_plan['Центр'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,
        contract_type__title__in=['Центр'],

        contract_status__title__in=['Запланирован'],
        contract_active = 'True'

    ).count()

    contracts_count_plan['Филиал'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,
        contract_type__title__in=['Филиал'],

        contract_status__title__in=['Запланирован'],
        contract_active='True'

    ).count()

    contracts_count_fact = {}

    contracts_count_fact['Все'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,

        contract_status__title__in=['Заключен', 'Исполнен'],
        contract_active='True'

    ).count()

    contracts_count_fact['Центр'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,
        contract_type__title__in=['Центр'],

        contract_status__title__in=['Заключен', 'Исполнен'],
        contract_active='True'

    ).count()

    contracts_count_fact['Филиал'] = contracts.filter(
        finance_cost_id=finance_cost_id,
        curator_id=curator_id,
        contract_type__title__in=['Филиал'],

        contract_status__title__in=['Заключен', 'Исполнен'],
        contract_active='True'

    ).count()

    return render(request,
                  template_name = "analytics/implementation_plan.html",
                  context = {
                      'curators':curators,
                      'FinanceCosts':finance_costs,
                      'contracts':contracts,
                      'contract_types': contract_types,
                      'contract_status': contract_status,
                      'planning': planning,
                      'years': YEARS,
                      'plan_sum_sap': plan_sum_sap_dict,
                      'contract_sum_without_NDS_BYN':contract_sum_without_NDS_BYN_dict,
                      'plannings': planning[0],
                      'forecast_total': forecast_total_dict,
                      'fact_total': fact_total_dict,
                      'contracts_count_plan': contracts_count_plan,
                      'contracts_count_fact': contracts_count_fact,
                      'year': year,
                      'finance_cost_title': finance_cost_title,
                      'curator_title':curator_title
                      })

def get_deviation_analysis(request):
    YEARS = [
        2018, 2019, 2020
    ]

    REPORTS = {
        '1': '1. Лимит средств (из раздела БПиЭА) - Плановая сумма SAP',
        '2': '2. Лимит средств - Сумма заключенного договора (по заключенным договорам)',
        '3': '3. Лимит средств - Прогноз по договорам (по всем договорам)',
        '4': '4. Лимит средств - Прогноз по договорам (только по заключенным договорам)',
        '5': '5. Лимит средств - Факт',
        '6': '6. Плановая сумма SAP - Сумма заключенного договора (по заключенным договорам)',
        '7': '7. Плановая сумма SAP - Прогноз по договорам (по всем договорам)',
        '8': '8. Плановая сумма SAP - Прогноз по договорам (только по заключенным договорам)',
        '9': '9. Плановая сумма SAP - Факт',
        '10': '10.Сумма заключенного договора (по заключенным договорам) - Прогноз исполнения по договору',
        '11': '11. Сумма заключенного договора (по заключенным договорам) - Факт',
        '12': '12. Прогноз по всем договорам - Факт'
    }

    reduced = {}
    subtracted = {}
    difference = {}

    curators = Curator.objects.all()
    finance_costs = FinanceCosts.objects.all()
    contracts = Contract.objects.all()
    # contract_types = ContractType.objects.all()
    # contract_status = ContractStatus.objects.all()

    year = '2020'
    curator_id = 1
    finance_cost_id = 1
    # contract_type_id = '1'
    # contract_status_id = '0'
    report= '1'

    if request.GET:
        year = request.GET['select_year']
        curator_id = request.GET['select_curator']
        finance_cost_id = request.GET['select_cost']
        report = request.GET['select_report']

    finance_cost_title = FinanceCosts.objects.filter(id=finance_cost_id).values('title')[0]['title']
    curator_title = Curator.objects.filter(id=curator_id).values('title')[0]['title']

    # if contract_type_id == '0':
    #     contract_types_ids = [value['id'] for value in contract_types.values('id')]
    # else:
    #     contract_types_ids = list(contract_type_id)

    # status_id = int(contract_status_id)
    #
    # contract_status_ids=['0']
    #
    # if contract_status_id == '0':
    #     contract_status_ids = [value['id'] for value in contract_status.values('id')]
    # elif contract_status.values('id', 'title').filter(id=status_id)[0]['title']=='Заключен':
    #     ad =[i['id']  for i in contract_status.values('id', 'title') if i['title'] == 'Исполнен']
    #     contract_status_ids = list(contract_status_id) + ad
    # elif contract_status.values('id', 'title').filter(id=status_id)[0]['title']=='Исполнен':
    #     ad =[i['id']  for i in contract_status.values('id', 'title') if i['title'] == 'Заключен']
    #     contract_status_ids = list(contract_status_id) + ad
    # else:
    #     contract_status_ids = list(contract_status_id)

    planning = Planning.objects.filter(
        FinanceCosts_id = finance_cost_id,
        curator_id = curator_id,
        year = year
    ).values()

    if not planning:
        a = Planning(year=year, FinanceCosts_id=finance_cost_id, curator_id=curator_id)
        cust_planning={}

        cust_planning['q_1']=a.q_1
        cust_planning['q_2'] = a.q_2
        cust_planning['q_3'] = a.q_3
        cust_planning['q_4'] = a.q_4
        cust_planning['q_all'] = a.q_all
        cust_planning['q_6_months'] = a.q_6_months
        cust_planning['q_9_months'] = a.q_9_months
        planning=[cust_planning]


    plan_sum_sap_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        plan_sum_sap_all = SumsBYN.objects.filter(
        period=period,
        year=year,
        contract__finance_cost_id = finance_cost_id,
        contract__curator_id = curator_id,
        # contract__contract_type_id__in=contract_types_ids,
        # contract__contract_status_id__in=contract_status_ids,
        contract__contract_active='True'
    ).aggregate(sum = Sum('plan_sum_SAP'))['sum']
        if not plan_sum_sap_all:
            plan_sum_sap_all='0'
        plan_sum_sap_dict[period] = plan_sum_sap_all

    contract_sum_without_NDS_BYN_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        contract_sum_without_NDS_BYN_all = SumsBYN.objects.filter(
            period=period,
            year=year,
            contract__finance_cost_id=finance_cost_id,
            contract__curator_id=curator_id,
            # contract__contract_type_id__in=contract_types_ids,
            contract__contract_status__title__in=['Заключен', 'Исполнен'],
            contract__contract_active='True'
        ).aggregate(sum=Sum('contract_sum_without_NDS_BYN'))['sum']
        if not contract_sum_without_NDS_BYN_all:
            contract_sum_without_NDS_BYN_all='0'
        contract_sum_without_NDS_BYN_dict[period] = contract_sum_without_NDS_BYN_all

    forecast_total_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        forecast_total_all = SumsBYN.objects.filter(
            period=period,
            year=year,
            contract__finance_cost_id=finance_cost_id,
            contract__curator_id=curator_id,
            contract__contract_status__title__in=['Заключен', 'Исполнен'],
            contract__contract_active='True'
        ).aggregate(sum=Sum('forecast_total'))['sum']
        if not forecast_total_all:
            forecast_total_all='0'
        forecast_total_dict[period] = forecast_total_all

    forecast_total_all_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        forecast_total_all = SumsBYN.objects.filter(
            period=period,
            year=year,
            contract__finance_cost_id=finance_cost_id,
            contract__curator_id=curator_id,
            contract__contract_active='True'
        ).aggregate(sum=Sum('forecast_total'))['sum']
        if not forecast_total_all:
            forecast_total_all='0'
        forecast_total_all_dict[period] = forecast_total_all

    fact_total_dict = {}
    for period in ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']:
        fact_total_all = SumsBYN.objects.filter(
            period=period,
            year=year,
            contract__finance_cost_id=finance_cost_id,
            contract__curator_id=curator_id,
            contract__contract_active='True'
        ).aggregate(sum=Sum('fact_total'))['sum']
        if not fact_total_all:
            fact_total_all='0'
        fact_total_dict[period] = fact_total_all

    replacements = {'q_1':'1quart',
                   'q_2': '2quart',
                   'q_3': '3quart',
                   'q_4': '4quart',
                   'q_all': 'year',
                   'q_6_months': '6months',
                   'q_9_months': '9months',
                   }
    rep_planning={}

    for key, value in planning[0].items():
        if key in replacements:
            rep_planning[replacements[key]]=Decimal(value)


    PERIODS = ['1quart', '2quart', '3quart', '4quart', '6months', '9months', 'year']
    if report in ['1']:
        reduced=rep_planning
        subtracted=plan_sum_sap_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])-Decimal(subtracted[p])
        difference['red_title']='Лимит средств (из раздела БПиЭА)'
        difference['sub_title']='Плановая сумма SAP'
    elif report in ['2']:
        reduced=rep_planning
        subtracted=contract_sum_without_NDS_BYN_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Лимит средств (из раздела БПиЭА)'
        difference['sub_title']='Сумма заключенного договора (по заключенным договорам)'
    elif report in ['3']:
        reduced=rep_planning
        subtracted=forecast_total_all_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Лимит средств (из раздела БПиЭА)'
        difference['sub_title']='Прогноз по договорам (по всем договорам)'
    elif report in ['4']:
        reduced=rep_planning
        subtracted=forecast_total_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Лимит средств (из раздела БПиЭА)'
        difference['sub_title']='Прогноз по договорам (по заключенным договорам)'
    elif report in ['5']:
        reduced=rep_planning
        subtracted=fact_total_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Лимит средств (из раздела БПиЭА)'
        difference['sub_title']='Факт'
    elif report in ['6']:
        reduced=plan_sum_sap_dict
        subtracted=contract_sum_without_NDS_BYN_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Плановая сумма SAP'
        difference['sub_title']='Сумма заключенного договора (по заключенным договорам)'
    elif report in ['7']:
        reduced=plan_sum_sap_dict
        subtracted=forecast_total_all_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Плановая сумма SAP'
        difference['sub_title']='Прогноз по договорам (по всем договорам)'
    elif report in ['8']:
        reduced=plan_sum_sap_dict
        subtracted=forecast_total_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Плановая сумма SAP'
        difference['sub_title']='Прогноз по договорам (только по заключенным договорам)'
    elif report in ['9']:
        reduced=plan_sum_sap_dict
        subtracted=fact_total_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Плановая сумма SAP'
        difference['sub_title']='Факт'
    elif report in ['10']:
        reduced=contract_sum_without_NDS_BYN_dict
        subtracted=forecast_total_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Сумма заключенного договора (по заключенным договорам)'
        difference['sub_title']='Прогноз исполнения по договору'
    elif report in ['11']:
        reduced=contract_sum_without_NDS_BYN_dict
        subtracted=fact_total_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Сумма заключенного договора (по заключенным договорам)'
        difference['sub_title']='Факт'
    elif report in ['12']:
        reduced=forecast_total_all_dict
        subtracted=fact_total_dict
        for p in PERIODS:
            difference[p]=Decimal(reduced[p])- Decimal(subtracted[p])
        difference['red_title']='Прогноз по всем договорам'
        difference['sub_title']='Факт'

    return render(request,
                  template_name = "analytics/deviation_analysis.html",
                  context = {
                      'curators':curators,
                      'FinanceCosts':finance_costs,
                      'contracts':contracts,
                      'years': YEARS,
                      'year': year,
                      'finance_cost_title': finance_cost_title,
                      'curator_title':curator_title,
                      'reports': REPORTS.items(),
                      'report_selected': int(report),
                      'reduced':reduced,
                      'subtracted':subtracted,
                      'difference':difference
                      })