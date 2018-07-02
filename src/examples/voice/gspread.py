import gspread
from oauth2client.service_account import ServiceAccountCredentials

SECRETS_FILE="../../../secrets/1-button-cardbox-78c4daa3a219.json"
SPREADSHEET_NAME="Baby Elsa"

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, scope)
gc = gspread.authorize(credentials)
a= gc.open(SPREADSHEET_NAME)
print(a)