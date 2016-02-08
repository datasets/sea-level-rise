
import csv
import zipfile

import os
import urllib
#import dataconverters.xls
epa_src = "http://www3.epa.gov/climatechange/images/\
indicator_downloads/sea-level_fig-1.csv"

csiro_src = "http://www.cmar.csiro.au/sealevel/downloads/\
church_white_gmsl_2011_up.zip"
archive = 'archive/'
data = 'data/'


def string_between(string, before, after):
    temp = string.split(before)[1]
    temp = temp.split(after)[0]
    return temp


def process():
    urllib.urlretrieve(epa_src, 'archive/sea-level_fig-1.csv')
    urllib.urlretrieve(csiro_src, 'archive/GMSL_SG_2011_up.zip')
    with zipfile.ZipFile('archive/GMSL_SG_2011_up.zip', 'r') as z:
        z.extractall('archive/')

    ## sea-level_fig-1.scv
    infile = 'archive/sea-level_fig-1.csv'
    with open(infile, 'rb') as f:
        reader = csv.reader(f)
        l = list(reader)
    header = ['Year', 'CSIRO Adjusted Sea Level', 'Lower Error Bound',
     'Upper Error Bound', 'NOAA Adjusted Sea Level']

    writer = csv.writer(open('data/epa-sea-level.csv', 'w'), lineterminator='\n')
    writer.writerow(header)
    writer.writerows(l[7:])

    ## church_white_gmsl_2011_up
    for dirs, subdirs, files in os.walk('archive/church_white_gmsl_2011_up'):
        for infile in files:
            if ('.csv' not in infile) or ('CSIRO' not in infile):
                continue
            l = []
            f = open(os.path.join(dirs, infile), 'rb')
            reader = csv.reader(f)
            l = list(reader)
            l[0] = [fix_header(x) for x in l[0]]
            l[1:] = [[fix_year(x[0])] + [fix(a) for a in x[1:]] for x in l[1:]]
            writer = csv.writer(open('data/'+infile, 'w'), lineterminator='\n')
            writer.writerows(l)


def fix_header(string):
    string = string.replace('"', '')
    string = string.replace('(mm)', '')
    return string.strip()


def fix_year(string):
    string = string.replace('.0417', '-Jan')
    string = string.replace('.1250', '-Feb')
    string = string.replace('.2083', '-Mar')
    string = string.replace('.2917', '-Apr')
    string = string.replace('.3750', '-May')
    string = string.replace('.4583', '-Jun')
    string = string.replace('.5417', '-Jul')
    string = string.replace('.6250', '-Aug')
    string = string.replace('.7083', '-Sep')
    string = string.replace('.7917', '-Oct')
    string = string.replace('.8750', '-Nov')
    string = string.replace('.9583', '-Dec')
    string = string.replace('.5', '')

    return string.strip()


def fix(string):
    return string.strip()


if __name__ == '__main__':
    process()
