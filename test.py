import sys
import requests
from PIL import Image

images=[]
url0 = 'https://api.opendota.com/apps/dota2/images/heroes/antimage_full.png?'
url1 = 'https://api.opendota.com/apps/dota2/images/heroes/bloodseeker_full.png?'
url2 = 'https://api.opendota.com/apps/dota2/images/heroes/axe_full.png?'

images.append(Image.open(requests.get(url0, stream=True).raw))
images.append(Image.open(requests.get(url1, stream=True).raw))
images.append(Image.open(requests.get(url2, stream=True).raw))

print(images)

widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('test.jpg')