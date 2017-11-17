/*
 * View model for Dual_Extruder_Setup
 *
 * Author: Matt Pedler
 * License: AGPLv3
 */
$(function() {
    function Dual_extruder_setupViewModel(parameters) {
        var self = this

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0]
        // self.settingsViewModel = parameters[1]

        // TODO: Implement your plugin's view model here.
        console.log("Starting up Robo Configuration Tool!")
        self.printer_options = []
        self.selected_model = ''
        self.width = 0
        self.get_printer_options = function(){
            //get options from backend
            $.ajax({
                url: PLUGIN_BASEURL + "Dual_Extruder_Setup/get_model_options",
                type: "GET",
                datatype: "json",
                //data: JSON.stringify({}),
                contentType: "application/json charset=UTF-8",
                success: function(response){
                    console.log(response)

                    self.printer_options = JSON.parse(response)
                    self.selected_model = self.printer_options[0]
                    

                }

            })
        }

        self.set_selected_model= function(){
            var model_index = document.getElementById("model_dropdown").selectedIndex
            self.selected_model = self.printer_options[model_index]
            console.log(self.selected_model)
        }

        self.change_configuration = function(){
            //self.get_progress()
            $.ajax({
                url: PLUGIN_BASEURL + "Dual_Extruder_Setup/change_and_install",
                type: "POST",
                datatype: "json",
                data: JSON.stringify({
                    model: self.selected_model
                }),
                contentType: "application/json charset=UTF-8",
                // success: function(response){
                //     location.reload()
                // }

            })
        }

        self.frame = function(){
            elem = document.getElementById("robo_progress_bar")            
            if (self.width <=25){
                elem.style.width = self.width + '%' 
                elem.innerHTML = "Download " + self.width + "%"
            }
            else if (self.width > 25 && self.width <= 75){
                elem.style.width = self.width + '%' 
                elem.innerHTML = "Firmware Upload " + self.width + "%"
            }
            else if(self.width > 75){ 
                elem.style.width = self.width + '%' 
                elem.innerHTML = "Profile Change " + self.width + "%"
            }
              
            
            
        }       

        self.get_progress = function(){
            
            self.width = 0
            self.frame()
            // document.getElementById("config_progress").visibility = 'visible'
        }

        self._firmware_progress = function(event){
            if ('data' in event){
                data = event['data']
                if (data['plugin'] == 'Dual_Extruder_Setup'){
                    data = data['data']
                    if (data['type'] == 'firmware_progress'){
                        self.width = data['data'] // data squared
                        self.frame()
                    }
                }
            }
        }

        

        self.get_printer_options()
        OctoPrint.socket.onMessage("plugin", self._firmware_progress)
            
        

    }
    
    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        Dual_extruder_setupViewModel,

        // e.g. loginStateViewModel, settingsViewModel, ...
        ['settingsViewModel' /* "loginStateViewModel", "settingsViewModel" */ ],

        // e.g. #settings_plugin_Dual_Extruder_Setup, #tab_plugin_Dual_Extruder_Setup, ...
        ['#settings_plugin_Dual_Extruder_Setup' /* ... */ ]
    ])
})
