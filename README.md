##### Jing Yang, Chun Ouyang, Maolin Pan, Yang Yu, Arthur H.M. ter Hofstede, *Finding the Liberos: Discover Organizational Models with Overlaps*, paper submitted to the 16th International Conference on Business Process Management (BPM 2018).


----------
This is the repository holding a standalone demo program mentioned in Sect. 5.1 of the submitted paper, in which both solutions (applying GMM/MOC) have been implemented.

There is an [Alternative Dropbox Link](https://www.dropbox.com/s/uzk82jxnry65nf8/artifact.zip?dl=0).

Users who just want to run a demo without having to prepare the input data may use the script file `demo_volvo.bat`, to perform a test run on the given example data "volvo_open". The result file would be `volvo_open_model.txt`.

Users may follow the instructions below to discover an organizational model with potential overlaps using any other event log file as input:
 1. Use [Disco](https://fluxicon.com/disco/) to import the target event log, and use the "export" function to convert to .csv format.
 2. Use the command line to start the program, and set the path to the csv log file as input, and specify the path for saving the output organizational model file.
    For example, in MS Windows, open command window, and navigate to the `artifact` folder and input:
    
    `.\dist\mine-om.exe .\example_event_logs\wabo_log.csv wabo_model.txt`

 3. Follow the prompt to select a method and set the value(s) of the required parameter(s).

The output file stores the info of the extracted organizational model in the format as the example below:

Group ID|Assigned tasks|Group members|
--- | --- | ---
0 | Task1; Task2 |Jack; Eva|
1 | Task 2; Task3; Task4; Task 5| Peter; John; Linda; Eva|
...| ...|...|

Each row contains the info of an organizational group in the model. And each column is separated by a colon while the listed values within a cell are separated by a semicolon.
