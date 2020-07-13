from PIL import Image , ImageDraw
import xml.etree.ElementTree as et
import numpy as np
import operator
from math import cos , sin 
import random

#reading labeling files and storing data in dicts
rect_lb_file_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/rects_lb.xml"
square_lb_file_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/squares_lb.xml"
img_rect_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/rectss.png"
img_squares_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/squares.png"
img_backgrd_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/background.png"

rect_tree = et.parse(rect_lb_file_path)
square_tree = et.parse(square_lb_file_path)
rect_root = rect_tree.getroot()
square_root = square_tree.getroot()

#extracting coordinates as (4x2) matrix , from the labeling files then storing in dicts
d_rect={}
d_square={}
for x in rect_root.findall("object"):
    name = x.find("name").text
    y = x.find("bndbox")
    t = np.array([int(y.find('xmin').text) , int(y.find('ymin').text) , int(y.find('xmax').text) , int(y.find('ymax').text)])
    t = np.reshape(t , (2,2))
    t = np.insert( t , 1 , [t[1,0],t[0,1]] , axis=0)
    t = np.insert( t , 3 , [t[0,0],t[2,1]] , axis=0)
    d_rect[name] = t

for x in square_root.findall("object"):
    name = x.find("name").text
    y = x.find("bndbox")
    t = np.array([int(y.find('xmin').text) , int(y.find('ymin').text) , int(y.find('xmax').text) , int(y.find('ymax').text)])
    t = np.reshape(t , (2,2))
    t = np.insert( t , 1 , [t[1,0] , t[0,1]] , axis=0)
    t = np.insert( t , 3 , [t[0,0] , t[2,1]] , axis=0)
    d_square[name] = t

img_rect = Image.open(img_rect_path)
img_squares = Image.open(img_squares_path)
img_backgrd = Image.open(img_backgrd_path)

class Block:
    def __init__(self , name , image , lb_file , coord):
        self.name = name
        self.image = image
        self.lb_file = lb_file
        self.coord = coord
        self.size = np.array(self.coord[2]-self.coord[0])
        self.old_center = np.array( self.coord[2] - (self.size/2) )
        self.new_coord = None
        
    #methods to manipulate blocks 
    def getCenter (self):
        l=self.coord
        c = np.array( self.coord[2] - (self.size/2) )
        print(self.size)
        return c

    def Crop(self ):
        crp = Image.open(self.image).crop(tuple(np.reshape( self.coord , (1,4) ))[0])
        return crp 

    def Rotate(self , angle):
        rot = self.Crop().rotate(angle, expand = True , fillcolor = "black")
        return rot

    def Place(self , pos , angle):
        copy = Image.open(img_backgrd_path).copy()
        copy.paste(self.Rotate(angle) , pos)
        self.drawMask()
        return copy

    #methods to deal with coordiantes and bboxes
    def getNewCenter(self , pos) :
        l = self.coord
        c = self.getCenter()
        nc = c + (np.array(list(pos)) - l[0])
        return nc

    def getNewCoord(self , angle , pos):
        l = self.coord
        c = self.getCenter()
        rm = np.array([[cos(angle) , sin(angle)] , [-sin(angle) , cos(angle)]])
        tv = (np.array(list(pos)) - l[0])
        nc = self.getNewCenter(pos) 
        fnc = [ ( (l[0] + tv) - nc ).dot(rm) , ( (l[1] + tv) - nc ).dot(rm) ]
        return fnc

    def drawBBox(self):
        arg = self.new_coord
        im = Image.open(img_backgrd)
        draw = ImageDraw.Draw(im)
        draw.rectangle( arg , outline=(0, 255, 0))

    def drawMask(self) : 
        arg = self.new_coord
        im = Image.open(img_backgrd)
        draw = ImageDraw.Draw(im)
        draw.rectangle( arg , outline=(0, 255, 0))


#creartin list of the basic shapes or blocks
base_blocks = []
for e in d_rect:
    base_blocks.append( Block(name = e , coord = d_rect[e] , image =img_rect_path , lb_file =rect_lb_file_path  ))       
for e in d_square:
    base_blocks.append( Block(name = e , coord = d_square[e] , image = img_squares_path , lb_file =square_lb_file_path  )) 

new_blocks = []
#------- generating new images



print(base_blocks[0].getCenter() ,'\n\n', base_blocks[0].coord)
'''
base_blocks[0].Crop().show()
base_blocks[1].Rotate(50).show()
base_blocks[2].Place((0,0)).show()
print(base_blocks[2].size , base_blocks[2].getNewCenter([0,0]))
base_blocks[0].Place((0,0) , 20).show()
'''

#image processing 
'''
for elm in d_rect:
    coord = d_rect[elm]
    angle = random.randint(0,180)
    crp = img_rect.crop(coord).rotate(angle , expand = True , fillcolor = "black")
    copy = img_backgrd.copy()
    xlim = img_backgrd.size[0] - crp.size[0]
    ylim = img_backgrd.size[1] - crp.size[1]
    place = (random.randint(0,xlim),random.randint(0,ylim))
    copy.paste(crp , place)
    copy.show()

for elm in d_square:
    coord = d_square[elm]
    angle = random.randint(0,180)
    crp = img_squares.crop(coord).rotate(angle , expand = True , fillcolor = "black" )
    copy = img_backgrd.copy()
    xlim = img_backgrd.size[0]-crp.size[0]
    ylim = img_backgrd.size[1]-crp.size[1]
    place = (random.randint(0,xlim),random.randint(0,ylim))
    copy.paste(crp , place)
    copy.show()
    '''