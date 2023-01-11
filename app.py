import sqlite3
from cs50 import SQL
import pandas as pd
from os import listdir
from os.path import isfile, join


def main():
    # Sample file paths
    dbfile = 'fba-data.db'
    csv_file = './templates/SAMPLETEMPLATE.tsv'

    # Open a SQLite connection and create cursor
    with sqlite3.connect(dbfile) as conn:
        
        # Create cursor for sqlite queries
        cursor = conn.cursor()

        # Open template file from csv into pandas dataframe
        data_df = open_template(csv_file)

        # Create SQLite table 'template'
        def create_table(schema, name):
            return f'CREATE TABLE IF NOT EXISTS {name}({schema});'

        # Create list of files in templates folder
        template_list = [f for f in listdir('./templates') if isfile(join('./templates', f))]
        print(template_list)

        # Iterate over the files in templates folder

        # Insert a shipment into the shipments table for each template

        shipment_schema = '''
            id INTEGER PRIMARY KEY AUTOINCREMENT
            shipmentid TEXT NOT NULL,
            name TEXT NOT NULL,
            shipto TEXT NOT NULL,
            type TEXT NOT NULL
        '''
        
        item_schema = '''
            ean TEXT PRIMARY KEY AUTOINCREMENT,
            merchantsku TEXT NOT NULL,
            title TEXT NOT NULL,
            asin TEXT NOT NULL,
            ean TEXT NOT NULL,
            whoprep TEXT NOT NULL,
            preptype TEXT NOT NULL,
            label TEXT NOT NULL
        '''

        order_item_schema = '''
            id INTEGER PRIMARY KEY AUTOINCREMENT
            orderid INTEGER NOT NULL,
            item TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (item) REFERENCES items (ean),
            FOREIGN KEY (orderid) REFERENCES shipments (id)
        '''

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