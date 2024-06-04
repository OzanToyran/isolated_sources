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
            'NAME': [] ,                # Jname obtained from ATNF Pulsar Catalogue
            'RAJD'  : [] ,              # RAJD obtained from ATNF Pulsar Catalogue
            'DECJD' : [] ,              # DECJD obtained from ATNF Pulsar Catalogue
            'XMM-OBS': [] ,             # [Boolean] Returns True if there exists an XMM-Newton Observation
            'XMM-IAUNAME' : [],         # Contains IAUNAME of the X-ray source for XMM-Newton sources 
            'XMM-OBSID' : [],           # Contains the given Observation ID for the XMM-Newton sources
            'CHANDRA-OBS' : [],         # [Boolean] Returns True if there exists a Chandra Observation
            'CHANDRA-NAME' : [],        # Contains the Chandra Name of the source
            'CHANDRA-OBSID' : []        # Contains the given Observation ID for the Chandra sources
}

outlog= pd.DataFrame(outlog)

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


#First we need to process the query response
#We obtain a Table.table and turn it into a DataFrame DataTable


#for table2 in result:
#    colnames = table2.colnames

the_table = result['XMM-EPIC']
iaunames = the_table['iauname']
obsids = the_table['observation_id']    

#Above arrays are likely to contain duplicate entries, so we only take the unique entries

list= {
    'iauname' : iaunames[:],
    'observation_id': obsids[:]
}
list = pd.DataFrame(list)
df_iauname=list['iauname'].unique()
df_obsids=list['observation_id'].unique()

#New we have the unique Obs IDs and Catalog Names

new_row = {
            'NAME': 'deneme' ,                # Jname obtained from ATNF Pulsar Catalogue
            'RAJD'  : 107.9757502 ,              # RAJD obtained from ATNF Pulsar Catalogue
            'DECJD' : -68.51315682 ,              # DECJD obtained from ATNF Pulsar Catalogue
            'XMM-OBS': True ,             # [Boolean] Returns True if there exists an XMM-Newton Observation
            'XMM-IAUNAME' : df_iauname[0],         # Contains IAUNAME of the X-ray source for XMM-Newton sources 
            'XMM-OBSID' : df_obsids,           # Contains the given Observation ID for the XMM-Newton sources
            'CHANDRA-OBS' : False,         # [Boolean] Returns True if there exists a Chandra Observation
            'CHANDRA-NAME' : None,        # Contains the Chandra Name of the source
            'CHANDRA-OBSID' : None        # Contains the given Observation ID for the Chandra sources
}

new_row= pd.DataFrame(new_row)

outlog = pd.concat([outlog,new_row],ignore_index=True)


outlog.to_csv('outlog_testing.csv', index=False) 



#ascii.write(outlog, 'values.txt', overwrite=True)


#print(the_table)
#Check and find if there are more than one observation id 




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