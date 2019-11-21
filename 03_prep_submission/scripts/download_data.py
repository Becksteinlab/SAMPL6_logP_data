#!/usr/bin/env python
# -*- coding: utf-8 -*-



# See https://towardsdatascience.com/how-to-access-google-sheet-data-using-the-python-api-and-convert-to-pandas-dataframe-5ec020564f0e and https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html


from apiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

SPREADSHEET_ID = "REMOVED"
RANGE_NAME = "Sheet1"

__doc__ = """Download spreadsheet {0} {1} as CSV.""".format(SPREADSHEET_ID, RANGE_NAME)

def get_google_sheet(spreadsheet_id, range_name, secretfile="client_secret.json"):
    """ Retrieve sheet data using OAuth credentials and Google Python API. """
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    # Setup the Sheets API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(secretfile, scope)

    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return gsheet


def gsheet2df(gsheet):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    header = gsheet.get('values', [])[0]   # Assumes first line is header!
    values = gsheet.get('values', [])[1:]  # Everything else is data.
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            try:
                # try to get numbers even with blank cells (-> NaN)
                ds = pd.to_numeric(ds)
            except ValueError:
                pass
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df

def get_SAMPL6(secretfile="client_secret.json"):
    gsheet = get_google_sheet(SPREADSHEET_ID, RANGE_NAME, secretfile=secretfile)
    return gsheet2df(gsheet)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--output", "-o",
                        metavar="FILE", type=str, default="SAMPL6.csv",
                        help="Name of the putput CSV file.")
    parser.add_argument("--secret", metavar="JSON", type=str, default="client_secret.json",
                        help="OAuth2 credentials from the Google API Console (service account; "
                        "access to the Google Sheet must must have been shared with the associated "
                        "email address cred.email.")

    args = parser.parse_args()

    df = get_SAMPL6(secretfile=args.secret)

    print('Dataframe size = ', df.shape)
    #print(df.head())

    df.to_csv(args.output, index=False)
    print("Wrote {2} from {0} {1}.""".format(SPREADSHEET_ID, RANGE_NAME, args.output))

