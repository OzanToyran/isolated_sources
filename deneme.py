#********************************************************************************************************************************************************************
#PURPOSE: This code used for testing of "cross_query_with_coords.py"
#
#Created by: Ozan Toyran , 28.05.2024
#
#
#OUTPUT: None
#
#Log: 
#
#********************************************************************************************************************************************************************

from astropy.io import ascii
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from astropy import units as u
from astroquery.esasky import ESASky

#table = pd.read_csv('rpps_all.csv')
#print(table)


outlog = {
            'Name': [] ,
            'Ra'  : [] ,
            'Dec' : [] ,
            'xray': []
}


#for i in table.index:
#    rajd=table.iloc[i,2]   #RAJD
#    decjd=table.iloc[i,3]  #DECJD
    
#    print(i,table.iloc[i,0])
#    outlog['Name'].append(table.iloc[i,0])
#    outlog['Ra'].append(rajd)
#    outlog['Dec'].append(decjd)

list_coords= SkyCoord(ra=107.9757502*u.deg,dec=-68.51315682*u.deg)


result = ESASky.query_region_catalogs(position=list_coords, radius=13 * u.arcmin, catalogs=['XMM-EPIC-STACK', 'XMM-EPIC'])
result2 = ESASky.query_region_catalogs(position=list_coords, radius=10 * u.arcmin, catalogs=['Chandra-SC2'])

for table2 in result:
    colnames = table2.colnames

the_table = result['XMM-EPIC']
obsids = the_table['observation_id']    


ascii.write(result['XMM-EPIC']['iauname'], 'values.txt', overwrite=True)


print(the_table)
#Check and find if there are more than one observation id 

list= {
    'observation_id': obsids[:]
}
list = pd.DataFrame(list)
#return unique observation ids
print(list['observation_id'].unique())


#print(result)
#print(result2)

#dist_table= table.iloc[:,4]
#bins = np.linspace(0, 2, 10)

#plt.figure(1)
#plt.hist([table['DIST'],table['DIST1']], bins  ,rwidth=0.5,  edgecolor = 'black' , label=['YM16','NE2001'])
#plt.xlabel('Distances (kpc)')
#plt.ylabel('Count')
#plt.legend(loc='upper right')
#plt.title('Distance distribution of RPPs < 2 kpc')
#plt.savefig('dist_pop.png')

#plt.figure(2)
#bins = np.linspace(10,1000,100)
#plt.hist(table['P0'],bins,rwidth=0.5,  edgecolor = 'black') 
#plt.xscale('log')
#plt.xlabel('Period (s)')
#plt.ylabel('Count')
#plt.title('Period distribution of RPPs < 2 kpc')
#plt.savefig('period_pop.png')