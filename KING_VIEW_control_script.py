import os
import paramiko
import pickle
import sys
import time


print("""

******************************ПРОГРАММА ДЛЯ НАСТРОЙКИ СУФЛЕРА ЧЕРЕЗ SSH***************************

Суфлер получает комманды через SSH, соответсвенно SSH должен быть настроен на суфлере,
При первом запуске нужно будет указать путь до папки назначения и данные для логина по SSH.
Программа запомнит данные и при повторном запуске не потребует эти данные снова. 
Чтобы запросить данные повторно удалите файлы "DestinationPATH.data и TPSavedAuth.data"

""")

Destination_path_data = 'DestinationPATH.data'

if not os.path.exists('DestinationPATH.data'):
    DESTINATION_PATH = input('Введите путь до папки share:   ')
    path_data_save = open(Destination_path_data, 'wb')
    pickle.dump(DESTINATION_PATH, path_data_save)
    path_data_save.close()
else:
    path_saved_data = open(Destination_path_data, 'rb')
    DESTINATION_PATH = pickle.load(path_saved_data)


# Консольный интерфейс
UI = """
1. Обновить текст
2. Отразить ОС по горизонтали
3. Перезагрузить суфлер
4. Удалить данные авторизации
5. Выход

"""


# Название файла дампа с данными авторизации
auth_data_save = 'TPSavedAuth.data'

# Если отсутсвует конфиг файла, то программа создает новый и запрашивает данные у пользователя
# если файл есть, то он использует его для логина

if not os.path.exists('TPSavedAuth.data'):

    hostname = input('Введите IP суфлера:')
    port = int(input('Введите порт: '))
    username = input('Введите Логин:  ')
    password = input('Введите пароль: ')

    AUTH_DATA=(hostname, port, username, password)

    auth_data_save = open(auth_data_save, 'wb')
    pickle.dump(AUTH_DATA, auth_data_save)
    auth_data_save.close()
else:
    saved_data = open(auth_data_save, 'rb')
    AUTH_DATA = pickle.load(saved_data)

# Подключение по SSH и открытие SFTP

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname= AUTH_DATA[0], port= AUTH_DATA[1], username=AUTH_DATA[2], password= AUTH_DATA[3])
    print('Авторизуюсь')
    sftp_client=ssh.open_sftp()

except:

    print('Сервер недоступен')
    print('Скрипт завершает работу')
    time.sleep(5)
    sys.exit()

# удалить массив в данными для авторизации
def destroy_auth():

    os.remove('TPSavedAuth.data')
    print('Данные авторизации уничтожены.')

# Перезагрузка устройства

def reboot():
    if not os.path.exists('Reboot.txt'):
        with open('Reboot.txt', 'a') as r:
            print('Reboot.txt создан')
        time.sleep(0.7)
        sftp_client.put('Reboot.txt', DESTINATION_PATH + 'Reboot.txt')

    else:
        sftp_client.put('Reboot.txt', DESTINATION_PATH + 'Reboot.txt')
        print('Суфлеру отправлен файл Reboot')

# Перевернуть ОС
def reverse():
    if not os.path.exists('Reverse.txt'):
        with open('Reverse.txt', 'a') as r:
            print('Reverse.txt created')
        sftp_client.put('Reverse.txt', DESTINATION_PATH + 'Reverse.txt')
        print('Отправлен файл Reverse.txt')
    else:
        sftp_client.put('Reverse.txt', DESTINATION_PATH + 'Reverse.txt')
        print('Отправлен файл Reverse.txt')

# отправить новую версию файла Scen.txt

def update_text():
    if not os.path.exists('Scen.txt'):
        print('Файл с текстом не найден в папке, положите файл Scen.txt в папку из которой запущен скрипт')
    else:
        sftp_client.put('Scen.txt', DESTINATION_PATH + 'Scen.txt')
        print('Scen.txt Отправлен на телепромтер')

# Запуск скрипта
def main():
    chose = ''
    while chose != '5':
        print(UI)
        chose = input('Выберите действие:  ')
        if chose == '1':
            update_text()
        if chose == '2':
            reverse()
        if chose == '3':
            reboot()
        if chose == '4':
            destroy_auth()
        elif chose == '5':
            print('Выход')
        else:
            print('Выберите пункты с 1 по 5')


if __name__ == '__main__':
    main()







sftp_client.close()
ssh.close()