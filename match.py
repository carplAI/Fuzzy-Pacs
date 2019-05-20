import mysql.connector
from datetime import datetime
from datetime import date 
from datetime import time
from datetime import timedelta
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

file = open('example.tsv','w')
file.write('ReportName	PACSName	Date	UHID	LedgerTransactionNo	Department	Modality	TestName	StudyInstanceUID	ScanDescription	LabDescription\n')
cnx = mysql.connector.connect(user='root', password='password', host='localhost', port="if-any", database='fuzzy')
cursor1 = cnx.cursor()
cursor2 = cnx.cursor()

def modalitymap(dep, mod):
	if dep == "SONOGRAPHY" or dep == "CARDIOLOGY" or dep == "DOPPLER":
		if mod == "US":
			return True
	if dep == "MRI":
		if mod == "MR":
			return True
	if dep == "CT":
		if mod == "CT":
			return True
	if dep == "PET CT":
		if mod == "PT":
			return True
	if dep == "MAMMOGRAPHY":
		if mod == "MG" or mod == "CR":
			return True
	if dep == "X-RAY":
		if mod == "CR" or mod == "DX":
			return True
	if dep == "CBCT":
		if mod == "PX DX":
			return True
	return False
start = date(2016, 5, 27)
end = date(2019, 3, 9)

while(start != end):
	reportresults = []
	imageresults = []
	query1 = ("SELECT NAME, testid, Date_Of_Registration, Department FROM his_data WHERE DATE(Date_Of_Registration) = \""
	 + str(start.year) + "-" + str(start.month).zfill(2) + "-" + str(start.day).zfill(2) + "\"")
	query2 = ("SELECT Name, Modality, StudyInstanceUID, Date, Description FROM pacs_data WHERE Date = \""
	 +str(start.year) + "-" + str(start.month).zfill(2) + "-" + str(start.day).zfill(2) + "\"")
	cursor1.execute(query1)
	for (NAME, TEST_ID, Date_Of_Registration, Department) in cursor1: 
		reportrow = {
			"name": NAME,
			"uhid": TEST_ID,
			"date": Date_Of_Registration,
			"dep": Department
		}
		reportresults.append(reportrow)

	cursor2.execute(query2)
	for (Name, Modality, StudyInstanceUID, Date, Description) in cursor2: 
		imagerow = {
			"name": Name,
			"mdl": Modality,
			"siuid": StudyInstanceUID,
			"date": Date, 
			"desc": Description
		}
		imageresults.append(imagerow)

	for(reportrow) in reportresults:
		for(imagerow) in imageresults:
			try:	
				if fuzz.token_set_ratio(str(reportrow["name"]), str(imagerow["name"])) > 95 and modalitymap(reportrow["dep"], imagerow["mdl"]):
					file.write("{}	{}	{}-{}-{}	{}	{}	{}	{}	{} \n".format(reportrow["name"], imagerow["name"],
					 reportrow["date"].year, reportrow["date"].month, reportrow["date"].day, reportrow["uhid"], reportrow["dep"],
					 imagerow["mdl"], imagerow["siuid"], imagerow["desc"].strip())) 
					print('.')
			except:
				print('Error')
	print(start)

	start += timedelta(days=1)
