from django.shortcuts import render, redirect
from .models import Manager, RESIDENT, STAFF, Visitor, EVENT, REPORT, Duties
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

def mainpage(request):
    return render(request, 'Mainpage_About.html')

def Choosepage(request):
    return render(request, 'choosepage.html')

def Rulespage(request):
    return render(request, 'RulesPage.html')

def Feedback(request):
    return render(request, 'Feedback.html')

def Residentlogin(request):
    error_message = None
    resident = None

    if request.method == 'POST':
        Resid = request.POST['Resid']
        ResPassword = request.POST['ResPassword']
        try:
            resident = RESIDENT.objects.get(Resid=Resid, ResPassword=ResPassword)
        except RESIDENT.DoesNotExist:
            error_message = 'Invalid ID or password'
        
        if resident:
            Resid = resident.Resid
            ResidentPage_url = reverse('ResidentPage', args=[Resid])
            return HttpResponseRedirect(ResidentPage_url)

    return render(request, "LoginpageResident.html", {'error_message': error_message})

def ResidentPage(request, Resid):
    residents = RESIDENT.objects.all()
    try:
        resident = RESIDENT.objects.get(Resid=Resid)
    except RESIDENT.DoesNotExist:
        return render(request, "LoginpageResident.html",)
    
    return render(request, "ResidentPage.html", {'resident': resident, 'residents': residents})

def ApplyEvent(request, Resid):
    residents = RESIDENT.objects.all()

    if request.method == 'POST':
        ResNumberHouse = request.POST.get('ResNumberHouse')
        ResidentName = request.POST.get('ResidentName')
        ResidentPurpose = request.POST.get('ResidentPurpose')
        ResidentStart = request.POST.get('ResidentStart')
        ResidentEnd = request.POST.get('ResidentEnd')

        if ResNumberHouse and ResidentName and ResidentPurpose and ResidentStart and ResidentEnd:
            try:
                # Fetch resident object
                resident = RESIDENT.objects.get(Resid=ResidentName)
                manager = resident.manager

                # Check for existing event with the same ResNumberHouse
                existing_event = EVENT.objects.filter(ResNumberHouse=ResNumberHouse).exists()
                if existing_event:
                    # If an event with the same ResNumberHouse already exists, show an error message
                    return render(request, "ApplyEvent_Resident.html", {
                        'residents': residents,
                        'Resid': Resid,
                        'error_message': 'An event with this house number already exists. Please choose a different house number.'
                    })

                # Create a new event
                event = EVENT.objects.create(
                    ResNumberHouse=ResNumberHouse,
                    Resname=resident,
                    ResidentPurpose=ResidentPurpose,
                    ResidentStart=ResidentStart,
                    ResidentEnd=ResidentEnd,
                    manager=manager
                )

                # Redirect to ResidentPage after event creation
                return redirect('ResidentPage', Resid=Resid)
            
            except RESIDENT.DoesNotExist:
                # Handle case where the resident does not exist
                return render(request, "ApplyEvent_Resident.html", {
                    'residents': residents,
                    'Resid': Resid,
                    'error_message': 'Selected resident does not exist.'
                })

            except IntegrityError:
                # Handle any integrity errors that might still occur
                return render(request, "ApplyEvent_Resident.html", {
                    'residents': residents,
                    'Resid': Resid,
                    'error_message': 'Failed to create the event due to a unique constraint violation.'
                })

        else:
            return render(request, "ApplyEvent_Resident.html", {
                'residents': residents,
                'Resid': Resid,
                'error_message': 'All fields are required.'
            })

    # Handle GET request (rendering the form initially)
    return render(request, "ApplyEvent_Resident.html", {'residents': residents, 'Resid': Resid})


def ApplyPassResident(request, Resid):
    try:
        resident = RESIDENT.objects.get(Resid=Resid)
    except RESIDENT.DoesNotExist:
        return render(request, "error.html", {'error_message': 'Profile not found'})

    if request.method == 'POST':
        visitor_number_ic = request.POST.get('VisitorNumberIC')
        visitor_house_number = request.POST.get('VisitorHouseNumber')
        visitor_purpose = request.POST.get('VisitorPurpose')

        if visitor_number_ic and visitor_house_number and visitor_purpose:
            manager = resident.manager
            
            visitor = Visitor.objects.create(
                VisitorNumberIC=visitor_number_ic,
                VisitorHouseNumber=visitor_house_number,
                VisitorPurpose=visitor_purpose,
                manager=manager
            )

            return redirect('ResidentPage', Resid=Resid)
        else:
            return render(request, "ApplyPassVisitorResident.html", {
                'resident': resident,
                'error_message': 'All fields are required.'
            })

    return render(request, "ApplyPassVisitorResident.html", {'resident': resident})


def Applyreport(request, Resid):
    residents = RESIDENT.objects.all()
    
    try:
        resident = RESIDENT.objects.get(Resid=Resid)
    except RESIDENT.DoesNotExist:
        resident = None
    
    if request.method == 'POST':
        ResNumberHouse = request.POST.get('ResNumberHouse')
        ResCategory = request.POST.get('ResCategory')
        ResDescription = request.POST.get('ResDescription')

        if ResNumberHouse and ResCategory and ResDescription:
            report = REPORT.objects.create(
                ResNumberHouse=ResNumberHouse,
                ResCategory=ResCategory,
                Resname=resident,
                ResDescription=ResDescription
            )
            return redirect('ResidentPage', Resid=Resid)
        else:
            messages.error(request, 'All fields are required.')

    return render(request, "Complain_Resident.html", {'residents': residents, 'resident': resident, 'Resid': Resid})



def Stafflogin(request):
    error_message = None
    staff = None

    if request.method == 'POST':
        Staffid = request.POST['Staffid']
        StaffPassword = request.POST['StaffPassword']
        try:
            staff = STAFF.objects.get(Staffid=Staffid, StaffPassword=StaffPassword)
        except STAFF.DoesNotExist:
            error_message = 'Invalid ID or password'
        
        if staff:
            staff = staff.Staffid
            StaffPage_url = reverse('StaffPage', args=[Staffid])
            return HttpResponseRedirect(StaffPage_url)

    return render(request, "LoginpageStaff.html", {'error_message': error_message})

def StaffPage(request, Staffid):
    staffs = STAFF.objects.all()
    try:
        staff = STAFF.objects.get(Staffid=Staffid)
    except STAFF.DoesNotExist:
        return render(request, "LoginpageStaff.html",)
    
    return render(request, "StaffPage.html", {'staff': staff, 'staffs': staffs})

def ViewDutiesShift(request, Staffid):
    try:
        staff = STAFF.objects.get(Staffid=Staffid)
        duties = Duties.objects.filter(Staffname=staff)  # Filter duties related to the staff member
    except STAFF.DoesNotExist:
        return render(request, "LoginpageStaff.html")
    
    context = {
        'staff': staff,
        'duties': duties
    }
    return render(request, "ViewDutyStaff.html", context)



def ViewResident(request, Staffid):
    try:
        staff = STAFF.objects.get(Staffid=Staffid)
        alldata = RESIDENT.objects.all()  # Fetch all resident data
    except STAFF.DoesNotExist:
        return render(request, "LoginpageStaff.html")
    
    context = {
        'staff': staff,
        'alldata': alldata
    }
    return render(request, "ViewResident.html", context)


def ViewVisitor(request, Staffid):
    try:
        staff = STAFF.objects.get(Staffid=Staffid)
        alldata = Visitor.objects.all()  # Fetch all visitor data
    except STAFF.DoesNotExist:
        return render(request, "LoginpageStaff.html")
    
    context = {
        'staff': staff,
        'alldata': alldata
    }
    return render(request, "ViewVisitor.html", context)

def ApplyPassStaff(request, Staffid):
    try:
        staff = STAFF.objects.get(Staffid=Staffid)
    except STAFF.DoesNotExist:
        return render(request, "error.html", {'error_message': 'Staff profile not found'})

    if request.method == 'POST':
        visitor_number_ic = request.POST.get('VisitorNumberIC')
        visitor_house_number = request.POST.get('VisitorHouseNumber')
        visitor_purpose = request.POST.get('VisitorPurpose')

        if visitor_number_ic and visitor_house_number and visitor_purpose:
            # Assuming you want to associate this visitor with the manager of the staff
            manager = staff.manager

            # Create Visitor object
            visitor = Visitor.objects.create(
                VisitorNumberIC=visitor_number_ic,
                VisitorHouseNumber=visitor_house_number,
                VisitorPurpose=visitor_purpose,
                manager=manager
            )

            # Redirect to staff page after successful submission
            return redirect('StaffPage', Staffid=Staffid)
        else:
            return render(request, "ApplyPassVisitorStaff.html", {
                'staff': staff,
                'error_message': 'All fields are required.'
            })

    return render(request, "ApplyPassVisitorStaff.html", {'staff': staff})

def Managerlogin(request):
    error_message = None
    manager = None

    if request.method == 'POST':
        Managerid = request.POST['Managerid']
        ManagerPassword = request.POST['ManagerPassword']
        try:
            manager = Manager.objects.get(Managerid=Managerid, ManagerPassword=ManagerPassword)
        except Manager.DoesNotExist:
            error_message = 'Invalid ID or password'
        
        if manager:
            Managerid = manager.Managerid
            ManagerPage_url = reverse('ManagerPage', args=[Managerid])
            return HttpResponseRedirect(ManagerPage_url)

    return render(request, "LoginpageManager.html", {'error_message': error_message})

def ManagerPage(request, Managerid):
    managers = Manager.objects.all()
    try:
        manager = Manager.objects.get(Managerid=Managerid)
    except Manager.DoesNotExist:
        return render(request, "LoginpageManager.html",)
    
    return render(request, "ManagerPage.html", {'manager': manager, 'managers': managers})

def ManageEvents(request, Managerid):
    managers = Manager.objects.all()
    try:
        manager = Manager.objects.get(Managerid=Managerid)
    except Manager.DoesNotExist:
        return render(request, "LoginpageManager.html")
    
    events = EVENT.objects.select_related('Resname').all()  # Ensure related Resident data is retrieved

    context = {
        'manager': manager,
        'managers': managers,
        'events': events
    }

    return render(request, "ManageEvent.html", context)

def DeleteEvent(request, ResNumberHouse, Managerid):
    event = get_object_or_404(EVENT, ResNumberHouse=ResNumberHouse)
    event.delete()
    return redirect('ManageEvents', Managerid=Managerid)


def ManageResident(request, Managerid):
    managers = Manager.objects.all()
    try:
        manager = Manager.objects.get(Managerid=Managerid)
    except Manager.DoesNotExist:
        return render(request, "LoginpageManager.html")
    
    residents = RESIDENT.objects.all()  # Retrieve all residents

    context = {
        'manager': manager,
        'managers': managers,
        'residents': residents
    }

    return render(request, "ManageResident.html", context)

def CreateResident(request, Managerid):
    managers = Manager.objects.all()
    try:
        manager = Manager.objects.get(Managerid=Managerid)
    except Manager.DoesNotExist:
        return render(request, "LoginpageManager.html")
    
    if request.method == "POST":
        res_name = request.POST.get('Resname')
        res_email = request.POST.get('Resemail')
        res_phone = request.POST.get('Resphonenumber')
        res_password = request.POST.get('ResPassword')
        
        if res_name and res_email and res_phone and res_password:
            new_resident = RESIDENT.objects.create(
                Resname=res_name,
                Resemail=res_email,
                Resphonenumber=res_phone,
                ResPassword=res_password,
                manager=manager  # Assign the manager instance to the manager field
            )
            return redirect('ManageResident', Managerid=Managerid)
        else:
            return HttpResponse("All fields are required")

    context = {
        'manager': manager,
        'managers': managers
    }

    return render(request, "CreateResident.html", context)

def DeleteResident(request, Resid):
    resident = get_object_or_404(RESIDENT, Resid=Resid)
    manager_id = resident.Managerid
    resident.delete()
    return redirect('ManageResident', Managerid=manager_id)


def ManageVisits(request, Managerid):
    managers = Manager.objects.all()
    try:
        manager = Manager.objects.get(Managerid=Managerid)
    except Manager.DoesNotExist:
        return render(request, "LoginpageManager.html")

    alldata = Visitor.objects.all()

    context = {
        'manager': manager,
        'managers': managers,
        'alldata': alldata
    }

    return render(request, "ManageVisits.html", context)

def DeleteVisitor(request, VisitorName, Managerid):
    visitor = get_object_or_404(Visitor, VisitorName=VisitorName)
    visitor.delete()
    return redirect('ManageVisits', Managerid=Managerid)



def ViewComplain(request, Managerid):
    managers = Manager.objects.all()
    try:
        manager = Manager.objects.get(Managerid=Managerid)
    except Manager.DoesNotExist:
        return render(request, "LoginpageManager.html",)
    
    alldata = REPORT.objects.all()  # Fetch all report data

    context = {
        'manager': manager,
        'managers': managers,
        'alldata': alldata
    }

    return render(request, "ViewComplain.html", context)

def ManageShiftDuty(request, Managerid):
    try:
        manager = Manager.objects.get(Managerid=Managerid)
    except Manager.DoesNotExist:
        return render(request, "LoginpageManager.html")

    duties = Duties.objects.filter(manager=manager)  # Filter duties by manager

    context = {
        'manager': manager,
        'duties': duties  # Pass duties queryset to the template
    }

    return render(request, "ManageShiftDuties.html", context)

def DeleteComplain(request, ResNumberHouse, Managerid):
    report = get_object_or_404(REPORT, ResNumberHouse=ResNumberHouse)
    report.delete()
    return redirect('ViewComplain', Managerid=Managerid)


def CreateShiftDuty(request, Managerid):
    try:
        manager = Manager.objects.get(Managerid=Managerid)
        staff_list = STAFF.objects.filter(manager=manager)
    except Manager.DoesNotExist:
        return render(request, "LoginpageManager.html")

    if request.method == "POST":
        staff_id = request.POST.get('StaffID')
        staff = get_object_or_404(STAFF, Staffid=staff_id, manager=manager)

        assign_to = request.POST.get('Assignto')
        due_date = request.POST.get('Duedate')

        if staff_id and assign_to and due_date:
            new_shift_duty = Duties.objects.create(
                Staffname=staff,
                Assignto=assign_to,
                Duedate=due_date,
                manager=manager
            )
            return redirect('ManageShiftDuty', Managerid=Managerid)
        else:
            return render(request, "CreateShiftDuty.html", {
                'manager': manager,
                'staff_list': staff_list,
                'error_message': "All fields are required"
            })

    context = {
        'manager': manager,
        'staff_list': staff_list,
    }

    return render(request, "CreateShiftDuty.html", context)

def DeleteShiftDuty(request, Managerid, Duties_number):
    try:
        manager = Manager.objects.get(Managerid=Managerid)
        # Fetch the duty object to delete
        shift_duty = Duties.objects.get(Duties_number=Duties_number, manager=manager)
        # Save the manager id for redirection after deletion
        manager_id = shift_duty.manager.Managerid
        # Delete the shift duty object
        shift_duty.delete()
        
        # Redirect to manage shift duty page
        return redirect('ManageShiftDuty', Managerid=manager_id)
    
    except Manager.DoesNotExist:
        return render(request, "LoginpageManager.html")
    except Duties.DoesNotExist:
        return render(request, "ErrorPage.html", {'error_message': 'Shift Duty not found.'})
def UpdateShiftDuty(request, Managerid, Duties_number):
    try:
        manager = Manager.objects.get(Managerid=Managerid)
        duty = Duties.objects.get(Duties_number=Duties_number, manager=manager)
        staff_list = STAFF.objects.filter(manager=manager)
        
        if request.method == 'POST':
            staff_id = request.POST.get('StaffID')
            Assignto = request.POST.get('Assignto')
            Duedate = request.POST.get('Duedate')
            
            # Fetch the staff object
            staff = get_object_or_404(STAFF, Staffid=staff_id, manager=manager)
            
            # Update the duty object
            duty.Staffname = staff
            duty.Assignto = Assignto
            duty.Duedate = Duedate
            duty.save()
            
            # Redirect to manage shift duty page
            return HttpResponseRedirect(reverse('ManageShiftDuty', args=(Managerid,)))
        
    except Manager.DoesNotExist:
        return render(request, "LoginpageManager.html")
    except Duties.DoesNotExist:
        return render(request, "ErrorPage.html", {'error_message': 'Shift Duty not found.'})
    
    context = {
        'manager': manager,
        'duty': duty,
        'staff_list': staff_list,
    }
    
    return render(request, "UpdateShiftDuty.html", context)


