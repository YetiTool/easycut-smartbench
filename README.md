## Raspberry Pi 3B+: 3<sup>rd</sup> Party Radio compliance testing

**VERSION 2**

<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")



## Introduction

For devices that incorporate Raspberry Pi 3 into the final product certain parts of the radio compliance testing will need to be completed.

To enable the various test modes you will need to follow the instructions in this doc

_For conducted tests a UFL connector can be soldered on the board, along with a change 0R resistor to allow for conducted testing, a small portion of the Ground plane will need to be uncovered for the second ground pad. Detailed instructions can be found in the ZIP above_

**Please note all commands in these documents are case sensitive, space sensitive and must be typed exactly as specified. Please also note the different uses of the “.”, “-” and “_” characters as it is critical they are correct.**


## RasPi setup


### Connect Console to WiFi

[Click here](https://www.yetitool.com/SUPPORT/KNOWLEDGE-BASE/smartbench1-console-operations-connecting-to-wifi-connecting-to-a-wireless-network-including-android-hotspot) to learn how to connect the console to your WiFi network


### Access the console terminal

You will need a USB keyboard, and will need to login to the terminal at the console

After the console has finished booting up, use the navigation arrows to locate **System tools**

Click **System Tools **> **Exit Software**

Then on the keyboard, **Alt+F2**

login: pi

password: pi _(this won’t be visible)_


### Switching branch

At the terminal prompt, type the following, in order:


*cd easycut-smartbench


*git pull


*git checkout rf_testing


*cd

(this line begins with a dot) 


*(this line begins with a dot) ./easycut-smartbench/ansible/templates/ansible-start.sh

Once ansible has finished running and the prompt returns (approx. 2 minutes)


*sudo reboot

Return to the command prompt **as before** via system tools > exit software, Alt+F2 and log in.

Setup is now complete!

See below to begin testing!


## Debugging

If “unable to resolve host” error occurs at any stage see [this help document ](https://docs.google.com/document/u/0/d/1fAAgWdwLec6NE5DElLsTQUh9Obn43d_CnfrTA-b3ThI/edit)


## Conducting tests



* To conduct the tests listed below:
    * WLAN 2.4GHz 802.11b
    * WLAN 2.4GHz 802.11g
    * WLAN 2.4GHz 802.11n 20MHz
    * WLAN 5150 – 5250 MHz @ 200mW
    * WLAN 5250 – 5350 MHz @ 200mW
    * WLAN 5725 -5850 MHz @ 4000mW
    * Bluetooth low frequency
    * Bluetooth medium frequency
    * Bluetooth high frequency
* The following **.sh** files have been prepared:
    * 2.4GHz_802.11b_1_mbs_ch_1.sh
    * 2.4GHz_802.11g_6_mbs_ch_1.sh
    * 2.4GHz_802.11n_20MHz_MCS0_ch_1.sh
    * 5GHz_5180MHz_200mW.sh
    * 5GHz_5260MHz_200mW.sh
    * 5GHz_5755MHz_4000mW.sh
    * bluetooth_low.sh
    * bluetooth_med.sh
    * bluetooth_high.sh
* These **.sh **files are scripts that run a series of commands automatically. The goal being to configure the relevant test, begin the transmission and stop it after 2 minutes. All of this will happen concurrently once the test is started.

_For reference, the “ls” (list) command lists the test files (among other things) in the terminal:_



<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline drawings not supported directly from Docs. You may want to copy the inline drawing to a standalone drawing and export by reference. See <a href="https://github.com/evbacher/gd2md-html/wiki/Google-Drawings-by-reference">Google Drawings by reference</a> for details. The img URL below is a placeholder. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![drawing](https://docs.google.com/drawings/d/12345/export/png)

<span style="text-decoration:underline;">To run a test, do the following, in order:</span>



* Into the terminal, type: bash
* Followed by the name of the test you wish to run, separating it from “bash” with a space. (E.g. “bash 2.4GHz_802.11b_1_mbs_ch_1.sh”
* To avoid typing long filenames, the use of the “tab” key on any keyboard will complete the rest of any given filename, if you’ve correctly typed the beginning of the given name. 
* For example, if one were to type “2.4” and press tab, the terminal would type “2.4Ghz_802.11” for you. 
* The terminal has not completely filled a filename because multiple files have names containing the “2.4” you provided the terminal with.
* To continue, specify which test you are referring to. In this case, you would add “b”, “g”, or “n” to the filename.
* Press tab again to have the terminal fully complete the filename.

_This process is depicted below for reference._



<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline drawings not supported directly from Docs. You may want to copy the inline drawing to a standalone drawing and export by reference. See <a href="https://github.com/evbacher/gd2md-html/wiki/Google-Drawings-by-reference">Google Drawings by reference</a> for details. The img URL below is a placeholder. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![drawing](https://docs.google.com/drawings/d/12345/export/png)



* Once the filename is entered correctly, **press enter to run the test. **(note: each test ends in the extension “.sh”)
* The test will begin and you will be greeted with prompts telling you the status of the test.



<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image2.png "image_tooltip")




* After time has passed and the test has completed, additional prompts will appear to indicate the end of the test.



<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image3.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image3.png "image_tooltip")




* At this point, the next test can be run by following the same process, starting with typing “bash” into the terminal.


## Appendix 

Necessary files are available in the [test assets ZIP file](https://drive.google.com/file/d/1SLF3A6scniUfYDOROdYN7bHO59lG9we2/view?usp=sharing) (RP-00111-CF-1.zip). Note this is protected under NDA. This has been incorporated into the setup process through the “git” commands. You shouldn’t need the ZIP file unless otherwise instructed.
