#!/usr/bin/python3
from PIL import Image
import os
import array

#im = Image.open("1.png")

#ACA TOMARIA LAS IMAGEN DE LA PAGINA
im = Image.open("TEMPORAL/1.png")
rgb_im = im.convert('RGB')
rgb_im.save('TEMPORAL/dog.jpg')
im2 = Image.open("TEMPORAL/dog.jpg")
im2.save("TEMPORAL/dog.ppm")


#im.save("dog.ppm")
width, height = im.size

fd = os.open("TEMPORAL/dog.ppm", os.O_RDONLY)
cabecera = os.read(fd,28)
print (cabecera)
imorig = os.read(fd, 18000000)
# PPM header
#width = 200
#height = 298
maxval = 255
ppm_header = f'P6 {width} {height} {maxval}\n'

# PPM image data (filled with blue)
image = array.array('B', [0, 0, 0] * width * height)
image2 = array.array('B', [0, 0, 0] * width * height)
image3 = array.array('B', [0, 0, 0] * width * height)
# Fill with red the rectangle with origin at (10, 10) and width x height = 50 x 80 pixels
for x in range(0, width - 1):
    for y in range(0, height - 1):
        index =  3 * (y * width + x)
        image[index] = imorig[index]          # red channel
        image[index + 1] = 0
        image[index + 2] = 0

# lena_red=np.copy(lena_rgb) # creo una copia de la imagen para preservar la original
# lena_red[:,:,1]=0
# lena_red[:,:,2]=0
# plt.title("Lena_ canal rojo")
# plt.imshow(lena_red)

for x in range(0, width - 1):
    for y in range(0, height - 1):
        index =  3 * (y * width + x)
        image2[index] = 0          # red channel
        image2[index + 1] = imorig[index]
        image2[index + 2] = 0

for x in range(0, width - 1):
    for y in range(0, height - 1):
        index =  3 * (y * width + x)
        image3[index] = 0          # red channel
        image3[index + 1] = 0
        image3[index + 2] = imorig[index]



f =  open('RGB/dog3-red.ppm', 'wb')
f.write(bytearray(ppm_header, 'ascii'))

f2 =  open('RGB/dog3-green.ppm', 'wb')
f2.write(bytearray(ppm_header, 'ascii'))

f3 =  open('RGB/dog3-blue.ppm', 'wb')
f3.write(bytearray(ppm_header, 'ascii'))

image.tofile(f)
image2.tofile(f2)
image3.tofile(f3)