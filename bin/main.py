"""
- create auth credentials here:
	- https://console.developers.google.com/
	- new project
	- name and create
	- Enable APIs and Services
	- search for google drive and enable
	- create credentials in top right
	- select google drive API
	- calling from webserver
	- accessing Application Data
	- not using API with App Engine or Compute Engine
- https://docs.google.com/spreadsheets/d/1mU6EXbxUFodzeeg9ZjbfwV6RHZ2DpyS5YZQqhJhAk14/edit#gid=0
"""

import sys
import yaml
import pprint

# set the src path
sys.path.insert(0, '.')

from src.patient_data_handler import PatientDataHandler

# load the configuration
with open("config_enviroment.yaml", "r") as f:
	c_e = yaml.load(f, Loader=yaml.FullLoader)

# set up the patient data loader
pdh = PatientDataHandler(c_e["filename_google_creds"],
                         c_e["google_sheetname"])
#pdh.load_data()
#quit()

import plotly
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
from OpenSSL import SSL

import src.pages.main_page as main_page
import src.pages.patient_details as patient_details

# set up Dash
server = Flask(__name__)
app = dash.Dash(server=server, url_base_pathname="/")
app.layout = html.Div([
	# represents the URL bar, doesn't render anything
	dcc.Location(id='url', refresh=False),
	# content will be rendered in this element
	html.Div(id='page-content')
])

# set up the parent callback
@app.callback(dash.dependencies.Output('page-content', 'children'),
			  [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
	# direct the request based on the path
	pathlist = pathname.split("/")[1:]
	if len(pathlist) == 1 and pathlist[0] == "":
		return main_page.render(pathlist, pdh)
	elif len(pathlist) == 1 and pathlist[0] != "":
		return patient_details.render(pathlist, pdh)
	else:
		return html.Div([html.H3("Error")])
	return None

# set up the server
if c_e["debug"] == True:
	server.run(debug=c_e["debug"])
else:
	ssl_details = (c_e["filename_server_cert"],
	               c_e["filename_server_key"])
	server.run(#debug=c_e["debug"],
	           debug=True,
	           host="0.0.0.0",
	           port=8080,
	           ssl_context=ssl_details)


















quit()



#from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    main()


"""
import sys

import plotly
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
from OpenSSL import SSL



sys.path.insert(0, "src")

# define the sever info
debug = True
filename_ssl_key = "data/server.key"
filename_ssl_cert = "data/server.crt"



# set up Dash
server = Flask(__name__)
app = dash.Dash(server=server, url_base_pathname="/")
app.layout = html.Div([
	# represents the URL bar, doesn't render anything
	dcc.Location(id='url', refresh=False),
	# content will be rendered in this element
	html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
			  [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
	# this is called every page load and every URL change
	# you can update your components with this URL in here
	return html.Div([
		html.H3('You are on page {}'.format(pathname))
	])









if debug == True:
	server.run(debug=True)
else:
	server.run(debug=False,
	           host="0.0.0.0",
	           port=8080,
	           ssl_context=(filename_ssl_cert, filename_ssl_key))
"""
