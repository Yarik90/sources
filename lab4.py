import argparse
import os
import sys


def RYA_createParser(): # Функция для объявления параметров вызова из консоли
    RYA_parser = argparse.ArgumentParser()
    RYA_parser.add_argument('-e')
    RYA_parser.add_argument('-d')

    return RYA_parser


def encode(input_string): # Фунция выполняющая архивацию
    count = 0
    prev = ''
    lst = []
    nonrep = []
    rep = []
    for character in input_string:
        if character != prev:
            if not rep:
                nonrep.append(character)
                count += 1
                prev = character
            else:
                entry = (prev, count)
                lst.append(entry)
                rep = []
                count = 1
                nonrep = []
                nonrep.append(character)
        else:
            if not rep:
                if len(nonrep) != 1:
                    rep.append(nonrep[-1])
                    rep.append(character)
                    nonrep = nonrep[0:-1]
                    entry = (''.join(nonrep), -(count-1))
                    lst.append(entry)
                    count = 2
                    nonrep = []
                else:
                    print('test')
                    rep.append(nonrep[0])
                    rep.append(character)
                    nonrep = []
                    count = 2
            else:
                rep.append(character)
                prev = character
                count += 1
    else:
        try:
            if rep:
                entry = (character, count)
                lst.append(entry)
            else:
                entry = (''.join(nonrep), -(count))
                lst.append(entry)
            return (lst, 0)
        except Exception as e:
            print("Exception encountered {e}".format(e=e))
            return (e, 1)


def decode(lst): # Фунция, выполняющая разархивацию
    q = ""
    for character, count in lst:
        if count < 0:
            q += character
        else:
            q += character * count
    return q


def transform(enc): # Функция преобразования заархивированного массива в строку для записи в файл
    q = ''
    for character, count in enc:
        q += str(count)
        q += character
    return q


def transform_r(f_name): # Функиция для преобразования считанной заархивированной строки в массив подходящий для разархивирования
    k = open(f_name, 'r')
    mas = []
    for t in range(os.path.getsize(f_name)):
        s = k.read(1)
        if s == '-':
            kk = int(k.read(1))
            p = (k.read(kk), -kk)
            mas.append(p)
        elif s.isdigit():
            p = (k.read(1), int(s))
            mas.append(p)
    return mas





if __name__ == '__main__':
    RYA_parser = RYA_createParser() # Парсер для считывания аргументов командной строки
    RYA_namespace = RYA_parser.parse_args(sys.argv[1:]) # Считывание аргументов командной строки
    if RYA_namespace.e:
        RYA_filename = RYA_namespace.e  # Имя файла для архивации
        RYA_f = open(RYA_filename, 'r')  # Открытие файла
        RYA_f1 = open(RYA_filename + '.arh', 'w')  # Создание файла для зашифрованного сообщения
        RYA_k = RYA_f.read()
        RYA_f1.write(transform(encode(RYA_k)[0]))
    if RYA_namespace.d:
        RYA_filename = RYA_namespace.d.replace('.arh', '')  # Отбрасывание расширение arh у закодированного файла
        if os.path.isfile(RYA_filename):  # Проверка существования файла с таким же именем
            RYA_filename = RYA_filename.replace('.', '(1).')
        RYA_f2 = open(RYA_filename, 'w')
        RYA_s = transform_r(RYA_namespace.d)
        RYA_k = decode(RYA_s)
        RYA_f2.write(RYA_k)