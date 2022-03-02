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
*If you do these steps out of order, you may get frustrated. Eclipse needs Java for its install, and PyDev and Kivy need Python. Save yourself the stress. 

### 1. Install Java Runtime Environment

Get JRE from [here]( 
https://www.oracle.com/technetwork/java/javase/downloads/jre8-downloads-2133155.html).

I downloaded and ran jre-8u202-windows-x64.exe. 

The wizard takes you through the entire installation.

You'll want to make sure you have Java 8 or higher for Eclipse. 


### 2. Install Python

I used Windows x86-64 MSI installer from [here] (https://www.python.org/downloads/release/python-2715/).

Download it and run it, as you did with the Java installer.

Make sure you use a version of Python 2. I downloaded Python 2.7.15 because it comes with pip, which we'll need later. 

Once again, the wizard is great and takes you through the entire installation. 

Make a note of where you installed Python, as you will need to know later on. 


### 3. Install Eclipse

Head to: https://www.eclipse.org/downloads/

I am using Eclipse IDE 2018-12 

Hit "Download", and then hit "Download" again. 

It will tell you where it's downloading from - don't worry about this, you'll get the same stuff wherever it's from.

When you run the installer, it will ask you to select and IDE. Select the **Eclipse IDE for Java Developers** 

After that, the wizard will guide you. 


### 4. Install PyDev in Eclipse. 

Open Eclipse, and then go to the toolbar, and select Help > Eclipse MarketPlace. 
  
Under the "Search" tab, type "PyDev" in front of "Find:", and press enter. 

Install the PyDev - Python IDE for Eclipse that comes up. 

As before, work through the wizard. 


### 5. Install Kivy

Go to [Kivy's website](https://kivy.org/doc/stable/installation/installation-windows.html) for the installation instructions, which are fairly good. 

In order to work through them, you'll need to open your Command Line. 

Open Command Line by using the shortcut windows+R, and then typing cmd in the box that comes up. Press ok. 

You'll need to navigate via the command line to the folder you installed python in. 

If you need to change which drive you're in, you can do this by typing the driver letter and a colon, e.g. "d:".

Then, use "cd" (which stands for "change directory") to jump to the relevant folder. 

For example, if you've installed Python in Yeti\Python27, you will want to enter:

cd Yeti\Python27

Once you're in the same folder as your Python installation, you can follow the instructions on [Kivy's website](https://kivy.org/doc/stable/installation/installation-windows.html). 

Keep command line open for the next step. 

### 6. Install the Serial module

You'll need to install this module with python in order for the UI to run. 

Stay in your command line as before (or open and navigate to your Python installation as in Step 5), and enter the following line: 

python -m pip install pyserial

Watch some text scroll before your eyes. Bam. You're sorted. 

### 7. Tell Eclipse where to find your Python interpreter

Open Eclipse (if you closed it). Go to the toolbar, and select Window > Preferences. Then, on the side-menu in Preferences, go to PyDev > Interpreters > Python. 

Click on “Browse for python/pypy exe”, and find your python.exe file, in the folder you installed it.

All of Kivy's libraries should automatically be loaded into Eclipse as well. 

Click "Apply and Close". 

Awesome. Almost done. 

### 8. Get easycut-smartbench from GitHub into Eclipse 

In Eclipse, go to the toolbar and select Window > Show View > Other. 

In the pop-up, expand the "Git" folder, and click on "Git Repositories". Click OK. 

Then, in the Eclipse toolbar go to File > Import. 

In the pop-up, select Projects from Git, and then Next. 

Click Clone from URI. 

Paste the following into the URI box: 

https://github.com/YetiTool/easycut-smartbench.git

The other information should auto-fill, so click Next. Click Next again. Choose a directory to install it in, and click Next again. 

Select "Import existing projects", click Next, and then click Finish. 

That should be you done! easycut-smartbench will show up under Git Repositorie.

Make sure you can also see Package Explorer in Eclipse - if you can't just go to Window > Show View > Package Explorer. 

If you want to try running the UI, Open "main.py" and click Run (the green play button). And off you go ;).


### Basic hardware test (optional)

If you have and Arduino Mega 2560, you can test comms right away by putting a basic grbl-Mega image onto the Arduino.

*Note: Due to lack of end switches, and therefore an inability to "home", some functionality will be unavailable, and EasyCut may crash unexpectedly.
*Note: Currently points to standard grbl-Mega, not YetiGrbl

* Follow compilation instructions [here](https://github.com/grbl/grbl/wiki/Compiling-Grbl), with one modification:
** When prompted to "Click the Download ZIP button on the Grbl home page" [download from grbl-Mega instead](https://github.com/gnea/grbl-Mega)
* Once compliled, determine which COM port the arduino sits on and ammed that value in "main.py"
* Run "main.py" :-)

