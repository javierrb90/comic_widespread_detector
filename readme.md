# Comic Widespread Detector

Analyzes a given comic or manga double page and tries to determine if it's a widespread or just two single pages glued together
## Getting Started


### Installing



```
pip install git+https://github.com/javierrb90/widespread_detector.git
```
```
pip install -r requirements.txt
```


### How to use

The heart of the package is the isWidespread() definition, analyzes an image (it can be a Pillow object or just a string of the path to the file) and returns a boolean with its verdict

```
import widespread_detector as wd
from PIL import Image

print ( wd.isWidespread( Image.open("samples/widespread.png") ) ) #returns True
```
```
import widespread_detector as wd
from PIL import Image

print ( wd.isWidespread( Image.open("samples/single_glued_01.png") ) ) #returns False
```
or
```
import widespread_detector as wd

print ( wd.isWidespread( "samples/widespread.png" ) ) #returns True
```
```
import widespread_detector as wd

print ( wd.isWidespread("samples/single_glued_01.png") ) #returns False
```

The analysis is made checking out the middle margin of the image that separates its two halves: if it's a solid color then the image is most likely two separate pictures glued together, because that'd mean that there's not anything drawed on the middle margin.

First we crop out the middle margin of the image, then we convert it to a grayscale so we can iterate its points and change them to black or white based on a certain threshold, this way we are able to clean all the dusk (if the image has been scanned) and ignore subtle patterns of the background.

The analysis is then completed after determining if the middle margin croped out (now converted to a black and white binary) is or not a solid color.

If True it means that the middle margin is empty and doesn't have any drawning.


The result of the analysis is determinated by two values: 
* The width of the margin on pixels, it's 50 by default (25px to the left and 25px to the right, from the middle point of the image ).

* The threshold to convert the gray scaled colors to black or white (150 by default, everything above it is turned white and everything under it is turned black)

You can change these values passing them as args when you analyse an image:

```
import widespread_detector as wd

wd.isWidespread("samples/single_glued_01.png",margin_width=20,threshold=100)
```

