
# importing required modules
from zipfile import ZipFile

# specifying the zip file name
user_input_zip = input("Enter/Paste filepath:")
file_name = user_input_zip

# opening the zip file in READ mode
with ZipFile(file_name, 'r') as zip:
	# printing all the contents of the zip file
	zip.printdir()

	# extracting all the files
	print('Extracting all the files now...')
	#zip.extractall()
	print('Done!')
