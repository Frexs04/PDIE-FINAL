from django.db import models

# Create your models here.
class Manager(models.Model):
    Managerid = models.AutoField(primary_key=True)
    Managername = models.CharField(max_length=20)
    Manageremail = models.EmailField(max_length=100)
    Managerphone_number = models.CharField(max_length=15)
    ManagerPassword = models.CharField(max_length=100)

class RESIDENT(models.Model):
    Resid=models.AutoField(primary_key=True)
    Resname=models.CharField(max_length=20)
    Resemail=models.CharField(max_length=100)
    Resphonenumber=models.CharField(max_length=15)
    ResPassword = models.CharField(max_length=100)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

class STAFF(models.Model):
    Staffid=models.AutoField(primary_key=True)
    Staffname=models.CharField(max_length=20)
    Staffemail=models.CharField(max_length=100)
    Staffphonenumber=models.CharField(max_length=15)
    StaffPassword = models.CharField(max_length=100)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

class Visitor(models.Model):
    VisitorName=models.AutoField(primary_key=True)
    VisitorNumberIC=models.CharField(max_length=15)
    VisitorHouseNumber=models.CharField(max_length=20)
    VisitorPurpose=models.CharField(max_length=100)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

class EVENT(models.Model):
    ResNumberHouse=models.CharField(primary_key=True,max_length=100)
    Resname = models.ForeignKey(RESIDENT, on_delete=models.CASCADE)
    ResidentPurpose=models.CharField(max_length=100)
    ResidentStart=models.CharField(max_length=15)
    ResidentEnd=models.CharField(max_length=15)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

class REPORT(models.Model):
    ResNumberHouse=models.CharField(primary_key=True,max_length=100)
    ResCategory=models.CharField(max_length=15)
    Resname = models.ForeignKey(RESIDENT, on_delete=models.CASCADE)
    ResDescription=models.CharField(max_length=1000)

class Duties(models.Model):
    Duties_number = models.AutoField(primary_key=True)
    Staffname = models.ForeignKey(STAFF, on_delete=models.CASCADE)
    Assignto =models.CharField(max_length=1000)
    Duedate =models.CharField(max_length=1000)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)



