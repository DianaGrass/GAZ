from django.forms import ModelForm, TextInput
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

class CatalogFinanceCostsForm(ModelForm):
    class Meta:
        model = FinanceCosts
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogActivityFormForm(ModelForm):
    class Meta:
        model = ActivityForm
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogCuratorForm(ModelForm):
    class Meta:
        model = Curator
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogContractTypeForm(ModelForm):
    class Meta:
        model = ContractType
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogContractModeForm(ModelForm):
    class Meta:
        model = ContractMode
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogPurchaseTypeForm(ModelForm):
    class Meta:
        model = PurchaseType
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogStateASEZForm(ModelForm):
    class Meta:
        model = StateASEZ
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogCounterpartForm(ModelForm):
    class Meta:
        model = Counterpart
        # fields = ('name',)
        fields = [
            'name',
            'UNP',
            'reg_addr',
            'phone',
            'email', ]
        widgets = {'name': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogContractStatusForm(ModelForm):
    class Meta:
        model = ContractStatus
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogUserTypesForm(ModelForm):
    class Meta:
        model = UserTypes
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogNumberPZTRUForm(ModelForm):
    class Meta:
        model = NumberPZTRU
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogCurrency(ModelForm):
    class Meta:
        model = Currency
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}

class CatalogCurrency(ModelForm):
    class Meta:
        model = Currency
        fields = ('title',)
        widgets = {'title': TextInput(attrs={'readonly': 'readonly'}),}
