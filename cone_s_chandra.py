from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.table import Table
import astropy.units as u
from astropy.io import ascii
import pandas as pd



# Specify the path to the FITS file
fits_file_path = r"C:\Users\Dell\Desktop\rpps\isolated_sources\catalogs\csccatalog.fits"
table = pd.read_csv('rpps_all.csv')

# Open the FITS file
hdul = fits.open(fits_file_path)

# Access the primary HDU (Header Data Unit)
primary_hdu = hdul[0]


table_data=hdul[1].data


print(hdul[1].header)

hdul.close()

outlog = Table()

ascii.write(outlog, "cone_search_chandra.txt", overwrite=True)


for i in table.index:

    n_det= 0 # set the initial number of detections
    print(i,table.iloc[i,0])

    # For each source, obtain RA and DEC values for cone search
    rajd=table.iloc[i,2]   #RAJD
    decjd=table.iloc[i,3]  #DECJD
    ra_star2 ,dec_star2 = rajd, decjd 

    source_name = table.iloc[i,0]


    if table_data is not None:
        
        # Check if the data is a table or an array with rows
        if isinstance(table_data, fits.FITS_rec):  # Table data
            for row_index, row in enumerate(table_data):
            #    print(f"Row {row_index}: {row['RA']}")

                ra_star1, dec_star1 = row['ra'], row['dec'] 
            #     print(ra_star1,ra_star2)
                # ra_star1, dec_star1 = table_data.field('ra')[i], table_data.field('dec')[i] 

                # Create SkyCoord objects for each star
                star1 = SkyCoord(ra=ra_star1*u.deg, dec=dec_star1*u.deg, frame='icrs')
                star2 = SkyCoord(ra=ra_star2*u.deg, dec=dec_star2*u.deg, frame='icrs')

                # Calculate the angular separation
                angular_distance = star1.separation(star2) #in degrees
#                position_angle= star1.position_angle(star2).to(u.arcminute) 

                dimensionless_sep =angular_distance.to('', equivalencies=u.dimensionless_angles())


                #Check if the distance is within the desired cone radius of 10 arcminutes for Chandra observations
                if ( dimensionless_sep*60 <= 10)  :
                    print("***CHANDRA DETECTION***")
                    print(f"Row {row_index}: {row['name']} is within {dimensionless_sep*60} arcminutes of your search cone!")
                    print(f"My source RA: {ra_star1}, DEC: {dec_star1}")
                    print(f"Target source RA: {ra_star2}, DEC: {dec_star2}")
                    n_det += 1

                    

                #if there is at least one observation within the cone, skip to the next source
                if (n_det > 0):
                    break

                    

        else:  # Numpy array data
            print("Data is not in table format.")
    else:
        print("No data")

    if (n_det == 0):
        results = ascii.read("cone_search_chandra.txt")
        new_row = Table(source_name)
        updated_results = Table.vstack([results,new_row])
        ascii.write(outlog, "cone_search_chandra.txt", overwrite=True)

#                new_row= pd.DataFrame(new_row)

