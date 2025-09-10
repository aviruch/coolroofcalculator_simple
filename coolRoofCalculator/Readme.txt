

Sytesm Argument must be in order Area(sqm), Weatherfile, BuildingType, HvacType, Daylight, CoolRoof, IntShadeCtrl, Floors, WindowType, 
WWR, WindowHeight,WindowWidthP,SillHeight,GlassU, SHGC, VLT, Orientation, OverHangDegree, AR, RoofInsulation, WallInsulation. 




python MainFile.py Area:1000 Weatherfile:IND_Ahmedabad.426470_ISHRAE.epw BuildignType:Office Hvac_Type:PTHP Daylight:ON 
CoolRoof:OFF IntShadeCtrl:OnHighSolar Floors:10 WindowType:Strip WWR:0.5 WindowHeight:NA WindowWidhtP:NA SillHeight:NA
GlassU:0.351 SHGC:0.5 VLT:0.2 Orientation:0 OverHangDegree:30 AR:2 RoofInsulation:0 WallInsulation:0


energyplus -w IND_Ahmedabad.426470_ISHRAE.epw -p ./Output/b -s C -x -m -r b_86.idf

Test case for Strip 
python MainFile.py 1000 IND_Ahmedabad.426470_ISHRAE.epw Office PTHP true false OnHighSolar 1 Strip 0.5 1 1 1 0.351 0.5 0.2 10 2 2 0 0

Test case for Regular
python MainFile.py 1000 IND_Ahmedabad.426470_ISHRAE.epw Office PTHP true false OnHighSolar 1 Regular 0.1 1 1 1 0.351 0.5 0.2 10 2 2 0 0


http://127.0.0.1:8000/result/?Simulation_id=1e6ebb35-2a18-430d-9829-f7712c9b0cf3

EnergyPlus v8.9

