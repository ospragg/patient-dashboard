import pprint
import datetime
import gspread
import pickle
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
		raw_sheets = client.open(self.sheetname)
		
		# make a list of worksheets
		i_worksheet = 0
		self.sheets = []
		while raw_sheets.get_worksheet(i_worksheet) != None:
			try:
				worksheet = raw_sheets.get_worksheet(i_worksheet)
				sd = worksheet.get_all_records()
				metric = worksheet.title
				days = [el[key_timestamp] for el in sd]
				readings = {k : [el[k] for el in sd] for k in sd[0].keys() if k != key_timestamp}
				if metric not in set([el["metric"] for el in self.sheets]):
					self.sheets.append({"metric" : metric,
					                   "days" : days,
					                   "readings" : readings})
			except:
				pass
			i_worksheet += 1
		