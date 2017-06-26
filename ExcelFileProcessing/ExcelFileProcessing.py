# -*- coding: utf-8 -*-

import csv
import xlsxwriter
import MySQLdb
import MySQLdb.cursors
import os
import glob

rnn_output_for_one_seq = []
neurons_locations_with_highest_output_for_a_seq = []
list_of_all_diacritized_letters = []
list_of_actual_letters = []
list_of_expected_letters = []

list_of_actual_letters_errors = []
list_of_expected_letters_errors = []
number_of_diacritization_errors = 0
sentence_number = 0
col = -1
col_for_error = -1

path = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample'
extension = 'csv'


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
    neurons_locations_with_highest_output_for_a_seq = []
    for row in rnn_output_for_one_seq:
        neurons_locations_with_highest_output_for_a_seq.append(row.index(max(row)))


def get_all_letters_from_db():

    list_of_all_diacritized_letters_query = "select DiacritizedCharacter from diaconehotencoding"

    cur.execute(list_of_all_diacritized_letters_query)

    global list_of_all_diacritized_letters
    list_of_all_diacritized_letters = cur.fetchall()


def get_actual_letters():
    global list_of_actual_letters
    list_of_actual_letters = []
    for neuron_location in neurons_locations_with_highest_output_for_a_seq:
        list_of_actual_letters.append(list_of_all_diacritized_letters[neuron_location - 1])


def get_expected_letters():

    global sentence_number
    list_of_expected_diacritized_letters_query = "select DiacritizedCharacter from parseddocument where " \
                                                 "LetterType='testing' and SentenceNumber = " + str(sentence_number)

    cur.execute(list_of_expected_diacritized_letters_query)

    global list_of_expected_letters
    list_of_expected_letters = []
    list_of_expected_letters = cur.fetchall()


def write_data_into_excel_file(path_of_file):
    workbook = xlsxwriter.Workbook(path_of_file)
    worksheet = workbook.add_worksheet()

    row = 0

    global col
    col += 1

    for letter in list_of_expected_letters:
        worksheet.write(row, col, letter[0])
        row += 1

    row = 0
    col += 1

    for letter in list_of_actual_letters:
        worksheet.write(row, col, letter[0])
        row += 1

    col += 1
    workbook.close()


def get_diacritization_error():
    global number_of_diacritization_errors
    counter = 0
    for letter in list_of_actual_letters:
        if letter[0] != (list_of_expected_letters[counter])[0]:
            list_of_actual_letters_errors.append(letter)
            list_of_expected_letters_errors.append(list_of_expected_letters[counter])
            number_of_diacritization_errors += 1

        counter += 1

    print number_of_diacritization_errors

    workbook = xlsxwriter.Workbook('D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\Errors'
                                   '\diacritizationErrors.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    global col_for_error
    col_for_error += 1

    for letter in list_of_actual_letters_errors:
        worksheet.write(row, col_for_error, letter[0])
        row += 1

    row = 0
    col_for_error += 1

    for letter in list_of_expected_letters_errors:
        worksheet.write(row, col_for_error, letter[0])
        row += 1

    col_for_error += 1
    workbook.close()


if __name__ == "__main__":
    connect_to_db()
    get_number_of_first_testing_sentence()

    os.chdir(path)
    result = [i for i in glob.glob('*.{}'.format(extension))]

    for file_name in result:
        read_csv_file(file_name)
        get_neurons_numbers_with_highest_output_value()
        connect_to_db()
        get_all_letters_from_db()
        get_actual_letters()
        get_expected_letters()
        write_data_into_excel_file('D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\Book1.xlsx')
        get_diacritization_error()
        sentence_number += 1
