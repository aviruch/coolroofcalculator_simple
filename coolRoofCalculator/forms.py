from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

#from django.utils.translation import ugettext_lazy as _
import datetime



class FormSimple(forms.Form):
    Area = forms.IntegerField()
    WeatherFile = forms.CharField()
    buildingtype = forms.CharField()
    Orientation = forms.IntegerField()
    WWR = forms. FloatField()
    HVAC_Type = forms.CharField()
    Slope_Angle = forms.FloatField()
    SR_Base = forms. FloatField()
    IE_Base = forms. FloatField()
    SR_Propose = forms. FloatField()
    IE_Propose = forms. FloatField()
    Electricity = forms. FloatField()
    RoofContruction = forms. CharField()