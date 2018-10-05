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
        self.backup_location = "/09_SHARED_FOLDER_EXTERN/backup_files"
        self.client = wc.Client(login_options)
        logging.info("Logged Into NTB Webdav")

    def backup_file(self, file_path):
        logging.info("Backing up " + file_path)
        backup_file_name = os.path.join(self.backup_location, os.path.basename(file_path))
        try:
            self.client.upload_sync(local_path=file_path, remote_path=backup_file_name)
        except wc.WebDavException as e:
            raise NTBCloudException(str(e))

    def ls(self, directory=''):
        return self.client.list(directory)

    def list_backed_up_files(self):
        return self.ls(self.backup_location)

    def download_file(self, filename, download_location='./'):
        self.__download_file(os.path.join(self.backup_location, filename), download_path=download_location+filename)

    def __download_file(self, path, download_path='./'):
        self.client.download(local_path=download_path, remote_path=path)

