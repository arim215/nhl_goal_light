# NHL Goal Light

[![GitHub release](https://img.shields.io/github/release/arim215/NHL_goal_light.svg)](https://github.com/arim215/nhl_goal_light/releases)
[![GitHub commits](https://img.shields.io/github/commits-since/arim215/NHL_goal_light/v1.1.svg)](https://github.com/arim215/nhl_goal_light/commits/master)
[![closed pull requests](https://img.shields.io/github/issues-pr-closed/arim215/NHL_goal_light.svg)](https://github.com/arim215/nhl_goal_light/pulls?q=is%3Apr+is%3Aclosed)
[![Libraries.io for GitHub](https://img.shields.io/librariesio/github/arim215/NHL_goal_light.svg)](https://github.com/arim215/nhl_goal_light/blob/master/requirements.txt)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/c0f4d36de7234c45bb7689af5a35c7ec/badge.svg)](https://www.quantifiedcode.com/app/project/c0f4d36de7234c45bb7689af5a35c7ec)
[![license](https://img.shields.io/github/license/arim215/NHL_goal_light.svg)](https://github.com/arim215/nhl_goal_light/blob/master/LICENSE)

##Overview

Nhl goal light python3 for raspberry pi GPIO. Works with any team, just enter team **name without city** when prompted.

Before using this file, make sure you have:

Python3, python3-pip, mpg123, goal_horn_1.mp3, goal_horn_2.mp3, goal_horn_3.mp3

Run the following commands manually to install requirements

run:

        $ sudo apt-get install mpg123 python3-pip 
and run:

        $ sudo pip3 install -r requirements.txt
        
**Always pass thru code to read comments and see necessary inputs for your setup!!**

For documentation on how to wire the GPIOs with the lights and the button, pleaser refer to the "docs" folder.

###Materials

* Raspberry Pi (currently using raspberry pi A model, but any model will work)
* Red Rotating Beacon Warning Light from ebay
* 5V 2 Channel Relay Module from ebay
* Momentary OFF ON Push Round Button
* 12V to 5V 1A adapter (used a car usb adapter) would be good to have a dual usb adapter in case you need to plug something else like a usb speaker.
* 3.5mm audio extension cable

###Audio
If you wish to change the audio clips to sounds with your teams goal horn and music, just download them, rename them (goal_horn_#.mp3) and save them in the "audio" folder.

##Tests
To test the response time of sources, please execute the test_source.py while whatching game and note time of goal (not time of periode, but time of the day). The time of the source update will be printed to a text file. You can send me results so i can compile them and see which source updates the fastest.

I've teste my code while watching Rogers Gamecenter Live and the stream seems to be a bit delayed, so i added a delay to my code to make the goal horn start later. You'll need to adjust it to your stream to make it work best. 

## TODO
* Test response time after a goal is scored
* Add option to select team thru webpage
* Make code pause between periods
* Allow the addition of a I2C display
* Add a text message service to notify goals and more
