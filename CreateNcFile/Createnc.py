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


def get_all_letters_of_corresponding_dataset_type(type_of_dataset):
    execute_calculate_total_number_Of_sentences_startTime = datetime.datetime.now()

    listOfSelectedLettersAndSentencesQuery = "select UnDiacritizedCharacter, DiacritizedCharacter, LetterType, SentenceNumber," \
                                             " Word, InputSequenceEncodedWords, TargetSequenceEncodedWords " \
                                             "from ParsedDocument where LetterType=" + "'%s'" % type_of_dataset

    cur.execute(listOfSelectedLettersAndSentencesQuery)
    global listOfSelectedLettersAndSentences
    listOfSelectedLettersAndSentences = []
    listOfSelectedLettersAndSentences = cur.fetchall()

    excutecalculateTotalNumberOfSentencesEndTime = datetime.datetime.now()
    print "get_all_letters_of_corresponding_dataset_type takes : ", excutecalculateTotalNumberOfSentencesEndTime - \
                                                      execute_calculate_total_number_Of_sentences_startTime
def excuteUnChangedSQLQueries():
    excuteChangedSQLQueriesStartTime = datetime.datetime.now()
    listOfUnDiacritizedCharacterQuery = "select * from UnDiacOneHotEncoding"
    cur.execute(listOfUnDiacritizedCharacterQuery)
    global listOfUnDiacritizedCharacter
    listOfUnDiacritizedCharacter = cur.fetchall()

    listOfDiacritizedCharacterQuery = "select * from DiacOneHotEncoding "
    cur.execute(listOfDiacritizedCharacterQuery)
    global listOfDiacritizedCharacter
    listOfDiacritizedCharacter = cur.fetchall()

    excuteChangedSQLQueriesEndTime = datetime.datetime.now()
    print "excuteChangedSQLQueries takes : ", excuteChangedSQLQueriesEndTime - excuteChangedSQLQueriesStartTime

def excuteChangedSQLQueries(dataSetType, startRange, endRange):
    excuteMySQLQueriesStartTime = datetime.datetime.now()
    listOfRecordsInParsedDocumentQuery = "select * from ParsedDocument where LetterType=" + "'%s'" % dataSetType +\
                                         " and SentenceNumber>=" + startRange + " and SentenceNumber< " + endRange + \
                                         " order by idCharacterNumber asc "
    cur.execute(listOfRecordsInParsedDocumentQuery)
    global listOfRecordsInParsedDocument
    listOfRecordsInParsedDocument = []
    listOfRecordsInParsedDocument = cur.fetchall()
    excuteMySQLQueriesEndTime = datetime.datetime.now()
    print "excuteMySQLQueries takes : ", excuteMySQLQueriesEndTime - excuteMySQLQueriesStartTime


def createNetCDFInput():
    excutecreateNetCDFInputStartTime = datetime.datetime.now()
    flag = True
    searchCounter = 0

    input = []
    global purifiedCDFInput
    purifiedCDFInput = []
    # Create Data of Input Variable
    for eachItem in range(0, len(listOfRecordsInParsedDocument)):
        yourLabel = listOfRecordsInParsedDocument[eachItem][2]
        flag = True
        while flag:
            if listOfUnDiacritizedCharacter[searchCounter][1] == yourLabel:
                flag = False
                UnDiacritizedCharacterOneHotEncoding = (str(listOfUnDiacritizedCharacter[searchCounter][2]))

                for eachItem in range(0, len(UnDiacritizedCharacterOneHotEncoding)):
                    test = [x for x in UnDiacritizedCharacterOneHotEncoding[eachItem] if
                            (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
                    if len(test) != 0:
                        input.append(int(test[0]))

                searchCounter = 0

                purifiedCDFInput.append(np.array(input))
                input = []
            else:
                searchCounter += 1

    excutecreateNetCDFInputEndTime = datetime.datetime.now()
    print "createNetCDFInput takes : ", excutecreateNetCDFInputEndTime - excutecreateNetCDFInputStartTime


def createNetCDFSeqLength():
    excutecreateNetCDFSeqLengthStartTime = datetime.datetime.now()
    letterCounterForEachSentence = 0
    global SEQLengths
    SEQLengths = []
    sentenceNumber = listOfRecordsInParsedDocument[0][5]

    # Create Data of SEQ Length Variable
    for eachItem in range(0, len(listOfRecordsInParsedDocument)):

        if listOfRecordsInParsedDocument[eachItem][5] == sentenceNumber:
            letterCounterForEachSentence += 1
        else:
            SEQLengths.append(letterCounterForEachSentence)
            sentenceNumber = listOfRecordsInParsedDocument[eachItem][5]
            letterCounterForEachSentence = 1

    SEQLengths.append(letterCounterForEachSentence)
    excutecreateNetCDFSeqLengthEndTime = datetime.datetime.now()
    print "createNetCDFSeqLength takes : ", excutecreateNetCDFSeqLengthEndTime - excutecreateNetCDFSeqLengthStartTime


def createNetCDFLabel():
    excutecreateNetCDFLabelStartTime = datetime.datetime.now()
    # extract one hot encoding column
    labels = [col[2] for col in listOfDiacritizedCharacter]

    # convert unicode to string
    labels = [x.encode('ascii') for x in labels]

    # convert array of string to array of char to be compatible with NETCDF
    # you will find strange values, but do not worry, it will exported correctly
    labels = netcdf_helpers.stringtochar(np.array(labels))
    label_list_after_removing_spaces_and_dots = []
    for eachItem in range(0, len(labels)):
        test = [x for x in labels[eachItem] if
                (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
        label_list_after_removing_spaces_and_dots.append(test)
    global purifiedLabels
    purifiedLabels = []
    purifiedLabels = netcdf_helpers.stringtochar(np.array(label_list_after_removing_spaces_and_dots))

    excutecreateNetCDFLabelEndTime = datetime.datetime.now()
    print "createNetCDFLabel takes : ", excutecreateNetCDFLabelEndTime - excutecreateNetCDFLabelStartTime


def createNetCDFTargetClasses():
    excutecreateNetCDFTargetClassesStartTime = datetime.datetime.now()

    searchCounter = 0
    targetClass = []
    for eachItem in range(0, len(listOfRecordsInParsedDocument)):
        yourLabel = listOfRecordsInParsedDocument[eachItem][3]
        OneHotTargetClassNotFound = True
        while OneHotTargetClassNotFound:
            if listOfDiacritizedCharacter[searchCounter][1] == yourLabel:
                OneHotTargetClassNotFound = False
                targetClass.append(listOfDiacritizedCharacter[searchCounter][2])
                searchCounter = 0
            else:
                searchCounter += 1

    targetClasses = netcdf_helpers.stringtochar(np.array(targetClass))

    targetClasses_list_after_removing_spaces_and_dots = []
    for eachRow in range(0, len(targetClasses)):
        for eachCol in range(0, len(targetClasses[eachRow])):
            test = [x for x in targetClasses[eachRow][eachCol] if
                    (x != '' and x != '.' and x != '[' and x != ']' and x != ' ' and x != '\n')]
            if len(test) != 0:
                targetClasses_list_after_removing_spaces_and_dots.append(int(test[0]))

    global purifiedTargetClasses
    purifiedTargetClasses = []
    purifiedTargetClasses = targetClasses_list_after_removing_spaces_and_dots

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
    global listOfSelectedLettersAndSentences
    listOfSelectedLettersAndSentences = []
    global listOfRecordsInParsedDocument
    listOfRecordsInParsedDocument = []
    # del listOfRecordsInParsedDocument[:]
    del purifiedCDFInput[:]
    del SEQLengths[:]
    del purifiedLabels[:]
    del purifiedTargetClasses[:]
    del seqTagSentences[:]
if __name__ == "__main__":
    availableDataSetTypes = ['training']
    patchSize = 500
    columnNumberOf_SentenceNumber = 3

    for x in range(0, len(availableDataSetTypes)):
        createMySQLConnection()
        get_all_letters_of_corresponding_dataset_type(availableDataSetTypes[0])
        excuteUnChangedSQLQueries()
        createNetCDFLabel()
        for punchOfSentences in range(0, len(listOfSelectedLettersAndSentences), patchSize):

            startRange = str(punchOfSentences + int(listOfSelectedLettersAndSentences[0][columnNumberOf_SentenceNumber]))
            print "start range:", startRange
            punchOfSentences += patchSize
            endRange = str(punchOfSentences + int(listOfSelectedLettersAndSentences[0][columnNumberOf_SentenceNumber]))
            print "end range:", endRange

            excuteChangedSQLQueries(availableDataSetTypes[x], startRange, endRange)
            createNetCDFInput()
            createNetCDFSeqLength()

            createNetCDFTargetClasses()
            createSeqTags()
            createNetCDFFile(availableDataSetTypes[x])
            resetAllLists()
