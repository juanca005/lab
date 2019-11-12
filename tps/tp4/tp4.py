#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

import re
import time
import sys, getopt
import os
from os.path import basename
from PIL import Image
import wget
from urllib.request import urlopen
import urllib.request
import re
import requests
from bs4 import BeautifulSoup
import array
from concurrent.futures import ProcessPoolExecutor
import io
# def download(url, NOMBRE):
#     try:
#         furl = urllib2.urlopen(url)
#         f = file("%s.png"%NOMBRE,'wb')
#         f.write(furl.read())
#         f.close()
#     except:
#         print 'Unable to download file'

# print "Descargar imagenes desde internet:\n"
# entrada = raw_input("ingrese url: ")
# renombrar = raw_input("nombre: ")
# download(entrada,renombrar)

EXTENSIONS = ['.jpg','.png','.gif','.jpeg','.jfif','.svg' ]
 
def download_images_from_url(url):
        if not url.lower().startswith('http://') and not url.lower().startswith('https://'):
                url = 'http://%s'%url
        print ('Descargando de %s...'%url)
        #print (os.getpid())
        with urllib.request.urlopen(url) as f:
        	html = f.read()
        	#print (type(html))
        	#aca html tiene el codigo literalmente en html
        	html = html.decode('utf-8')
        	webpage_regex = re.compile('img .*?src="(.*?)"',re.IGNORECASE)
        	print ("webpage",webpage_regex)

        	links = webpage_regex.findall(html)
        	#print ("acaa tenemos",links)
        #urlContent = urllib.request.urlopen(url).read()
        #print (type(urlContent)) urlContent=html


    # Búsqueda del tag img en la página web.
        # HTML image tag: <img src="url" alt="some_text"/>
        #htmltext = urlContent.read().decode('utf-8')
        #print (type(htmltext))
        #imgUrls = re.findall('img .*?src="(.*?)"', htmltext)
        executor=ProcessPoolExecutor(max_workers = 3)
        
        # Descargar todas las imágenes
        for imgUrl in links:
 		
        # El print me sirvio para identificar los url relativos,
        # a continuación intenta descargar el archivo con wget.

	                #print (url+'/'+imgUrl)
                        urlFinal=url+'/'+imgUrl
                #print(imgUrl)
                #print (re.split(r"\|.|_/",imgUrl))
                
                
                
                #directorio = imgUrl
                #print (directorio)
          
                        #try:
                            #os.stat(directorio)
                        #except:
                            #os.mkdir(directorio)
                        
	                #os.system('wget -q -nc ' + imgUrl)
	                #arreglo="archivo"
                        file_name=imgUrl.split("/")[-1]
                        print (file_name)  #file_name =str
                        print ("executor")
                
	                #executor = ProcessPoolExecutor(max_workers=2)
                        executor.submit(imagen,file_name,urlFinal)
	                    #task = executor.submit(imagen(file_name,urlFinal))
	                   
	                #task2 = executor.submit(imagen(file_name,urlFinal))
	                #imagen(file_name,urlFinal)
	                
def imagen(file_name,urlFinal):	                
	                #furl = urllib.request.urlopen(urlFinal)
	                
	                print ("SOY EL PROCESO:",os.getpid())
	                with urllib.request.urlopen(urlFinal) as response, open(file_name, 'wb') as out_file:
	                	RUTA="TEMPORAL"
	                	data = response.read() # a `bytes` object

	                	out_file.write(data)
	                	
	                	im = Image.open(file_name)
	                	
	                	#print(im)
	                	rgb_im = im.convert('RGB')
	                	rgb_im.save(RUTA+'/'+file_name+'.jpg')
	                	im2 = Image.open(RUTA+'/'+file_name+'.jpg')
	                	RUTA2="TEMPORAL2"
	                	im2.save(RUTA2+'/'+file_name+'.ppm')
	                	width, height = im.size
	                	fd = os.open(RUTA2+'/'+file_name+'.ppm', os.O_RDONLY)
	                	cabecera = os.read(fd,50)
	                	#print (cabecera)
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
	                RUTA3="RGB"
	                f =  open(RUTA3+'/'+file_name+'red'+'.ppm', 'wb')
	                f.write(bytearray(ppm_header, 'ascii'))
	                image.tofile(f)

	                for x in range(0, width - 1):
	                	for y in range(0, height - 1):
	                		index =  3 * (y * width + x)
	                		image2[index] = 0          # red channel
	                		image2[index + 1] = imorig[index]
	                		image2[index + 2] = 0
	                f2 =  open(RUTA3+'/'+file_name+'green'+'.ppm', 'wb')
	                f2.write(bytearray(ppm_header, 'ascii'))
	                image2.tofile(f2)
	               
	                for x in range(0, width - 1):
	                	for y in range(0, height - 1):
	                		index =  3 * (y * width + x)
	                		image3[index] = 0          # red channel
	                		image3[index + 1] = 0
	                		image3[index + 2] = imorig[index]
	                f3 =  open(RUTA3+'/'+file_name+'blue'+'.ppm', 'wb')
	                f3.write(bytearray(ppm_header, 'ascii'))
	                image3.tofile(f3)
	                
	                
	                
	                # with urllib.request.urlopen(urlFinal) as g:
	                # 	final = g.read()
	                # 	final2 = file(final,'wb')
	                # 	final2.write(final.read())
	                # 	final2.close()

	                #f = file(imgUrl,'wb')
	                #f.write(furl.read())
	                #f.close()
	                
	                return 0
 



if __name__ == '__main__':
        args = sys.argv
        
        work=4
        task=[1,2,3,4]
        if len(args) < 2:
                print ('Necesito una dirección URL para descargar imágenes')
                exit(-1)
        #print (args)
        
        for i in range(1,len(args)):
            #print (args[i])
            #print(task[i])
            #executor = ProcessPoolExecutor(max_workers=work)
            #task[i] = executor.submit(download_images_from_url(args[i]))
            download_images_from_url(args[i])
        #fullCmdArguments = sys.argv
        #task=[]
        # - further arguments
        #argumentList = fullCmdArguments[1:]
        
        #for i in range(len(sys.argv)):
            #print (argumentList[1])
            
            
        
        #executor = ProcessPoolExecutor(max_workers=work)
            #print(args[i])
            
            
        #task1 = executor.submit(download_images_from_url(args[1]))
        #task2 = executor.submit(download_images_from_url(args[2]))
           #task1 = executor.submit(download_images_from_url(args[1]))   
            #print (args[2])
            #executor = ProcessPoolExecutor(max_workers=3)
        
        
            #task1 = executor.submit(download_images_from_url(args[1]))
            #task2 = executor.submit(download_images_from_url(args[2]))


            #download_images_from_url(args[1])
        exit(0)









