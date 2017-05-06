# -*- coding: utf-8 -*-
import netCDF4 as netcdf_helpers
import MySQLdb
import numpy as np
import pandas as pd

docName = "الجامع الصحيح المسمى صحيح مسلم.txt"

db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Islammega88",  # your password
                     db="mstdb",  # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()


selected_letters_in_this_loopQuery = "select * from ParsedDocument where SentenceNumber<=500 order by idCharacterNumber asc "
cur.execute(selected_letters_in_this_loopQuery)
selected_letters_in_this_loop = cur.fetchall()

listOfDiacritizedCharacterQuery = "select * from DiacOneHotEncoding "
cur.execute(listOfDiacritizedCharacterQuery)
listOfDiacritizedCharacter = cur.fetchall()


flag = True
searchCounter = 0
targetClasses = []

for eachItem in range(0, len(selected_letters_in_this_loop)):
    yourLabel = selected_letters_in_this_loop[eachItem][3]
    flag = True
    while flag:
        if listOfDiacritizedCharacter[searchCounter][1] == yourLabel:
            flag = False
            targetClasses.append(listOfDiacritizedCharacter[searchCounter][2])
            searchCounter = 0
        else:
            searchCounter += 1

targetClasses = netcdf_helpers.stringtochar(np.array(targetClasses))

str_list = []
for eachItem in range(0, len(targetClasses)):
    test = [x for x in targetClasses[eachItem] if (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
    str_list.append(test)

purifiedTargetClasses = str_list
outputFilename = "NCFileTargetClasses.nc"

# create a new .nc file
dataset = netcdf_helpers.Dataset(outputFilename, 'w', format='NETCDF4')

dataset.createDimension('numTimeSteps', len(purifiedTargetClasses))
dataset.createDimension('width', len(purifiedTargetClasses[0]))


# create the variables

netCDFLabels = dataset.createVariable('netCDFLabels', 'i4', ('numTimeSteps', 'width'))
netCDFLabels[:] = purifiedTargetClasses