import pandas as pd
import os
import csv
import glob

# Set path to current file location
path = os.path.dirname(os.path.realpath(__file__))
Inpath = path + '\\FBA Templates'
all_files = glob.glob(os.path.join(Inpath, '*.tsv'))

df = pd.DataFrame()
for file in all_files:
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if len(row) and row[0] == 'Shipment ID':
                ShippingId = row[1]
            elif len(row) and row[0] =='Name':
                sep = '-'
                FBA_name = row[1].split(sep, 1)[0]
                break
        template = pd.read_table(f, delimiter='\t', header=4)
        template.insert(10,'ShippingID', ShippingId)
        df = pd.concat([df,template])
df = df.rename(columns={'Shipped':'OnOrder'})

sorting_df = df.copy()
sorting_df['Difference'], sorting_df['Sorted'] = [sorting_df['OnOrder'], 0]

boxing_df = df.copy()
boxing_df['Difference'], boxing_df['Boxed'] = [boxing_df['OnOrder'], 0]

print(boxing_df)