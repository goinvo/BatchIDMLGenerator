#!/usr/bin/python3
import csv
import glob
import os
import shutil
import time

#Filename of IDML file (template) in the same directory including ".idml".
#change this
idml = 'my_idml_template.idml'

#Filename of the CSV file (data) in the same directory, including ".csv"
#change this
csv_file = 'my_data_file.csv'

#The search strings we are using with the key from the CSV file that we want to replace it with.
fields_to_replace = [{'search':'###First###', 'replace_key':'First Name'},
{'search':'###Last###', 'replace_key':'Last Name'},
{'search':'###Age###', 'replace_key':'Age'},
{'search':'###Zip###', 'replace_key':'Zip'},
{'search':'###Gender###', 'replace_key':'Gender'},
{'search':'###Study###', 'replace_key':'Study'},
{'search':'###City###', 'replace_key':'City'},
{'search':'###State###', 'replace_key':'State'},
{'search':'###Street###', 'replace_key':'Street'}]

#Unzip the IDML file and save it locally
template = 'template/'
shutil.unpack_archive(idml,template, 'zip')

tld = 'output'+str(int(time.time()))+'/'

#open the CSV file
with open(csv_file, 'rt') as csvfile:
	#construct our reader for the CSV file
	reader = csv.reader(csvfile, delimiter=',')
	#read the header line
	header = next(reader)

	for row in reader:
		#For each row in our CSV
		#Grab a few variables
		fname = row[header.index('First Name')]
		lname = row[header.index('Last Name')]
		study = row[header.index('Study')]
		zipcode = row[header.index('Zip')]
		age = row[header.index('Age')]
		#make our filename
		filename = 'the_resilience_project_report_'+study+'_'+fname+'_'+lname+'_'+zipcode+'_'+age+''
		#print it out to the console
		print(filename)

		#Make a copy of our template
		shutil.copytree(template,'tmp/')

		stories = os.listdir(template+'Stories')
		#for each file that we want to modify
		for entry in stories:
			#open a new file that we will write to
			with open('tmp.tmp', "wt") as fout:
				#open the file that we want to read from
				with open(template+'Stories/'+entry, "rt") as fin:
					#on every line
					for line in fin:
						line2 = line
						#for every thing we want to search for
						for rep in fields_to_replace:
							#see if this line has anything to replace and replace it with data from our CSV file
							line2 = line2.replace(rep['search'], row[header.index(rep['replace_key'])])
						#write this line
						fout.write(line2)
			#move the file to where it should be
			shutil.move('tmp.tmp', 'tmp/'+'Stories/'+entry)

		#make a .zip of the folder
		shutil.make_archive(tld+filename, 'zip', 'tmp/')
		#change the name to .idml
		shutil.move(tld+filename+'.zip', tld+'/'+filename+'.idml')
		#delete the folder we were working in
		shutil.rmtree('tmp/')

#delete our unzipped IDML directory
shutil.rmtree(template)

