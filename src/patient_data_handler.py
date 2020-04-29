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
dt_update = 5.0 * 60.0

# load the configuration
with open("config_enviroment.yaml", "r") as f:
	c_e = yaml.load(f, Loader=yaml.FullLoader)


def load_data(filename_google_creds, sheetname, t_sleep=2.0):
	
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
		time.sleep(t_sleep)
		if worksheet != None:
			sd = worksheet.get_all_records()
			if len(sd) > 0 and all([key_timestamp in el for el in sd]):
				metric = worksheet.title
				days = [el[key_timestamp] for el in sd]
				readings = {k : [el[k] for el in sd] for k in sd[0].keys() if k != key_timestamp}
				sheet = {"metric" : metric, "days" : days, "readings" : readings}
				sheets.append(copy.deepcopy(sheet))
		i_worksheet += 1
		time.sleep(t_sleep)
	
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
				try:
					new_sheets = load_data(self.filename_google_creds,
					                       self.sheetname)
				except Exception as e:
					self.sheets = []
					print("failed to load data with exception:\n%s" % str(e))
			else:
				with open("data/example_patient_data.pkl", "rb") as f:
					new_sheets = pickle.loads(f.read())
			
			self.writing_to_sheets = True
			self.sheets = copy.deepcopy(new_sheets)
			self.writing_to_sheets = False
			
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
		return self.sheets




