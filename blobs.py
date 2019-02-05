#!/usr/bin/python3.5

from PIL import Image
import random
import math

# image/canvas size
image_x_size = 1920
image_y_size = 1080

# blob properies
blobs = 10
max_blob_size = 1080
min_blob_size = 10
max_alpha = 100

# create background and foreground canvas and set 'pixels' to foreground.
# background is black and fully opaque
background = Image.new ('RGBA', (image_x_size,image_y_size), (0,0,0,255))
# foreground is black but fully transparent
foreground = Image.new ('RGBA', (image_x_size,image_y_size), (0,0,0,0))
pixels = foreground.load()


# do for every blob
for blob in range(blobs):

# randomize the blob size
  blob_size = random.randint(min_blob_size, max_blob_size)
  blob_area = blob_size * blob_size
  blob_origo = blob_radius = int(blob_size / 2)
  blob_fade = int(blob_size * 0.2)

# randomize the color. Strong shades of red, green, blue, magenta, cyan, yellow
  rgb_rand = random.randint(0,5)
  if rgb_rand == 0:
    red = random.randint(150,255)
    green = random.randint(0,55)
    blue = random.randint(0,55)
  elif rgb_rand == 1:
    red = random.randint(0,55)
    green = random.randint(150,255)
    blue = random.randint(0,55)
  elif rgb_rand == 2:
    red = random.randint(0,55)
    green = random.randint(0,55)
    blue = random.randint(150,255)
  elif rgb_rand == 3:
    red = random.randint(150,255)
    green = random.randint(0,55)
    blue = random.randint(150,255)
  elif rgb_rand == 4:
    red = random.randint(0,55)
    green = random.randint(150,255)
    blue = random.randint(150,255)
  elif rgb_rand == 5:
    red = random.randint(150,255)
    green = random.randint(150,255)
    blue = random.randint(0,55)

# randomize the position for the upper left corner of the blob
# the range is such that up to half the blob can end up outside the image, true for both x and y
  blob_x_pos = random.randrange(0 - blob_radius, image_x_size - blob_radius, 1)
  blob_y_pos = random.randrange(0 - blob_radius, image_y_size - blob_radius, 1)

  blob_origo_x = blob_x_pos + blob_origo
  blob_origo_y = blob_y_pos + blob_origo

# if parts of the blob end up outside of the visible area, set visible start and end positions
  if blob_x_pos < 0:
    blob_visible_x_start = 0
  else:
    blob_visible_x_start = blob_x_pos
  
  if blob_x_pos + blob_size > image_x_size:
    blob_visible_x_end = image_x_size
  else:
    blob_visible_x_end = blob_x_pos + blob_size

  if blob_y_pos < 0:
    blob_visible_y_start = 0
  else:
    blob_visible_y_start = blob_y_pos

  if blob_y_pos + blob_size > image_y_size:
    blob_visible_y_end = image_y_size
  else:
    blob_visible_y_end = blob_y_pos + blob_size


  for y in range(blob_visible_y_start, blob_visible_y_end, 1):
    for x in range(blob_visible_x_start, blob_visible_x_end, 1):
      
      # get the values for the current pixel
      current_pixel = foreground.getpixel((x, y))

      # calculate pixel distance from blob (hypotenuse)
      x_pos = abs(blob_origo_x - x)
      y_pos = abs(blob_origo_y - y)
      distance = math.sqrt(x_pos * x_pos + y_pos * y_pos)

      if distance > blob_radius:
        # outside of blob, no change to pixel
        r = current_pixel[0]
        g = current_pixel[1]
        b = current_pixel[2]
        a = current_pixel[3]
      elif distance < (blob_radius - blob_fade):
        # inside of area for max blob opaqueness, add blob color and alpha to pixel
        r = current_pixel[0] + red
        g = current_pixel[1] + green
        b = current_pixel[2] + blue
        a = current_pixel[3] + max_alpha
      else:
        # in fade area, calculate which amount of color and alpha to add
        fade_level = (blob_radius - distance) / blob_fade
        fade_pixel = (6.28 * fade_level - math.sin(6.28 * fade_level)) / 6.28
        alpha = int(max_alpha * fade_pixel)
        r = int(current_pixel[0] + red * fade_pixel)
        g = int(current_pixel[1] + green * fade_pixel)
        b = int(current_pixel[2] + blue * fade_pixel)
        a = current_pixel[3] + alpha

      # if color or alpha is out of bounds, get it back in line
      if r > 255:
        r = 255
      if g > 255:
        g = 255
      if b > 255:
        b = 255
      if a > 255:
        a = 255

      # put pixel
      pixels[x, y] = (r, g, b, a)

# create file pointer to png file, write binary
fp = open("/tmp/blob.png","wb")

# merge background and foreground and save to file pointer
merged_image = Image.alpha_composite (background, foreground)
merged_image.save(fp, "PNG")
fp.close

# show the image
merged_image.show()

