
from tkinter import *
import numpy as np
import cv2
import os

def display(img1):
    cv2.imshow("image", img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




def getContours(img1, img2):
    contours, hirearchy = cv2.findContours(img1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img2, contours, -1, (255,0,0), 1)
    arr0 = []
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        cv2.rectangle(img2, (x,y), (x+w,y+h), (255,0,255), 1)
        arr = [x, w, y, h]
        arr0.append(arr)
    return arr0  


# # Capturing video through ipcam




cap = cv2.VideoCapture('http://192.168.43.1:8080/video') # Taking a picture from Ipcam
while True:
    succ, img = cap.read()
    img = cv2.resize(img, (800,450))
    imgBlur = cv2.GaussianBlur(img, (7,7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, 50, 50)
    kernel = np.ones((4,4))
    imgDilate = cv2.dilate(imgCanny, kernel, iterations=1)
    imgErode = cv2.erode(imgDilate, kernel, iterations=1)
    img0 = img.copy()
    getContours(imgDilate, img0)
    cv2.imshow('image', img0)
    inp = cv2.waitKey(1) & 0xFF
    if inp==ord('k'):
        cap.release()
        cv2.destroyAllWindows()
        break
img00 = img.copy()


# # Extracting high lines from image




lines = cv2.HoughLinesP(imgDilate, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
lines0 = []
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 1)
    arr = [x1, y1, x2, y2]
    lines0.append(arr)


# # Fine tuning to remove duplicate lines




slopes = []
horizontals = []
verticals = []
distY = []
distX = []

for line in lines0:
    x1, y1, x2, y2 = line
    slope = (y2-y1)/(x2-x1)
    if slope<1 and slope>-1:
        horizontals.append(line)
        avg = (y1+y2)/2
        distY.append(avg)
    else:
        verticals.append(line)
        avg = (x1+x2)/2
        distX.append(avg)
    slopes.append(slope)

distX.sort()
distY.sort()
distx = []
disty = []

for i in distX:
    canbeplaced = True
    for j in distx:
        diff = i-j
        if diff<0:
            diff=-diff
        if diff<50:
            canbeplaced = False
            break
    if canbeplaced==True:
        distx.append(i)
        
for i in distY:
    canbeplaced = True
    for j in disty:
        diff = i-j
        if diff<0:
            diff=-diff
        if diff<50:
            canbeplaced = False
            break
    if canbeplaced==True:
        disty.append(i)
        
num1 = distx[0]

for i in range(len(distx)):
    distx[i] -= num1

num2 = distx[len(distx)-1]

for i in range(len(distx)):
    distx[i] = (distx[i]/num2)*800
    
num1 = disty[0]

for i in range(len(disty)):
    disty[i] -= num1

num2 = disty[len(disty)-1]

for i in range(len(disty)):
    disty[i] = (disty[i]/num2)*450
    
for i in range(len(distx)):
    distx[i] = int(distx[i])
    
for i in range(len(disty)):
    disty[i] = int(disty[i])
    
ndivs = (len(distx)-1)*(len(disty)-1)

percentagesV = []
percentagesH = []

for x in distx:
    percent = int((x/800)*100)
    percentagesV.append(percent)
    
for y in disty:
    percent = int((y/450)*100)
    percentagesH.append(percent)


# # Code to generate html and css files



from random import random

colors = []

for i in range(ndivs):
    ranum = (int(random()*100))/100
    color = 'rgba(0, 0, 0, '+str(ranum)+')'
    colors.append(color)
    
# the directory where the file needs to be created
f = open(r'E:\tonyStark\@projects\gridCreator\temp\test.html' , 'w')
s0 = f'''<html>
<head>
    <meta http-equiv="refresh" content="1" >
    <link rel="stylesheet" type="text/css" href="main.css">
    <title></title>
</head>
<body>
<div id="header">
'''
s2 = '''
</div>
</body>
</html>
'''

temp=0
s = s0

for temp in range(ndivs):
    s1 = f'''
        <div id="name{temp}"></div>
'''
    s = s+s1

s = s+s2


f.write(s)
f.close()

def update():
    rows = []
    columns = []
    for i in range(1, len(percentagesH)):
        diff = percentagesH[i] - percentagesH[i-1]
        rows.append(diff)

    for i in range(1, len(percentagesV)):
        diff = percentagesV[i]-percentagesV[i-1]
        columns.append(diff)
        
    f = open(r'E:\tonyStark\@projects\gridCreator\temp\main.css', 'w')

    c0 = '''*{
        margin:0;
    }

html, body{
    height:100vh;
}

#header{
    width:100%;
    height:100%;
    display:grid;
    grid-template-rows:
    '''
    for i in range(len(rows)):
        temp = str(rows[i])+'% '
        c0 = c0+temp
    c0 = c0+''';
    grid-template-columns:
    '''

    for i in range(len(columns)):
        temp = str(columns[i])+'% '
        c0 = c0+temp
    c0 = c0 + ''';
    grid-template-areas:
    '''

    for i in range(len(rows)):
        c0 = c0 + '"'
        for j in range(len(columns)):
            c0 = c0 + 'area'+ str(i) + str(j) + ' '
        c0 = c0 + '"'+'\n'

    c0 = c0 + '}' + '\n'

    for i in range(ndivs):
        c0 = c0+'#name'+str(i)+'''{
        grid-area : area'''
        c0 = c0+ str(int(i/len(columns)))+str(i%(len(columns)))+ ';\n'
        c0 = c0 + f'\t\tbackground-color: {colors[i]}' + '\n' + '}' + '\n'

    f.write(c0)
    f.close()
    
update()


# # Tkinter GUI display of grid



root = Tk()

tem = 20

clickedOnce = 0

color0 = '33313b'
color1 = 'eeeeee'
color2 = 'ffffff'
colorHighlighted = 'f64668'

canvas = Canvas(root, width=830, height=480, bg='#'+color0)
canvas.pack()



linesh = []
linesv = []

percentv = []
percenth = []


for x in distx:
    line = canvas.create_line(x, 0, x, 450, width=3, fill='#'+color1)
    linesv.append(line)
    percent = int((x/800)*100)
    text = canvas.create_text(x, 470, text=str(percent)+'%', fill='#'+color2)
    percentv.append(text)
    
for y in disty:
    line = canvas.create_line(0, y, 800, y, width=3, fill='#'+color1)
    linesh.append(line)
    percent = int((y/450)*100)
    text = canvas.create_text(820, y, text=str(percent)+'%', fill='#'+color2)
    percenth.append(text)
    
def hover(event):
    update()
    for line in linesh:
        x0, y0, x1, y1 = canvas.coords(line)
        x = event.x
        y = event.y
        diff = y-y1
        if diff<0:
            diff=-diff
            

        if diff<10:
            canvas['cursor'] = 'fleur'
            canvas.itemconfig(line, fill='#'+colorHighlighted)
            return
        else:
            canvas['cursor'] = ''
            canvas.itemconfig(line, fill='#'+color1)
            
    for line in linesv:
        x0, y0, x1, y1 = canvas.coords(line)
        x = event.x
        y = event.y
        diff = x-x1
        if diff<0:
            diff=-diff

        if diff<10:
            canvas['cursor'] = 'fleur'
            canvas.itemconfig(line, fill='#'+colorHighlighted)
            return
        else:
            canvas['cursor'] = ''
            canvas.itemconfig(line, fill='#'+color1)


        
def drag(event):
    i=-1
    for line in linesh:
        i+=1
        x0, y0, x1, y1 = canvas.coords(line)
        x = event.x
        y = event.y
        diff = y-y1
        if diff<0:
            diff=-diff
        if diff<10:
            canvas.coords(line, 0, y, 800, y)
            percent = int((y/450)*100)
            canvas.itemconfig(percenth[i], text=str(percent)+'%')
            canvas.coords(percenth[i], 820, y)
            percentagesH[i] = percent
    i=-1  
    for line in linesv:
        i+=1
        x0, y0, x1, y1 = canvas.coords(line)
        x = event.x
        y = event.y
        diff = x-x1
        if diff<0:
            diff=-diff
        if diff<10:
            canvas.coords(line, x, 0, x, 450)
            percent = int((x/800)*100)
            canvas.itemconfig(percentv[i], text=str(percent)+'%')
            canvas.coords(percentv[i], x, 470)
            percentagesV[i] = percent
    update()
            
canvas.bind('<Motion>', hover)

canvas.bind('<B1-Motion>', drag)

canvas.create_rectangle(5, 5, 800, 450, width=3, outline='#c0c0c0')
root.mainloop()







