import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

table = pd.read_csv('rpps_all.csv')
print(table)


outlog = {
            'Name': [] ,
            'Ra'  : [] ,
            'Dec' : [] ,
            'xray': []
}

for i in table.index:
    ra=table.iloc[i,2]   #RAJD
    dec=table.iloc[i,3]  #DECJD
    
    print(i,table.iloc[i,0])
    outlog['Name'].append(table.iloc[i,0])
    outlog['Ra'].append(ra)
    outlog['Dec'].append(dec)

dist_table= table.iloc[:,4]
bins = np.linspace(0, 2, 10)

plt.figure(1)
plt.hist([table['DIST'],table['DIST1']], bins  ,rwidth=0.5,  edgecolor = 'black' , label=['YM16','NE2001'])
plt.xlabel('Distances (kpc)')
plt.ylabel('Count')
plt.legend(loc='upper right')
plt.title('Distance distribution of RPPs < 2 kpc')
plt.savefig('dist_pop.png')




plt.figure(2)
bins = np.linspace(10,1000,100)
plt.hist(table['P0'],bins,rwidth=0.5,  edgecolor = 'black')
#plt.xlim([10,1000]) 
plt.xscale('log')
plt.xlabel('Period (s)')
plt.ylabel('Count')
plt.title('Period distribution of RPPs < 2 kpc')
plt.savefig('period_pop.png')