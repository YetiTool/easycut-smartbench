# easycut-smartbench
Console UI for YetiTool's SmartBench


Buffer logging:
- Output of grbl serial char and line buffer now standard in 'go' screen.
- To enable writing to file, tap "buffer log" toggle button in dev tab. (Blue=on)
	- WARNING: File overwritten on the start of next stream job.
	
Virtual HW:
- Designed for use of Arduino without any switches
- Essential, before enabling: On arduino, to avoid door error, connect Analouge 11 to GND (think E must have inverted the setting in the config file, was surprised to see this error)
- WARNING: toggle effects are persistent in grbl. So ensure to toggle state back to required status before powering down device to avoid unexpected results on startup (toggle state defaults to disabled, regardless of persistent settings. If this happens, just flick the toggle at least once to sync toggle with state)
- WARNING: In virtual mode, Mpos will default to 0,0,0 so 
	- Head will be at wrong end of bed to start with
	- Running virtual hw with actual machine plugged in will cause plenty of conflict :-) Don't!
- After clicking play button to enter the go screen, ignore popup errors and click on 'continue anyway'


# Build steps for Windows 
Setup of tools that allow you to play with & test out the UI with ease. 

## Important notes: 
* The following set-up is done on Windows.
  * Make sure you are consistent in whether you choose to install x86 or x64 software, otherwise the different programs will fail to find each other (e.g. Eclipse and Java). 
  * I have used x64 throughout this example. 
* I personally installed everything in one "Yeti" folder, and all of the software was able to find all the other software with no issues. But you do you. 
* If you do these steps out of order, you may get frustrated. Eclipse needs Java for its install, and PyDev and Kivy need Python. Save yourself the stress.

### 1. Install Python

I used Windows x86-64 MSI installer from [here](https://www.python.org/downloads/release/python-2718/).

Download it and run it.

After choosing the install path, make sure to select "Add python.exe to Path". After this change, all optional features should be selected.

Make sure you use a version of Python 2. I downloaded Python 2.7.18 because it comes with pip, which we'll need later. 

Once again, the wizard is great and takes you through the entire installation. 

Make a note of where you installed Python, as you will need to know later on - by default it's `C:/Python27`

To validate the installation, open the Command Prompt and type `python --version` and you should get back `Python 2.7.18`


### 2. Install an IDE

You will need to install an IDE. This can be anything you like but we'll use PyCharm in this guide.

Head to: https://www.jetbrains.com/pycharm/download/#section=windows

Download the "Community version" as it is the free version and follow the installer steps.


### 3. Get easycut-smartbench from GitHub into your IDE 

This step will vary depending on your IDE so if you use something other than PyCharm, consult your IDE's website.

Open PyCharm, go to `File > Settings > Version Control > GitHub` and connect your account. For more details click [here](https://www.jetbrains.com/help/pycharm/github.html)

Then, go to `Git > Clone` and copy and paste the link to the GitHub repository in the URL section and select where you'd like the repository to get stored **locally**. Make sure you remember this location. For more details click [here](https://www.jetbrains.com/help/pycharm/manage-projects-hosted-on-github.html)

If the code shows a lot of errors, don't worry, it's expected at this stage.

### 4. Select your interpreter in your IDE

Once again, this step will vary depending on your IDE, so please consult your IDE's website if you use something other than PyCharm.

In PyCharm, when you cloned the repository, you should have gotten a notification asking you to select the interpreter. If you did, click on it and select `Python 2.7` from the dropdown list.

If you didn't get the notification, navigate to `File > Settings > Project: <project name> > Python Interpreter` and select `Python 2.7` as your interpreter.

If `Python 2.7` does not show up in the list, go to `Add Interpreter > Add Local Interpreter` and navigate to the location where you installed python and select the `python.exe` file. If you installed in the default location, this should be `C:/Python27/python.exe`.

For additional information, click [here](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#add-existing-interpreter)

### 5. Install dependencies

Now we can put aside the IDE open Command Prompt to install the dependencies.

Navigate to the folder where you saved the repository. You can do this using `cd <path to repository>`. NOTE: if the path is on a separate partition, for example `D:`, you will need to enter `D:` in the command prompt before you can use `cd <path to repository>`.

You should now be in the same repository as the `requirements.txt` file. In this case, you can simply enter `pip install -r requirements.txt` and wait for pip to install all the dependencies. You may need to occasionally type `Y` or `yes` to agree to installing the dependencies.

Wait for pip to finish installing everything and you're done! You can use `pip list` to show all the dependencies installed and their versions.

At this stage, you're done and you can run the UI! Open the `main.py` file and click run (the green play button). And off you go ;).

### Basic hardware test (optional)

If you have and Arduino Mega 2560, you can test comms right away by putting a basic grbl-Mega image onto the Arduino.

*Note: Due to lack of end switches, and therefore an inability to "home", some functionality will be unavailable, and EasyCut may crash unexpectedly.
*Note: Currently points to standard grbl-Mega, not YetiGrbl

* Follow compilation instructions [here](https://github.com/grbl/grbl/wiki/Compiling-Grbl), with one modification:
** When prompted to "Click the Download ZIP button on the Grbl home page" [download from grbl-Mega instead](https://github.com/gnea/grbl-Mega)
* Once compliled, determine which COM port the arduino sits on and ammed that value in "main.py"
* Run "main.py" :-)

