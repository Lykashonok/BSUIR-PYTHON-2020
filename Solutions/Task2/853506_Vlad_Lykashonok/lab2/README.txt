Description
===========

Вторая лаборорная по питону. Гр 853506, Лукашёнок Владислав.

Использовал Linux mint, код писал в visual studio code, запуская всё вручную, т.е. для адекватной работы никаких ide не нужно
Установку лабы как пакета делал по https://klen.github.io/create-python-packages.html

Каждое задание - пакет внутри лабы: externalSortByVlad, memoizationByVlad, singletonByVlad, vectorByVlad, testModuleByVlad
Для externalSortByVlad (как и для testModuleByVlad) требуется наличие файла numbers.txt (в том месте, откуда вызываете)
Сортировку тестировал на файле в 400 мб, брал по 40 мб в буфер, всё работало

Работу каждого пакета кроме singletonByVlad можно проверить запустив модуль testModuleByVlad
Чтобы запустить вместе с coverage нужно написать:
$ coverage run (путь до пакета)/testModuleByVlad/core.py && coverage report

Работу singletonByVlad можно проверить либо вызвав функцию checkWork() прямиком из файла,
А можно через команду checkSingleton с помощью виртуального окружения с установленным пакетом 
(некоторые команды нужно запускать с правами администратора):
$ virtualenv env
$ ./env/bin/python setup.py install
$ source ./env/bin/activate
(env)
$ checkSingleton

Также можно создать файл.py в другом месте и импортить и проверять пакеты вручную, у меня всё импортилось и запускалось
