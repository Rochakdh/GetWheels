from django.db import models
from django.db import models
from datetime import time
from django.shortcuts import reverse
from django.conf import settings
import uuid
import random
import string
# from django.template.defaultfilters import slugify

# Create your models here.
VTYPE=(('Car','Car'),('Bike','Bike'),('Bus','Bus'),('Truck','Truck'),('Bicycle','Bicycle'))
RENTERTYPE=(('Individual','Individual'),('Company','Company'))

class Renter(models.Model):

    register_as = models.TextField(choices=RENTERTYPE)
    com_ind_name = models.TextField(max_length=500)
    available_from=models.TimeField()
    available_till = models.TimeField()
    autocode = models.CharField(max_length=100, blank=True, unique=True,default=uuid.uuid4)
    phoneno = models.IntegerField()
    special_rating = models.BooleanField(default=0)
    def __str__(self):
        return self.com_ind_name

class VehicleAvailable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None,null=True)
    vech_owner = models.ForeignKey(Renter,on_delete=models.CASCADE)
    type = models.TextField()
    manufacturer_company = models.TextField(max_length=100)
    model = models.TextField(max_length=100)
    pickup = models.TextField(max_length=300)
    dropup = models.TextField(max_length=300)
    available_till_time = models.TimeField(null= True,blank=True)
    available_till_date = models.DateField()
    # special_rating=models.BooleanField(default=0)
    description = models.TextField(max_length=500)
    image = models.TextField()
    priceph = models.IntegerField()
    km_travelled = models.IntegerField()
    slug  = models.SlugField(unique=True)
    ordered = models.BooleanField(default=False)
    # date_created = models.DateTimeField(auto_now_add=True,default='')
    # date_modifried = models.DateTimeField(auto_now=True,default='')
    # slug_random=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

    def __str__(self):
        title=self.manufacturer_company+" "+self.model+" "+self.type
        return title

    def get_absolute_url(self):
        return reverse("home:reservation", kwargs={'slug': self.slug})

# class (models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     items = models.ManyToManyField(VehicleAvailable)
#     # renter_details=items.vech_owner
#     ordered = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.user.username

class UserAvailable(models.Model):#all details of users that want to order vehicle
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,default=None,null=True)
    phone=models.IntegerField()
    items = models.ManyToManyField(VehicleAvailable)
    location=models.TextField(max_length=200)
    renter_details=models.ForeignKey(Renter,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    info=models.TextField(max_length=400)
    def __str__(self):
        return self.user.username +"-->"+ self.items.__str__()


class ItemsOrdered(models.Model): #all vehicles detail tha has been ordered for trasanction history
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING)
    item = models.ForeignKey(VehicleAvailable,on_delete=models.CASCADE)
    orderedfrom = models.ForeignKey(Renter,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    free = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username +"-->"+ self.item.__str__()