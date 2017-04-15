# -*- coding: utf-8 -*-
import netCDF4 as netcdf_helpers
import MySQLdb
import numpy as np

docName = "الجامع الصحيح المسمى صحيح مسلم.txt"

db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Islammega88",  # your password
                     db="mstdb",  # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()

listOfRecordsInParsedDocumentQuery = "select * from ParsedDocument order by idCharacterNumber asc "

cur.execute(listOfRecordsInParsedDocumentQuery)
listOfRecordsInParsedDocument = cur.fetchall()

labels = []

for eachItem in range(0, len(listOfRecordsInParsedDocument)):
    yourLabel = str((listOfRecordsInParsedDocument[eachItem][10]))
    labels.append(yourLabel)

numLabels = len(labels)
maxLabelLength = 1

outputFilename = "TestNCFile.nc"
str_out = netcdf_helpers.stringtochar(np.array(labels))
# create a new .nc file
dataset = netcdf_helpers.Dataset(outputFilename, 'w', format='NETCDF4')


dataset.createDimension('rows', numLabels)
dataset.createDimension('col', 5)
test = dataset.createVariable('test', 'S1', ('rows', 'col'))
test[:] = str_out
x=0
#netcdf_helpers.createNcStrings(file, 'labels', labels, ('numLabels', 'maxLabelLength'), 'labels')