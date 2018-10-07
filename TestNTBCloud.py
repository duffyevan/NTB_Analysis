import os
import unittest

from NTBCloud import NTBWebdav


class AnalysisTest(unittest.TestCase):

    def test_ls(self):
        loginData = open('login.csv', 'r').readlines()[0].strip().split(',')
        print('loginData: ' + str(loginData))
        client = NTBWebdav(loginData[0], loginData[1], loginData[2])
        print(client.ls())
        print(client.ls('/09_SHARED_FOLDER_EXTERN'))
        self.assertTrue(True)  # if there was no errors, pass

    def test_download(self):
        loginData = open('login.csv', 'r').readlines()[0].strip().split(',')
        print('loginData: ' + str(loginData))
        client = NTBWebdav(loginData[0], loginData[1], loginData[2])
        file = client.list_backed_up_files()[0]
        download_location = './'
        client.download_file(file, download_location)
        self.assertTrue(os.path.exists(os.path.join(download_location, file)))
        os.remove(os.path.join(download_location, file))