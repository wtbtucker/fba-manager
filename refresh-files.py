import pandas as pd
import os
import csv
import glob
import PySimpleGUI as sg

# TODO: store NOO
def main():
    df, FBA_name = import_templates()

    # Initialize dataframes for sorting and boxing
    location_list = df['ShippingID'].unique().tolist()

    sorting_df = df.copy()
    sorting_df['Difference'], sorting_df['Sorted'] = [sorting_df['OnOrder'], 0]
    boxing_df = df.copy()
    boxing_df['Difference'], boxing_df['Boxed'] = [boxing_df['OnOrder'], 0]


    # TODO: list for listbox instead of df to list
    # TODO: change headings to what we actually use
    # TODO: list of locations in sorting_df
    header_list = ['Title', 'external-id ', 'Shipment ID', 'Location']
    sorted_items = [""]

    sort_layout = [[sg.Text(FBA_name)],
        [sg.Input(key='-IN-', do_not_clear=False)],
        [sg.Text('SKU'), sg.Text('UPC'), sg.Text('Location'), sg.Text('Location Number')],
        [sg.Table(headings=header_list,
                  values=sorted_items, 
                  alternating_row_color='lightblue',
                  auto_size_columns = True,
                  size=(50,30), key='-LIST-')],
        [sg.Button('Exit')]]


    window = sg.Window('Sorting App', sort_layout, finalize=True)
    window['-IN-'].bind('<Return>', '_Enter')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-IN-' + '_Enter':
            user_input = values['-IN-']

            # return first index where user_input matches UPC and Difference > 0
            idx_list = sorting_df.index[(sorting_df['external-id '] == user_input) & (sorting_df['Difference'] > 0)].tolist()
            if idx_list:
                idx = idx_list[0]
                # edit sorting df to reflect scanned item
                sorting_df.loc[idx,'Sorted'] = sorting_df.loc[idx,'Sorted'] + 1
                sorting_df.loc[idx,'Difference'] = sorting_df.loc[idx,'Difference'] - 1

                out_list = sorting_df.loc[[idx], ['Title', 'external-id ', 'ShippingID']].values.tolist()
                location = location_list.index(out_list[0][2]) + 1
                out_list[0].append(location)
            else:
                out_list = [['Not on order', user_input,"",""]]

            sorted_items.extend(out_list)
            window['-LIST-'].update(values=sorted_items)
            window.refresh()

    window.close()


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
    
main()