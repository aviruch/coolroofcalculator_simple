# This code is to comnine idf files as per selection 
# This is only for single floor, Finally it will generate template file
# April 16 2017  

Schedule = "OFFICE" # Other Options are "Retail" and "Institute"
#DesignDay  Need to change with weather file selection 
CoolRoof="NO"  #Other Option "Yes"
DayLightSensor="ON"  #Other Option "OFF"
IntShades="OFF"  # Other Option "ON"
HVAC="CWC" #Other Options are "CentralWaterCooledChiller: CWC" and "CentralAirCooledChiller: CAC"

f=open("SingleFloorTemplate.idf",'w')


# Header file
print "Header file"
file_Header=open("01_Header.idf","r")
g_1=file_Header.read()
f.write(g_1)
file_Header.close()



#DDY File
print "DDY File"
file_DDY=open("02B_Size_WeatherData.idf","r")
g_2=file_DDY.read()
f.write(g_2)
file_DDY.close()

# Schedule file
print "Schedule file"

if Schedule=="OFFICE":
    file_Schedule_Office=open("03A_Schedule_Office.idf","r")
    g_3=file_Schedule_Office.read()
    f.write(g_3)
    file_Schedule_Office.close()

elif Schedule=="RETAIL":
    file_Schedule_Retail=open("03B_Schedule_Retail.idf","r")
    g_3=file_Schedule_Retail.read()
    f.write(g_3)
    file_Schedule_Retail.close()

else:
    file_Schedule_Institute=open("03C_Schedule_Institute.idf","r")
    g_3=file_Schedule_Institute.read()
    f.write(g_3)
    file_Schedule_Institute.close()



# Cool Roof
print "Cool Roof file"

if CoolRoof=="NO":
    file_CoolRoof_Off=open("04A_CoolRoof_OFF.idf","r")
    g_4=file_CoolRoof_Off.read()
    f.write(g_4)
    file_CoolRoof_Off.close()
else:
    file_CoolRoof_On=open("04B_CoolRoof_ON.idf","r")
    g_4=file_CoolRoof_On.read()
    f.write(g_4)
    file_CoolRoof_On.close()


# Zones
print "Zones"
file_Zones=open("05_Zones.idf","r")
g_5=file_Zones.read()
f.write(g_5)
file_Zones.close()


# Gains
print "Gains"
file_Gains=open("06_Gains.idf","r")
g_6=file_Gains.read()
f.write(g_6)
file_Gains.close()


# Daylight
print "Daylight"

if DayLightSensor=="ON": 
    file_DayLight_ON=open("07A_Daylight_ON.idf","r")
    g_7=file_DayLight_ON.read()
    f.write(g_7)
    file_DayLight_ON.close()
else:
    file_DayLight_OFF=open("07B_Daylight_OFF.idf","r")
    g_7=file_DayLight_OFF.read()
    f.write(g_7)
    file_DayLight_OFF.close()




# Internal Shades
print "Internal Shades"

if IntShades=="OFF":
    file_IntShade_OFF=open("08A_IntShade_OFF.idf","r")
    g_8=file_IntShade_OFF.read()
    f.write(g_8)
    file_IntShade_OFF.close()
else:
    file_IntShade_ON=open("08A_IntShade_ON.idf","r")
    g_8=file_IntShade_ON.read()
    f.write(g_8)
    file_IntShade_ON.close()



# HVAC
print "HVAC"

if HVAC=="PTHP": 
    file_HVAC_PTHP=open("09A_HVAC_PTHP.idf","r")
    g_9=file_HVAC_PTHP.read()
    f.write(g_9)
    file_HVAC_PTHP.close()
elif HVAC=="CWC":
    file_HVAC=open("09B_HVAC_CWC.idf","r")
    g_9=file_HVAC.read()
    f.write(g_9)
    file_HVAC.close()
else:

    file_HVAC=open("09C_HVAC_CAC.idf","r")
    g_9=file_HVAC.read()
    f.write(g_9)
    file_HVAC.close()



# Economics
print "Economics"
file_Economics=open("10_Economics.idf","r")
g_10=file_Economics.read()
f.write(g_10)
file_Economics.close()


# Output
print "Output"
file_Output=open("11_Output.idf","r")
g_11=file_Output.read()
f.write(g_11)
file_Output.close()


f.close()

print "Finish"