from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from .views import (
    register_view,
    ContractView,
    adding_click_to_UserActivityJournal,
    curators,
    from_js,
    edit_plane,
    add,
    plane,
    ContractFabric,
    DeletedContracts,
test
)

app_name = "planes"


urlpatterns = [
    path('', plane, name='planes' ),
    path('register/', register_view, name='register'),
    path('contracts/', login_required(ContractView.as_view()), name='contracts'),
    path('contracts/create_contract/',
         login_required(
            # permission_required('planes:add_contract')
             (ContractFabric.as_view())
         ),
         name='create_contract'),
    path('contracts/change_contract/<contract_id>',
         login_required(
             # permission_required('planes.change_contract')
             (ContractFabric.as_view())
         ),
         name='change_contract'),
    path('contracts/copy_contract/',
         login_required(
            # permission_required('planes:add_contract')
            (ContractFabric.as_view())
         ),
         name='copy_contract'),
    path('contracts/deleted_contracts/', DeletedContracts.as_view(), name='deleted_contracts'),
    path('add_click/', adding_click_to_UserActivityJournal, name='add_click'),
    path('<int:year>/<int:finance_cost_id>/curators/', curators, name='curators'),
    path('to_server/', from_js, name='from_js'),
    path('<int:year>/<int:item_id>/edit-plane', edit_plane, name='edit_plane'),
    path('<int:year>/<int:finance_cost_id>/add/', add, name= 'add'),
    path('recovery/<int:contract_id>', DeletedContracts.as_view(), name='recover_contract'),

    path('test', test)

]


