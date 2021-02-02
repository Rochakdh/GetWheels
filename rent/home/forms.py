from django.forms import ModelForm
from .models import Consultaion

class ConsultaionForm(ModelForm):
    class Meta:
        model = Consultaion
        fields = '__all__'


