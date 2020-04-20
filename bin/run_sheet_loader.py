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
import os
import time
import pickle

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

# set the src path
sys.path.insert(0, '.')

import src.patient_data_handler as pdh
import src.helper_functions as hf

# load the configuration
with open("config_enviroment.yaml", "r") as f:
	c_e = yaml.load(f, Loader=yaml.FullLoader)

# infinite loop
while 1:
	
	# make sure the path exists for the sheets
	hf.check_path(c_e["path_sheet_data"], create_if_not_exist=True)
	
	try:
		
		# use creds to create a client to interact with the Google Drive API
		google_url = 'https://www.googleapis.com/auth/drive'
		creds = ServiceAccountCredentials.from_json_keyfile_name(c_e["filename_google_creds"],
																 google_url)
		service = discovery.build('drive', 'v3', credentials=creds)
		
		# Call the Drive v3 API
		results = service.files().list(pageSize=10,
		                               fields="nextPageToken, files(name, mimeType)").execute()
		items = results.get('files', [])
		sheet_names = [el["name"] for el in items if "spreadsheet" in el["mimeType"]]
		
	except Exception as e:
		print("failed to load sheet names with error:\n%s" % str(e))
		sheet_names = []
	
	print("got sheet names: %s" % str(sheet_names))
	
	time.sleep(2.0)
	
	# process the sheets
	for sheet_name in sheet_names:
		try:
			
			# load some sheet data
			sheet_data = pdh.load_data(c_e["filename_google_creds"], sheet_name, t_sleep=2.0)
			
			# write the sheet data
			with open("%s/%s.pkl" % (c_e["path_sheet_data"], sheet_name), "wb") as f:
				f.write(pickle.dumps(sheet_data))
			
		except Exception as e:
			print("failed to process sheet %s with error:\n%s" % (sheet_name, str(e)))
		
		time.sleep(2.0)
	
	time.sleep(5.0)

