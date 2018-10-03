from PIL import Image
img = Image.open("/Users/47510753/Desktop/B2H6.png")
# Get the size of the image
#width, height = picture.size

# Process every pixel
pixels = img.load() # create the pixel map

d={(213,60,35):(251,234,0,255),(213,60,48):(182,121,26,255)}

for i in range(img.size[0]): # for every pixel:
    for j in range(img.size[1]):
        r,g,b,a=pixels[i,j]
        if r==213 and g==60 and b==35:
        	print r,g,b
        if (r,g,b) in d:
        	print r,g,b
        	pixels[i,j] = d[(r,g,b)]

img.show()