# -*- coding: utf-8 -*-
# @Author: Matt Pedler
# @Date:   2017-11-07 12:00:08
# @Last Modified by:   Matt Pedler
# @Last Modified time: 2017-11-07 13:59:20

class Octo_Setup(object):
    """docstring for Octo_Setup"""
    def __init__(self):
        super(Octo_Setup, self).__init__()
        
    def check_connection(self):
        '''
        This Function will check the connection to the internet. It will return true or false
        '''
        pass

    def download_firmware(self, version="R2"):
        '''
        This Function will download a corresponding up to date version of the firmware
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

        