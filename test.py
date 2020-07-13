from PIL import Image , ImageDraw
import numpy as np
from math import cos , sin , pi

tom = Image.open("C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/tom.jpg")
tom = tom.convert("RGBA")
tom.thumbnail((250,250))
blue  = Image.new("RGBA", (500,500), "blue" )
blue2 = Image.new("RGBA", (500,500), "blue" )

pos = (0,0)
angle = - pi/4
rot = tom.rotate( angle *(180/pi) , expand=1 )
blue.paste( rot , pos , rot )
blue2.paste(tom , pos , tom )

i = (0,0,250,250)
ii = np.array(i).reshape((2,2))
ii = np.insert(ii , 1 , ii.diagonal(), axis = 0) 
ii = np.insert(ii , 3 , ii.diagonal()[::-1] , axis = 0)
print(ii , '\n')

c = (ii[2]+ii[0]) / 2

print(c, '\n')

draw = ImageDraw.Draw(blue)
draw2 = ImageDraw.Draw(blue2)
rm = np.array([[cos(angle) , sin(angle)] , [-sin(angle) , cos(angle)]])
print(rm, '\n')
nc=[]
for i in ii : 
    nc.append(rm.dot(i-c)+c)

print(nc, '\n')

'''

draw2.polygon(((50,50) , (300,50) , (300,300) , (50,300)),  outline=(255, 0, 0) )
draw.polygon((A,B,C,D),  outline=(255, 0, 0) )

blue.show()
blue2.show()
'''