import os
from django.conf import settings
import gspread
import pandas as pd
from django.core.files.base import ContentFile


def update_order_sheet(order_list):
    gc = gspread.service_account(filename=os.path.join(settings.BASE_DIR,
                                                       'adminsys/gaimiz-sheets-3cd9ec2cff2e.json'))

    # get the instance of the Spreadsheet
    sheet = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1yJfYWPpLAO1ZjPmRH3ob0dpwiabuMQAX2ODJv1Uxvng/edit#gid=0')
    orders_sheet = sheet.worksheet("Website Orders")
    records_data = orders_sheet.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)
    print(records_df.tail())
    records_df.loc[len(records_df)] = order_list
    print(records_df.tail())
    orders_sheet.update([records_df.columns.values.tolist()
                         ] + records_df.values.tolist())
