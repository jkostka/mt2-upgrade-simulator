## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Addition info](#info)

## General info
This project is a simulator for upgrading talismans and snake equipment in the game Metin2.
The maximum upgrade level for a talisman is +200, and for snake equipment it's +15.
Each upgrade level has a different percentage chance of success.
For talismans, the base chance is cyclical:

+01 55%
+02 50%
+03 45%
+04 40%
+05 35%
+06 30%
+07 25%
+08 20%
+09 15%
+10 10%
+11 55%
+12 50%
(...)
+85 20%
(...)
+99 15%
(...)
+125 35%

For snake equipment, the base chances are as follows:

+01 90%
+02 75%
+03 60%
+04 50%
+05 40%
+06 30%
+07 25%
+08 15%
+09 08%
+10 05%
+11 05%
+12 05%
+13 05%
+14 03%
+15 03%

The above chances are the base chances. The data comes from https://metin2alerts.com/upgradeList/

Magic stones do not increase the chance of upgrading an item.
For ritual stones, I have assumed an additional 10 percentage points for each upgrade level.
For the Dragon God's Seal, an additional 15 percentage points.
The actual increase in chances for these two types of scrolls is not known, but these chances are generally accepted among players. If the actual chances are ever revealed, the code will be corrected.

Ritual stones and Dragon God's Seals are only available for snake equipment upgrades, as there is no possibility to upgrade talismans with them.
Live: https://catastroph1c.pythonanywhere.com
	
## Technologies
Project is created with:
* Python 3.12.5
* Flask 3.1.0
* HTML5
  
	
## Setup
To run this project perform the following steps

```
$ pip install flask
$ python ./app.py
```

## Info
I am not a professional programmer, the code was written as a hobby with the help of AI tools.
