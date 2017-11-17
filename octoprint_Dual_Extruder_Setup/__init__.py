# -*- coding: utf-8 -*-
# @Author: Matt Pedler
# @Date:   2017-11-07 11:43:20
# @Last Modified by:   Matt Pedler
# @Last Modified time: 2017-11-16 17:12:44
# coding=utf-8

from __future__ import absolute_import
from . import Octo_Setup 
from .Octo_Setup.Robo_Octo_Setup import Robo_Octo_Setup
import flask
import json

import octoprint.plugin

class Dual_Extruder_Setup(octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.AssetPlugin,
                          octoprint.plugin.TemplatePlugin,
                          octoprint.plugin.StartupPlugin,
                          octoprint.plugin.BlueprintPlugin):
    '''
    The Goal for this plugin is to have a cross platform Single touch setup for Dual Extrusion on the Robo R2 and C2 printers.
    We will accomplish this by exporting a function that will change the following
     - Change the firmware to the most recent stable firmware
     - Change the default printer profile to a Dual Extrusion profile

    Secondary Goals will be to also have the ability to change back to a single extrusion machine on the fly.
    '''
    # def __init__(self, *args, **kwargs):
    #     super(Dual_Extruder_Setup, self).__init__(*args, **kwargs)

    #     pass

    overall_progress = 0

    def on_after_startup(self):
        #Get the firmware plugin
        #get the helper function to determine if the board is updating or not
        helpers = self._plugin_manager.get_helpers("firmwareupdater", "firmware_updating","flash_usb")
        if helpers:
            self._logger.info("Firmware updater has helper functions")

            #Grab firmware updating
            if "firmware_updating" in helpers:            
                self.firmware_updating = helpers["firmware_updating"]
            else:
                self.firmware_updating = self.updater_placeholder

            #Grab flash usb
            if "flash_usb" in helpers:
                self.flash_usb = helpers["flash_usb"]
            else:
                self.flash_usb = self.updater_placeholder
        #if there aren't any helpers then use place holders
        else :
            self._logger.info("Firmware updater does not have a helper function")
            self.firmware_updating = self.updater_placeholder
            self.flash_usb = self.updater_placeholder


        #make a bridge to Octo_Setup for octoprint 
        self.octo_setup = Robo_Octo_Setup(self)

    #place holder just in case
    def updater_placeholder(self, *args, **kwargs):
        return False

    def firmware_progress(self, value):

        self.overall_progress = value
        #send the progress as a message to anyone who is listening.
        self._plugin_manager.send_plugin_message(self._identifier, dict(type="firmware_progress", data=self.overall_progress))

    def install_firmware(self, model='R2'):

        #get firmware
        if self.octo_setup.check_connection():
            self._logger.info("Downloading Firmware")
            self.octo_setup.clear_callbacks()
            self.octo_setup.register_progress_callback(self.firmware_progress)
            firm_path = self.octo_setup.download_firmware(version=model)
            self._logger.info("Installing Firmware")
            self.flash_usb(firm_path)
        else:
            self._logger.info("No Connection to Lambda Function")
            return False

    def change_profile(self, model='R2'):
        self._logger.info("Changing Profile")
        self.octo_setup.change_profile(version=model)

    @octoprint.plugin.BlueprintPlugin.route("/change_and_install", methods=['POST'])
    def change_and_install(self, **kwargs):
        self._logger.info("Change and install called.")
        if 'model' in flask.request.json:
            model = flask.request.json['model']
            #report model            
            if model == "R2 Dual":
                model = "R2_Dual"
            self._logger.info("Model is: " + str(model))
            #install Firmware
            self.install_firmware(model=str(model))
            #change profile
            self.change_profile(model=str(model))
            #return okay
            return flask.make_response("Ok.", 200)
        return flask.make_response("Error.", 500)

    @octoprint.plugin.BlueprintPlugin.route("/get_model_options", methods=['GET'])
    def get_model_options(self):
        profile = self._settings.global_get(['printerProfiles', 'defaultProfile'])

        model=None
        if 'model' in profile:
            model = profile['model']

       
        if model == "Robo R2":
            return json.dumps(['R2', 'R2 Dual'])
        elif model == 'Robo C2':
            return json.dumps(['C2'])
        else:
            return json.dumps(['C2', 'R2', 'R2 Dual'])
       


    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/Dual_Extruder_Setup.js"],
            css=["css/Dual_Extruder_Setup.css"],
            less=["less/Dual_Extruder_Setup.less"]
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Robo Configuration Tool"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Dual_Extruder_Setup()

    global __plugin_hooks__
    __plugin_hooks__ = {
        
    }

