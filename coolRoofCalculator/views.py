from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import SimpleForm
from .models import SimpleForm_Base
from .models import SimpleForm_Proposed
from .forms import FormSimple
from .codecheck import do_something
from .MainFile import ProcessSingleFloor
from .MainFile import RunSimulations
from .MainFile import FetchResutls
#import mysql.connector
import uuid
import os
import sys
import re
DirPath = os.path.dirname(os.path.abspath(__file__))
#disabling csrf (cross site request forgery)
@csrf_exempt


def glossary(request):
    return render(request, 'glossary.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def testindex(request):
    return render(request, 'test.html')

def index(request):
    return render(request, 'index.html')

def insertdb(request):
    if request.method == 'POST':
        form = FormSimple(request.POST)
        if form.is_valid():
            Area = request.POST.get('Area')
            WeatherFile = request.POST.get('WeatherFile')
            Buildingtype = request.POST.get('buildingtype')
            OrientationOfRoof = request.POST.get('Orientation')
            WWR = request.POST.get('WWR')
            HVAC_Type = request.POST.get('HVAC_Type')
            Slope_Angle = request.POST.get('Slope_Angle')
            Electricity = request.POST.get('Electricity')
            RoofContructionc = request.POST.get('RoofContruction')
            SR_Basec = request.POST.get('SR_Base')
            IE_Basec = request.POST.get('IE_Base')
            SR_Proposec = request.POST.get('SR_Propose')
            IE_Proposec = request.POST.get('IE_Propose')
            check = do_something(17)
            simpleform_obj=SimpleForm(Area=Area,OrientationOfRoof=OrientationOfRoof,\
                WeatherFile=WeatherFile,WWR=WWR, Coolroof=True,SR_Base=SR_Basec,IE_Base=IE_Basec,SR_Propose=SR_Proposec,IE_Propose=IE_Proposec,RoofContruction=RoofContructionc,ElectricityRate=Electricity)
            useriddisplay = simpleform_obj.Userid
            timedisplay = simpleform_obj.Timestamp
            simpleform_obj.save()
            executed=0
            Coolroof="ON"
            print (useriddisplay)
            executed,BaseDirAddr,ProposedDirAddr = ProcessSingleFloor(Buildingtype,HVAC_Type,Coolroof,OrientationOfRoof,\
                        WWR,Area,useriddisplay,SR_Basec,IE_Basec,SR_Proposec,IE_Proposec,Electricity,Slope_Angle,RoofContructionc)
            if executed == 1:
                #filename ='/b.idf'
                #simulationSuccess_Flag =1
                simulationSuccess_Flag = RunSimulations(WeatherFile,BaseDirAddr,ProposedDirAddr)
                if simulationSuccess_Flag==1:
                    EnergyOut = 1991
                    Datbasestaus = "Test Sucess"
                    BCoolingResult,BHeatingResult,PCoolingResult,PHeatingResult= FetchResutls(BaseDirAddr,ProposedDirAddr)
                    Datbasestaus = databaseinsert(BCoolingResult,BHeatingResult,PCoolingResult,PHeatingResult,Area,\
                        OrientationOfRoof,WeatherFile,WWR,timedisplay,useriddisplay,Electricity)
                    return redirect('/result?'+"Simulation_id="+str(useriddisplay))
            else:
                return HttpResponse("error in generating IDF")
    else:
        return HttpResponse("Error!")

def databaseinsert(BCoolingResult,BHeatingResult,PCoolingResult,PHeatingResult,Area,OrientationOfRoof,WeatherFile,WWR,timedisplay,useriddisplay,ElectricityCost):
    simpleformbase_obj=SimpleForm_Base(Userid=useriddisplay,Area=Area,OrientationOfRoof=OrientationOfRoof, WeatherFile=WeatherFile,WWR=WWR,ElectricityRate =ElectricityCost,\
                Heating_Jan=BHeatingResult[0],Heating_Feb=BHeatingResult[1],Heating_March=BHeatingResult[2],\
                Heating_April=BHeatingResult[3],Heating_May=BHeatingResult[4],Heating_June=BHeatingResult[5],\
                Heating_July=BHeatingResult[6],Heating_August=BHeatingResult[7],Heating_Sept=BHeatingResult[8],\
                Heating_Oct=BHeatingResult[9],Heating_Nov=BHeatingResult[10],Heating_Dec=BHeatingResult[11],\
                Cooling_Jan=BCoolingResult[0],Cooling_Feb=BCoolingResult[1],Cooling_March=BCoolingResult[2],\
                Cooling_April=BCoolingResult[3],Cooling_May=BCoolingResult[4],Cooling_June=BCoolingResult[5],\
                Cooling_July=BCoolingResult[6],Cooling_August=BCoolingResult[7],Cooling_Sept=BCoolingResult[8],\
                Cooling_Oct=BCoolingResult[9],Cooling_Nov=BCoolingResult[10],Cooling_Dec=BCoolingResult[11])
    simpleformPropose_obj = SimpleForm_Proposed(Userid=useriddisplay,Area=Area,OrientationOfRoof=OrientationOfRoof, WeatherFile=WeatherFile,WWR=WWR,ElectricityRate = ElectricityCost,\
                Heating_Jan=PHeatingResult[0],Heating_Feb=PHeatingResult[1],Heating_March=PHeatingResult[2],\
                Heating_April=PHeatingResult[3],Heating_May=PHeatingResult[4],Heating_June=PHeatingResult[5],\
                Heating_July=PHeatingResult[6],Heating_August=PHeatingResult[7],Heating_Sept=PHeatingResult[8],\
                Heating_Oct=PHeatingResult[9],Heating_Nov=PHeatingResult[10],Heating_Dec=PHeatingResult[11],\
                Cooling_Jan=PCoolingResult[0],Cooling_Feb=PCoolingResult[1],Cooling_March=PCoolingResult[2],\
                Cooling_April=PCoolingResult[3],Cooling_May=PCoolingResult[4],Cooling_June=PCoolingResult[5],\
                Cooling_July=PCoolingResult[6],Cooling_August=PCoolingResult[7],Cooling_Sept=PCoolingResult[8],\
                Cooling_Oct=PCoolingResult[9],Cooling_Nov=PCoolingResult[10],Cooling_Dec=PCoolingResult[11])
    simpleformbase_obj.save()
    simpleformPropose_obj.save()
    return "Success"

def displayResult(request):
    Simulation_id_hex = request.GET.get('Simulation_id')
    Simulation_code = re.sub('-','',Simulation_id_hex)
    print (Simulation_code)
    con = mysql.connector.connect(user='root',password='docnme@123',host='localhost',database='coolroof')
    cur = con.cursor()
    commandBase ="select * from coolRoofCalculator_simpleform_base where Userid ="+"'"+str(Simulation_code)+"'"
    print (commandBase)
    cur.execute(commandBase)
    BResult = cur.fetchall()
    commandPropose = "select * from coolRoofCalculator_simpleform_proposed where Userid ="+"'"+str(Simulation_code)+"'"
    print (commandPropose)
    cur.execute(commandPropose)
    PResult = cur.fetchall()
    cur.close()
    Cost1 = BResult[0][5]
    Cost2 = PResult[0][5]
    Area = BResult[0][1]
    BCoolingResult=[0,0,0,0,0,0,0,0,0,0,0,0]
    PCoolingResult=[0,0,0,0,0,0,0,0,0,0,0,0]
    BHeatingResult=[0,0,0,0,0,0,0,0,0,0,0,0]
    PHeatingResult=[0,0,0,0,0,0,0,0,0,0,0,0]
    j=0
    for i in range (6,18):
    	BHeatingResult[j]=BResult[0][i]
    	PHeatingResult[j]=PResult[0][i]
    	j=j+1
    j=0
    for i in range (18,30):
    	BCoolingResult[j]=BResult[0][i]
    	PCoolingResult[j]=PResult[0][i]
    	j=j+1
    TotalBCoolingEnergy=0
    TotalBHeatingEnergy=0
    TotalPCoolingEnergy=0
    TotalPHeatingEnergy=0
    for	i in range(12):
    	TotalBCoolingEnergy = TotalBCoolingEnergy + BCoolingResult[i]
    	TotalPCoolingEnergy=TotalPCoolingEnergy + PCoolingResult[i]
    	TotalBHeatingEnergy =TotalBHeatingEnergy + BHeatingResult[i]
    	TotalPHeatingEnergy=TotalPHeatingEnergy + PHeatingResult[i]
    TotalEnergy=[TotalBCoolingEnergy,TotalPCoolingEnergy,TotalBHeatingEnergy,TotalPHeatingEnergy]
    CoolingSavings = (TotalBCoolingEnergy - TotalPCoolingEnergy)
    HeatingSavings = (TotalBHeatingEnergy - TotalPHeatingEnergy)
    CoolingSavingperArea = float(CoolingSavings/Area)
    HeatingSavingperArea = float(HeatingSavings/Area)
    CoolingSavingsCost = float(Cost1*CoolingSavings)
    HeatingSavingsCost=  float(Cost1*HeatingSavings)
    OverallEnergySavings = (CoolingSavings-(-HeatingSavings))
    overallAreaSavings = (CoolingSavingperArea-(-HeatingSavingperArea))
    OverallCostSavings = (CoolingSavingsCost-(-HeatingSavingsCost))
    return render(request, 'Linechart.html',{'BCool':BCoolingResult,'PCool':PCoolingResult,\
    'BHeat':BHeatingResult,'PHeat':PHeatingResult,'CoolEnergy':CoolingSavings,'HeatEnergy':HeatingSavings,\
    'OverallEnergy':OverallEnergySavings,'CoolEnergyArea':CoolingSavingperArea,\
    'HeatEnergyArea':HeatingSavingperArea,'OverallEnergyArea':overallAreaSavings,\
    'CostCooling':CoolingSavingsCost,'CostHeating':HeatingSavingsCost,\
    'OverallCost':OverallCostSavings})
