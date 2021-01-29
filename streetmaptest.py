from io import BytesIO
from PIL import Image
import requests
from matplotlib import pyplot as plt
# https://bryanbrattlof.com/adding-openstreetmaps-to-matplotlib/
URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png".format
import math
TILE_SIZE = 256

def point_to_pixels(lon, lat, zoom):
    """convert gps coordinates to web mercator"""
    r = math.pow(2, zoom) * TILE_SIZE
    lat = math.radians(lat)

    x = int((lon + 180.0) / 360.0 * r)
    y = int((1.0 - math.log(math.tan(lat) + (1.0 / math.cos(lat))) / math.pi) / 2.0 * r)

    return x, y

#zoom = 16
#x, y = point_to_pixels(-3.3094, 56.0953, zoom)
#x_tiles, y_tiles = int(x / TILE_SIZE), int(y / TILE_SIZE)



# format the url
#url = URL(x=x_tiles, y=y_tiles, z=zoom)

# make the request
#with requests.get(url) as resp:
#    img = Image.open(BytesIO(resp.content))

# plot the tile
#plt.imshow(img)
#plt.show()

# Get more than one tile
lat_max = 56.132276
lat_min = 56.060534
lon_min = -3.3733
lon_max = -3.244456

#################################
#      Multi Tile Visual
#################################
top, bot = lat_max, lat_min
lef, rgt = lon_min, lon_max

zoom = 13
x0, y0 = point_to_pixels(lef, top, zoom)
x1, y1 = point_to_pixels(rgt, bot, zoom)

x0_tile, y0_tile = int(x0 / TILE_SIZE), int(y0 / TILE_SIZE)
x1_tile, y1_tile = math.ceil(x1 / TILE_SIZE), math.ceil(y1 / TILE_SIZE)

assert (x1_tile - x0_tile) * (y1_tile - y0_tile) < 50, "That's too many tiles!"

from itertools import product

# full size image we'll add tiles to
img = Image.new('RGB', (
        (x1_tile - x0_tile) * TILE_SIZE,
        (y1_tile - y0_tile) * TILE_SIZE))

# loop through every tile inside our bounded box
for x_tile, y_tile in product(range(x0_tile, x1_tile),
                              range(y0_tile, y1_tile)):

    with requests.get(URL(x=x_tile, y=y_tile, z=zoom)) as resp:
        tile_img = Image.open(BytesIO(resp.content))

    # add each tile to the full size image
    img.paste(
        im=tile_img,
        box=((x_tile - x0_tile) * TILE_SIZE,\
             (y_tile - y0_tile) * TILE_SIZE))

plt.imshow(img)
plt.savefig('mossmorran_0.png', bbox_inches ="tight")


#################################
#      Crop Lines Visual
#  Don't include this in article
#################################
from PIL import ImageDraw
img2 = img.copy()

# find the mercator coordinates of the top-left corner of all
# the tiles we downloaded from OpenStreetMap
x, y = x0_tile * TILE_SIZE, y0_tile * TILE_SIZE

# draw a red rectangle of the part of the image we want to keep
draw = ImageDraw.Draw(img2)
draw.rectangle(
    (x0 - x,  # left
     y0 - y,  # top
     x1 - x,  # right
     y1 - y), # bottom
    outline=(255, 0, 0),
    width=5)

# draw black rectangles around each individual tile
for x_tile, y_tile in product(range(0, (x1_tile - x0_tile)),
                              range(0, (y1_tile - y0_tile))):

    x, y = x_tile * TILE_SIZE, y_tile * TILE_SIZE
    draw.rectangle(
        (x - 2,  # left
         y - 2,  # top
         (x + TILE_SIZE),  # right
         (y + TILE_SIZE)), # bottom
        outline=(0, 0, 0),
        width=2)

plt.imshow(img2)
plt.savefig('mossmorran.png', bbox_inches ="tight")

#################################
# Cropping The Multi Tile Visual
#################################
x, y = x0_tile * TILE_SIZE, y0_tile * TILE_SIZE

img = img.crop((
    x0 - x,  # left
    y0 - y,  # top
    x1 - x,  # right
    y1 - y)) # bottom

plt.imshow(img)
plt.savefig('mossmorran-cropped.png', bbox_inches ="tight")

#################################
#       Final Visual
#################################
fig, ax = plt.subplots()

ax.set_ylim(bot, top)
ax.set_xlim(lef, rgt)

#ax.scatter(df.lon, df.lat, alpha=0.1, c='red', s=1)
ax.imshow(img, extent=(lef, rgt, bot, top))
plt.show()
plt.savefig('mossmorran_final.png')


