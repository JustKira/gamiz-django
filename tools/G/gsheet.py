import gspread
import pandas as pd

def update_order_sheet(order_list):
    gc = gspread.service_account(filename='gaimiz-sheets-3cd9ec2cff2e.json')

    # get the instance of the Spreadsheet
    sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1yJfYWPpLAO1ZjPmRH3ob0dpwiabuMQAX2ODJv1Uxvng/edit#gid=0')
    orders_sheet = sheet.worksheet("Website Orders")
    records_data = orders_sheet.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)
    print(records_df.tail())
    records_df.loc[len(records_df)] = order_list
    orders_sheet.update([records_df.columns.values.tolist()] + records_df.values.tolist())


update_order_sheet(['test', 'test', 'test'])