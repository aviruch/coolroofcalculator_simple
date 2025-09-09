import math
import re
import sys
import os
import time
import xml.etree.cElementTree as ET
import linecache
DirPath = os.path.dirname(os.path.abspath(__file__))

# #### define static params ######

# Area=1000.0;
Height=3.0;
Wall_H = Height
DaylightCtrl = "OFF"
ShadingCtrl = "OFF"
Floors = 1
#Area = BuildingArea/Floors
WindowType = 'STRIP'

WindowHeight = 1
SilHeight= 0.75
WindowWidthP=1

U_value = 3.5
Shgc = 0.3
Vlt = 0.5

Overhang = 0.1
global Shade_Depth
Shade_Depth =0.1
Aspect_Ratio = 1
# #cost fixed as of now
cost_glass = 5000
glass=(Shgc,Vlt,U_value,cost_glass)
monthlist=['January', 'February', 'March', 'April', 'May', 'June', 'July', \
                      'August', 'September', 'October', 'November', 'December'];
#///////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////
def FetchResutls(BaseDirAddr,ProposedDirAddr):
	#time.sleep(1)
	#os.system("clear")
	BaseCaseCoolingResult=[1,2,3,4,5,6,7,8,9,10,11,12]
	BaseCaseHeatingResult=[1,2,3,4,5,6,7,8,9,10,11,12]
	ProposedCaseCoolingResult=[1,2,3,4,5,6,7,8,9,10,11,12]
	ProposedCaseHeatingResult=[1,2,3,4,5,6,7,8,9,10,11,12]
	BaseOutputDirAddr = BaseDirAddr+'/Output/bTable.xml'
	ProposedOutputDirAddr = ProposedDirAddr+'/Output/bTable.xml'
	if (((os.path.exists(BaseDirAddr))==True) and ((os.path.exists(BaseDirAddr))== True)):
		tree1 = ET.ElementTree(file=BaseOutputDirAddr)
		tree2 = ET.ElementTree(file=ProposedOutputDirAddr)
		print ("Base simulation result Cooling")
		for i in range(12):
			BaseCaseCoolingResult[i]=tree1.find('Enduseenergyconsumptionelectricitymonthly/CustomMonthlyReport[8]/'+ monthlist[i]).text
			BaseCaseHeatingResult[i] = tree1.find('Enduseenergyconsumptionelectricitymonthly/CustomMonthlyReport[7]/'+ monthlist[i]).text
			ProposedCaseCoolingResult[i] = tree2.find('Enduseenergyconsumptionelectricitymonthly/CustomMonthlyReport[8]/'+ monthlist[i]).text
			ProposedCaseHeatingResult[i] = tree2.find('Enduseenergyconsumptionelectricitymonthly/CustomMonthlyReport[7]/'+ monthlist[i]).text
		return BaseCaseCoolingResult,BaseCaseHeatingResult,ProposedCaseCoolingResult,ProposedCaseHeatingResult
	else :
		return "Simulation Failure"
#////////////////////////////////////////////////////////////////////////////////////

def RunSimulations(WeatherFile,BaseDirAddr,ProposedDirAddr):
	WeatherFilePath = DirPath+'/WeatherData/' + WeatherFile
	Directorylist =[BaseDirAddr,ProposedDirAddr]
	filename = '/b.idf'
	#energyplus -w IND_Ahmedabad.426470_ISHRAE.epw -p ./Output/b -s C -x -m -r b_86.idf
	for i in range(len(Directorylist)):
		if ((os.path.exists(Directorylist[i]+'/'+'Output')) == True):
			pass
		else:
			#os.mkdir(Directorylist[i]+'/'+'Output', 0777)
			#os.chmod(Directorylist[i]+'/'+'Output', 0777)
			os.mkdir(Directorylist[i]+'/'+'Output', 0o777)
			os.chmod(Directorylist[i]+'/'+'Output', 0o777)
			cmd_test = "/usr/local/bin/energyplus -w "+ WeatherFilePath+ " -p "+Directorylist[i]+ "/Output/b -s C -x -m -r " + Directorylist[i] + filename
			print (cmd_test)
			#os.system("rm -rf ./Output")
			#os.system("mkdir /Output")
			os.system(cmd_test)
			#os.system("gnome-terminal -e 'bash -c \'"+cmd_test+"'\'")
	return 1

#////////////////////////////////////////////////////////////////////////////////////
def generate_co_SingleFloor(Orientation,Area,Ar,Wwr,glass,Overhang,SR,IE,P,ElectricityPrice,RoofContruction):
    
    #STRUCTURAL REPRESENTATION

    #P = 20.0; # Slant Angle
    H = 3.5; # Floor to floor height
    Frame_Width = 0.01 # 10 mm  

    ### Independent Params ###

    W = math.sqrt(Area/Ar);
    L = W*Ar ; 

    ## Derived Vars ##


    #North_Wall_Area = L*H
    #South_Wall_Area = L*H
    #East_Wall_Area  = W*H
    #West_Wall_Area  = W*H
    
    #North_Win_area  = Wwr*L*H
    #South_Win_area  = Wwr*L*H
    #East_Win_area   = Wwr*W*H
    #West_Win_area   = Wwr*W*H

    Window_Length = L - Frame_Width * 2

    Window_Height = Wwr*L*H / Window_Length

    Window_Sill = ( H - Window_Height)/ 2
    # DICTIONARY REPRESENTATION 

    RQ_VAL={};
    RQ_VAL['###ORIENT'] = Orientation 
    RQ_VAL['###GLASS_U_FACTOR'] =  glass[2]
    RQ_VAL['###GLASS_SHGC'] =  glass[0]
    RQ_VAL['###GLASS_VT'] =  glass[1]
    RQ_VAL['###Glass_Cost'] = glass[3] 
    
    RQ_VAL['###X'] =  L
    RQ_VAL['###H1'] =  H
    RQ_VAL['###H2'] =  H + float( L * math.tan((P*3.14)/180) )
    RQ_VAL['###Z_1_DLC_X'] = 1 
    RQ_VAL['###Z_1_DLC_Y'] = 1
    RQ_VAL['###C'] = ElectricityPrice
    RQ_VAL['###SA'] = 1 - float(SR)
    RQ_VAL['###IE'] = float(IE)

    RQ_VAL['###Win_Sill'] = Window_Sill
    RQ_VAL['###Frame_D'] = Frame_Width
    RQ_VAL['###Win_L'] = Window_Length
    RQ_VAL['###Win_H'] = Window_Height
    return RQ_VAL


def GenerateTemplateSingleFloor(Schedule,CoolRoof,DayLightSensor,IntShades,HVAC,RoofContruction,UserDirPath):

    #Schedule = "ResidentialDay" # Other Options are "Retail" and "Institute"
    #DesignDay  Need to change with weather file selection 
    CoolRoof="ON"  #Other Option "Yes"
    DayLightSensor="ON"  #Other Option "OFF"
    IntShades="OFF"  # Other Option "ON"
    HVAC="PTHP" #Other Options are "CentralWaterCooledChiller: CWC" and "CentralAirCooledChiller: CAC"
    UserIDFDirPath= UserDirPath+"/SingleFloorTemplate.idf"
    f=open(UserIDFDirPath,'w')
    #f=open("./SingleFloorTemplate.idf",'w')
    
    # Header file
    print ("Header file")
    file_Header=open(DirPath+"/SingleFloor/01_Header.idf","r")
    g_1=file_Header.read()
    f.write(g_1)
    file_Header.close()
    
 
    #DDY File
    print ("DDY File")
    file_DDY=open(DirPath+"/SingleFloor/02_Size_WeatherData.idf","r")
    g_2=file_DDY.read()
    f.write(g_2)
    file_DDY.close()
    
    # Schedule file
    print ("Schedule file")
    
    if Schedule=="ResidentialDay":
        file_Schedule_ResidentialNight=open(DirPath+"/SingleFloor/03A_Schedule_ResidentialNight.idf","r")
        g_3=file_Schedule_ResidentialNight.read()
        f.write(g_3)
        file_Schedule_ResidentialNight.close()
    
    else :
        file_Schedule_Residential24=open(DirPath+"/SingleFloor/03B_Schedule_Residential24.idf","r")
        g_3=file_Schedule_Residential24.read()
        f.write(g_3)
        file_Schedule_Residential24.close()
    
	
	
	
    '''# Cool Roof
    print "Cool Roof file"
    file_CoolRoof=open(DirPath+"/SingleFloor/04_Roof_SR.idf","r")
    g_4=file_CoolRoof.read()
    f.write(g_4)
    file_CoolRoof.close()
       ''' 
	   
	#//////////////////////////////
	# Materials
    print ("Materials")
    file_Materials=open(DirPath+"/SingleFloor/04A_Materials.idf","r")
    g_4A=file_Materials.read()
    f.write(g_4A)
    file_Materials.close()
        
        
        
	# Construction other than roof
    #print "Construction other than Roof"
    file_Construction=open(DirPath+"/SingleFloor/04B_Construction.idf","r")
    g_4B=file_Construction.read()
    f.write(g_4B)
    file_Construction.close()        
        
        
	# Roof consturciton details        
    #print "Roof Construction Applied"  
    if RoofContruction =="Roof_1": 
        file_RoofCons=open(DirPath+"/SingleFloor/04C_Roof_1_Uninsulated.idf","r")
        g_9=file_RoofCons.read()
        f.write(g_9)
        file_RoofCons.close()
    elif RoofContruction=="Roof_2":
        file_RoofCons=open(DirPath+"/SingleFloor/04C_Roof_2_Insulated25.idf","r")
        g_9=file_RoofCons.read()
        f.write(g_9)
        file_RoofCons.close()
    elif RoofContruction=="Roof_3":
        file_RoofCons=open(DirPath+"/SingleFloor/04C_Roof_3_Insulated50.idf","r")
        g_9=file_RoofCons.read()
        f.write(g_9)
        file_RoofCons.close()    
    else:
    
        file_RoofCons=open(DirPath+"/SingleFloor/04C_Roof_4_Insulated75.idf","r")
        g_9=file_RoofCons.read()
        f.write(g_9)
        file_RoofCons.close()
	#/////////////////////////////
  # Zones
    #print "Zones"
    file_Zones=open(DirPath+"/SingleFloor/05_Zones.idf","r")
    g_5=file_Zones.read()
    f.write(g_5)
    file_Zones.close()

    # Windows
    #print "Windows"
    file_Windows=open(DirPath+"/SingleFloor/05B_Windows.idf","r")
    g_5B=file_Windows.read()
    f.write(g_5B)
    file_Windows.close()
    
    # Gains
    #print "Gains"
    file_Gains=open(DirPath+"/SingleFloor/06_Gains.idf","r")
    g_6=file_Gains.read()
    f.write(g_6)
    file_Gains.close()
    
   # Daylight
    #print "Daylight"
    
    if DayLightSensor=="true": 
        file_DayLight_ON=open(DirPath+"/SingleFloor/07A_Daylight_ON.idf","r")
        g_7=file_DayLight_ON.read()
        f.write(g_7)
        file_DayLight_ON.close()
    else:
        file_DayLight_OFF=open(DirPath+"/SingleFloor/07B_Daylight_OFF.idf","r")
        g_7=file_DayLight_OFF.read()
        f.write(g_7)
        file_DayLight_OFF.close()
   
    
    # Internal Shades
    #print "Internal Shades"
    
    if IntShades=="OFF":
        file_IntShade_OFF=open(DirPath+"/SingleFloor/08A_IntShade_OFF.idf","r")
        g_8=file_IntShade_OFF.read()
        f.write(g_8)
        file_IntShade_OFF.close()
    else:
        file_IntShade_ON=open(DirPath+"/SingleFloor/08A_IntShade_ON.idf","r")
        g_8=file_IntShade_ON.read()
        f.write(g_8)
        file_IntShade_ON.close()
    
   
    # HVAC
    #print "HVAC"
    
    if HVAC=="PTHP": 
        file_HVAC_PTHP=open(DirPath+"/SingleFloor/09A_HVAC_PTHP.idf","r")
        g_9=file_HVAC_PTHP.read()
        f.write(g_9)
        file_HVAC_PTHP.close()
    elif HVAC=="CWC":
        file_HVAC=open(DirPath+"/SingleFloor/09B_HVAC_CWC.idf","r")
        g_9=file_HVAC.read()
        f.write(g_9)
        file_HVAC.close()
    else:
        file_HVAC=open(DirPath+"/SingleFloor/09C_HVAC_CAC.idf","r")
        g_9=file_HVAC.read()
        f.write(g_9)
        file_HVAC.close()

    # Economics
    #print "Economics"
    file_Economics=open(DirPath+"/SingleFloor/10_Economics.idf","r")
    g_10=file_Economics.read()
    f.write(g_10)
    file_Economics.close()
 
    # Output
    #print "Output"
    file_Output=open(DirPath+"/SingleFloor/11_Output.idf","r")
    g_11=file_Output.read()
    f.write(g_11)
    file_Output.close()
   
    f.close()
    
    #print "Finish"

#//////////////////////////////////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////////////////////////////////

def ProcessSingleFloor(
    inputBuildingtype,
    inputHVACtype,
    inputCoolRoof,
    inputOrientation,
    inputwwr,
    inputArea,
    useridpassed,
    SR_Base,
    IE_Base,
    SR_Propose,
    IE_Propose,
    ElectricityPrice,
    Slope_Angle,
    RoofContruction
):
    GenTemplateBuildingType = inputBuildingtype
    GenTemplateCoolRoof = inputCoolRoof
    GenTemplateHVAC_Type = inputHVACtype
    GenTemplateOrientation = int(inputOrientation)
    GenTemplateArea = int(inputArea)
    GenTemplateWwr = float(inputwwr)
    P = float(Slope_Angle)
    val = 0
    angle = Overhang
    checkfilecreation = creatdirectory(useridpassed)

    if int(checkfilecreation) == 1:
        UserDirPath = DirPath + '/SimulationOutput/' + str(useridpassed)
        BaseDirAddr = UserDirPath + '/' + "Base"
        ProposedDirAddr = UserDirPath + '/' + "Proposed"
        directorylist = [BaseDirAddr, ProposedDirAddr]

        for i in range(len(directorylist)):
            if i == 0:
                SR = SR_Base
                IE = IE_Base
            else:
                SR = SR_Propose
                IE = IE_Propose

            RQ_VAL = generate_co_SingleFloor(
                GenTemplateOrientation,
                GenTemplateArea,
                Aspect_Ratio,
                GenTemplateWwr,
                glass,
                angle,
                SR,
                IE,
                P,
                ElectricityPrice,
                RoofContruction
            )

            GenerateTemplateSingleFloor(
                GenTemplateBuildingType,
                GenTemplateCoolRoof,
                DaylightCtrl,
                ShadingCtrl,
                RoofContruction,
                GenTemplateHVAC_Type,
                directorylist[i]
            )

            filename = directorylist[i] + '/b.idf'
            f = open(directorylist[i] + '/SingleFloorTemplate.idf')
            w = open(filename, 'w')

            for line in f:
                sets = re.findall(r'#.*?[,;]', line)
                for j in sets:
                    j = j[:-1]
                    line = line.replace(j, str(RQ_VAL[j]))
                w.write(line)
                val = 1

            w.close()
    else:
        return 0

    return val, BaseDirAddr, ProposedDirAddr

##def ProcessSingleFloor(inputBuildingtype,inputHVACtype,inputCoolRoof,inputOrientation,inputwwr, \
##                                    inputArea,useridpassed,SR_Base,IE_Base,SR_Propose,IE_Propose,ElectricityPrice,Slope_Angle,RoofContruction):
##    GenTemplateBuildingType=inputBuildingtype
##    GenTemplateCoolRoof=inputCoolRoof
##    GenTemplateHVAC_Type=inputHVACtype
##    GenTemplateOrientation=int(inputOrientation)
##    GenTemplateArea=int(inputArea)
##    GenTemplateWwr=float(inputwwr)
##    P = float(Slope_Angle)
##    val = 0
##    angle=Overhang
##    checkfilecreation = creatdirectory(useridpassed)
##    if(int(checkfilecreation)==1):
##            UserDirPath=DirPath+'/SimulationOutput'+'/'+str(useridpassed)
##            BaseDirAddr = UserDirPath+'/'+"Base"
##	    ProposedDirAddr = UserDirPath+'/'+"Proposed"
##	    directorylist =[BaseDirAddr,ProposedDirAddr]
##	    for i in range(len(directorylist)):
##                    if i == 0:
##                            SR = SR_Base
##                            IE = IE_Base
##                    else :
##                            SR = SR_Propose
##			    IE = IE_Propose
##		    RQ_VAL=generate_co_SingleFloor(GenTemplateOrientation,GenTemplateArea,Aspect_Ratio,GenTemplateWwr,glass,angle,SR,IE,P,ElectricityPrice,RoofContruction);
##			GenerateTemplateSingleFloor(GenTemplateBuildingType,GenTemplateCoolRoof,DaylightCtrl,ShadingCtrl,RoofContruction,GenTemplateHVAC_Type,directorylist[i])
##			filename =directorylist[i]+'/b.idf'
##			f=open(directorylist[i]+'/SingleFloorTemplate.idf');
##			w=open(filename,'w');
##			for line in f:
##				sets=re.findall(r'#.*?[,;]',line);
##				for j in sets:
##					j=j[:-1];
##					line=line.replace(j,str(RQ_VAL[j]));
##				w.write(line);
##				val=1
##			w.close();
##	else:
##        return 0
##    return val,BaseDirAddr,ProposedDirAddr


#////////////////////////////////////////////////////////////////////////////////////////////////////
def creatdirectory(useridpassed):
	UserDirPath = DirPath+'/SimulationOutput'+'/'+str(useridpassed)
	BaseCase = UserDirPath+'/'+"Base"
	ProposedCase = UserDirPath+'/'+"Proposed"
	if ((os.path.exists(UserDirPath)) == True):
		return 1
	else:
		os.mkdir(UserDirPath, 0o777 )
		os.chmod(UserDirPath, 0o777)
		if ((os.path.exists(UserDirPath)) == True):
			os.mkdir(BaseCase, 0o777)
			os.chmod(BaseCase, 0o777)
			os.mkdir(ProposedCase, 0o777)
			os.chmod(ProposedCase, 0o777)
			return 1
		else:
			return 0
