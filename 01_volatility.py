# -*- coding: utf-8 -*-
import os
from decorator import time_track


class Volatility:
    """
    Программа для подсчета волатильности на основе входных данных
    """
    def __init__(self, file_name, dir_name):
        """
        :param file_name: имя файла
        :param dir_name: имя директории
        """
        self.file_name = file_name
        self.dir_name = dir_name
        self.volatility, self.max_price, self.min_price = 0, 0, 0

    def run(self):
        """
        Запуск программы
        :return: None
        """
        self.max_price, self.min_price = 0, 0
        full_file_path = os.path.join(self.dir_name, self.file_name)
        with open(file=full_file_path, mode='r', encoding='cp1251') as data:
            file_content = data.read().split('\n')
            for line in file_content:
                if line != '':
                    price = line.split(',')[2]
                    if price != 'PRICE':
                        price = float(price)
                        if self.max_price != 0 and self.min_price != 0:
                            if price > self.max_price:
                                self.max_price = price
                            elif price < self.min_price:
                                self.min_price = price
                        else:
                            self.max_price, self.min_price = price, price
        half_sum = (self.max_price + self.min_price) / 2
        self.volatility = round(((self.max_price - self.min_price) / half_sum) * 100, 2)


@time_track
def main():
    """
    Вывод трех тикеров с максимальной и трех с минимальной волатильностью
    Вывод нулевой волатильности
    :return: None
    """
    dir = r'trades'
    files = os.listdir(dir)
    volatilities = [Volatility(file_name=file_name, dir_name=dir) for file_name in files]
    result = {}
    for volatility in volatilities:
        volatility.run()
        result[volatility.file_name] = volatility.volatility
    print('Максимальная волатильность:')
    counter = 0
    number_of_max_and_min_volatility = 3
    for num_max in sorted(result.items(), key=lambda x: x[1], reverse=True):
        if counter == number_of_max_and_min_volatility:
            break
        print(' ' * 4, num_max[0].split('.')[0], '-', num_max[1], '%')
        counter += 1

    print('Минимальная волатильность:')
    counter = 0
    for num_min in sorted(result.items(), key=lambda x: x[1]):
        if num_min[1] != 0:
            if counter == number_of_max_and_min_volatility:
                break
            print(' ' * 4, num_min[0].split('.')[0], '-', num_min[1], '%')
            counter += 1

    print('Нулевая волатильность:')
    list_of_zero_volatility = []
    for i in sorted(result.items(), key=lambda x: x[0]):
        if i[1] == 0:
            list_of_zero_volatility.append(i[0].split('.')[0])
    print(' ' * 4, ', '.join(list_of_zero_volatility))


if __name__ == '__main__':
    main()