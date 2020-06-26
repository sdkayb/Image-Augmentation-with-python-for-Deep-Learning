from PIL import Image
import xml.etree.ElementTree as et
import random

class Block:
    def __init__(self,name , lb_file,coord):
        self.name = name
        self.lb_file=lb_file
        self.coord=coord

    def Crop(self,lb_file,crp_img):
        self.lb_file=lb_file
        self.crp_img=crp_img
        
#reading labeling files and storing data in dicts

rect_tree = et.parse("C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/images/rects_lb.xml")
square_tree = et.parse("C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/images/squares_lb.xml")
rect_root = rect_tree.getroot()
square_root = square_tree.getroot()
d_rect={}
d_square={}
for x in rect_root.findall("object"):
    name = x.find("name").text
    y = x.find("bndbox")
    t = (int(y.find('xmin').text) , int(y.find('ymin').text) , int(y.find('xmax').text) , int(y.find('ymax').text))
    d_rect[name] = t
for x in square_root.findall("object"):
    name = x.find("name").text
    y = x.find("bndbox")
    t = (int(y.find('xmin').text) , int(y.find('ymin').text) , int(y.find('xmax').text) , int(y.find('ymax').text))
    d_square[name] = t

#image processing 
    
img_rect = Image.open("C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/images/rectss.png")
img_squares = Image.open("C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/images/squares.png")
img_backgrd = Image.open("C:/Users/sdkay/Documents/INPT/s2/p2/projet pfa/images/background2.png")


for elm in d_rect:
    coord = d_rect[elm]
    angle = random.randint(0,180)
    crp = img_rect.crop(coord).rotate(angle , expand = True )
    copy = img_backgrd.copy()
    xlim = img_backgrd.size[0]-crp.size[0]
    ylim = img_backgrd.size[1]-crp.size[1]
    place = (random.randint(0,xlim),random.randint(0,ylim))
    copy.paste(crp , place)
    copy.show()

for elm in d_square:
    coord = d_square[elm]
    angle = random.randint(0,180)
    crp = img_squares.crop(coord).rotate(angle , expand = True )
    copy = img_backgrd.copy()
    xlim = img_backgrd.size[0]-crp.size[0]
    ylim = img_backgrd.size[1]-crp.size[1]
    place = (random.randint(0,xlim),random.randint(0,ylim))
    copy.paste(crp , place)
    copy.show()