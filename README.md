# Fuzzy-Pacs

Fuzzy Matching of PACS Data with HIS/RIS Data

This project contains 2 scripts named script.py and match.py & Pynetdicom3 Module zip file

Prerequisites:
1. Python 3.+
2. Pynetdicom3,Pydicom, mysql.connector,datetime,fuzzywuzzy Module for python
3. Mysql 5.7+ server
4. Little knowledge of csv/tsv writing.
5. Active connection to PACS.

script.py: 

This script helps to get data like (PatientName, StudyInstanceUID, StudyDescription, StudyDate etc.) from your PACS between specified date range as a csv file.
1. Enter a name for the output csv file.
	file = open('example.csv','w')
2. Enter Date range in (YYYYMMDD) format.
	rangestart = 20160101
	rangeend = 20190418
Also, write date(rangeend +1 day) in this line
	while rangeend < 20190419:
3. Enter PACS details like AE-Title, IP Address & Port Number.
	assoc = ae.associate('127.0.0.1', 11112, 'AETITLE')
4. Run the script using python 3+.

After this you will get a csv file with all the data.

match.py:

This script needs both PACS data and HIS/RIS data to be stored in Mysql database seperately.
1. Enter the name for the output tsv file.
	file = open('example.tsv','w')
2. Enter the mysql database details:
	cnx = mysql.connector.connect(user='root', password='password', host='localhost', port="if-any", database='fuzzy')
3. Enter start date and end date in (YYYY,MM,DD) format
	start = date(2016, 5, 27)
	end = date(2019, 3, 9)
4. Please ensure the correct column names and table names
	query1 = ("SELECT NAME, testid, Date_Of_Registration, Department FROM his_data WHERE DATE(Date_Of_Registration) = \""
	 + str(start.year) + "-" + str(start.month).zfill(2) + "-" + str(start.day).zfill(2) + "\"")
	query2 = ("SELECT Name, Modality, StudyInstanceUID, Date, Description FROM pacs_data WHERE Date = \""
	 +str(start.year) + "-" + str(start.month).zfill(2) + "-" + str(start.day).zfill(2) + "\"")
5. Run the script using python 3+.
