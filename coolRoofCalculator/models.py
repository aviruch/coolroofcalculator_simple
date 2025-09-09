import uuid
from django.db import models

class SimpleForm(models.Model):
    Userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Timestamp = models.DateTimeField(auto_now_add=True)
    Area = models.IntegerField()
    OrientationOfRoof = models.IntegerField()
    WeatherFile = models.CharField(max_length=120, blank=True, null=True)
    WWR = models.FloatField()
    SR_Base = models.FloatField()
    IE_Base = models.FloatField()
    SR_Propose = models.FloatField()
    IE_Propose = models.FloatField()
    Coolroof = models.BooleanField()
    RoofContruction = models.CharField(max_length=120, blank=True, null=True)
    ElectricityRate = models.FloatField()
    Email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Simulation {self.Userid} - Area {self.Area}"


class SimpleForm_Base(models.Model):
    Userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Timestamp = models.DateTimeField(auto_now_add=True)
    Area = models.IntegerField()
    OrientationOfRoof = models.IntegerField()
    WeatherFile = models.CharField(max_length=120, blank=True, null=True)
    WWR = models.FloatField()
    ElectricityRate = models.FloatField()

    # Monthly heating/cooling values
    Heating_Jan = models.FloatField()
    Heating_Feb = models.FloatField()
    Heating_March = models.FloatField()
    Heating_April = models.FloatField()
    Heating_May = models.FloatField()
    Heating_June = models.FloatField()
    Heating_July = models.FloatField()
    Heating_August = models.FloatField()
    Heating_Sept = models.FloatField()
    Heating_Oct = models.FloatField()
    Heating_Nov = models.FloatField()
    Heating_Dec = models.FloatField()

    Cooling_Jan = models.FloatField()
    Cooling_Feb = models.FloatField()
    Cooling_March = models.FloatField()
    Cooling_April = models.FloatField()
    Cooling_May = models.FloatField()
    Cooling_June = models.FloatField()
    Cooling_July = models.FloatField()
    Cooling_August = models.FloatField()
    Cooling_Sept = models.FloatField()
    Cooling_Oct = models.FloatField()
    Cooling_Nov = models.FloatField()
    Cooling_Dec = models.FloatField()


class SimpleForm_Proposed(models.Model):
    Userid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Timestamp = models.DateTimeField(auto_now_add=True)
    Area = models.IntegerField()
    OrientationOfRoof = models.IntegerField()
    WeatherFile = models.CharField(max_length=120, blank=True, null=True)
    WWR = models.FloatField()
    ElectricityRate = models.FloatField()

    # Monthly heating/cooling values
    Heating_Jan = models.FloatField()
    Heating_Feb = models.FloatField()
    Heating_March = models.FloatField()
    Heating_April = models.FloatField()
    Heating_May = models.FloatField()
    Heating_June = models.FloatField()
    Heating_July = models.FloatField()
    Heating_August = models.FloatField()
    Heating_Sept = models.FloatField()
    Heating_Oct = models.FloatField()
    Heating_Nov = models.FloatField()
    Heating_Dec = models.FloatField()

    Cooling_Jan = models.FloatField()
    Cooling_Feb = models.FloatField()
    Cooling_March = models.FloatField()
    Cooling_April = models.FloatField()
    Cooling_May = models.FloatField()
    Cooling_June = models.FloatField()
    Cooling_July = models.FloatField()
    Cooling_August = models.FloatField()
    Cooling_Sept = models.FloatField()
    Cooling_Oct = models.FloatField()
    Cooling_Nov = models.FloatField()
    Cooling_Dec = models.FloatField()
