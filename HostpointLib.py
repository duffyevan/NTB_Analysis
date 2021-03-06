from datetime import datetime, date, timedelta
import logging
import posixpath
from ftplib import FTP
import os


class HostpointClient:

    ## The Constructor
    # @param hostname {string} hostname of the HostPoint ftp server
    # @param username {string} username for the HostPoint ftp server
    # @param password {string} password for said user
    def __init__(self, hostname, username, password):
        self.client = FTP(hostname)
        self.client.login(username, password)
        logging.info("Logged into HostPoint")

    ## Upload a single file from the local storage to the FTP server
    # @param filename {string} Path to the file on the local storage to upload
    def upload_file(self, filename):
        logging.info("Uploading " + filename)
        file = open(filename, 'rb')
        self.client.storbinary('STOR %s' % posixpath.basename(filename), file)
        file.close()

    ## Downloads a single file
    # @param remote_file The path on the remote server to the file
    # @param download_location The path to the folder where the file should be put
    # @returns The path to the newly downloaded local file
    def download_file(self, remote_filename, download_location='./'):
        logging.info("Downloading %s to %s" % (remote_filename, download_location))
        if not posixpath.exists(download_location) or not posixpath.isdir(download_location):
            os.makedirs(download_location)
        file = open(posixpath.join(download_location,posixpath.basename(remote_filename)), 'wb')
        self.client.retrbinary('RETR %s' % remote_filename, file.write)
        file.close()
        return posixpath.join(download_location,posixpath.basename(remote_filename))

    ## Downloads a list of files
    # @param files The list of files to be downloaded
    # @param download_location The path to where the files should be placed
    # @returns A list of the paths to the local files just downloaded
    def download_files(self, files, download_location='./'):
        local_files = []
        for file in files:
            local_files.append(self.download_file(file, download_location))
        return local_files

    ## As the name suggests
    # @param name The name of the PLC in F00x Format
    # @param date The datetime.date for the day to get the files for
    # @param download_location String representing the folder to put the downloaded files in
    # @returns A list of local files
    def download_files_for_plc_and_day(self, name, date, download_location='./'):
        local_files = []
        for file in self.list_files():
            data = self.__name_to_plc_and_date(file)
            if data[1].__eq__(date) and data[0] == int(name.replace('F','')):
                local_files.append(self.download_file(file, download_location))
        return local_files

    ## Upload a list of files from the local storage to the FTP server
    # @param filelist {list[string]} A list of paths to files on the local storage
    def upload_files(self, filelist):
        for file in filelist:
            self.upload_file(file)

    ## Upload all the files in a given directory on the local storage to the FTP server
    # @param directory {string} Path to the directory on the local storage

    def upload_all_files_in_directory(self, directory):
        self.upload_files([posixpath.join(directory, file) for file in os.listdir(directory)])


    ## Close the connection with HostPoint server
    def close(self):
        logging.info("Closing connection to HostPoint")
        self.client.close()

    def ls(self):
        return self.client.nlst()

    ## Get the PLCs that reported in on a given day based on the files posesed in the cache
    # @param day The datetime.date that should be checked
    # @returns A set of PLC numbers
    def get_plcs_for_day(self, day):
        plc_numbers = set()
        for filename in self.list_files():
            data = self.__name_to_plc_and_date(filename)
            if data[1].__eq__(day):
                plc_numbers.add(data[0])
        return plc_numbers

    ## Get the PLC names that reported in on a given day based on the files posesed in the cache
    # @param day The datetime.date that should be checked
    # @returns A set of PLC names as strings
    def get_plc_names_for_day(self, day):
        plc_names = set()
        for filename in self.list_files():
            data = self.__name_to_plc_and_date(filename)
            if data[1].__eq__(day):
                plc_names.add(filename.split('_')[0])
        return plc_names

    ## Get the PLC names that reported in on any day based on the files posesed in the cache
    # @returns A set of PLC names as strings
    def get_plc_names(self):
        plc_names = set()
        for filename in self.list_files():
            plc_names.add(filename.split('_')[0])
        return plc_names

    ## Static method for converting a filename to a PLC number and a date contained within a tuple
    # @param filename The name of the file to convert
    # @returns A tuple like this: (plcnumber, datetime.date)
    @staticmethod
    def __name_to_plc_and_date(filename):
        if '.xls' not in filename:
            print("Data Not Found For " + filename)
            return None
        parts = filename.replace('.xls', '').split('_')
        number = int(parts[0].replace('F', ''))
        d = datetime.strptime(parts[1], "%Y%m%d").date()
        return number, d

    ## List out the .xls files in the remote directory
    # @returns a list of file names representing the .xls files on the remote server
    def list_files(self):
        return [f for f in self.client.nlst() if '.xls' in f]  # doing this is called a 'list comprehension'
