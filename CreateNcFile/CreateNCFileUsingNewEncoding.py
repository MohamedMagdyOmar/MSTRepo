import netCDF4 as netcdf_helpers
import MySQLdb
import numpy as np
import datetime

global punchNumber
punchNumber = 0


def createMySQLConnection():
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="Islammega88",  # your password
                         db="mstdb",  # name of the data base
                         use_unicode=True,
                         charset="utf8",
                         init_command='SET NAMES UTF8')
    global cur
    cur = db.cursor()


def calculateTotalNumberOfSentences(dataSetType):
    excutecalculateTotalNumberOfSentencesStartTime = datetime.datetime.now()

    listOfSelectedSentencesQuery = "select UnDiacritizedCharacter, DiacritizedCharacter, LetterType, SentenceNumber," \
                                   " Word, InputSequenceEncodedWords, TargetSequenceEncodedWords " \
                                   "from ParsedDocument where LetterType=" + "'%s'" % dataSetType + " limit 300"

    cur.execute(listOfSelectedSentencesQuery)
    global listOfSelectedSentences
    listOfSelectedSentences = []
    listOfSelectedSentences = cur.fetchall()

    excutecalculateTotalNumberOfSentencesEndTime = datetime.datetime.now()
    print "calculateTotalNumberOfSentences takes : ", excutecalculateTotalNumberOfSentencesEndTime - \
                                                      excutecalculateTotalNumberOfSentencesStartTime


def createNetCDFLabel():

    execute_create_NetCDF_Label_StartTime = datetime.datetime.now()

    cur.execute("select distinct DiacritizedCharacter,TargetSequenceEncodedWords from parseddocument")
    list_of_labels = np.array(cur.fetchall())
    labels = list_of_labels[:, 1]
    label_list_after_removing_spaces_and_dots = []
    for eachItem in labels:
        selectedLabel = netcdf_helpers.stringtochar(np.array(eachItem))
        test = [str(x) for x in selectedLabel if
                (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
        label_list_after_removing_spaces_and_dots.append(test)

    global purifiedLabels
    purifiedLabels = []
    purifiedLabels = netcdf_helpers.stringtochar(np.array(label_list_after_removing_spaces_and_dots))

    excutecreateNetCDFLabelEndTime = datetime.datetime.now()
    print "createNetCDFLabel takes : ", excutecreateNetCDFLabelEndTime - execute_create_NetCDF_Label_StartTime


def excuteChangedSQLQueries(dataSetType, startRange, endRange):
    excuteMySQLQueriesStartTime = datetime.datetime.now()

    global listOfRecordsInParsedDocument
    listOfRecordsInParsedDocument = []

    listOfRecordsInParsedDocument = []
    [listOfRecordsInParsedDocument.append(item) for item in listOfSelectedSentences
     if int(startRange) <= int(item[3]) < int(endRange) and dataSetType == str(item[2])]

    excuteMySQLQueriesEndTime = datetime.datetime.now()
    print "excuteMySQLQueries takes : ", excuteMySQLQueriesEndTime - excuteMySQLQueriesStartTime


def createNetCDFInput():
    excutecreateNetCDFInputStartTime = datetime.datetime.now()

    global purifiedCDFInput
    purifiedCDFInput = []

    listOfExtractedCode = []

    for eachItem in listOfRecordsInParsedDocument:
        listOfExtractedCode.append(str(eachItem[5]))

    listNetCDFCode = netcdf_helpers.stringtochar(np.array(listOfExtractedCode))
    del listOfExtractedCode[:]

    input_list_after_removing_spaces_and_dots = []
    for eachRow in listNetCDFCode:
        test = [x for x in eachRow if
                (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
        input_list_after_removing_spaces_and_dots.append(test)

    purifiedCDFInput = netcdf_helpers.stringtochar(np.array(input_list_after_removing_spaces_and_dots))
    del input_list_after_removing_spaces_and_dots[:]

    excutecreateNetCDFInputEndTime = datetime.datetime.now()
    print "createNetCDFInput takes : ", excutecreateNetCDFInputEndTime - excutecreateNetCDFInputStartTime


def createNetCDFSeqLength():
    excutecreateNetCDFSeqLengthStartTime = datetime.datetime.now()
    letterCounterForEachSentence = 0
    global SEQLengths
    SEQLengths = []
    sentenceNumber = listOfRecordsInParsedDocument[0][3]

    # Create Data of SEQ Length Variable
    for eachItem in range(0, len(listOfRecordsInParsedDocument)):

        if listOfRecordsInParsedDocument[eachItem][3] == sentenceNumber:
            letterCounterForEachSentence += 1
        else:
            SEQLengths.append(letterCounterForEachSentence)
            sentenceNumber = listOfRecordsInParsedDocument[eachItem][3]
            letterCounterForEachSentence = 1

    SEQLengths.append(letterCounterForEachSentence)
    excutecreateNetCDFSeqLengthEndTime = datetime.datetime.now()
    print "createNetCDFSeqLength takes : ", excutecreateNetCDFSeqLengthEndTime - excutecreateNetCDFSeqLengthStartTime


def createNetCDFTargetClasses():

    excutecreateNetCDFTargetClassesStartTime = datetime.datetime.now()

    global purifiedTargetClasses
    purifiedTargetClasses = []

    listOfExtractedCode = []

    for eachItem in listOfRecordsInParsedDocument:
        listOfExtractedCode.append(str(eachItem[6]))

    listNetCDFCode = netcdf_helpers.stringtochar(np.array(listOfExtractedCode))
    del listOfExtractedCode[:]

    targetClasses_list_after_removing_spaces_and_dots = []
    for eachRow in listNetCDFCode:
            test = [x for x in eachRow if
                    (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
            targetClasses_list_after_removing_spaces_and_dots.append(test)

    purifiedTargetClasses = netcdf_helpers.stringtochar(np.array(targetClasses_list_after_removing_spaces_and_dots).ravel())
    del targetClasses_list_after_removing_spaces_and_dots[:]

    excutecreateNetCDFTargetClassesEndTime = datetime.datetime.now()
    print "createNetCDFTargetClasses takes : ", excutecreateNetCDFTargetClassesEndTime - excutecreateNetCDFTargetClassesStartTime


#  added due to error in running library
def createSeqTags():
    excutecreateSeqTagsStartTime = datetime.datetime.now()
    global seqTagSentences
    seqTagSentences = []
    counter = 1
    for eachItem in range(0, len(SEQLengths)):
        sentenceNumber = counter

        # converted to string because if int, the library will give error [Attempt to convert between text & numbers]
        seqTagSentences.append(str(sentenceNumber))
        counter += 1

    seqTagSentences = (np.array(seqTagSentences))

    excutecreateSeqTagsEndTime = datetime.datetime.now()
    print "createSeqTags takes : ", excutecreateSeqTagsEndTime - excutecreateSeqTagsStartTime


###
def createNetCDFFile(dataSetType):
    global punchNumber
    punchNumber += 1
    print "punch Number: ", punchNumber
    outputFilename = dataSetType + "NCFile_" + str(punchNumber) + ".nc"
    outputFilename = "test.nc"
    # create a new .nc file
    dataset = netcdf_helpers.Dataset(outputFilename, 'w', format='NETCDF4')

    # create the dimensions

    dataset.createDimension('numTimesteps', len(purifiedCDFInput))
    dataset.createDimension('inputPattSize', len(purifiedCDFInput[0]))
    dataset.createDimension('numLabels', len(purifiedLabels))
    dataset.createDimension('maxLabelLength', len(purifiedLabels[0]))  # you get this value from the array 'labels'
    dataset.createDimension('numSeqs', len(SEQLengths))
    dataset.createDimension('numTimeSteps', len(purifiedTargetClasses))
    #    dataset.createDimension('width', len(purifiedTargetClasses[0]))

    #  added due to error in running library
    dataset.createDimension('maxSeqTagLength', 1)

    # create the variables

    netCDFLabels = dataset.createVariable('labels', 'S1', ('numLabels', 'maxLabelLength'))
    netCDFLabels[:] = purifiedLabels

    netCDFInput = dataset.createVariable('inputs', 'i4', ('numTimesteps', 'inputPattSize'))
    netCDFInput[:] = purifiedCDFInput

    netCDFSEQLengths = dataset.createVariable('seqLengths', 'i4', ('numSeqs'))
    netCDFSEQLengths[:] = SEQLengths

    netCDFTargetClasses = dataset.createVariable('targetClasses', 'i4', ('numTimeSteps'))
    netCDFTargetClasses[:] = purifiedTargetClasses

    netCDFSeqTags = dataset.createVariable('seqTags', 'S1', ('numSeqs', 'maxSeqTagLength'))
    netCDFSeqTags[:] = seqTagSentences

    # write the data to disk
    print "writing data to", outputFilename
    dataset.close()


def resetAllLists():
    global listOfSelectedSentences
    listOfSelectedSentences= []
    del listOfRecordsInParsedDocument[:]
    del purifiedCDFInput[:]
    del SEQLengths[:]
    del purifiedLabels[:]
    del purifiedTargetClasses[:]
    del seqTagSentences[:]
if __name__ == "__main__":
    patchSize = 3
    availableDataSetTypes = ['training']
    for x in range(0, len(availableDataSetTypes)):
        createMySQLConnection()
        calculateTotalNumberOfSentences(availableDataSetTypes[0])
        createNetCDFLabel()
        for punchOfSentences in range(0, len(listOfSelectedSentences), 3):

            startRange = str(punchOfSentences + int(listOfSelectedSentences[0][3]))
            print "start range:", startRange
            punchOfSentences += patchSize
            endRange = str(punchOfSentences + int(listOfSelectedSentences[0][3]))
            print "end range:", endRange

            excuteChangedSQLQueries(availableDataSetTypes[0], startRange, endRange)
            createNetCDFInput()
            createNetCDFSeqLength()
            createNetCDFTargetClasses()
            createSeqTags()
            createNetCDFFile(availableDataSetTypes[0])
            x = 1
