import pandas as pd
import os
import csv
import glob
import PySimpleGUI as sg

def main():
    df, FBA_name = import_templates()

    # Initialize dataframes for sorting and boxing
    sorting_df = df.copy()
    sorting_df['Difference'], sorting_df['Sorted'] = [sorting_df['OnOrder'], 0]
    boxing_df = df.copy()
    boxing_df['Difference'], boxing_df['Boxed'] = [boxing_df['OnOrder'], 0]

    sorted_items = []
    sorted_NOO = []
    sort_layout = [[sg.Text(FBA_name)],
        [sg.Input(key='-IN-', do_not_clear=False)],
        [sg.Listbox(values=sorted_items, size=(43,20), key='-LIST-')],
        [sg.Button('Exit')]]


    window = sg.Window('Sorting App', sort_layout, finalize=True)
    window['-IN-'].bind('<Return>', '_Enter')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-IN-' + '_Enter':
            user_input = values['-IN-']
            out_string = sort(user_input, sorting_df)
            sorted_items.append(out_string)
            window['-LIST-'].update(values=sorted_items)

    window.close()


# TODO: Sorting
# count of items on order
# free-text box, event = enter

# TODO: Add functionality for when the sorting app is opened
# Current FBA orders created by refresh files
# format of OpenFile and OpenBox file and when  they are created?
# format of temp files

def import_templates():
    # Read all of the files in FBA templates folder
    path = os.path.dirname(os.path.realpath(__file__))
    Inpath = path + '\\FBA Templates'
    all_files = glob.glob(os.path.join(Inpath, '*.tsv'))

    df = pd.DataFrame()
    for file in all_files:
        with open(file, "r") as f:
            # Extract Shipment ID and FBA name from the tsv header
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) and row[0] == 'Shipment ID':
                    ShippingId = row[1]
                elif len(row) and row[0] =='Name':
                    sep = '-'
                    FBA_name = row[1].split(sep, 1)[0]
                    break
            # Read tsv file into dataframe after header
            template = pd.read_table(f, delimiter='\t', header=4)
            template.insert(10,'ShippingID', ShippingId)
            df = pd.concat([df,template])
    df = df.rename(columns={'Shipped':'OnOrder'})
    df['external-id '] = df['external-id '].map(lambda u: u.lstrip('UPC: '))
    df = df.reset_index(drop=True)
    return df, FBA_name

def sort(user_input, sorting_df):
    # If query returns dataframe
    idx_list = sorting_df.index[(sorting_df['external-id '] == user_input) & (sorting_df['Difference'] > 0)].tolist()
    if idx_list:
        idx = idx_list[0]
        sorting_df.loc[idx,'Sorted'] = sorting_df.loc[idx,'Sorted'] + 1
        sorting_df.loc[idx,'Difference'] -= sorting_df.loc[idx,'Difference']
        SKU = sorting_df.loc[idx,'Merchant SKU']
        Location = sorting_df.loc[idx, 'ShippingID']
        out_string = SKU + ' ' + user_input + ' ' + Location
    else:
        out_string = 'Not on order' + ' ' + user_input
    return out_string
    
main()