## Pic2Character ##

### What you need ###
import pygame ———— pip install <font color="#dd0000">pygame</font>

import cv2 ———— pip install <font color="#dd0000">opencv-python</font>

### Something you can change ###
+ main.py
+ + block = 8 (it's best)
+ + path = "" (path of picture)
+ + weight = [] (权重 the weight of pixel)
+ qumo.py
+ + block = 15 (it's best)
+ + weight = []
+ list.txt (字符集 characters to cover the picture)
+ Keyboard.ttf (字体 form)

### How to use ###
put a picture in the directory
change the path in main.py
run main.py directly or run qumo.py firstly

### Result ###
<font color="#dd0000">qumo.py</font>
get a new character.txt which contains weights of characters

<font color="#dd0000">main.py</font>
get a trans.jpg and a pygame window showing the progress of covering

