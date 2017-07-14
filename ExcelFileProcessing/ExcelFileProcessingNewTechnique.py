# -*- coding: utf-8 -*-

import csv
import xlsxwriter
import MySQLdb
import MySQLdb.cursors
import os
import glob
import unicodedata
from xlrd import open_workbook
from xlutils.copy import copy


class fatha_correction_class():
    def __init__(self, location, position, letter):
        self.location = location
        self.position = position
        self.letter = letter

    location = ""
    position = 0
    letter = ""

rnn_output_for_one_seq = []
neurons_locations_with_highest_output_for_a_seq = []
list_of_all_diacritized_letters = []
list_of_actual_letters = []
list_of_expected_letters = []

list_of_actual_letters_errors = []
list_of_expected_letters_errors = []
current_sentence = []

letters_of_fatha_correction = [u'ة', u'ا', u'ى']
locations_of_fatha_correction_letters = []
list_of_location_types = []
total_error = 0
sentence_number = 0
currentSentence = 0
row_of_letters_excel_file = 0
first_time = True
path = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample'
diacritization_error_excel_file_path = "D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\Errors" \
                                       "\Book1.xls "
extension = 'csv'

row_of_errors_excel_file = 1

workbook = xlsxwriter.Workbook(diacritization_error_excel_file_path)
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'Expected')
worksheet.write(0, 1, 'Actual')
worksheet.write(0, 2, 'Error Location')
workbook.close()


def connect_to_db():
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="Islammega88",  # your password
                         db="mstdb",  # name of the data base
                         cursorclass=MySQLdb.cursors.SSCursor,
                         use_unicode=True,
                         charset="utf8",
                         init_command='SET NAMES UTF8')
    global cur
    cur = db.cursor()


def get_number_of_first_testing_sentence():
    sentence_number_of_testing_query = "select SentenceNumber from parseddocument where LetterType='testing' limit 1"

    cur.execute(sentence_number_of_testing_query)

    global sentence_number
    sentence_number = (cur.fetchall())
    sentence_number = int((sentence_number[0])[0])


def get_sentence_from_db():
    connect_to_db()
    selected_sentence_query = "select Word from parseddocument where LetterType='testing' and SentenceNumber = " + \
                              str(sentence_number)

    cur.execute(selected_sentence_query)

    global current_sentence
    current_sentence = cur.fetchall()
    current_sentence = sorted(set(current_sentence), key=lambda x: current_sentence.index(x))


def read_csv_file(filename):
    path_of_file = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\\' + filename

    # with open('D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\\1.csv', 'rb') as csvfile:

    with open(path_of_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        global rnn_output_for_one_seq
        rnn_output_for_one_seq = []
        for row in reader:
            rnn_output_for_one_seq.append(map(float, row))


def get_neurons_numbers_with_highest_output_value():
    global rnn_output_for_one_seq
    global neurons_locations_with_highest_output_for_a_seq
    neurons_locations_with_highest_output_for_a_seq = []
    for row in rnn_output_for_one_seq:
        neurons_locations_with_highest_output_for_a_seq.append(row.index(max(row)))


def get_all_letters_from_db():
    list_of_all_diacritized_letters_query = "select diacritics from distinctdiacritics"

    cur.execute(list_of_all_diacritized_letters_query)

    global list_of_all_diacritized_letters
    list_of_all_diacritized_letters = cur.fetchall()


def get_actual_letters():
    global list_of_actual_letters
    list_of_actual_letters = []

    global neurons_locations_with_highest_output_for_a_seq
    for neuron_location in neurons_locations_with_highest_output_for_a_seq:
        list_of_actual_letters.append(list_of_all_diacritized_letters[neuron_location - 1])


def get_expected_letters():
    global sentence_number
    list_of_expected_diacritized_letters_query = "select Diacritics from parseddocument where " \
                                                 "LetterType='testing' and SentenceNumber = " + str(sentence_number)

    cur.execute(list_of_expected_diacritized_letters_query)

    global list_of_expected_letters
    list_of_expected_letters = []
    list_of_expected_letters = cur.fetchall()


def write_data_into_excel_file(path_of_file):

    global first_time
    if first_time:
        workbook = xlsxwriter.Workbook(path_of_file)
        worksheet = workbook.add_worksheet()

    else:
        wb = open_workbook(path_of_file)
        w = copy(wb)
        worksheet = w.get_sheet(0)

    global row_of_letters_excel_file
    row_of_letters_excel_file += 1

    column = 0

    for expected_letter, actual_letter in zip(list_of_expected_letters, list_of_actual_letters):
        worksheet.write(row_of_letters_excel_file, column, expected_letter[0])
        column = 1
        worksheet.write(row_of_letters_excel_file, column, actual_letter[0])
        row_of_letters_excel_file += 1
        column = 0

    row_of_letters_excel_file += 1

    if not first_time:
        w.save(path_of_file)

    first_time = False
    workbook.close()


def fatha_correction():
    get_locations_of_letters_of_fatha_correction()
    get_type_of_locations_of_fatha_correction()
    correct_fatha_errors()

    x = 1


def get_locations_of_letters_of_fatha_correction():
    global locations_of_fatha_correction_letters
    locations_of_fatha_correction_letters = []

    counter = -1
    for each_letter in list_of_actual_letters:
        counter += 1
        if any(each_letter[0] in s for s in letters_of_fatha_correction):
            locations_of_fatha_correction_letters.append(counter)


def get_type_of_locations_of_fatha_correction():
    global list_of_location_types
    list_of_location_types = []

    for each_word in current_sentence:
        number_of_letters = 0
        nfkd_form = unicodedata.normalize('NFKD', each_word[0])

        unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
        for each_letter in unDiacritizedWord:
            number_of_letters += 1

        location_counter = 0
        for each_letter in unDiacritizedWord:
            location_counter += 1
            if any(each_letter in s for s in letters_of_fatha_correction):
                if location_counter > 1:
                    fatha = fatha_correction_class('', 0, '')
                    fatha.letter = each_letter
                    if location_counter == number_of_letters:
                        fatha.location = 'last'
                    else:
                        fatha.location = 'middle'

                    list_of_location_types.append(fatha)
        x = 1


def correct_fatha_errors():
    letterFoundFlag = False
    prevCharWasDiac = False
    overall = ""
    comp = ''
    global list_of_location_types
    global list_of_actual_letters
    for each_location, each_object in zip(locations_of_fatha_correction_letters, list_of_location_types):

        if getattr(each_object, 'location') != 'first' and getattr(each_object, 'letter') == u'ا':
            nfkd_form = unicodedata.normalize('NFKD', (list_of_actual_letters[each_location - 1])[0])
            for c in nfkd_form:
                if not unicodedata.combining(c):
                    overall = c
                    letterFoundFlag = True
                elif (letterFoundFlag and c != u'ٔ' and c != u'ٕ') and (len(nfkd_form) > 1):
                    prevCharWasDiac = True
                    letterFoundFlag = False
                    if c == u'ٌ' or c == u'ْ' or c == u'ُ' or c == u'ِ' or c == u'ٍ':
                        c = u'َ'
                    overall += c
                    comp = unicodedata.normalize('NFC', overall)
                elif (prevCharWasDiac and c != u'ٔ' and c != u'ٕ') and (len(nfkd_form) > 2):  # second diacritization

                    if c == u'ٌ' or c == u'ْ' or c == u'ُ' or c == u'ِ' or c == u'ٍ':
                        c = u'َ'
                    letterFoundFlag = False
                    prevCharWasDiac = False
                    overall += c
                    comp = unicodedata.normalize('NFC', overall)


            x = 1
        elif getattr(each_object, 'location') == 'last' and getattr(each_object, 'letter') == u'ة':
            nfkd_form = unicodedata.normalize('NFKD', (list_of_actual_letters[each_location - 1])[0])
            for c in nfkd_form:
                if not unicodedata.combining(c):
                    overall = c
                    letterFoundFlag = True
                elif (letterFoundFlag and c != u'ٔ' and c != u'ٕ') and (len(nfkd_form) > 1):
                    prevCharWasDiac = True
                    letterFoundFlag = False
                    if c == u'ٌ' or c == u'ْ' or c == u'ُ' or c == u'ِ' or c == u'ٍ':
                        c = u'َ'
                    overall += c
                    comp = unicodedata.normalize('NFC', overall + c)
                elif (prevCharWasDiac and c != u'ٔ' and c != u'ٕ') and (len(nfkd_form) > 2):

                    if c == u'ٌ' or c == u'ْ' or c == u'ُ' or c == u'ِ' or c == u'ٍ':
                        c = u'َ'
                    letterFoundFlag = False
                    prevCharWasDiac = False
                    overall += c
                    comp = unicodedata.normalize('NFC', overall + c)
        elif getattr(each_object, 'location') == 'last' and getattr(each_object, 'letter') == u'ى':
            nfkd_form = unicodedata.normalize('NFKD', (list_of_actual_letters[each_location - 1])[0])
            for c in nfkd_form:
                if not unicodedata.combining(c):
                    overall = c
                    letterFoundFlag = True
                elif (letterFoundFlag and c != u'ٔ' and c != u'ٕ') and (len(nfkd_form) > 1):
                    prevCharWasDiac = True
                    letterFoundFlag = False
                    if c == u'ٌ' or c == u'ْ' or c == u'ُ' or c == u'ِ' or c == u'ٍ':
                        c = u'َ'
                    overall += c
                    comp = unicodedata.normalize('NFC', overall + c)
                elif (prevCharWasDiac and c != u'ٔ' and c != u'ٕ') and (len(nfkd_form) > 2):

                    if c == u'ٌ' or c == u'ْ' or c == u'ُ' or c == u'ِ' or c == u'ٍ':
                        c = u'َ'
                    letterFoundFlag = False
                    prevCharWasDiac = False
                    overall += c
                    comp = unicodedata.normalize('NFC', overall + c)


        list_of_actual_letters = [list(elem) for elem in list_of_actual_letters]

        (list_of_actual_letters[each_location - 1])[0] = comp
        list_of_actual_letters = [tuple(elem) for elem in list_of_actual_letters]
        list_of_actual_letters = tuple(list_of_actual_letters)


def get_diacritization_error():
    global list_of_actual_letters_errors
    global list_of_expected_letters_errors
    global total_error

    number_of_diacritization_errors = 0
    counter = 0
    letter_location = 0
    list_of_error_locations = []
    for letter in list_of_actual_letters:
        letter_location += 1
        if letter[0] != (list_of_expected_letters[counter])[0]:
            list_of_actual_letters_errors.append(letter)
            list_of_expected_letters_errors.append(list_of_expected_letters[counter])
            list_of_error_locations.append(letter_location)
            number_of_diacritization_errors += 1

        counter += 1

    total_error += number_of_diacritization_errors

    print number_of_diacritization_errors
    print 'total error: ', total_error

    wb = open_workbook(diacritization_error_excel_file_path)
    w = copy(wb)
    worksheet = w.get_sheet(0)

    global row_of_errors_excel_file
    row_of_errors_excel_file += 1

    column = 0
    i = 0
    for expected_letter, actual_letter in zip(list_of_expected_letters_errors, list_of_actual_letters_errors):
        worksheet.write(row_of_errors_excel_file, column, expected_letter[0])

        column = 1
        worksheet.write(row_of_errors_excel_file, column, actual_letter[0])

        column = 2
        worksheet.write(row_of_errors_excel_file, column, list_of_error_locations[i])

        i += 1
        row_of_errors_excel_file += 1
        column = 0

    all_sentence = ''
    for each_word in current_sentence:
        all_sentence += each_word[0] + ' '

    worksheet.write(row_of_errors_excel_file, column, all_sentence)

    row_of_errors_excel_file += 1

    w.save(diacritization_error_excel_file_path)

    workbook.close()

    list_of_actual_letters_errors = []
    list_of_expected_letters_errors = []

if __name__ == "__main__":
    connect_to_db()
    get_number_of_first_testing_sentence()

    os.chdir(path)
    result = [i for i in glob.glob('*.{}'.format(extension))]

    for file_name in result:
        get_sentence_from_db()
        read_csv_file(file_name)
        get_neurons_numbers_with_highest_output_value()
        connect_to_db()
        get_all_letters_from_db()
        get_actual_letters()
        get_expected_letters()
        # fatha_correction()
        # write_data_into_excel_file('D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\Book2.xlsx')
        get_diacritization_error()
        currentSentence += 1
        print 'sentence number: ', currentSentence
        sentence_number += 1

