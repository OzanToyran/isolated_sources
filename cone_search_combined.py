from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.table import Table
import astropy.units as u
from astropy.io import ascii
import pandas as pd


# Specify the path to the FITS file
xmm_path = r"C:\Users\Dell\Desktop\rpps\isolated_sources\catalogs\4XMM_DR13cat_v1.0.fits"
chandra_path = r"C:\Users\Dell\Desktop\rpps\isolated_sources\catalogs\csccatalog.fits"
table = pd.read_csv('rpps_all.csv')



# Open the FITS file
hdul_xmm = fits.open(xmm_path)
hdul_cha = fits.open(chandra_path)


xmm_data = hdul_xmm[1].data
cha_data = hdul_cha[1].data
hdul_xmm.close()
hdul_cha.close()
#print(table_data.field('ra'))

#Create necessarcy variables for storage and flagging
outlog =  Table()
n_candidate_targets= 0

ascii.write(outlog, "cone_search_combined.txt", overwrite=True)


for i in (table.index -1):
    n_det = 0 # set total number of detections
    n_det_xmm = 0 # set the initial number of detections
    n_det_cha = 0
    print(i,table.iloc[i,0])

    # For each source, obtain RA and DEC values for cone search
    rajd=table.iloc[i,2]   #RAJD
    decjd=table.iloc[i,3]  #DECJD
    ra_star2 ,dec_star2 = rajd, decjd 

    source_name = table.iloc[i,0]

    for row_index, row in enumerate(xmm_data):
    #    print(f"Row {row_index}: {row['RA']}")

        ra_star1, dec_star1 = row['RA'], row['DEC'] 
    #     print(ra_star1,ra_star2)
        # ra_star1, dec_star1 = table_data.field('ra')[i], table_data.field('dec')[i] 

        # Create SkyCoord objects for each star
        star1 = SkyCoord(ra=ra_star1*u.deg, dec=dec_star1*u.deg, frame='icrs')
        star2 = SkyCoord(ra=ra_star2*u.deg, dec=dec_star2*u.deg, frame='icrs')

        # Calculate the angular separation on the sky
        angular_distance = star1.separation(star2) #in degrees
#                position_angle= star1.position_angle(star2).to(u.arcminute) 

        dimensionless_sep =angular_distance.to('', equivalencies=u.dimensionless_angles())


        #Check if the distance is within the desired cone radius of 13 arcminutes for XMM-Newton
        if ( dimensionless_sep*60 <= 13)  :
            print("***XMM-Newton DETECTION***")
            print(f"Row {row_index}: {row['IAUNAME']} is within {dimensionless_sep*60} arcminutes of your search cone!")
            print(f"My source RA: {ra_star1}, DEC: {dec_star1}")
            print(f"Target source RA: {ra_star2}, DEC: {dec_star2}")
            n_det_xmm += 1

            

        #if there is at least one observation within the cone, skip to the next source
        if (n_det_xmm > 0):
            break
                

    
    #If no xmm observations found, next search the Chandra Catalog
    if (n_det_xmm == 0):           

        for row_index, row in enumerate(cha_data):
        #    print(f"Row {row_index}: {row['RA']}")

            ra_star1, dec_star1 = row['ra'], row['dec'] 
        #     print(ra_star1,ra_star2)
            # ra_star1, dec_star1 = table_data.field('ra')[i], table_data.field('dec')[i] 

            # Create SkyCoord objects for each star
            star1 = SkyCoord(ra=ra_star1*u.deg, dec=dec_star1*u.deg, frame='icrs')
            star2 = SkyCoord(ra=ra_star2*u.deg, dec=dec_star2*u.deg, frame='icrs')

            # Calculate the angular separation on the sky
            angular_distance = star1.separation(star2) #in degrees
    #                position_angle= star1.position_angle(star2).to(u.arcminute) 

            dimensionless_sep =angular_distance.to('', equivalencies=u.dimensionless_angles())


            #Check if the distance is within the desired cone radius of 10 arcminutes for Chandra observations
            if ( dimensionless_sep*60 <= 10)  :
                print("***CHANDRA DETECTION***")
                print(f"Row {row_index}: {row['name']} is within {dimensionless_sep*60} arcminutes of your search cone!")
                print(f"My source RA: {ra_star1}, DEC: {dec_star1}")
                print(f"Target source RA: {ra_star2}, DEC: {dec_star2}")
                n_det_cha += 1

                

            #if there is at least one observation within the cone, skip to the next source
            if (n_det_cha > 0):
                break

    #Calculate total number of detections in the catalogs
    n_det = n_det_xmm + n_det_cha

    if (n_det == 0):

        results = ascii.read("cone_search_combined.txt")
        new_row = Table(source_name)
        updated_results = Table.vstack([results,new_row])
        ascii.write(outlog, "cone_search_combined.txt", overwrite=True)
        n_candidate_targets += 1

print(f'Total number of candidate sources found: {n_candidate_targets}')







