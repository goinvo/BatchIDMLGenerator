#!/usr/bin/python3
import csv
import glob
import os
import shutil
import time

#Filename of IDML file (template) in the same directory including ".idml".
#change this
idml = 'example/business_cards_template.idml'

#Filename of the CSV file (data) in the same directory, including ".csv"
#change this
csv_file = 'example/my_data_file.csv'

#The search strings we are using with the key from the CSV file that we want to replace it with.
fields_to_replace = [{'search':'###first###', 'replace_key':'First Name'},
{'search':'###last###', 'replace_key':'Last Name'},
{'search':'###title###', 'replace_key':'Title'},
{'search':'###email###', 'replace_key':'E-mail'}]

output_filename_template = '###first###-###last###-card'

#Unzip the IDML file and save it locally
template = 'template/'
shutil.unpack_archive(idml,template, 'zip')

tld = 'output'+str(int(time.time()))+'/'

print('Saving to '+tld+'...')

#open the CSV file
with open(csv_file, 'rt') as csvfile:
	#construct our reader for the CSV file
	reader = csv.reader(csvfile, delimiter=',')
	#read the header line
	header = next(reader)

	for row in reader:
		#For each row in our CSV

		#make our filename
		filename = output_filename_template
		for rep in fields_to_replace:
			filename = filename.replace(rep['search'], row[header.index(rep['replace_key'])])
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

