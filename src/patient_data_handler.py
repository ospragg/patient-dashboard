import pprint
import datetime
import gspread
import pickle
import time
from threading import Thread
import copy
from oauth2client.service_account import ServiceAccountCredentials
import yaml

key_timestamp = "day"
dt_update = 60.0

# load the configuration
with open("config_enviroment.yaml", "r") as f:
	c_e = yaml.load(f, Loader=yaml.FullLoader)


def load_data(filename_google_creds, sheetname):
	
	# use creds to create a client to interact with the Google Drive API
	google_url = 'https://www.googleapis.com/auth/drive'
	creds = ServiceAccountCredentials.from_json_keyfile_name(filename_google_creds,
	                                                         google_url)
	client = gspread.authorize(creds)
	raw_sheets = client.open(sheetname)
	
	# make a list of worksheets
	sheets = []
	worksheet = 0
	i_worksheet = 0
	while worksheet != None:
		worksheet = raw_sheets.get_worksheet(i_worksheet)
		if worksheet != None:
			sd = worksheet.get_all_records()
			metric = worksheet.title
			days = [el[key_timestamp] for el in sd]
			readings = {k : [el[k] for el in sd] for k in sd[0].keys() if k != key_timestamp}
			sheet = {"metric" : metric, "days" : days, "readings" : readings}
			sheets.append(copy.deepcopy(sheet))
		i_worksheet += 1
	
	return sheets

class PatientDataHandler:
	
	def __init__(self, filename_google_creds, sheetname):
		self.filename_google_creds = filename_google_creds
		self.sheetname = sheetname
		self.sheets = None
		self.writing_to_sheets = False
	
	def load_data(self):
		
		while 1:
			if c_e["debug"] == False:
				self.writing_to_sheets = True
				try:
					self.sheets = load_data(self.filename_google_creds,
					                        self.sheetname)
				except Exception as e:
					self.sheets = []
					print("failed to load data with exception:\n%s" % str(e))
				self.writing_to_sheets = False
			else:
				with open("data/example_patient_data.pkl", "rb") as f:
					self.sheets = pickle.loads(f.read())
			
			with open("data/example_patient_data.pkl", "wb") as f:
				f.write(pickle.dumps(self.sheets))
			
			time.sleep(dt_update)
	
	def start_load_data_deamon(self):
		process = Thread(target=self.load_data)
		process.start()
	
	def get_sheets(self):
		while self.sheets == None:
			while self.writing_to_sheets == True:
				time.sleep(0.1)
		return copy.deepcopy(self.sheets)




