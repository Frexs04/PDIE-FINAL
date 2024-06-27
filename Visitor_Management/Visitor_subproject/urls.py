from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('Choosepage/', views.Choosepage, name='Choosepage'),
    path('Rulespage/', views.Rulespage, name='Rulespage'),
    path('Feedback/', views.Feedback, name='Feedback'),

    
    path('Residentlogin/', views.Residentlogin, name='Residentlogin'),
    path('ResidentPage/<int:Resid>/', views.ResidentPage, name='ResidentPage'),
    path('ApplyEvent/<int:Resid>/', views.ApplyEvent, name='ApplyEvent'),
    path('ApplyPassResident/<int:Resid>/', views.ApplyPassResident, name='ApplyPassResident'),
    path('Applyreport/<int:Resid>/', views.Applyreport, name='Applyreport'),


    path('Stafflogin/', views.Stafflogin, name='Stafflogin'),
    path('StaffPage/<int:Staffid>/', views.StaffPage, name='StaffPage'),
    path('ViewDutiesShift/<int:Staffid>/', views.ViewDutiesShift, name='ViewDutiesShift'),

    path('ViewDutiesShift/<int:Staffid>/', views.ViewDutiesShift, name='ViewDutiesShift'),
   


    path('ViewResident/<int:Staffid>/', views.ViewResident, name='ViewResident'),
    path('ViewVisitor/<int:Staffid>/', views.ViewVisitor, name='ViewVisitor'),
    path('ApplyPassStaff/<int:Staffid>/', views.ApplyPassStaff, name='ApplyPassStaff'),


    path('Managerlogin/', views.Managerlogin, name='Managerlogin'),
    path('ManagerPage/<int:Managerid>/', views.ManagerPage, name='ManagerPage'),
    
    path('ManageVisits/<int:Managerid>/', views.ManageVisits, name='ManageVisits'),
    path('delete/<str:VisitorName>/<int:Managerid>/', views.DeleteVisitor, name='Deletevisitor'),

    path('ManageEvents/<int:Managerid>/', views.ManageEvents, name='ManageEvents'),
    path('delete_event/<str:ResNumberHouse>/<int:Managerid>/', views.DeleteEvent, name='DeleteEvent'),
    
    path('ManageResident/<int:Managerid>/', views.ManageResident, name='ManageResident'),
    path('CreateResident/<int:Managerid>/', views.CreateResident, name='CreateResident'),
    path('DeleteResident/<int:Resid>/', views.DeleteResident, name='DeleteResident'),

    path('ViewComplain/<int:Managerid>/', views.ViewComplain, name='ViewComplain'),
    path('delete_complain/<str:ResNumberHouse>/<int:Managerid>/', views.DeleteComplain, name='DeleteComplain'),



    path('manager/<int:Managerid>/shift_duty/', views.ManageShiftDuty, name='ManageShiftDuty'),
    path('manager/<int:Managerid>/shift_duty/create/', views.CreateShiftDuty, name='CreateShiftDuty'),
    path('manager/<int:Managerid>/shift_duty/update/<int:Duties_number>/', views.UpdateShiftDuty, name='UpdateShiftDuty'),
    path('manager/<int:Managerid>/shift_duty/delete/<int:Duties_number>/', views.DeleteShiftDuty, name='DeleteShiftDuty'),
]
