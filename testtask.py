#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 07:16:32 2017

@author: alex
"""
import re
import pandas as pd
from dbfread import DBF

import matplotlib.pyplot as plt



base = DBF('russia.dbf') # open russian database
frame = pd.DataFrame(iter(base))
del frame['OPSNAME'] # delete unused columns
del frame['OPSTYPE']
del frame['OPSSUBM']
del frame['AREA']
del frame['CITY']
del frame['CITY_1']
del frame['ACTDATE']
del frame['INDEXOLD']





book = pd.read_excel('test.xlsx', parse_cols=[0,1,2,3]) #open test.file
book['INDEX'] = book['Адрес покупателя'].apply(lambda x: re.findall(r'\d\d\d\d\d\d',x))
#get all indexes from address
def clear(x): #clear empty
    if x != []:
        return x
    else:
        return ['000']
book['INDEX'] = book['INDEX'].apply(lambda x: clear(x)[0]) 
data = pd.merge(book, frame, left_on = 'INDEX', right_on = 'INDEX') #join by INDEX
data.loc[data["REGION"] == '','REGION'] = data["AUTONOM"] #get AO in region column
    
by_region = []
for i in sorted(set(data.REGION.values)): #separate dataframe by region
    result = data[data['REGION'] == i]
    by_region.append(result)
    
"""
Код ниже записывает данные по регионам в книгу MS excel
"""

#writer = pd.ExcelWriter('byregion.xls') # write to excel by region
#for i in range(len(by_region)):
#        by_region[i].to_excel(writer, str(by_region[i].REGION.values[1][:10]), 
#                     index=False, header=False)
#writer.save()



'''
PLOTS
'''
def min_max_orders_plot(by_region, less,more):
    '''
    Builds a hystogram of orders by region.
    less = less than quantity of orders
    more = more than quantity of orders
    '''
    quant_orders_by_region = {by_region[i].REGION.values[0]:len(by_region[i]) for i in range(len(by_region))
                           if len(by_region[i]) < less 
                           and len(by_region[i]) > more} 
    plt.bar(range(len(quant_orders_by_region)), quant_orders_by_region.values(), align='center')
    plt.xticks(range(len(quant_orders_by_region)), quant_orders_by_region.keys(), rotation=90)
    plt.title('Заказов на регион')


#min_max_orders_plot(by_region,1000,150) # График 1
#min_max_orders_plot(by_region,20,0) # График 2

"""
Больше всего заказов в Краснодарском крае(более 400), далее МО и Москва(по ~300)
Меньше всего заказов в Чукотском АО(1), Чеченская республика(3-4), Севастополь(5). 
(График 1, График 2)
"""



'''
$ of orders by category in region
'''
#by_region[14].groupby(['Категория товара']).sum().plot.bar(title=by_region[14].REGION.values[0])
#График 3
"""
В дагестане больше всего потратили на Обувь(График 3)
"""

'''
Money spent by region
'''

def min_max_spent_plot(by_region, less, more):
    '''
    Builds a hystogram of money spent by region.
    less = less than $ spent
    more = more than $ spent
    '''
    quant_orders_by_region = {by_region[i].REGION.values[0]: by_region[i]['Сумма заказа, $'].sum() for i in range(len(by_region))
                           if by_region[i]['Сумма заказа, $'].sum() < less 
                           and by_region[i]['Сумма заказа, $'].sum() > more} 
    plt.bar(range(len(quant_orders_by_region)), quant_orders_by_region.values(), align='center')
    plt.xticks(range(len(quant_orders_by_region)), quant_orders_by_region.keys(), rotation=90)
    plt.title('Потрачено $ в регионе')


#min_max_spent_plot(by_region,100,0) #График 4
#min_max_spent_plot(by_region,10000,1000) # График 5
"""
Больше всего денег потрачено в Краснодаре, МО и Москве
(2700, 2500, 2100) Соответственно.(График 5)
"""

def average_spent(by_region, less, more):
    '''
    Builds a hystogram of average spent by region.
    less = less than $ spent
    more = more than $ spent
    '''
    quant_orders_by_region = {
            by_region[i].REGION.values[0]: by_region[i]['Сумма заказа, $'].sum()/len(by_region[i])
                           for i in range(len(by_region))
                           if by_region[i]['Сумма заказа, $'].sum() < less 
                           and by_region[i]['Сумма заказа, $'].sum() > more} 
    plt.bar(range(len(quant_orders_by_region)), quant_orders_by_region.values(), align='center')
    plt.xticks(range(len(quant_orders_by_region)), quant_orders_by_region.keys(), rotation=90)
    plt.title('Средний чек $ в регионе')

#average_spent(by_region,10000,370) #График 6
#average_spent(by_region,200,0)  #График 7
"""
Самый большой средний чек в Ленинградской области из ТОПА по кол-ву заказов.(График 6)
Из регионом с маленьким количеством заказов, средний чек самый большой в 
Ингушетии и Чукотском АО. Больше чем у Ленинградской, больше 12 $ за покупку.(График 7)
"""


def cat_byregion_plot(by_region, less, more, cat):
    '''
    Builds a hystogram of category orders by region.
    less = less than $ spent
    more = more than $ spent
    cat = category
    '''
    quant_orders_by_region = {by_region[i].REGION.values[0]: by_region[i].groupby(['Категория товара']).sum().loc[cat][0]
                           for i in range(len(by_region))
                           if cat in list(by_region[i].groupby(['Категория товара']).sum().index)
                           and by_region[i].groupby(['Категория товара']).sum().loc[cat][0] < less 
                           and by_region[i].groupby(['Категория товара']).sum().loc[cat][0] > more} 
    plt.bar(range(len(quant_orders_by_region)), quant_orders_by_region.values(), align='center')
    plt.xticks(range(len(quant_orders_by_region)), quant_orders_by_region.keys(), rotation=90)
    plt.title('Потрачено $ на ' + cat)


#cat_byregion_plot(by_region,1000,150, 'Платья') #График 8
"""
Больше всего потрачено на платья в МО(~790$), Краснодарский край(~750$),
Москва(~520$)(График 8)
"""
#cat_byregion_plot(by_region,10000,50, 'Сумки и кошельки') #График 9
"""
Больше всего потрачено на Сумки и кошельки в Москве(~170$), МО(~150$),
Ростовская область(~145$)(График 9)
"""
#cat_byregion_plot(by_region,10000,50, 'Аксессуары')
#cat_byregion_plot(by_region,10000,50, 'Для детей')
#cat_byregion_plot(by_region,10000,50, 'Часы')
#cat_byregion_plot(by_region,10000,50, 'Верх')


#cat_byregion_plot(by_region,10000,50, 'Низ') #График 10
"""
Больше всего потрачено на категорию Низ в СПб(~250$) и МО(~240$)(График 10)
"""
#cat_byregion_plot(by_region,10000,50, 'Красота')
#cat_byregion_plot(by_region,10000,50, 'Бельё и купальники') #График 11
"""
На категорию белье и купальники больше всего потрачено в Краснодарском крае(400$),
из за наличия моря в крае,(График 11)
далее МО(200$) и Москва(140$) и Нижегородская область(140$). 
"""

#cat_byregion_plot(by_region,10000,20, 'Для телефона')
#cat_byregion_plot(by_region,10000,50, 'Для мужчин')  #График 12
"""
Категория Ддя мужчин продается больше всего в Свердловской области (110$),
Воронежской области(90$), и Ростовской области(50$)(График 12)
"""
#cat_byregion_plot(by_region,10000,50, 'Электроника') (#График 13)
"""
Потрачено на электронику МО(115), Москва(110), Волгоградская область(85).
(График 13)
"""



data['Дата покупки'] = pd.to_datetime(data['Дата покупки'])
data['Дата покупки'] = data['Дата покупки'].apply(lambda x: x.date())

#print(data.groupby(['Дата покупки']).size()) #таблица покупок
#data.groupby(['Дата покупки']).size().plot(rot=25)#график 14
"""
Покупок в день по России.
Из графика 14 видно, что в июле было больше заказов чем в июне.
Самое большее число заказов 15 июля.(Таблица покупок) Видимо день зарплаты у покупателей.
Больше заказов сделано во второй половине месяца, нежели в первой.
"""

#data['Дата покупки'] = data['Дата покупки'].apply(lambda x: x.time())
#data['Дата покупки'] = data['Дата покупки'].apply(lambda x: x.hour)
#print(data.groupby(['Дата покупки']).size())

#data.groupby(['Дата покупки']).size().plot(rot=25,xticks=(range(0,24))) #График 15
"""
Больше всего заказов между 7-9 утра, что видно из графика 15.
Значительно снижается число заказов после 8 вечера.
"""


#by_region[31]['Дата покупки'] = pd.to_datetime(by_region[31]['Дата покупки'])
#by_region[31]['Дата покупки'] = by_region[31]['Дата покупки'].apply(lambda x: x.date())

#print(by_region[31].groupby(['Дата покупки']).size()) #кол-во продаж по дням Краснодар
#by_region[31].groupby(['Дата покупки']).size().plot(rot=25)#график продаж по дням


"""
В Краснодаре больше всего заказов сделано 6-7 июля. 13 июля на третьем месте.
В июня так же меньше заказов чем в июле.
"""
#by_region[41]['Дата покупки'] = pd.to_datetime(by_region[41]['Дата покупки'])
#by_region[41]['Дата покупки'] = by_region[41]['Дата покупки'].apply(lambda x: x.date())
#print(by_region[41].groupby(['Дата покупки']).size()) #Табилца покупок Москва
#by_region[41].groupby(['Дата покупки']).size().plot(rot=25)
'''
В Москве больше всего заказов сделано 6 июля и 25 июня.(Таблица покупок Москва)
'''




#print(by_region[41]['Категория товара'].value_counts().plot(rot=50))
#print(by_region[41]['Категория товара'].value_counts()) #Таблица категорий Москва
"""
Больше всего в Москве купили Платьев, аксессуары на втором места, Для детей на третьем.
(Таблица категорий Москва)
"""

#print(by_region[31]['Категория товара'].value_counts()) #Таблица категорий Краснодар
#print(by_region[31]['Категория товара'].value_counts().plot(rot=50))
"""
В Краснодаре больше всего продано Платьев, Белье и купальники на втором месте,
категория верх на третьем.(Таблица категорий Краснодар)
"""

"""
Так же можно посчитать:
    Отношение кол-ва покупок в регионе к общему числу покупок
    Отношение покупок одной категории относительно другой
    В какие даты, какой категории покупали больше в регионе и России.
    и т.д.
"""
    



   