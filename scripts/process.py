"""
    This script processes the archive folder and puts processed data to data/ folder.
    Note:
    1. Currently, the FTP server doesn't produce the data for the CSIRO_Recons_gmsl_mo_{year}.csv file, it only produces
       yearly data. So, in order to not mess the process of the data, old data from CHURCH/WHITE source for 2015 monthly is used.
"""
import os
import csv
import zipfile
import requests

csiro_src = "http://www.cmar.csiro.au/sealevel/downloads/\
church_white_gmsl_2011_up.zip"
archive = 'archive/'
data = 'data/'


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def process():
    print('Downloading files from the old source data...')
    zip_file_path = os.path.join('archive', 'GMSL_SG_2011_up.zip')
    response = requests.get(csiro_src)
    with open(zip_file_path, 'wb') as f:
        f.write(response.content)

    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        z.extractall(archive)

    print('Zip files downloaded successfully.')
    ## church_white_gmsl_2011_up
    print('Processing files from zip file...')
    for dirs, subdirs, files in os.walk(archive + 'church_white_gmsl_2011_up'):
        for infile in files:
            if 'csiro_recons_gmsl_mo_2015.csv' not in infile.lower():
                continue
            l = []
            with open(os.path.join(dirs, infile), 'r', newline='') as f:
                reader = csv.reader(f)
                l = list(reader)
            l[0] = [fix_header(x) for x in l[0]]
            l[1:] = [[fix_year(x[0])] + [fix(a) for a in x[1:]] for x in l[1:]]
            writer = csv.writer(open(data+infile, 'w'), lineterminator='\n')
            writer.writerows(l)
    print('Processing files from the sea-level data...')
    for file in os.listdir(archive):
        if '.csv' in file and 'sea-level' not in file.lower():
            l = []
            path_to_read = os.path.join(os.getcwd(), archive + file)
            with open(path_to_read, 'r', newline='') as f:
                reader = csv.reader(f)
                l = list(reader)
            l[0] = [fix_header(x) for x in l[0]]
            l[1:] = [[fix_year(x[0])] + [fix(a) for a in x[1:]] for x in l[1:]]
            path_to_write = os.path.join(os.getcwd(), data + file)
            writer = csv.writer(open(data+file, 'w'), lineterminator='\n')
            #print(path_to_write)
            writer.writerows(l)
    print('Files processed successfully.')

def fix_header(string):
    string = string.replace('"', '')
    string = string.replace('(mm)', '')
    return string.strip()


def fix_year(string):
    string = string.replace('.0417', '-Jan')
    string = string.replace('.042', '-Jan')
    string = string.replace('.1250', '-Feb')
    string = string.replace('.125', '-Feb')
    string = string.replace('.2083', '-Mar')
    string = string.replace('.208', '-Mar')
    string = string.replace('.2917', '-Apr')
    string = string.replace('.292', '-Apr')
    string = string.replace('.3750', '-May')
    string = string.replace('.375', '-May')
    string = string.replace('.4583', '-Jun')
    string = string.replace('.458', '-Jun')
    string = string.replace('.5417', '-Jul')
    string = string.replace('.542', '-Jul')
    if len(string) > 4 and string[4:] == '42':
        string = string[:4] + '-Jul'
    string = string.replace('.6250', '-Aug')
    string = string.replace('.625', '-Aug')
    string = string.replace('.7083', '-Sep')
    string = string.replace('.708', '-Sep')
    string = string.replace('.7917', '-Oct')
    string = string.replace('.792', '-Oct')
    string = string.replace('.8750', '-Nov')
    string = string.replace('.875', '-Nov')
    string = string.replace('.9583', '-Dec')
    string = string.replace('.958', '-Dec')
    string = string.replace('.500', '')
    string = string.replace('.5', '')

    return string.strip()


def fix(string):
    return string.strip()


if __name__ == '__main__':
    process()