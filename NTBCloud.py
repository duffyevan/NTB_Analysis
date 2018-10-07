import logging
import os

import webdav.client as wc


class NTBCloudException(Exception):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return self.info


class NTBWebdav:
    def __init__(self, hostname, username, password):
        login_options = {
            'webdav_hostname': hostname,
            'webdav_root': '/remote.php/webdav/',
            'webdav_login': username,
            'webdav_password': password
        }
        self.backup_location = "/09_SHARED_FOLDER_EXTERN/Messdaten_Feldmessung"
        self.client = wc.Client(login_options)
        logging.info("Logged Into NTB Webdav")

    ## Back up a single file to NTB's Cloud Server
    # @param file_path The full path to the file to be uploaded.
    # All files are placed in /backup_files/ in the shared folder
    def backup_file(self, file_path):
        logging.info("Backing up " + file_path)
        backup_file_name = os.path.join(self.backup_location, os.path.basename(file_path))
        try:
            self.client.upload_sync(local_path=file_path, remote_path=backup_file_name)
        except wc.WebDavException as e:
            raise NTBCloudException(str(e))

    ## Run ls on a directory or the current directory
    # @param directory (optional) The directory to list the contents of. If not specified the current dir will be used
    def ls(self, directory=''):
        return self.client.list(directory)

    ## List the files in the folder that files are backed up to. Effectively gets a list of files that have been backed up
    def list_backed_up_files(self):
        return [f for f in self.ls(self.backup_location) if '.xls' in f]

    ## Download a single file from the backup_files folder.
    # @param filename The name of the file in the backup_files folder to download
    # @param download_location (optional) the location to download the file to, ./ by default
    def download_file(self, filename, download_location='./'):
        self.__download_file(os.path.join(self.backup_location, filename), download_path=download_location+filename)

    ## Lover level version of download file. Downloads a file from path to path
    # @param path The path to the file on the server to download
    # @param download_path The path to download the file to (must include file name in path)
    def __download_file(self, path, download_path='./'):
        self.client.download(local_path=download_path, remote_path=path)

