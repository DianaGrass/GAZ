from django.contrib import admin
from .models import (
    Curator,
    UserTypes,
    CustomUser,
    UserActivityJournal,
    FinanceCosts,
    PurchaseType,
    ActivityForm,
    StateASEZ,
    NumberPZTRU,
    ContractStatus,
    Currency,
    ContractType,
    ContractMode,
    Counterpart,
    SumsRUR,
    SumsBYN,
    Planning,
    Contract,
    # PlanningYearFunding,
    # YearPeriod,
)

models = (
    Curator,
    # UserTypes,
    # UserSub,
    # CustomUser,
    # UserActivityJournal,
    # FinanceCosts,
    # PurchaseType,
    # ActivityForm,
    # StateASEZ,
    # NumberPZTRU,
    # ContractStatus,
    # Currency,
    # ContractType,
    # ContractMode,
    # Counterpart,
    # SumsRUR,
    # SumsBYN,
    # Planning,
    # PlanningYearFunding,
    # YearPeriod,
    UserTypes,
    CustomUser,
    UserActivityJournal,
    FinanceCosts,
    PurchaseType,
    ActivityForm,
    StateASEZ,
    NumberPZTRU,
    ContractStatus,
    Currency,
    ContractType,
    ContractMode,
    Counterpart,
    SumsRUR,
    #SumsBYN,
)


class ContractAdmin(admin.ModelAdmin):
    class Media:
        js = ("blabla.js", )


admin.site.register(Contract, ContractAdmin)

class SumsBYNAdmin(admin.ModelAdmin):
    list_display = ('contract', 'year', 'period',)
    list_filter = ('contract', 'year', 'period',)

admin.site.register(SumsBYN, SumsBYNAdmin)

for model in models:
    admin.site.register(model)
# Register your models here.

@admin.register(Planning)
class PlanningAdmin(admin.ModelAdmin):
    list_display = (
        'FinanceCosts',
        'curator',
        'year',
        'q_1',
        'q_2',
        'q_3',
        'q_4'

    )
    list_filter = ('FinanceCosts', 'curator', 'year')

