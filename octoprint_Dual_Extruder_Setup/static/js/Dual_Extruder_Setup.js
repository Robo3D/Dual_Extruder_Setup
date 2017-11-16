/*
 * View model for Dual_Extruder_Setup
 *
 * Author: Matt Pedler
 * License: AGPLv3
 */
$(function() {
    function Dual_extruder_setupViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.

        self.change_r2 = function(){
            $.ajax({
                url: PLUGIN_BASEURL + "Dual_Extruder_Setup/change_and_install",
                type: "POST",
                datatype: "json",
                data: JSON.stringify({
                    model: "R2"
                }),
                contentType: "application/json; charset=UTF-8"

            });
        };

        self.myFunction = function() {
            document.getElementById("setup_choices").classList.toggle("show");
            }
            
        

    }
    // Close the dropdown menu if the user clicks outside of it
    window.onclick = function(event) {
      if (!event.target.matches('.dropbtn')) {
    
        var dropdowns = document.getElementsByClassName("robo_config_dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
          }
        }
      }
    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        Dual_extruder_setupViewModel,

        // e.g. loginStateViewModel, settingsViewModel, ...
        ['settingsViewModel' /* "loginStateViewModel", "settingsViewModel" */ ],

        // e.g. #settings_plugin_Dual_Extruder_Setup, #tab_plugin_Dual_Extruder_Setup, ...
        ['#settings_plugin_Dual_Extruder_Setup' /* ... */ ]
    ]);
});
