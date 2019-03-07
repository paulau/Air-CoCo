                                               Air-CoCo                                          
                                       Air  Control & Company                                    
                      Air Properties Monitoring, Ventilation Control, Data Visualisation           



                                               Picture 1                                          
                                       The structure of the project.                              
                                           _________________                                      
                                          |                 |                                     
                                          |  settingsMC.py  |                                     
                                          |_________________|                                     
                                                   |                                              
                                                   | Used once at first start                     
                                                   | to fill MySQL Database                       
                                       ____________|___________                                   
                                      |                        |         ________________         
         _____________                |    ________________    |        |Monicontrolclass|        
        |             | Collected     |   |                |   |/______\|  |             |        
        |   Files in  |<==============|   |   monicontrol  |   |\      /|  |             |        
     ---|    Folder   |   Data        |   |      main      |   |        | Server         |        
    |   |     data/   |               |   |    (Thread)    |   |        | Socket         |
    |   |_____________|               |   |   algorithm    |   |        | Thread         |         __________________
    |                                 |   |                |   |        |                |        |                  |
    |                                 |   |________________|   |        |                |<------>|      MySQL       |
    |                                 |                        |        |________________|        |  Parameters only |
    |                                 |                        |               /\  |              |                  |
    |    _______________              |                        |               |   |              |__________________|
    |   |   Hardware    | Commands    |                        |               |   |                      /\
    |   |   - Raspberry |<===========>|                        |               |   |                      |  
    |   |   - Sensors   |   State     |                        |     Control   |   | State Data           |
    |   |   - Relays    |   Data      |                        |     Commands  |   |   via                |
    |   |_______________|             |________________________|    via Socket |   |  socket              |
    |                                                                          |   |                      |
    |                                                                          |   |                      |
    |                                                                          |   |                      |
    |                                                                          |   \/                     |
    |                                                              _________________________________      |
    |       __________________        __________________          |                                 |     |
    |      |                  |      |                  |         |          Apache                 |     |
    |      |   Visualisation  |      |   Visualisation  |         |  _____________________________  |<-----
     ----->|                  |----->|      Files       |-------->| | PHP(Java)-interaction-layer | |
           |                  |      |     in www       |         | |_____________________________| |
           |__________________|      |__________________|         |_________________________________|   
                                                         
        
                                     
  __________________ 
 | git Repository   |
 |   Air-CoCo       |
 |__________________|
                     
At the moment - public access to the project related data

Table 1:  Modules and their description
_______________________________________________________________________________________________________________
| Name                     | Core concept                                                | Files               
|--------------------------|-------------------------------------------------------------|---------------------
| settingsMC.py            | To keep factory settings                                    | settingsMC.py
|--------------------------|-------------------------------------------------------------|---------------------
| monicontrol main Thread  | Makes main Job                                              | monicontrol.py
|--------------------------|-------------------------------------------------------------|---------------------
| monicontrolclass         | class with complete functionality                           | monicontrolclass.py
|                          | needed for the "main Job"                                   | Test Materials
|                          | additionally, to return the state                           | in Client-Server
|                          | to external requests via socket.                            |
|--------------------------|-------------------------------------------------------------|---------------------
| MySQL                    | To set user defined parameters                              |
|--------------------------|-------------------------------------------------------------|---------------------
| Files in Folder data     | To keep the data of monitoring                              | .../data/
|--------------------------|-------------------------------------------------------------|---------------------
| Hardware                 | Hardware modul built of Raspberry,                          |
|                          | sensors and relays                                          | Docs
|                          | Attached to more complicated network of devices             |
|--------------------------|-------------------------------------------------------------|---------------------
| Visualisation            | To transform ascii text data into charts-pictures           |
|--------------------------|-------------------------------------------------------------|---------------------
| Visualisation files      | To store visualised pics for fast acces via web             |
|--------------------------|-------------------------------------------------------------|---------------------
| Apache + PHP             | To visualise Data and to control Monitoring-control system  | .php
|--------------------------|-------------------------------------------------------------|---------------------
