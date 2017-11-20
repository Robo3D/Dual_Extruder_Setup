/*
 * View model for Dual_Extruder_Setup
 *
 * Author: Matt Pedler
 * License: AGPLv3
 */
$(function() {
    function Dual_extruder_setupViewModel(parameters) {
        var self = this
        self.printer_options = [] // This variable is used for gathering options from the backend
        self.selected_model = '' // This variable is used to check the selected version
        self.width = 0 // This is the progress of downloading

        //This function will gather the printer options from the backend
        self.get_printer_options = function(){
            //get options from backend
            $.ajax({
                url: PLUGIN_BASEURL + "Dual_Extruder_Setup/get_model_options",
                type: "GET",
                datatype: "json",
                contentType: "application/json charset=UTF-8",
                success: function(response){
                    self.printer_options = JSON.parse(response)
                    self.selected_model = self.printer_options[0]
                    

                }

            })
        }

        //This function gets called every time the user changes their choice on the frontend
        self.set_selected_model= function(){
            var model_index = document.getElementById("model_dropdown").selectedIndex
            self.selected_model = self.printer_options[model_index]
            console.log(self.selected_model)
        }

        //This will start the configuration process
        self.change_configuration = function(){
            $.ajax({
                url: PLUGIN_BASEURL + "Dual_Extruder_Setup/change_and_install",
                type: "POST",
                datatype: "json",
                data: JSON.stringify({
                    model: self.selected_model
                }),
                contentType: "application/json charset=UTF-8",
            })
        }

        //This gets called every time a progress bar message gets recieved
        self.frame = function(){
            elem = document.getElementById("robo_progress_bar")            
            state = document.getElementById("state_label")
            elem.style.width = self.width + '%' 
            state.innerHTML = "Downloading Firmware " + self.width + "%"
        }       

        //This gets called every time there is a plugin event
        self._plugin_event = function(event){
            if ('data' in event){
                data = event['data']
                if (data['plugin'] == 'Dual_Extruder_Setup'){
                    data = data['data']
                    if (data['type'] == 'firmware_progress'){
                        self.width = data['data'] // data squared
                        self.frame()
                    } else if(data['type'] == 'state'){
                        state = document.getElementById("state_label")
                        state.innerHTML = data['data']

                        if(data['data'] == "Finished!"){
                            setTimeout(self.cleanup_elements, 2000)
                        }
                    }
                }
            }
        }

        //This gets called after the config process is finished. It will reload the page so the 
        //Printer default profile gets updated
        self.cleanup_elements = function(){
            state = document.getElementById("state_label")
            state.innerHTML = "Reloading"
            elem = document.getElementById("robo_progress_bar")    
            elem.style.width = 0

            location.reload()

        }

        self.add_to_printer_section = function(){

            if(document.getElementById("settings_gcodeScripts_link") != null){
                //delete old thing
                old_elem = document.getElementById("settings_plugin_Dual_Extruder_Setup_link")
                old_elem.remove()
    
                //add to new thing
                elem = document.getElementById("settings_gcodeScripts_link")
                elem.insertAdjacentHTML('afterend', '<li id="settings_plugin_Dual_Extruder_Setup_link" data-bind="allowBindings: true" class=" "><a href="#settings_plugin_Dual_Extruder_Setup" data-toggle="tab">Robo Configuration Tool</a></li>')

            }else{
                console.log("Cannot find GCODE scripts and we will not be moving our link")
            }

            
        }

        //put us in the printer tab
        self.add_to_printer_section()
        //get the options right off the bat
        self.get_printer_options()
        //Register the callback for a plugin message
        OctoPrint.socket.onMessage("plugin", self._plugin_event)
            
        

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
