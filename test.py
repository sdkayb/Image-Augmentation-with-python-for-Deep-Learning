from PIL import Image , ImageDraw
import numpy as np
from math import cos , sin , pi

tom = Image.open("C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/tom.jpg")
tom = tom.convert("RGBA")
tom = tom.resize((250,250))
blue  = Image.new("RGBA", (500,500), "blue" )
blue2 = Image.new("RGBA", (500,500), "blue" )

pos = (0,0)
angle = - pi/4
rot = tom.rotate( angle *(180/pi) , expand=1 )
print(rot.size)
blue.paste( rot , pos , rot )
blue2.paste(tom , (50,50) , tom )


i = (0 , 0 , 250 , 250)
ii = np.array(i).reshape((2,2))
ii = np.insert(ii , 1 , ii.diagonal(), axis = 0) 
ii = np.insert(ii , 3 , ii.diagonal()[::-1] , axis = 0)
print("ii=" , ii , '\n')

c = (ii[2]+ii[0]) / 2
print("center = " , c)
ncenter = np.array([rot.size[0]/2 , rot.size[1]/2])
print("new center = " , ncenter, '\n')

draw = ImageDraw.Draw(blue)
draw2 = ImageDraw.Draw(blue2)
rm = np.array([[cos(angle) , sin(angle)] , [-sin(angle) , cos(angle)]])
print("rotation matrix = " , rm, '\n')
nc=[]
for i in ii : 
    nc.append(rm.dot(i-c)+c)

print("rot * coord = " , nc, '\n')



def rotatePolygon(points , center, angle):
        angle = - angle*np.pi/180 #in radian
        return np.dot(np.array(points)-list(center),np.array([[np.cos(angle),np.sin(angle)],[-np.sin(angle),np.cos(angle)]])) + center

hh = (rotatePolygon(ii , c , -45))

A = tuple(hh[0]  +ncenter-c)
B = tuple(hh[1]  +ncenter-c)
C = tuple(hh[2]  +ncenter-c)
D = tuple(hh[3]  +ncenter-c)

l = [A,B,C,D]
print("new coords = " , l)
xl , yl = [] , []
for i in l :
    xl.append(i[0])
    yl.append(i[1])

xmin = min(xl)
xmax = max(xl)
ymin = min(yl)
ymax = max(yl)    

draw.rectangle((xmin, ymin, xmax, ymax), outline=(255, 255, 255))


draw2.polygon(((50,50) , (300,50) , (300,300) , (50,300)),  outline=(255, 0, 0) )
draw.polygon((A,B,C,D),  outline=(255, 0, 0) )

blue.show()
blue2.show()
