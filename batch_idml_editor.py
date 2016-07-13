#!/usr/bin/python3
import csv
import glob
import os
import shutil
import time
import codecs

#Path and Filename of IDML file (template), including ".idml".
#change this
idml = 'example/business_cards_template.idml'

#Path and Filename of the CSV file (data), including ".csv"
#change this
csv_file = 'example/my_data_file.csv'

#Separator for fields in the CSV file (in case you want a 'tab', just change to '\t')
#change this
separator=','

#The search strings we are using with the key from the CSV file that we want to replace it with.
fields_to_replace = [
	{'search':'###first###', 'replace_key':'First Name'},
	{'search':'###last###', 'replace_key':'Last Name'},
	{'search':'###title###', 'replace_key':'Title'},
	{'search':'###email###', 'replace_key':'E-mail'}
]

output_filename_template = '###first###-###last###-card'

#Unzip the IDML file and save it locally

template = 'template/'
shutil.unpack_archive(idml,template, 'zip')

tld = 'output'+str(int(time.time()))+'/'

print('Saving to '+tld+'...')

#open the CSV file
with codecs.open(csv_file, 'r', encoding='utf-8-sig') as csvfile:
    #construct our reader for the CSV file
    reader = csv.reader(csvfile, delimiter=separator)
    #read the header line
    header = next(reader)

    for row in reader:
        #For each row in our CSV

        #make our filename
        filename = output_filename_template
        for rep in fields_to_replace:
                try:
                        filename = filename.replace(rep['search'], row[header.index(rep['replace_key'])])
                except ValueError:
                        print("\nPlease check that {} is encoded using 'utf-8' or try using 'utf-8-sig'".format(csv_file))
                        break
                                
        #print it out to the console
        print(filename)

        #Make a copy of our template
        try:
                shutil.copytree(template,'tmp/')
        except FileExistsError:
                        #'tmp/' may be leftover from a previous attempt, or your OS handles file deletion poorly
                        if os.path.isdir('tmp')==True:
                                dlt = input("\ntmp/ directory exists\nYou may need to re-run the program \nRemove tmp/(y/n)?").lower()
                                if dlt != 'n':
                                        shutil.rmtree('tmp/')
                                else:
                                        print("\nPlease manually remove 'tmp/' and try again")
                                        break

        stories = os.listdir(template+'Stories')
        #for each file that we want to modify
        for entry in stories:
            #open a new file that we will write to
            try: 
                with codecs.open('tmp.tmp', "w", encoding='utf-8') as fout:
                    #open the file that we want to read from
                    with codecs.open(template+'Stories/'+entry, "r", encoding='utf-8') as fin:
                        #on every line
                        for line in fin:
                            line2 = line
                            #for every thing we want to search for
                        
                            for rep in fields_to_replace:
                                #see if this line has anything to replace and replace it with data from our CSV file
                                line2 = line2.replace(rep['search'], row[header.index(rep['replace_key'])])
                            #write this line
                            fout.write(line2)
            except PermissionError:
                break

        
            shutil.move('tmp.tmp', 'tmp/'+'Stories/'+entry)
        
        
        #make a .zip of the folder
        shutil.make_archive(tld+filename, 'zip', 'tmp/')
        #change the name to .idml
        shutil.move(tld+filename+'.zip', tld+'/'+filename+'.idml')
        #delete the folder we were working in
        shutil.rmtree('tmp/')
        


#delete our unzipped IDML directory
shutil.rmtree(template)

