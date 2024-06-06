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


#loop through each source, get their Rajd and decjd

outlog = {
    'NAME': [] ,                # Jname obtained from ATNF Pulsar Catalogue
    'RAJD'  : [] ,              # RAJD obtained from ATNF Pulsar Catalogue
    'DECJD' : [] ,              # DECJD obtained from ATNF Pulsar Catalogue
    'XMM-OBS': [] ,             # [Boolean] Returns True if there exists an XMM-Newton Observation
    'XMM-OBSID' : [],           # Contains the given Observation ID for the XMM-Newton sources
    'NX_OBS' : [],              # Number of individual XMM Observation IDs for the source 
    'CHANDRA-OBS' : [],         # [Boolean] Returns True if there exists a Chandra Observation
    'CHANDRA-OBSID' : [],        # Contains the given Observation ID for the Chandra sources
    'NC_OBS' : []              # Number of individual Chandra Observation IDs for the source 
}

outlog= pd.DataFrame(outlog)

for i in table.index:


    if i == 100:
        outlog.to_csv('outlog.txt', index=False) 
        


    print(i,table.iloc[i,0])

    rajd=table.iloc[i,2]   #RAJD
    decjd=table.iloc[i,3]  #DECJD

    list_coords= SkyCoord(ra=rajd*u.deg,dec=decjd*u.deg)


#--------------------XMM NEWTON SEARCH-----------------------

    result = ESASky.query_region_catalogs(position=list_coords, radius=13 * u.arcmin, catalogs=['XMM-EPIC-STACK', 'XMM-EPIC'])

    # Record Name and coordinates of the source

#    outlog['NAME'].append(table.iloc[i,0])
#    outlog['RAJD'].append(rajd)
#    outlog['DECJD'].append(decjd)
        
    new_row = {
        'NAME': table.iloc[i,0] ,                # Jname obtained from ATNF Pulsar Catalogue
        'RAJD'  : rajd ,              # RAJD obtained from ATNF Pulsar Catalogue
        'DECJD' : decjd                # DECJD obtained from ATNF Pulsar Catalogue
    }


    # If a XMM-Newton observation entry found in the catalogue
    if result == []:

        new_row['XMM-OBS'] = [0]
        new_row['XMM-OBSID'] = [None]
        new_row['NX_OBS'] = [0]

    else:

        the_table = result['XMM-EPIC']
        obsids = the_table['observation_id']  
        #Above arrays are likely to contain duplicate entries, so we only take the unique entries

        list= {
            'observation_id': obsids[:]
        }
        list = pd.DataFrame(list)
        df_obsids=list['observation_id'].unique()
        nx_obs=len(df_obsids)
        print(df_obsids)

        #if there are more than one observation take the first one
        df_obsids=df_obsids[0]
        
        new_row['XMM-OBS']= [1]              # [Boolean] Returns True if there exists an XMM-Newton Observation
        new_row['XMM-OBSID']= [df_obsids]           # Contains the given Observation ID for the XMM-Newton sources
        new_row['NX_OBS'] = [nx_obs]
        


#--------------------CHANDRA SEARCH-----------------------

    result2 = ESASky.query_region_catalogs(position=list_coords, radius=10 * u.arcmin, catalogs=['Chandra-SC2'])

    # If a Chandra observation entry found in the catalogue
    if result2 == []:

        new_row['CHANDRA-OBS'] = [0]
        new_row['CHANDRA-OBSID'] = [None]
        new_row['NC_OBS'] = [0]


    else:

        the_table2 = result2['CHANDRA-SC2']
        names = the_table2['name']  
        #Above arrays are likely to contain duplicate entries, so we only take the unique entries

        list2= {
            'names': names[:]
        }
        list2 = pd.DataFrame(list2)
        df_names=list2['names'].unique()
        nc_obs=len(df_names)
        print(df_names)

        #if there are more than one observation take the first one
        df_names=df_names[0]
        
        new_row['CHANDRA-OBS']= [1]              # [Boolean] Returns True if there exists an XMM-Newton Observation
        new_row['CHANDRA-OBSID']= [df_names]           # Contains the given Observation ID for the XMM-Newton sources
        new_row['NC_OBS'] = [nc_obs]


#--------------------Record the query results-------------
    print(new_row)
    new_row= pd.DataFrame(new_row)

    outlog = pd.concat([outlog,new_row],ignore_index=True)

outlog.to_csv('outlog.txt', index=False) 