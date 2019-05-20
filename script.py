from pydicom.dataset import Dataset
from pynetdicom3 import AE
from pynetdicom3 import QueryRetrieveSOPClassList

file = open('example.csv','w')
file.write('Name,Date,Modality,StudyTime,StudyInstanceUID,Description\n')

ae = AE(scu_sop_class=QueryRetrieveSOPClassList)

rangestart = 20160101
rangeend = 20190418

while rangeend < 20190419:
	print('Requesting Association with the peer')
	assoc = ae.associate('127.0.0.1', 11112, 'AETITLE')
	if assoc.is_established:
		print('Association accepted by the peer')

		dataset = Dataset()
		dataset.StudyInstanceUID = ''
		dataset.PatientName = ''
		dataset.StudyDate = str(rangestart) + '-' + str(rangeend)
		dataset.QueryRetrieveLevel = 'STUDY'
		dataset.ModalitiesInStudy = ''
		dataset.StudyDescription = ''

		responses = assoc.send_c_find(dataset, query_model='S')

		for (status, result) in responses:
			if result:
				try:
					datenum = int(str(result.StudyDate))
					date = str(int((datenum - (datenum % 10000)) / 10000)) + '-' + str(int(((datenum % 10000) - (datenum % 100)) / 100)).zfill(2) + '-' + str(datenum % 100).zfill(2)
					file.write("\""+str(result.PatientName) + "\"," + date + ",\"" + str(result.ModalitiesInStudy) + "\"," + str(result.StudyInstanceUID) +",\"" + str(result.StudyDescription) + "\"\n")
					print('.')
				except:
					print('Error')

		assoc.release()

	rangestart = rangeend
	currentmonth = int(((rangeend%10000) - (rangeend%100))/100)
	if currentmonth > 10:
		rangeend = rangeend + 9000
	else:
		rangeend = rangeend + 200
