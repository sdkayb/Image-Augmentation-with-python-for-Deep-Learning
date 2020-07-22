#importing lib
from PIL import Image , ImageDraw , ImageFont
import xml.etree.ElementTree as et
import numpy as np
import operator
from math import cos , sin , pi
import random
import copy

class Block :
    img_backgrd_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/background.png"
    font_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/IntroDemo-BlackCAPS.ttf"
    def __init__(self , name , image , lb_file , coord , diag ):
        self.name = name 
        self.image = image 
        self.lb_file = lb_file
        self.coord = coord
        self.diag = diag
        self.new_image = None
        self.new_lb_file = None
        self.new_coord = None
        self.new_diag = None
        self.size = np.array(self.coord[2]-self.coord[0])
        self.angle = None
        self.position = None
    
    #calculates center of the block befor rotation and traslation
    def getCenter(self):
        c = np.array( self.coord[2] - (self.size/2) )
        return c
    
    #crops clock image from the base image
    def Crop(self ):
        crp = Image.open(self.image).crop(self.diag)
        return crp 
    
    #creates image of the block after rotation and translation
    def Rotate(self , angle):
        rot = self.Crop().rotate(angle, expand = True , fillcolor = "black")
        return rot
    
    #creates image of the block on backround image after rotation and translation
    def Place(self ,angle, pos, image = img_backgrd_path):
        copy = Image.open(image).copy()
        copy.paste(self.Rotate(angle) , pos)
        
        return copy
    
    #calculates the coordinates of the 4 corners of the block after rotation and traslation
    def getNewCoord (self , angle , pos) : 
        rm = np.array([[cos(angle*pi/180) , sin(angle*pi/180)] , [-sin(angle*pi/180) , cos(angle*pi/180)]])
        c = self.getCenter()
        nc=[]
        for i in self.coord : 
            nc.append((rm.dot(i-c)) + c)
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
        self.new_coord = nc
        '''xl , yl = [] , []
        for i in nc :
            xl.append(i[0])
            yl.append(i[1])
        xmin = min(xl)
        xmax = max(xl)
        ymin = min(yl)
        ymax = max(yl)
        self.new_diag = [xmin , ymin , xmax , ymax]'''
        return nc
    
    #calculates the coordinates of the new center of the block after rotation and traslation 
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
    
    #draw mask (on the edges of the block)
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
    
    #draw bounding box around the block
    def drawBBox(self , angle , pos , image = img_backgrd_path ):
        pic = self.Place(angle , pos , image)
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
        draw.rectangle((xmin, ymin, xmax, ymax), width = 10 ,outline=(0, 255, 0))
        fnt = ImageFont.truetype( font = Block.font_path , size = 50)
        draw.text((xmin+20,ymax-70) , font = fnt , text = self.name )
        
        self.new_diag = [xmin , ymin , xmax , ymax]
        print('\n Self diagonal updated', [xmin , ymin , xmax , ymax])
        return pic
    
    #calculates the coordinates and draws the new center of the block after rotation and translation
    def drawNewCenter(self , angle ,pos):
        pic = self.Place(angle , pos)
        draw = ImageDraw.Draw(pic)
        nc = self.getNewCenter(angle , pos)
        nc = np.insert(nc , 2 , nc+20 , axis = 0)
        print(nc)
        #p = list(map(tuple, nc))
        draw.ellipse(list(nc) , fill ="#ffff33", outline ="red" )
        return pic
    
    #creating labeling csv file with image,blockname,boundingbox coordinates (object detection),mask coordinate (segmentation)
    def labeling(self ,compteur, csv_path):
        nc = self.getNewCoord(self.angle , self.position)
        xl , yl = [] , []
        for i in nc :
            xl.append(i[0])
            yl.append(i[1])
        xmin = min(xl)
        xmax = max(xl)
        ymin = min(yl)
        ymax = max(yl)
    
        self.new_image = 'img_'+ str(compteur)+'.png'
        self.new_lb_file = csv_path
        with open("gen_lb.csv" , mode = 'a') as f:
            f.write('\n{},{},{},{},{},{},{}'.format(self.new_image , self.name , xmin , ymin , xmax , ymax , self.getNewCoord(self.angle , self.position)))
    
    #checks if two blocks are not one on top of the other
    def checkNotOverlap(self , bl ):
        c1 = self.new_diag
        c2 = bl.new_diag
        print("c1" , c1)
        print("c2" , c2)
        if c2[0]>c1[2]+10 or c2[1]>c1[3]+10 or c2[2]<c1[0]-10 or c2[3]<c1[1]-10 :
            print('no ovelap')
            
            return True 
        else : 
            print('overlap')
            return False
    
    #check if each new crop is not overlapping with others
    def doMultipleOverlap(self, blocklist):
        for block in blocklist:
            if self.checkNotOverlap(block):
                continue
            else:
                return False
        return True

    #generate angle and position 
    def generateAP(self):
        angle = random.randint(0,18)
        angle = angle *10
        xlim = img_backgrd.size[0]-self.Rotate(angle).size[0]
        ylim = img_backgrd.size[1]-self.Rotate(angle).size[1]
        position = (random.randint(5,xlim-5),random.randint(5,ylim-5))
        return angle , position

    #pick random block objects from the baseblocks 
    def chooseRandomBlocks(baselist):
        # 5 is max number of blocks to have on a picture
        i = random.randrange(3, 6)
        print('Numbers of choosen Blocks = ' + str(i))
        return random.choices(baselist, k=i)




if __name__=="__main__":

#################################### DATA FETCHING ###################################################

    #reading labeling files and storing data in dicts:
    rect_lb_file_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/rects_lb.xml"
    square_lb_file_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/squares_lb.xml"
    img_rect_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/rects.png"
    img_squares_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/squares.png"
    img_backgrd_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/images/background.png"
    csv_path = "C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/code/gen_lb.csv"

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

    #creartin list of the basic shapes or blocks
    base_rect_blocks = []
    for e in d_rect:
        base_rect_blocks.append( Block(name = e , coord = d_rect[e][0] , image =img_rect_path , lb_file =rect_lb_file_path , diag=d_rect[e][1]  ))     
    base_square_blocks = []  
    for e in d_square:
        base_square_blocks.append( Block(name = e , coord = d_square[e][0] , image = img_squares_path , lb_file =square_lb_file_path , diag=d_square[e][1] )) 
    base_blocks = base_rect_blocks + base_square_blocks

    ################################## IMAGES GENERATION ##########################################################
    imageNumber = int(input("Entrer le nombre d'images à générer :"))
    compteur = 0
    for f in range(imageNumber):
        print('NEW IMAGE GENERATION: ',f)
        block_liste=[]

        block_liste = Block.chooseRandomBlocks(base_blocks)
        print('\n New Blocklist: ',[block.name for block in block_liste])
        valid_block = []
        print('Valid_block length', len(valid_block))
        for i in range(len(block_liste)):
            print('Block position in block liste',i)
            ang , position = block_liste[i].generateAP()
            print('\nGenerated angle:',ang, position)

            im = block_liste[i].drawBBox(ang , position)
            if i==0 :
                #im = block_liste[i].drawBBox(ang , position)
                block_liste[0].angle = ang
                block_liste[0].position = position
                sn = copy.deepcopy(block_liste[0])
                valid_block.append(sn)
                print('First block added to valid blocks \n')
                print('Valid Blocks after first block : ',[block.name for block in valid_block])
            else :
                for k in range(20):
                    print('Test Rotation',k)

                    if block_liste[i].doMultipleOverlap(valid_block):
                        block_liste[i].angle = ang
                        block_liste[i].position = position
                        bl = copy.deepcopy( block_liste[i])
                        valid_block.append(bl)
                        print('new block added to valid blocks')
                        print('Valid Blocks after new block : ',[block.name for block in valid_block])
                        break
                    else :
                        ang , position = block_liste[i].generateAP()
                        print('\nnew generated angle:',ang, position)
                        block_liste[i].drawBBox(ang , position)

        print('\nlength of valid_blocks:', len(valid_block))

        new_im = Image.new('RGB', (4500,4500))
        for block in valid_block:
            new_im.paste(block.Crop().rotate(block.angle, expand = True , fillcolor = "black"), block.position)
            block.labeling(compteur,csv_path)
        new_im.show()
        new_im.save(str(compteur)+'.png')
        print('Image printed')
        compteur += 1 
