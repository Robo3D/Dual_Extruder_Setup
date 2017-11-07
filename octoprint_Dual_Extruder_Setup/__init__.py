# -*- coding: utf-8 -*-
# @Author: Matt Pedler
# @Date:   2017-11-07 11:43:20
# @Last Modified by:   Matt Pedler
# @Last Modified time: 2017-11-07 11:49:17
# coding=utf-8

from __future__ import absolute_import

import octoprint.plugin

class Dual_Extruder_Setup(octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.AssetPlugin,
                          octoprint.plugin.TemplatePlugin):
    '''
    The Goal for this plugin is to have a cross platform Single touch setup for Dual Extrusion on the Robo R2 and C2 printers.
    We will accomplish this by exporting a function that will change the following
     - Change the firmware to the most recent stable firmware
     - Change the default printer profile to a Dual Extrusion profile

    Secondary Goals will be to also have the ability to change back to a single extrusion machine on the fly.
    '''

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
__plugin_name__ = "Dual Extruder Setup"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Dual_Extruder_Setup()

    global __plugin_hooks__
    __plugin_hooks__ = {
        
    }

