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

f=open("output.csv",'w')
for i in glob.glob("*.html"):
        result=fetch_TotalSiteEnergy(i)
        #print i,",",result
        l=i+","+result
        print l
        f.write(l)
        f.write("\n")
    
    
    
f.close()