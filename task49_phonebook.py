# Задача №49. Решение в группах
# Создать телефонный справочник с
# возможностью импорта и экспорта данных в
# формате .txt. Фамилия, имя, отчество, номер
# телефона - данные, которые должны находиться
# в файле.
# 1. Программа должна выводить данные
# 2. Программа должна сохранять данные в
# текстовом файле
# 3. Пользователь может ввести одну из
# характеристик для поиска определенной
# записи(Например имя или фамилию
# человека)
# 4. Использование функций. Ваша программа
# не должна быть линейной

from csv import DictReader, DictWriter
from os.path import exists


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


def print_help():
    commands_list = {
        'r': 'чтение из файла',
        'w': 'запись данных в файл',
        'delete': 'удаление строки из файла',
        'copy': 'копирование всех данных в новый файл',
        'copyrow': 'копирование определенной строки в новый файл',
        'q': 'выход из программы',
        'help': 'вывод списка команд'
    }
    for key, value in commands_list.items():
        print(f'{key} - {value}')


def get_info():
    flag = False
    while not flag:
        try:
            first_name = input('Имя: ')
            if len(first_name) < 2:
                raise NameError('Слишком короткое имя')
            second_name = input('Введите фамилию: ')
            if len(second_name) < 2:
                raise NameError('Слишком короткая фамилия')
            phone_number = input('Введите номер телефона: ')
            if len(phone_number) < 11:
                raise NameError(f'Номер телефона слишком короткий')
        except NameError as err:
            print(err)
        else:
            flag = True
    return [first_name, second_name, phone_number]


def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        f_w = DictWriter(f, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()


def write_file(file_name):
    res = read_file(file_name)
    user_data = get_info()
    new_obj = {'first_name': user_data[0], 'second_name': user_data[1], 'phone_number': user_data[2]}
    res.append(new_obj)
    standart_write(file_name, res)


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        f_r = DictReader(f)
        return list(f_r)


def remove_row(file_name):
    search = int(input('Введите номер строки для удаления: '))
    res = read_file(file_name)
    if search <= len(res):
        res.pop(search - 1)
        standart_write(file_name, res)
    else:
        print('В файле нет строки с таким номером.')


def standart_write(file_name, res):
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        f_w = DictWriter(f, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()
        f_w.writerows(res)


def copy_data(file_name):
    res = read_file(file_name)
    new_file_name = input('Введите имя для нового файла: ')
    if not exists(new_file_name):
        create_file(new_file_name)
    standart_write(new_file_name, res)


def copy_row(file_name):
    res = read_file(file_name)
    row_number = int(input('Введите номер строки для копирования: '))
    if row_number <= len(res):
        row = [res[row_number - 1]]
    new_file_name = input('Введите имя для нового файла: ')
    standart_write(new_file_name, row)
    print(res)
    print(row)


file_name = 'phone.csv'


def main():
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'help':
            print_help()
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
        elif command == 'r':
            if not exists(file_name):
                print('Файла нет. Создайте его.')
                continue
            print(*read_file(file_name))
        elif command == 'delete':
            if not exists(file_name):
                print('Файла нет. Создайте его.')
                continue
            remove_row(file_name)
        elif command == 'copy':
            if not exists(file_name):
                print('Нет файла для копирования. Сначала создайте файл.')
            else:
                copy_data(file_name)
        elif command == 'copyrow':
            if not exists(file_name):
                print('Нет файла для копирования. Сначала создайте файл.')
            else:
                copy_row(file_name)


main()
