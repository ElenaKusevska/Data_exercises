#!/usr/bin/python3.6

# Based on:
# https://www.coursera.org/learn/sql-data-science/ungradedLti/uCNuW/hands-on-lab-3-analyzing-a-real-world-data-set
# https://www.dataquest.io/blog/python-pandas-databases/
# https://stackoverflow.com/questions/14431646/how-to-write-pandas-dataframe-to-sqlite-with-index
# https://stackoverflow.com/questions/2796517/navigating-cursor-rows-in-sqlite-can-we-rewind-reset-the-cursor-i-e-go-back-to
# https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

import pandas
import sqlite3
import matplotlib.pyplot as plt
import pandasql
import seaborn

# Pull CSD (Chicago Socioeconomic Data) into Pandas dataframe:
CSD = pandas.read_csv('https://data.cityofchicago.org/resource/jcxq-k9xf.csv')
print(CSD.iloc[:5])

# Establish connection to local database:
conn = sqlite3.connect('./sqlite_CSD.sqlite') # Create database
cur = conn.cursor()

# Drop table:
cur.execute('''DROP TABLE IF EXISTS CSD''')
print(cur.fetchall())

# Write pandas dataframe to sqlite3 database:
CSD.to_sql('CSD', conn, if_exists='replace', index=False)

# Verify that the table creation was succesfull:
cur.execute('select * from CSD limit 5;')
print(cur.fetchall())

# How many rows are in the dataset?
cur.execute('SELECT COUNT(*) FROM CSD;')
print(cur.fetchall())

# How many community areas in Chicago have a hardship index greater than 50.0?
cur.execute('SELECT COUNT(*) FROM CSD WHERE hardship_index > 50.0;')
print(cur.fetchall())

# What is the maximum value of hardship index in this dataset?
cur.execute('SELECT MAX(hardship_index) FROM CSD')
print(cur.fetchall())

# Which community area has the highest hardship index?

## We can use the result of the last query as an input to this query:
cur.execute('SELECT community_area_name FROM CSD where hardship_index=98.0')
print(cur.fetchall())

## or you can use a sub-query to determine the max hardship index:
cur.execute('select community_area_name from CSD where hardship_index = ( select max(hardship_index) from CSD )')
print(cur.fetchall())

# Which Chicago community areas have per-capita incomes greater than $60,000?
cur.execute('SELECT community_area_name FROM CSD WHERE per_capita_income_ > 60000;')
print(cur.fetchall())

# Get some info about database tables:

# All info
cur.execute("PRAGMA TABLE_INFO({})".format('CSD'))
print(cur.fetchall())
print(" ")

# Column names
cur.execute("PRAGMA TABLE_INFO({})".format('CSD'))
names = [tup[1] for tup in cur.fetchall()]
print(names)
print(" ")

# The SQLite interface in Python 3.1 is based on PEP 249, which only specifies
# that cursors have to support sequential access to the records of a query 
# result. An alternative option to doing an execute/fetchall is to save
# the result from the first fetchall in a variable:

# All info:
table_info = cur.execute("PRAGMA TABLE_INFO({})".format('CSD'))
names = [tup[:] for tup in table_info]
print(names)
print(" ")

# Column names:
cur.execute("PRAGMA TABLE_INFO({})".format('CSD'))
names = [tup[1] for tup in table_info]
print(names)
print(" ")


# scatterplot:
income_db = list(cur.execute('SELECT per_capita_income_ FROM CSD;'))
hardship_db = list(cur.execute('SELECT hardship_index FROM CSD;'))

income = []
hardship = []
for i in range(0,len(income_db)):
    if (income_db[i][0] is None):
        pass
    if (hardship_db[i][0] is None):
        pass
    else:
        income.append(float(income_db[i][0]))
        hardship.append(float(hardship_db[i][0]))
print(len(income), len(hardship), type(income[5]), type(hardship[5]))

plt.scatter(income, hardship, facecolors='none', edgecolors='k')
plt.show()

cur.close()
conn.close()

