import os
import sys

from PIL import Image

EXTS = ('.jpg', '.png')
#!defaults##################
foldername = 'WaterMarked' #!
transparency = float(0.5)  #!
pos = 'center'             #!
#!##########################

if len(sys.argv) < 3:
    print('Usage: watermark.py \'image path\' \'logo path\' [0-1]* [topleft, topright, bottomleft, bottomright, center]*')
    print('items marked whith * are optional')
    sys.exit()
elif len(sys.argv) == 4:
    if not(sys.argv[3].isdecimal):
        path = sys.argv[1]
        lgo = sys.argv[2]
        pos = sys.argv[3]
    elif sys.argv[3].isdecimal and sys.argv[3] > 0 and 0 > sys.argv[3]:
        path = sys.argv[1]
        lgo = sys.argv[2]
        transparency = float(sys.argv[3])
    else:
        print("transparency: [" + transparency + "] is not a valid transparency")        
        sys.exit()
elif len(sys.argv) == 5:
    path = sys.argv[1]
    lgo = sys.argv[2]
    transparency = float(sys.argv[3])
    pos = sys.argv[4]
else:
    path = sys.argv[1]
    lgo = sys.argv[2]
    pos = "center" 

logo = Image.open(lgo).convert('RGBA')
logoWidth = logo.width
logoHeight = logo.height
pixeldata = list(logo.getdata())

for i,pixel in enumerate(pixeldata):
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    a = pixel[3]

    #this is to avoid negative alpha values and make the transparency proportional#
    alpha = int(256*transparency)
    alpha = (a - (256 - alpha)) if (a - (256 - alpha)) > 0 else 0 
    ###############################################################################

    if pixel[3] != 0:
        pixeldata[i] = (r, g, b, alpha)

logo.putdata(pixeldata)
if not os.path.isdir(path + '/' + foldername):
    os.mkdir(path + '/' + foldername)

for filename in os.listdir(path):
    if any([filename.lower().endswith(ext) for ext in EXTS]) and filename != lgo:
        image = Image.open(path + '/' + filename)
        imageWidth = image.width
        imageHeight = image.height

        try:
            if pos == 'topleft':
                image.paste(logo, (0, 0), logo)
            elif pos == 'topright':
                image.paste(logo, (imageWidth - logoWidth, 0), logo)
            elif pos == 'bottomleft':
                image.paste(logo, (0, imageHeight - logoHeight), logo)
            elif pos == 'bottomright':
                image.paste(logo, (imageWidth - logoWidth, imageHeight - logoHeight), logo)
            elif pos == 'center':
                image.paste(logo, ((imageWidth - logoWidth)/2, (imageHeight - logoHeight)/2), logo)
            else:
                print('Error: ' + pos + ' is not a valid position')
                print('Usage: watermark.py \'image path\' \'logo path\' [0-1]* [topleft, topright, bottomleft, bottomright, center]*')
                print('items marked whith * are optional')

            image.save(path + '/' + foldername + '/' + filename)
            print('Added watermark to ' + path + '/' + filename + ' in ' + path + '/' + foldername + '/' + filename)

        except:
            image.paste(logo, (int((imageWidth - logoWidth)/2), int((imageHeight - logoHeight)/2)), logo)
            image.save(path + '/' + foldername + '/' + filename)
            print('Added watermark to ' + path + '/' + filename + ' in ' + path + '/' + foldername + '/' + filename)
