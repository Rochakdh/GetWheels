from django.contrib import admin
from  .models import VehicleAvailable,UserAvailable,ItemsOrdered,Consultaion
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAd
# import random
# import string



# class VehicleAvailableAdmin(admin.ModelAdmin):
#     list_display=('title_name','user','vech_owner','manufacturer_company','type','model','available_till_date',)
#     search_fields=('user__username','vech_owner__com_ind_name','manufacturer_company','type','manufacturer_company','model',)
#     list_filter=('type',)
#     # prepopulated_fields={'slug':('manufacturer_company','type','model',VehicleAvailable.rand_slug())}
#
#     def title_name(self,VehicleAvailable):
#         title="{}-{}-{}".format(VehicleAvailable.manufacturer_company,VehicleAvailable.model,VehicleAvailable.type)
#         return title

    #  def rand_slug(self):
    #     return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))



# admin.site.register(VehicleAvailable,VehicleAvailableAdmin)
admin.site.register(VehicleAvailable)
admin.site.register(UserAvailable)
# admin.site.register(Renter)
admin.site.register(ItemsOrdered)
admin.site.register(Consultaion)