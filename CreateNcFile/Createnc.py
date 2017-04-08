import netcdf_helpers
import MySQLdb
from PIL import Image
from numpy import *


db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Islammega88",  # your password
                     db="MSTDB",  # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()

listOfUnDiacritizedCharacterQuery = "select * from UnDiacOneHotEncoding where UnDiacritizedCharacter!='' and " \
                                    "UnDiacritizedCharacter!='.' "

cur.execute(listOfUnDiacritizedCharacterQuery)
listOfUnDiacritizedCharacter = cur.fetchall()

listOfDiacritizedCharacterQuery = "select * from DiacOneHotEncoding where DiacritizedCharacter!='' and " \
                                  "DiacritizedCharacter!='.' "

cur.execute(listOfDiacritizedCharacterQuery)
listOfDiacritizedCharacter = cur.fetchall()

listOfRecordsInParsedDocumentQuery = "select * from ParsedDocument where UnDiacritizedCharacter!='.' and  " \
                                     "UnDiacritizedCharacter!='' order by idCharacterNumber asc "

cur.execute(listOfRecordsInParsedDocumentQuery)
listOfRecordsInParsedDocument = cur.fetchall()

test = listOfRecordsInParsedDocument[-1]
seqLengths = listOfRecordsInParsedDocument[-1][5]
numTimeSteps = len(listOfRecordsInParsedDocument)
inputPatternSize = len(listOfUnDiacritizedCharacter)
numOfLabels = len(listOfDiacritizedCharacter)
maxLabelLength = len(listOfDiacritizedCharacter)  # I need to recheck it again
maxTargetStringLength = 5000  # i need to recheck it again
maxSeqTagLength = 800   # i need to recheck it again

numTargetClasses = len(listOfDiacritizedCharacter)
labels = []
targetStrings = []
for eachItem in range(0, len(listOfRecordsInParsedDocumentQuery)):
    labels.append(listOfRecordsInParsedDocumentQuery[eachItem][3])


for filename in seqTags:
    print "reading image file", filename
    image = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
    # image.getdata() returns the pixel value
    # pixel value: number indicates how bright that pixel is, and/or what color it should be
    # since the image has only white and black, so pixels values
    # will be either 255 [white], or 0 [black]
    for i in image.getdata():
        inputs[offset][0] = (float(i) - inputMean) / inputStd
        offset += 1

outputFilename = "TestNCFile"

# create a new .nc file
file = netcdf_helpers.NetCDFFile(outputFilename, 'w')

# create the dimensions
netcdf_helpers.createNcDim(file, 'numSeqs', len(seqLengths))
netcdf_helpers.createNcDim(file, 'numTimesteps', len(inputs))
netcdf_helpers.createNcDim(file, 'inputPattSize', len(inputs[0]))
netcdf_helpers.createNcDim(file, 'numLabels', len(labels))

# create the variables

netcdf_helpers.createNcStrings(file, 'labels', labels, ('numLabels', 'maxLabelLength'), 'labels')
netcdf_helpers.createNcStrings(file, 'targetStrings', targetStrings, ('numSeqs', 'maxTargStringLength'),
                               'target strings')
netcdf_helpers.createNcStrings(file, 'seqTags', seqTags, ('numSeqs', 'maxSeqTagLength'), 'sequence tags')
netcdf_helpers.createNcVar(file, 'seqLengths', seqLengths, 'i', ('numSeqs',), 'sequence lengths')
netcdf_helpers.createNcStrings(file, 'wordTargetStrings', wordTargetStrings, ('numSeqs', 'maxWordTargStringLength'),
                               'target strings')
netcdf_helpers.createNcVar(file, 'inputs', inputs, 'f', ('numTimesteps', 'inputPattSize'), 'input patterns')


# write the data to disk
print "writing data to", outputFilename
file.close()