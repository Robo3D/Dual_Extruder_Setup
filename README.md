# Dual_Extruder_Setup

This software is a cross platform Dual Extrusion Setup and has(will have) the following features

- Flash firmware to the most recent Dual Extrusion firmware
- Flash firmware back to a single extrusion firmware
- change the default profile to a Dual Extrusion Profile
- change the default profile back to a Single Extrusion Profile

# Warning
The current hex files associated with this program are not up to date. Do not use yet.

# Shared Functions

This Plugin has a backend and a web frontend currently, but any other device should be able to use 
its backend function if they use the URL "plugin/Dual_Extruder_Setup/change_and_install" You would
have to write data to it as well using this dictionary tag:
```
model: "R2" 
```
Or any other model you would like to setup the printer as (R2, C2, R2 Dual)

Any other device would also be able to pick up the plugin events being thrown off by this plugin.
Currently there are two event channels. One is the firmware download progress, and the other is the
state of the overall process. Developers can use these to create their own frontends to this process

Here is the js plugin event handler as an example:
```
OctoPrint.socket.onMessage("plugin", self._plugin_event)

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
```
Any other device should be able to connect to the event socket and read events. 