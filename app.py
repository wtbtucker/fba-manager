import sqlite3
import csv
import pandas as pd


def main():
    # Sample file paths
    dbfile = 'fba-data.db'
    csv_file = 'SAMPLETEMPLATE.tsv'

    # Open a SQLite connection and create cursor
    with sqlite3.connect(dbfile) as conn:
        
        # Create cursor for sqlite queries
        cursor = conn.cursor()

        # Open template file from csv into pandas dataframe
        data_df = open_template(csv_file)


        # Create SQLite table 'template'
        create_table = '''CREATE TABLE IF NOT EXISTS template(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merchantsku TEXT NOT NULL,
            title TEXT NOT NULL,
            asin TEXT NOT NULL,
            ean TEXT NOT NULL,
            whoprep TEXT NOT NULL,
            preptype TEXT NOT NULL,
            label TEXT NOT NULL,
            onorder TEXT NOT NULL);'''
        cursor.execute(create_table)

        # Insert the dataframe into the template SQL table
        data_df.to_sql('template', conn, if_exists='append')

        # Select row from table
        selection = cursor.execute('SELECT * FROM template LIMIT 2;')
        print(selection)

# Open csv file and return dataframe
def open_template(csv_file):

    # Use specified columns and rename to fit SQL schema
    data = pd.read_csv(csv_file, index_col=0, header=7, usecols=[0,1,2,4,6,7,8,9], dtype={'external-id': str}, sep='\t')
    data = data.rename(columns={
        'Title': 'title',
    	'ASIN': 'asin',
        'external-id': 'ean',
        'Who will prep?': 'whoprep',
        'Prep Type': 'preptype',
        'Who will label?': 'label',
        'Shipped': 'onorder'
    })

    # Rename column 0 to fit SQL schema
    data.index.names = ['merchantsku']
    return data


main()