Batch-IDML-Generator
====================
Sometimes you want to incorporate data into your designs. This is a simple tool that lets you batch generate IDML files using data from a CSV file based on a template.

Example Usage
=============
In the `example` folder, you will find a sample IDML file for a business card. In that file, we added `###first###`, `###last###`, `###title###`, and `###email###` as fields which should be driven by data.

The `example/my_data_file.csv` file contains the names, titles, and e-mail addresses of the people we want to generate business cards for.

In `batch_idml_editor.py`, we have changed the following variables to be paths to our files
```python
#Path and Filename of IDML file (template), including ".idml".
#change this
idml = 'example/business_cards_template.idml'

#Path and Filename of the CSV file (data), including ".csv"
#change this
csv_file = 'example/my_data_file.csv'
```

We have also created a mapping of the template fields in our IDML file (`###first###`, `###last###`, etc) to the fields in our CSV file

```python
#The search strings we are using with the key from the CSV file that we want to replace it with.
fields_to_replace = [{'search':'###first###', 'replace_key':'First Name'},
{'search':'###last###', 'replace_key':'Last Name'},
{'search':'###title###', 'replace_key':'Title'},
{'search':'###email###', 'replace_key':'E-mail'}]
```

Finally, we made a template string which is the filename for each of the exported IDML files
```python
output_filename_template = '###first###-###last###-card'
```

To run this tool, open a terminal window in this directory and type:
```
python3 batch_idml_editor.py
```

The script should output:
```
Saving to output1397664993/...
Ben-Salinas-card
Eric-Benoit-card
```

Each time you run the script, a new output directory will be created. Inside that directory, you will find IDML files that should data representing each row of the CSV file.

After you have your directory of IDML files, you can use a script like the one at http://www.kahrel.plus.com/indesign/batch_convert.html to do a batch convert to PDF or other format.

Why Not InDesign DataMerge
==========================
The DataMerge feature in Adobe InDesign and Illustrator is very powerful and allows you to do basically the same thing(and more!) within the app itself. We have found that this is a great option, but has some limits on the number of rows it can process and doesn't play well with multi-page documents. It also doesn't let you create meaningful filenames for the resulting files. In particular, we built this to be able to export several hundred PDFs with custom filenames based on the content of the data.

Dependencies
============
* python3
* InDesign

Note that this has only been tested on Mac OSX. There will likely need to be a few small changes to make it work on Windows.

Contributing
============
To make changes or improvements, fork this repo. Pull requests accepted. Feel free to create issue tickets to ask questions about how it works or suggest improvements.
