# -*- coding: utf-8 -*-

import csv
import xlsxwriter
import MySQLdb
import MySQLdb.cursors
import os
import glob
import unicodedata
from xlrd import open_workbook
from itertools import groupby
from xlutils.copy import copy
import locale

final_list_of_actual_letters_after_post_processing = []
final_list_of_word = []
rnn_output_for_one_seq = []
neurons_locations_with_highest_output_for_a_seq = []
list_of_all_diacritized_letters = []

list_of_actual_letters_before_sukun_correction = []
list_of_expected_letters_before_sukun_correction = []
final_list_of_actual_letters = []
dictionary_correction_list = []

list_of_actual_letters = []
list_of_expected_letters = []
list_of_testing_words = []
list_of_actual_letters_errors = []
list_of_expected_letters_errors = []
current_sentence = []
list_of_required_info = []
location_of_last_character = []

list_of_actual_letters_with_its_location = []

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
last_character_location = 0

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
    list_of_all_diacritized_letters_query = "select DiacritizedCharacter from diaconehotencoding"

    cur.execute(list_of_all_diacritized_letters_query)

    global list_of_all_diacritized_letters
    list_of_all_diacritized_letters = cur.fetchall()


def get_actual_letters():

    global list_of_actual_letters_before_sukun_correction
    list_of_actual_letters_before_sukun_correction = []

    global neurons_locations_with_highest_output_for_a_seq
    for neuron_location in neurons_locations_with_highest_output_for_a_seq:
        list_of_actual_letters_before_sukun_correction.append(list_of_all_diacritized_letters[neuron_location - 1])


def get_expected_letters():
    global sentence_number
    list_of_expected_diacritized_letters_query = "select DiacritizedCharacter from parseddocument where " \
                                                 "LetterType='testing' and SentenceNumber = " + str(sentence_number)

    cur.execute(list_of_expected_diacritized_letters_query)

    global list_of_expected_letters_before_sukun_correction
    list_of_expected_letters_before_sukun_correction = []
    list_of_expected_letters_before_sukun_correction = cur.fetchall()


def sukun_correction():
    global list_of_actual_letters
    list_of_actual_letters = []

    global list_of_expected_letters
    list_of_expected_letters = []

    for each_character in list_of_actual_letters_before_sukun_correction:
        spaChar = unicodedata.normalize('NFC', each_character[0])
        if u'ْ' in spaChar:
            for c in spaChar:
                if not unicodedata.combining(c):
                    list_of_actual_letters.append(tuple(unicodedata.normalize('NFC', c)))
        else:
            list_of_actual_letters.append(each_character)

    for each_character in list_of_expected_letters_before_sukun_correction:
        spaChar = unicodedata.normalize('NFC', each_character[0])
        if u'ْ' in spaChar:
            for c in spaChar:
                if not unicodedata.combining(c):
                    list_of_expected_letters.append(tuple(unicodedata.normalize('NFC', c)))
        else:
            list_of_expected_letters.append(each_character)


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
        worksheet.write(row_of_errors_excel_file, column, actual_letter)

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
        sukun_correction()

        get_diacritization_error()
        currentSentence += 1
        print 'sentence number: ', currentSentence
        sentence_number += 1
