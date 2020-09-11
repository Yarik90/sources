from ctypes import c_uint32
import sys
import random
import os
import argparse
from random import choice
from string import ascii_letters


def RYA_createParser(): # Функция для объявления параметров вызова из консоли
    RYA_parser = argparse.ArgumentParser()
    RYA_parser.add_argument('-e')
    RYA_parser.add_argument('-d', nargs='+')

    return RYA_parser


def RYA_encrypt(RYA_text, RYA_key): # Функция зашифровывания по алгортиму TEA
    RYA_sum = c_uint32(0) # Переменная, использующая для хранения константы дельта умноженной но номер цикла
    RYA_delta = 0x9e3779b9 # Константа дельта, добавленная чтобы защититься от простых атак, основанных на симметрии раундов

    for i in range(32): # Блок данных шифруется на протяжении 32 циклов (64 раундов) с помщью операций побитового сдвига, побитового исключающего или, сложения по модулю 2^32
        RYA_sum.value += RYA_delta
        RYA_text[0].value += (RYA_text[1].value << 4) + RYA_key[0].value ^ RYA_text[1].value + RYA_sum.value ^ (RYA_text[1].value >> 5) + RYA_key[1].value
        RYA_text[1].value += (RYA_text[0].value << 4) + RYA_key[2].value ^ RYA_text[0].value + RYA_sum.value ^ (RYA_text[0].value >> 5) + RYA_key[3].value

    return RYA_text


def RYA_decrypt(RYA_text, RYA_key): # Функция расшифровывания по алгортиму TEA

    RYA_sum = c_uint32(0xc6ef3720) # значение полученное путем переменожения количества циклов на константу дельта
    RYA_delta = 0x9e3779b9 # Константа дельта

    for i in range(32): # Блок данных расшифровывается с помощью ключа в обратном порядке
        RYA_text[1].value -= (RYA_text[0].value << 4) + RYA_key[2].value ^ RYA_text[0].value + RYA_sum.value ^ (RYA_text[0].value >> 5) + RYA_key[3].value
        RYA_text[0].value -= (RYA_text[1].value << 4) + RYA_key[0].value ^ RYA_text[1].value + RYA_sum.value ^ (RYA_text[1].value >> 5) + RYA_key[1].value
        RYA_sum.value -= RYA_delta

    return RYA_text


def RYA_gen_key(): # Функция генерации псевдослучайного ключа
    RYA_key = []
    for i in range(4):
        RYA_key.append(''.join(choice(ascii_letters) for i in range(4)).encode())  # Переменная хранящая ключ разбитый на 4 части
    RYA_f = open('key.txt','wb') # Открытие файла для записи ключа
    for i in RYA_key: # Запись ключа в файл
        RYA_f.write(i)
    RYA_f.close() # Закрытие файла


def RYA_read_key(keyn): # Функция чтения ключа из файла
    RYA_f = open(keyn,'rb') # Открытие файла с ключом для чтения побайтово
    RYA_key = [] # Переменная для хранения считываемого ключа
    for i in range(4):
        RYA_t = int.from_bytes(RYA_f.read(4),'big') # Преобразование считанного ключа в целочисленнй формат
        RYA_key.append(RYA_t)
    RYA_f.close()
    return RYA_key


def RYA_ciph_block(RYA_mod, RYA_block, RYA_ciph, RYA_o_file):
    if RYA_mod == 0:
        RYA_t = int.from_bytes(RYA_block, 'big') ^ RYA_ciph[0].value
        RYA_o_file.write(RYA_t.to_bytes(len(RYA_block), 'big'))
    elif RYA_mod == 1:
        RYA_t = int.from_bytes(RYA_block, 'big') ^ RYA_ciph[0].value
        RYA_o_file.write(RYA_t.to_bytes(len(RYA_block), 'big').decode())


if __name__ == '__main__':
    RYA_parser = RYA_createParser() # Парсер для считывания аргументов командной строки
    RYA_namespace = RYA_parser.parse_args(sys.argv[1:]) # Считывание аргументов командной строки
    RYA_init = [c_uint32(554433), c_uint32(333232)]
    if RYA_namespace.e:
        RYA_gen_key() # Генерация ключа
        RYA_k = RYA_read_key('key.txt') # Считывание ключа из файла
        RYA_key1 = [c_uint32(RYA_k[0]), c_uint32(RYA_k[1]), c_uint32(RYA_k[2]), c_uint32(RYA_k[3])] # Преобразование ключа к формату uint_32
        RYA_filename = RYA_namespace.e # Имя файла для шифрования
        RYA_f = open(RYA_filename, 'rb') # Открытие файла в байтовом режиме
        RYA_f1 = open(RYA_filename + '.enc', 'wb') # Создание файла для зашифровынного сообщения
        RYA_block = RYA_init
        sizef = os.path.getsize(RYA_namespace.e)//8
        for i in range(sizef):
            RYA_t1 = RYA_f.read(4)  # Считывание блоков по 32 битов
            RYA_t2 = RYA_f.read(4)
            RYA_text1 = int.from_bytes(RYA_t1, 'big')  # Преобразование байтов в числа
            RYA_text2 = int.from_bytes(RYA_t2, 'big')
            RYA_cip = RYA_encrypt(RYA_block, RYA_key1) # Зашифровывание вектора инициализации
            RYA_block = RYA_cip
            RYA_enc_text = [RYA_text1 ^ RYA_cip[0].value, RYA_text2 ^ RYA_cip[1].value] # Зашифровывание блока данных
            RYA_f1.write(RYA_enc_text[0].to_bytes(4, 'big')) # Запись в файл зашифровынного сообщения с преобразованием чисел в байтовые коды
            RYA_f1.write(RYA_enc_text[1].to_bytes(4, 'big'))
        RYA_b = RYA_f.read()
        RYA_ciph_block(0,RYA_b,RYA_block,RYA_f1)
        RYA_f.close()
        RYA_f1.close()
    if RYA_namespace.d:
        RYA_filename = RYA_namespace.d[0].replace('.enc', '')  # Отбрасывание расширение enc у закодированного файла
        if os.path.isfile(RYA_filename):  # Проверка существования файла с таким же именем
            RYA_filename = RYA_filename.replace('.', '(1).')
        RYA_f2 = open(RYA_filename, 'w')
        RYA_f = open(RYA_namespace.d[0], 'rb') # Открытие файла для расшифрования
        RYA_block = RYA_init
        sizef = os.path.getsize(RYA_namespace.d[0]) // 8
        for i in range(sizef):
            RYA_t1 = RYA_f.read(4) # Чтение 2 блоков по 32 бита
            RYA_t2 = RYA_f.read(4)
            RYA_text1 = int.from_bytes(RYA_t1, 'big') # Преобразование байтовых кодов к численному типу
            RYA_text2 = int.from_bytes(RYA_t2, 'big')
            RYA_k = RYA_read_key(RYA_namespace.d[1]) # Чтение ключа из файла
            RYA_key1 = [c_uint32(RYA_k[0]), c_uint32(RYA_k[1]), c_uint32(RYA_k[2]), c_uint32(RYA_k[3])] # Преобразование чисел ключа к формату uint_32
            RYA_cip = RYA_encrypt(RYA_block, RYA_key1)
            RYA_block = RYA_cip
            RYA_dec_text = [RYA_text1 ^ RYA_cip[0].value, RYA_text2 ^ RYA_cip[1].value]
            RYA_dec_text1= RYA_dec_text[0].to_bytes(4, 'big').decode() #Преобразование чисел в байтовый код
            RYA_dec_text2= RYA_dec_text[1].to_bytes(4, 'big').decode()
            RYA_f2.write(RYA_dec_text1 + RYA_dec_text2) # Запись расшифрованного сообщения в файл
        RYA_b = RYA_f.read()
        RYA_ciph_block(1, RYA_b, RYA_block, RYA_f2)
        RYA_f2.close()

