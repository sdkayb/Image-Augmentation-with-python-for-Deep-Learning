from PIL import Image , ImageDraw
import xml.etree.ElementTree as et
import numpy as np
import operator
import math
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

#extracting coordinates from the labeling files storing in dicts
d_rect={}
d_square={}
for x in rect_root.findall("object"):
    name = x.find("name").text
    y = x.find("bndbox")
    t = [int(y.find('xmin').text) , int(y.find('ymin').text) , int(y.find('xmax').text) , int(y.find('ymax').text)]
    d_rect[name] = t
for x in square_root.findall("object"):
    name = x.find("name").text
    y = x.find("bndbox")
    t = [int(y.find('xmin').text) , int(y.find('ymin').text) , int(y.find('xmax').text) , int(y.find('ymax').text)]
    d_square[name] = t


class Block:
    def __init__(self , name , image , lb_file , coord):
        self.name = name
        self.image = image
        self.lb_file=lb_file
        self.coord=coord
        self.old_center = None
        self.new_coord = None
        self.size = np.array([self.coord[2]-self.coord[0] , self.coord[3]-self.coord[1]])

    def getCenter (self):
        l=self.coord
        c = np.array([ l[2]-(l[2]-l[0])/2 , l[3]-(l[3]-l[1])/2 ])
        return c

    def Crop(self ):
        crp = Image.open(self.image).crop(self.coord)
        return crp 

    def Rotate(self , angle):
        rot = self.Crop().rotate(angle, expand = True , fillcolor = "black")
        return rot

    def Place(self , pos):
        copy = Image.open(img_backgrd_path).copy()
        copy.paste(self.Crop() , pos)
        return copy

    def getNewCenter(self , pos) :
        l=self.coord
        c = self.getCenter()
        if l[0]<pos[0]:
            if l[1]<pos[1]:
                nc = c + np.array(pos)
            elif l[1]>pos[1]: 
                nc = [ c[0]+pos[0] , c[1]-pos[1] ]
        elif l[0]>pos[0]:
            if l[1]<pos[1]:
                nc = [ c[0]-pos[0] , c[1]+pos[1] ]
            elif l[1]>pos[1]:
                nc = c - np.array(pos)
        return nc

    def newCoord(self):
        pass
    def drawBBox(self):
        pass

#creartin list of the basic shapes or blocks
base_blocks = []
for e in d_rect:
    base_blocks.append( Block(name = e ,image =img_rect_path , lb_file =rect_lb_file_path , coord = d_rect[e] ))       
for e in d_square:
    base_blocks.append( Block(name = e , image = img_squares_path , lb_file =square_lb_file_path , coord = d_square[e] )) 
'''
base_blocks[0].Crop().show()
base_blocks[1].Rotate(50).show()'''
base_blocks[2].Place((0,0)).show()
print(base_blocks[2].size , base_blocks[2].getNewCenter([0,0]))
#image processing 
'''
img_rect = Image.open(img_rect_path)
img_squares = Image.open(img_squares_path)
img_backgrd = Image.open(img_backgrd_path)


for elm in d_rect:
    coord = d_rect[elm]
    angle = random.randint(0,180)
    crp = img_rect.crop(coord).rotate(angle , expand = True , fillcolor = "black")
    copy = img_backgrd.copy()
    xlim = img_backgrd.size[0]-crp.size[0]
    ylim = img_backgrd.size[1]-crp.size[1]
    place = (random.randint(0,xlim),random.randint(0,ylim))
    copy.paste(crp , place)
    copy.show()

for elm in d_square:
    coord = d_square[elm]
    angle = random.randint(1,180)
    crp = img_squares.crop(coord).rotate(angle , expand = True , fillcolor = "black" )
    copy = img_backgrd.copy()
    xlim = img_backgrd.size[0]-crp.size[0]
    ylim = img_backgrd.size[1]-crp.size[1]
    place = (random.randint(0,xlim),random.randint(0,ylim))
    copy.paste(crp , place)
    copy.show()'''