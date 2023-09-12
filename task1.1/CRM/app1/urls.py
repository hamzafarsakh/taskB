


from django.urls import path
from django.contrib import admin

from app1.views import (

    registerVueView,
    allCust,
    allServ,
    AddCustomerPage,
    CustInfo,
    updateCustomerPage,
    # loginVue,
    AllServInCust,
    AllServNotInCust,
    addServ,
    log,
    activation,
    AllActivesForCustMain,
    SearchView,
    activationServ,
    deleteCust,
)

urlpatterns = [

    path('registerVue', registerVueView.as_view(), name='registerVue'),
    path('allCust', allCust.as_view(), name='allCust'),
    path('allServ', allServ.as_view(), name='allServ'),

    path('AddCustomerPage', AddCustomerPage.as_view(), name='AddCustomerPage'),
    path('CustInfo/<int:id>', CustInfo.as_view(), name='CustInfo'),
    path('updateCustomerPage', updateCustomerPage.as_view(), name='updateCustomerPage'),
    # path('loginvue', loginVue.as_view(), name='loginVue'),
    path('AllServInCust/<int:id>', AllServInCust.as_view(), name='AllServInCust'),
    path('AllServNotInCust/<int:id>', AllServNotInCust.as_view(), name='AllServNotInCust'),
    path('addServ/<int:custId>/<int:servId>', addServ.as_view(), name='addServ'),
    path('log/<email>/<pwd>', log.as_view(), name='log'),
    path('activation/<int:activeId>/<int:custId>', activation.as_view(), name='activation'),
    path('AllActivesForCustMain/<int:custId>', AllActivesForCustMain.as_view(), name='AllActivesForCustMain'),
    path('search/<searchSrt>', SearchView.as_view(), name='SearchView'),
    path('activationServ/<int:servId>', activationServ.as_view(), name='activationServ'),
    path('deleteCust/<int:custId>', deleteCust.as_view(), name='deleteCust'),


]
