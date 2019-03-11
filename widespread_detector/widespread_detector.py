from PIL import Image, ImageChops

# The size of the middle margin that we want to check out
margin_width_default = 50 # pixels

# The threshold used to convert an image to a black and white binary, this is the value that you should play with if the image has dusk or a faint pattern as background
threshold_default = 150 # 0 black -> 255 white

def isWidespread(img,margin_width=margin_width_default,threshold=threshold_default):

        if not isinstance(img,Image.Image):
                # We try to create an Image object if we haven't received one yet
                img = Image.open(img)

        # 1- We just want to analyze the middle margin, so we crop it out
        middle_crop = getMiddleMarginCrop(img,margin_width)

        # 2 - The crop needs to be a black and white binary (this way we can remove the dusk, ignore backgrounds with subtle patterns...)
        middle_crop = getBlackWhiteBinary(middle_crop,threshold)

        # 3 - Now that we have a clean crop we can check out if it's a solid color (black or white) or if it's a mix (black and white)
        if not isSolidColor(middle_crop):   
            #The crop mixes colours, but we need to analyze its two halves to be really sure that it's a widespread
            left, right = getImageHalves(middle_crop)

            #If one of the halves is solid it means that the image is likely two pictures sticked together
            return not isSolidColor(left) and not isSolidColor(right)
        else:
            #The middle crop is a full color, so it's pretty likely that it's not a widespread
            return False

def getMiddleMarginCrop(img,margin_width=margin_width_default):
        #1-We need to know where is the middle of the image and how big the crop needs to be
        middle_point = int(img.width/2)
        half_margin = int(margin_width)

        #2-Now we need the exact coords of the margin to crop it out
        left = middle_point - half_margin
        top = 0
        right = middle_point + half_margin
        bottom = img.height

        return img.crop((left,top,right,bottom))

def getBlackWhiteBinary(img, threshold = threshold_default):
        # The image need to be a grayscale
        img = img.convert('L')

        # We iterate over all the image points to change them to black or white using the threshold to decide 
        return img.point(lambda x: 0 if x<threshold else 255, '1')

def isSolidColor(img):
        # At this point the image should be black, white or a mixed between the two, so we should be able to determine if it's or not a solid color using the boundingbox ( https://pillow.readthedocs.io/en/4.1.x/reference/Image.html#PIL.Image.Image.getbbox )
        return not ImageChops.invert(img).getbbox() or not img.getbbox()

def getImageHalves(img):
        middle_point = int(img.width/2)

        left = img.crop((0,0,middle_point,img.height))
        right = img.crop((middle_point,0,img.width,img.height))

        return left,right