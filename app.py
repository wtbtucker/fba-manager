import sqlite3
import csv
import pandas as pd


def main():
    # Sample file paths
    dbfile = 'fba-data.db'
    csv_file = 'SAMPLETEMPLATE.tsv'

    # Open a SQLite connection and create cursor
    with sqlite3.connect(dbfile) as conn:
        prepare_data(conn, csv_file)

def prepare_data(conn, csv_file):
    # Create cursor for sqlite queries
    db = conn.cursor()

    # Create sqlite table
    create_table = '''CREATE TABLE template(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        merchantsku TEXT NOT NULL,
        title TEXT NOT NULL,
        asin TEXT NOT NULL,
        upc TEXT NOT NULL,
        whoprep TEXT NOT NULL,
        preptype TEXT NOT NULL,
        label TEXT NOT NULL,
        onorder TEXT NOT NULL);'''
    db.execute(create_table)

    # Open CSV file and append data to the sqlite table
    open_template(csv_file, conn)


    

def open_template(csv_file, connection):  
    data = pd.read_csv(csv_file, index_col=0, header=7, usecols=[0,1,2,4,6,7,8,9], dtype={'external-id': str}, sep='\t')
    
    data = data.rename(columns={
        'Title': 'title',
    	'ASIN': 'asin',
        'external-id': 'upc',
        'Who will prep?': 'whoprep',
        'Prep Type': 'preptype',
        'Who will label?': 'label',
        'Shipped': 'onorder'
    })
    data.index.names = ['merchantsku']

    data.to_sql('template', connection, if_exists='append')


# SQL query to insert list of strings into SQL table
def insert_records(content):
    global db
    print(content)
    sql_args = '?, ?, ?, ?, ?, ?, ?, ?'
    records = f'INSERT INTO person VALUES ({sql_args})'
    db.execute(records, content)


main()