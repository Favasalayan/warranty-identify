from django.urls import path

from . import views

urlpatterns = [

path('', views.search_invoice),

path('history/', views.history),

path("print/<str:invoice>/", views.print_warranty),

path("save_customer/", views.save_customer),

path('clear_history/', views.clear_history),

path('result/<str:invoice>/', views.view_result),

path('warranty-cards/', views.warranty_cards),

path('verify/<str:invoice>/', views.verify_warranty),

]