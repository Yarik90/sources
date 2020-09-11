from ctypes import c_uint32
import sys
import random
import os
import argparse
from random import choice
from string import ascii_letters
import getpass
import hashlib


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


def RYA_transform_key(keyn): # Функция чтения ключа из файла
    RYA_key = [] # Переменная для хранения считываемого ключа
    for i in range(4):
        RYA_t = c_uint32(int.from_bytes(keyn[i],'big')) # Преобразование считанного ключа в целочисленнй формат
        RYA_key.append(RYA_t)
    return RYA_key


if __name__ == '__main__':
    RYA_key = [c_uint32(random.randrange(100000,1000000)), c_uint32(random.randrange(100000,1000000)), c_uint32(random.randrange(100000,1000000)), c_uint32(random.randrange(100000,1000000))] # ключ сеанса
    RYA_filename = input('Введите имя файла для шифровывания:')
    RYA_f = open(RYA_filename, 'rb')  # Открытие файла в байтовом режиме
    RYA_f1 = open(RYA_filename + '.enc', 'wb')  # Создание файла для зашифровынного сообщения
    sizef = os.path.getsize(RYA_filename) // 8
    for i in range(sizef): # Шифрованиефайла с помощью ключа сеанса
        RYA_t1 = RYA_f.read(4)  # Считывание блоков по 32 битов
        RYA_t2 = RYA_f.read(4)
        RYA_text1 = int.from_bytes(RYA_t1, 'big')  # Преобразование байтов в числа
        RYA_text2 = int.from_bytes(RYA_t2, 'big')
        RYA_t = [c_uint32(RYA_text1), c_uint32(RYA_text2)]  # Преобразование чисел к формату uint_32
        RYA_enc_text = RYA_encrypt(RYA_t, RYA_key)  # Зашифровывание сообщения
        RYA_f1.write(RYA_enc_text[0].value.to_bytes(4, 'big'))  # Запись в файл зашифровынного сообщения с преобразованием чисел в байтовые коды
        RYA_f1.write(RYA_enc_text[1].value.to_bytes(4, 'big'))
    RYA_f.close()
    RYA_f1.close()
    RYA_passw = getpass.getpass('Введите пароль:')
    RYA_data = hashlib.md5(RYA_passw.encode()).digest() # создание на основе введеного пароля ключ шифрования с помощью алгоритма MD5
    RYA_ckey = [RYA_data[i:i + 4] for i in range(0, len(RYA_data), 4)] # Разделение ключа шифрования на 4 части по 4 байта
    RYA_ckey = RYA_transform_key(RYA_ckey)
    RYA_k1 = [RYA_key[0], RYA_key[1]]
    RYA_k2 = [RYA_key[2], RYA_key[3]]
    RYA_enc_k1 = RYA_encrypt(RYA_k1, RYA_ckey) # Шифрование ключа сеанса ключом шифрования
    RYA_enc_k2 = RYA_encrypt(RYA_k2, RYA_ckey)
    with open(RYA_filename + '.enc', 'rb+') as fio: # Запись зашифрованного ключа сеанса в начало зашифрованного файла
        data = fio.read()
        fio.seek(0)
        fio.write(RYA_enc_k1[0].value.to_bytes(4, 'big'))
        fio.write(RYA_enc_k1[1].value.to_bytes(4, 'big'))
        fio.write(RYA_enc_k2[0].value.to_bytes(4, 'big'))
        fio.write(RYA_enc_k2[1].value.to_bytes(4, 'big'))
        fio.write(data)
        fio.close()
    RYA_f = open(RYA_filename + '.enc', 'rb')
    sizef = (os.path.getsize(RYA_filename + '.enc') - 16) // 8
    if os.path.isfile(RYA_filename):
        RYA_filename = RYA_filename.replace('.', '(1).')
    RYA_f2 = open(RYA_filename, 'w')
    RYA_kkey = [c_uint32(int.from_bytes(RYA_f.read(4),'big')), c_uint32(int.from_bytes(RYA_f.read(4),'big')), c_uint32(int.from_bytes(RYA_f.read(4),'big')), c_uint32(int.from_bytes(RYA_f.read(4),'big'))] # Считывание ключа сеанса из файла
    RYA_ck = [RYA_kkey[0], RYA_kkey[1]]
    RYA_ck2 = [RYA_kkey[2], RYA_kkey[3]]
    RYA_ck = RYA_decrypt(RYA_ck, RYA_ckey) # Расшифровка ключа сеанса
    RYA_ck2 = RYA_decrypt(RYA_ck2, RYA_ckey)
    RYA_kkey = [RYA_ck[0], RYA_ck[1], RYA_ck2[0], RYA_ck2[1]]
    for i in range(sizef):  # Расшифровка файла с помощью ключа сеанса
        RYA_t1 = RYA_f.read(4)  # Чтение 2 блоков по 32 бита
        RYA_t2 = RYA_f.read(4)
        RYA_text1 = int.from_bytes(RYA_t1, 'big')  # Преобразование байтовых кодов к численному типу
        RYA_text2 = int.from_bytes(RYA_t2, 'big')
        RYA_t = [c_uint32(RYA_text1), c_uint32(RYA_text2)]  # Преобразование чисел к формату uint_32
        RYA_dec_text = RYA_decrypt(RYA_t, RYA_kkey)  # Расшифровка сообщения
        RYA_f2.write(RYA_dec_text[0].value.to_bytes(4, 'big').decode())
        RYA_f2.write(RYA_dec_text[1].value.to_bytes(4, 'big').decode())