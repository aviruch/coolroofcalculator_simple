# This script can factch Total site energy form the genrated HTML file from EnergyPlus
# It searchs all html files in a folder and fatch results from it
# Created on Oct 25, 2016
# Author Aviruch Bhatia

#import pandas as pd
from bs4 import BeautifulSoup
import glob
import string as str

def fetch_TotalSiteEnergy(filename):
    html = open (filename, 'r')
    soup = BeautifulSoup(html)
    table = soup.find("table", attrs={"border":"1"})

    m=[]
    for row in table.find_all("tr")[1:]:
        l=[]    
        for td in row.find_all("td"):        
            l.append(td.get_text())   
        m.append(l)
 
    #df = pd.DataFrame(m)
    #print "\tTotal Site Energy=\t", df.ix[0,1]
    #print "Total Site Energy,", str.strip(m[0][1])
    html.close()
    #print m
    return str.strip(m[0][1])


def fetch_MonthlyEnergy(filename):
    html = open (filename, 'r')
    html1 = open ("temp.html", 'w')
    i=0
    Lines = html.readline()
    for line in html:
        i=i+1
        if "<p>Report:<b> EndUseEnergyConsumptionElectricityMonthly</b></p>" in line:
            found = True
            
            break
    print "Found"
    print i
    j=0
    
    
    for line in html:
        html1.write(line)
        
        
            
        
            
    soup = BeautifulSoup(html1)
##    table = soup.find("table", attrs={"border":"1"})
##
##    m=[]
##    for row in table.find_all("tr")[1:]:
##        l=[]    
##        for td in row.find_all("td"):        
##            l.append(td.get_text())   
##        m.append(l)
## 
##    #df = pd.DataFrame(m)
##    #print "\tTotal Site Energy=\t", df.ix[0,1]
##    #print "Total Site Energy,", str.strip(m[0][1])
    html.close()
    html1.close()
##    #print m
    return i
    return str.strip(m[0][1])

#f=open("output.csv",'w')
for i in glob.glob("*.html"):
        #result=fetch_TotalSiteEnergy(i)
        result=fetch_MonthlyEnergy(i)
        #print i,",",result
        
        print result
##        f.write(l)
##        f.write("\n")
    
    
    
#f.close()
