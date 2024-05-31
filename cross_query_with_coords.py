import pandas as pd
import pyvo as vo


from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.table import QTable
from astropy.time import Time
from astropy.utils.data import download_file

from astroquery.esasky import ESASky

from psrqpy import QueryATNF

#query = QueryATNF(loadquery=['C:\Users\Dell\Desktop\rpps\psrcat_tar\psrcat.db'])
#query = QueryATNF(params=['JName','PX','RaJD','DecJD','Dist','Dist1','DMSinb','Edot'],condition='dist < 2.0 && dist1 <2.0')
#query = QueryATNF()

table = pd.read_csv('rpps.csv')
print(table)

outlog = {
            'Name': [] ,
            'Ra'  : [] ,
            'Dec' : [] ,
            'xray_xmm': [] ,
            'xray_xmm_info' : []
}



for i in table.index:
    print(i,table.iloc[i,0])

    rajd=table.iloc[i,2]   #RAJD
    decjd=table.iloc[i,3]  #DECJD

    list_coords= SkyCoord(ra=rajd*u.deg,dec=decjd*u.deg)


#--------------------XMM NEWTON SEARCH-----------------------

    result = ESASky.query_region_catalogs(position=list_coords, radius=13 * u.arcmin, catalogs=['XMM-EPIC-STACK', 'XMM-EPIC'])

    for table2 in result:
        colnames = table2.colnames

    


    if result == []:
        outlog['Name'].append(table.iloc[i,0])
        outlog['Ra'].append(rajd)
        outlog['Dec'].append(decjd)
        outlog['xray_xmm'].append('no')
    else:
        outlog['Name'].append(table.iloc[i,0])
        outlog['Ra'].append(rajd)
        outlog['Dec'].append(decjd)        
        outlog['xray_xmm'].append('yes')
        outlog['xray_xmm_info'].append(colnames)


#    for table_name in result.keys():
#        table = result[table_name]

    #print(table.columns)
#    print(table['observation_id','n_detections'])
outlog.to_csv('outlog.csv', index=False) 