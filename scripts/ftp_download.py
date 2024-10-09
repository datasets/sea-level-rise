"""
    This script downloads the latest release of the CSIRO sea level data from the FTP server and loads into the archive/ folder.
"""

import os
import ftplib


# Define the FTP server address and directory
ftp_server = 'ftp.csiro.au'
ftp_directory = '/legresy/gmsl_files/'

def process():
    print('Downloading files from the FTP server...')
    # Connect to the FTP server
    ftp = ftplib.FTP(ftp_server)
    ftp.login()  # Assuming anonymous login (no credentials needed)
    ftp.cwd(ftp_directory)

    # List files in the directory
    files = ftp.nlst()  # This lists all the files in the directory
    latest_file = ''
    print('Processing files...')
    # Print the available files
    for file in files:
        if file.endswith('.csv') and ('yr' in file or 'yearly' in file or 'seas' in file):
            local_filename = os.path.join(os.getcwd(), 'archive/' + file)
            # Check for the latest release of the CSIRO data
            if 'csiro_recons' in file.lower() and not latest_file:
                latest_file = file
            elif 'csiro_recons' in file.lower() and latest_file:
                if file > latest_file:
                    latest_file = file
            else:
                with open(local_filename, 'wb') as local_file:
                    ftp.retrbinary(f"RETR {file}", local_file.write)

    with open(os.path.join(os.getcwd(),'archive/' + latest_file), 'wb') as local_file:
        ftp.retrbinary(f"RETR {latest_file}", local_file.write)
    with open(os.path.join(os.getcwd(),'archive/' + 'church_white_gmsl_2011_tg_list.zip'), 'wb') as local_file:
        ftp.retrbinary(f"RETR {latest_file}", local_file.write)
    print('Files downloaded successfully.')

if __name__ == '__main__':
    process()
