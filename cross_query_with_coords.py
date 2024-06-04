#********************************************************************************************************************************************************************
#PURPOSE: This code takes the coordinates (RAJD,DECJD) of a list of sources and performs cone search of X-ray observations in the XMM-Newton and Chandra Archives.
#
#Created by: Ozan Toyran , 28.05.2024
#
#
#OUTPUT: A logfile named "outlog.csv" that contains JNAME, RA, DEC, XMM-Newton Archive info (if exists), Chandra Archive info (if exists)
#
#
#Log: 
#
#********************************************************************************************************************************************************************

import pandas as pd
import pyvo as vo

from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.table import QTable
from astropy.utils.data import download_file

from astroquery.esasky import ESASky

from psrqpy import QueryATNF

#query = QueryATNF(loadquery=['C:\Users\Dell\Desktop\rpps\psrcat_tar\psrcat.db'])
#query = QueryATNF(params=['JName','PX','RaJD','DecJD','Dist','Dist1','DMSinb','Edot'],condition='dist < 2.0 && dist1 <2.0')
#query = QueryATNF()

table = pd.read_csv('rpps.csv')
print(table)

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

#loop through each source, get their Rajd and decjd

for i in table.index:
    print(i,table.iloc[i,0])

    rajd=table.iloc[i,2]   #RAJD
    decjd=table.iloc[i,3]  #DECJD

    list_coords= SkyCoord(ra=rajd*u.deg,dec=decjd*u.deg)


#--------------------XMM NEWTON SEARCH-----------------------

    result = ESASky.query_region_catalogs(position=list_coords, radius=13 * u.arcmin, catalogs=['XMM-EPIC-STACK', 'XMM-EPIC'])

    # Record Name and coordinates of the source

    outlog['NAME'].append(table.iloc[i,0])
    outlog['RAJD'].append(rajd)
    outlog['DECJD'].append(decjd)

    if result == []:

        outlog['XMM-OBS'].append(False)
        outlog['XMM-IAUNAME'].append('')
        outlog['XMM-OBSID'].append('')

    else:

        outlog['XMM-OBS'].append(True)
        outlog['XMM-IAUNAME'].append(result['XMM-EPIC']['iauname'])
        outlog['XMM-OBSID'].append()

#    for table_name in result.keys():
#        table = result[table_name]

    #print(table.columns)
#    print(table['observation_id','n_detections'])
outlog.to_csv('outlog.csv', index=False) 