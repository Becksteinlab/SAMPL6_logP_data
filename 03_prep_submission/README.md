# Create SAMPL6 submissions

## Download data

Download the spreadsheet from
https://docs.google.com/spreadsheets/d/REMOVED
as CSV file, e.g., `SAMPL6.csv` or use
```bash
./scripts/download_data.py
```
or even simpler: use the `--download` option in the next step and let
`create_sampl6.py` do it automatically.

NOTE: The `download_data.py` script and the `--download` option
require the access key in `client_secret.json`, which has been
redacted for the public release of this repository. Furthermore,
private URLs have also been REMOVED.

See
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
for how to create read-only (script) access to a Google spread sheet
via the Google API console and create the OAuth2 client secret for a
service account.

## Run `create_sampl6.py`

Create all files with the `create_sampl6.py` script in directory `--outdir` 
```bash
./scripts/create_sampl6.py --outdir ../04_submission --download SAMPL6.csv
```

The `--download` option pulls the online spreadsheet and saves a copy
in `SAMPL6.csv`. (This requires the OAuth2 secret in
`client_secret.json` and the email address in this file needs to have
at least view access to the Google sheet.)

Add and `git commit` the changes.

## Changing file content

1. To change software versions and methods, edit the variables at the
   top of `create_sampl6.py`.
2. To change computed data, change the spreadsheet and regenerate the
   `SAMPL6.csv` file, e.g., by using `--download`. 
   
Then re-run the above procedure.   



