import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

key_timestamp = "day"

class PatientDataHandler:
	
	def __init__(self, filename_google_creds, sheetname):
		self.filename_google_creds = filename_google_creds
		self.sheetname = sheetname
	
	def load_data(self):
		
		# use creds to create a client to interact with the Google Drive API
		creds = ServiceAccountCredentials.from_json_keyfile_name(self.filename_google_creds,
		                                                         'https://www.googleapis.com/auth/drive')
		client = gspread.authorize(creds)
		sheet = client.open(self.sheetname).sheet1
		sd = sheet.get_all_records()
		
		"""
		sd = [{'datetime': '2020-01-01 09:00', 'p1': 0.1, 'p2': 0.2, 'p3': 0.4, 'p4': 0.9}, {'datetime': '2020-01-02 09:00', 'p1': 0.5, 'p2': 0.2, 'p3': 3, 'p4': 0.9}, {'datetime': '2020-01-03 09:00', 'p1': 0.2, 'p2': 0.5, 'p3': 0.9, 'p4': 0.8}, {'datetime': '2020-01-04 09:00', 'p1': 0.7, 'p2': 0.4, 'p3': 0.2, 'p4': 0.7}, {'datetime': '2020-01-05 09:00', 'p1': 0.6, 'p2': 0.12, 'p3': 0.1, 'p4': 0.6}, {'datetime': '2020-01-06 09:00', 'p1': 0.5, 'p2': 0.3, 'p3': 0.1, 'p4': 0.5}, {'datetime': '2020-01-07 09:00', 'p1': 2, 'p2': 0.2, 'p3': 0.9, 'p4': 0.4}, {'datetime': '2020-01-08 09:00', 'p1': 0.6, 'p2': 0.7, 'p3': 0.3, 'p4': 0.3}, {'datetime': '2020-01-09 09:00', 'p1': 0.3, 'p2': 0.8, 'p3': 0.4, 'p4': 0.2}, {'datetime': '2020-01-10 09:00', 'p1': 0.6, 'p2': 0.7, 'p3': 0.3, 'p4': 0.1}]
		"""
		
		# get the timestamps
		#self.datetimes = [datetime.datetime.strptime(el["datetime"], "%Y-%m-%d %H:%M") for el in sd]
		self.datetimes = [el[key_timestamp] for el in sd]
		
		# get the patient data
		self.readings = {k : [el[k] for el in sd] for k in sd[0].keys() if k != key_timestamp}
		