from rest_framework import serializers
from home.models import VehicleAvailable

class ItemSerializers(serializers.ModelSerializer):
    # name = serializers.StringRelatedField(many=True)
    class Meta:
        model= VehicleAvailable
        fields = [
        # 'vech_owner__com_ind_name',
        'type','manufacturer_company','model','pickup','dropup',
        'available_till_time','available_till_date','description','image','priceph','km_travelled','slug',
        ]