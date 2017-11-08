# -*- coding: utf-8 -*-
# @Author: Matt Pedler
# @Date:   2017-11-07 12:00:08
# @Last Modified by:   Matt Pedler
# @Last Modified time: 2017-11-07 16:37:36

import requests
import json
import os


class Octo_Setup(object):
    """docstring for Octo_Setup"""
    def __init__(self):
        super(Octo_Setup, self).__init__()
        #This URL will supply the most recent firmware release download links. 
        self.firmware_checker_addr = 'https://3ym5t3go29.execute-api.us-east-1.amazonaws.com/prod/Current_Firmware'

    def check_connection(self):
        '''
        This Function will check the connection to the internet. It will return true or false
        '''
        payload = json.dumps({"action": "PING",})
        response = self.send_payload(payload)

        if response.status_code == 200:
            return True
        else:
            return False

    def download_firmware(self, version="R2"):
        '''
        This Function will download a corresponding up to date version of the firmware
        '''

        #dummy check to see if we are requesting the right data
        dummy_check = ['R2', 'C2', 'R2_Dual']
        if not version in dummy_check:
            return False

        #check to see if we are connected
        if not self.check_connection():
            return False

        #get firmware URL
        payload = json.dumps({"action": str(version)})
        response = self.send_payload(payload)

        #check to see that the response is what we want
        r_dict = {}
        if response.status_code == 200:
            r_dict = json.loads(response.text)
            print(str(r_dict))
        else:
            return False

        #get the file url
        download_url = ''
        if 'response' in r_dict:
            download_url = r_dict['response']
        else:
            return False

        #define download directory
        files_directory = "/tmp/firmware/"

        #check to see if the dir exists
        if not os.path.exists(files_directory):
            #make dir
            try:
                os.makedirs(files_directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        #define the download path with the URL filename
        dl_path = files_directory + download_url.split('/')[-1]

        #download the file
        r = requests.get(download_url, stream=True)
        length = float(int(r.headers['content-length']))
        size = 0.00
        progress = 0.00
        with open(dl_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    #write chunk
                    f.write(chunk)
                    #record progress
                    size += 1024.00 #not exact size of chunk, but close enough for this purpose
                    progress = int((size/length)*100.00)
                    self.download_progress(progress)


        return dl_path


    def download_progress(self, progress):
        print(progress)
        '''
        overwritable function
        '''
        pass        

    def install_firmware(self, path):
        '''
        This will interface with the Firmware Update plugin and install firmware from a path
        '''
        pass

    def change_profile(self, version):
        '''
        This will change the default profile to a Single or Dual Extruder profile for the R2 and C2
        Version can be set as R2, C2, or R2_Dual
        '''
        pass

    def load_configs(self):
        '''
        This function loads the default_profile.yaml
        '''
        pass

    def send_payload(self, payload):
        '''
        This function will send any payload to the lambda function
        '''
        response = requests.post(self.firmware_checker_addr, data=payload)
        return response

# oset = Octo_Setup()
# print(oset.download_firmware())
# print(oset.download_firmware(version='C2'))
# print(oset.download_firmware(version='R2'))
# print(oset.download_firmware(version='R2_Dual'))
# print(oset.download_firmware(version='failed test'))