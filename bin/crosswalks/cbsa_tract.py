"""cbsa_tract.py

Extract the crosswalk between cbsa and tracts.
"""
import os
import csv
import fiona
import collections


#
# Read preliminary data
#

## MSA to counties crosswalk
county_to_cbsa = {}
with open('data/crosswalks/cbsa_county.txt', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        county = rows[1]
        cbsa = rows[0]
        county_to_cbsa[county] = cbsa


## List of states
states = []
with open('data/misc/states_list.txt') as source:
    line = source.readline()
    while line:
        states.append(line.replace('\n', ''))
        line = source.readline()



#
# Extract blockgroups per MSA by iterating through shapefiles
#
cbsa_tract = {}
for st in states:
    tracts = []
    with fiona.open('data/shp/state/%s/tracts.shp'%st, 'r',
            'ESRI Shapefile') as source:
        source_crs = source.crs
        for f in source:
            county = (f['properties']['STATEFP'] +
                    f['properties']['COUNTYFP']).encode('utf8')

            ## Skip rural counties
            try:
                cbsa = county_to_cbsa[county.encode('utf8')]

                if cbsa not in cbsa_tract:
                    cbsa_tract[cbsa] = []
                cbsa_tract[cbsa].append(f['properties']['GEOID'])

            except:
                pass 




#
# Save the crosswalk 
#
with open('data/crosswalks/cbsa_tract.txt', 'w') as output:
    output.write('MSA FIP\tTRACT FIP\n')
    for cbsa in cbsa_tract:
        ## Remove duplicates
        tracts = list(set(cbsa_tract[cbsa]))
        for tr in tracts:
            output.write('%s\t%s\n'%(cbsa, tr))
