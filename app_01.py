#importing lib
from PIL import Image , ImageDraw , ImageFont
import xml.etree.ElementTree as et
import numpy as np
import operator
from math import cos , sin , pi
import random

#reading labeling files and storing data in dicts:
rect_lb_file_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/rects_lb.xml"
square_lb_file_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/squares_lb.xml"
img_rect_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/rectss.png"
img_squares_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/squares.png"
img_backgrd_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/background.png"

rect_tree = et.parse(rect_lb_file_path)
square_tree = et.parse(square_lb_file_path)
rect_root = rect_tree.getroot()
square_root = square_tree.getroot()

#extracting coordinates as (4x2) matrixs , from the labeling files then storing in dicts:
d_rect={}
d_square={}
for x in rect_root.findall("object"):
    name = x.find("name").text
    y = x.find("bndbox")
    d = (int(y.find('xmin').text) , int(y.find('ymin').text) , int(y.find('xmax').text) , int(y.find('ymax').text))
    t = np.array([int(y.find('xmin').text) , int(y.find('ymin').text) , int(y.find('xmax').text) , int(y.find('ymax').text)])
    t = np.reshape(t , (2,2))
    t = np.insert( t , 1 , [t[1,0],t[0,1]] , axis=0)
    t = np.insert( t , 3 , [t[0,0],t[2,1]] , axis=0)
    d_rect[name] = [t , d]

for x in square_root.findall("object"):
    name = x.find("name").text
    y = x.find("bndbox")
    d = (int(y.find('xmin').text) , int(y.find('ymin').text) , int(y.find('xmax').text) , int(y.find('ymax').text))
    t = np.array([int(y.find('xmin').text) , int(y.find('ymin').text) , int(y.find('xmax').text) , int(y.find('ymax').text)])
    t = np.reshape(t , (2,2))
    t = np.insert( t , 1 , [t[1,0] , t[0,1]] , axis=0)
    t = np.insert( t , 3 , [t[0,0] , t[2,1]] , axis=0)
    d_square[name] = [t , d]

#opening base images:
img_rect = Image.open(img_rect_path)
img_squares = Image.open(img_squares_path)
img_backgrd = Image.open(img_backgrd_path)

#print(d_square)

class Block :
    def __init__(self , name , image , lb_file , coord , diag ):
        self.name = name 
        self.image = image 
        self.lb_file = lb_file
        self.coord = coord
        self.size = np.array(self.coord[2]-self.coord[0])
        self.diag = diag
        self.new_image = None
        self.new_lb_file = None
    
    def getCenter(self):
        c = np.array( self.coord[2] - (self.size/2) )
        return c

    def Crop(self ):
        crp = Image.open(self.image).crop(self.diag)
        return crp 

    def Rotate(self , angle):
        rot = self.Crop().rotate(angle, expand = True , fillcolor = "black")
        return rot

    def Place(self ,angle, pos):
        copy = Image.open(img_backgrd_path).copy()
        copy.paste(self.Rotate(angle) , pos)
        
        return copy

    def getNewCoord (self , angle , pos) : 
        rm = np.array([[cos(angle*pi/180) , sin(angle*pi/180)] , [-sin(angle*pi/180) , cos(angle*pi/180)]])
        c = self.getCenter()
        #print("rotation matrix = " , rm , "center = " , c)
        nc=[]
        for i in self.coord : 
            nc.append((rm.dot(i-c)) + c)
        #print(nc)

        #bounding_box
        xl , yl = [] , []
        for i in nc :
            xl.append(i[0])
            yl.append(i[1])
        xmin = min(xl)
        xmax = max(xl)
        ymin = min(yl)
        ymax = max(yl)

        nc = np.array(nc) + (np.array(pos)-np.array([xmin , ymin]))
        return nc

    def getNewCenter(self , angle , pos):
        size = np.array(self.Rotate(angle).size)
        newcoord = self.getNewCoord(angle , pos)
        xl , yl = [] , []
        for i in newcoord :
            xl.append(i[0])
            yl.append(i[1])
        xmin = min(xl)
        xmax = max(xl)
        ymin = min(yl)
        ymax = max(yl)
        bbox = np.array([xmax , ymax])
        nc = bbox - (size/2)
    
        return nc

    def drawMask(self , angle , pos) :
        pic = self.Place(angle , pos)
        draw = ImageDraw.Draw(pic)
        l = self.getNewCoord(angle , pos)
        AA = tuple(l[0])
        B  = tuple(l[1])
        C  = tuple(l[2])
        D  = tuple(l[3])
        draw.line((AA,B,C,D,AA), width=10 , fill="red" )
        return pic

    def drawBBox(self , angle , pos ):
        pic = self.Place(angle , pos)
        draw = ImageDraw.Draw(pic)
        nc = self.getNewCoord(angle , pos)
        xl , yl = [] , []
        for i in nc :
            xl.append(i[0])
            yl.append(i[1])
        xmin = min(xl)
        xmax = max(xl)
        ymin = min(yl)
        ymax = max(yl)
        draw.rectangle((xmin, ymin, xmax, ymax), width = 10 ,outline=(255, 0, 0))
        fnt = ImageFont.truetype( font = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/IntroDemo-BlackCAPS.ttf" , size = 50)
        draw.text((xmin,ymax-60) , font = fnt , text = self.name )
        return pic

    def drawNewCenter(self , angle ,pos):
        pic = self.Place(angle , pos)
        draw = ImageDraw.Draw(pic)
        nc = self.getNewCenter(angle , pos)
        nc = np.insert(nc , 2 , nc+20 , axis = 0)
        print(nc)
        #p = list(map(tuple, nc))
        draw.ellipse(list(nc) , fill ="#ffff33", outline ="red" )
        return pic
    
    def labeling(self , angle ,pos , compteur):
        nc = self.getNewCoord(angle , pos)
        xl , yl = [] , []
        for i in nc :
            xl.append(i[0])
            yl.append(i[1])
        xmin = min(xl)
        xmax = max(xl)
        ymin = min(yl)
        ymax = max(yl)
    
        self.new_image = 'img_'+ str(compteur)
        self.new_lb_file = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/gen_lb.csv"
        with open("gen_lb.csv" , mode = 'a') as f:
            f.write('\n{},{},{},{},{},{},{}'.format(self.new_image , self.name , xmin , ymin , xmax , ymax , self.getNewCoord(angle , pos)))
        
#creartin list of the basic shapes or blocks
base_rect_blocks = []
for e in d_rect:
    base_rect_blocks.append( Block(name = e , coord = d_rect[e][0] , image =img_rect_path , lb_file =rect_lb_file_path , diag=d_rect[e][1]  ))     
base_square_blocks = []  
for e in d_square:
    base_square_blocks.append( Block(name = e , coord = d_square[e][0] , image = img_squares_path , lb_file =square_lb_file_path , diag=d_square[e][1] )) 

base_blocks = base_rect_blocks + base_square_blocks
compt = 0
for i in base_blocks:
    compt +=1 
    angle_rot = random.randint(0,180)
    xlim = img_backgrd.size[0]-i.Rotate(angle_rot).size[0]
    ylim = img_backgrd.size[1]-i.Rotate(angle_rot).size[1]
    position = (random.randint(0,xlim),random.randint(0,ylim))
    print(compt)
    #i.Place(angle_rot , position).show()
    #i.drawBBox(angle_rot , position).show()
    i.labeling(angle_rot , position , compt)
    #i.Place(angle_rot , position).save()

