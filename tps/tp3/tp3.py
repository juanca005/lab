#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys,thread,socket
import datetime, locale
import time
from urlparse import urlparse, urldefrag
from cgi import parse_qs, parse_qsl

#********* VARIABLES *********
BACKLOG = 50            # CONEXIONES PENDIENTES EN LA COLA
MAX_DATA_RECV = 999999  #  MAXIMO NUMERO DE BYTES QUE VAMOS A RECIBIR
DEBUG = True            #  TRUE PARA VER MENSAJES
BLOCKED = []            # REMOVER  [""] PARA NO BLOQUEAR TODO.
BLOCKED2 = [""]
#**************************************
#********* MAIN  ***************
#**************************************
def main():
    

    #print var  imprime el dia

    #  CHEQUEA LONGITUD 
    if (len(sys.argv)<3):
        print "No se definio el puerto, usando el :8080. No se definio el archivo de configuracion" 
        port = 8080
        hora = time.strftime("%c")
        hora_final = datetime.time(12,30, 0)
        #port = int(sys.argv[1]) # port from argument
        archivo_origen="/home/juanca05/Escritorio/TP3/archivo_def.txt"
        print archivo_origen
        fdo = os.open( archivo_origen, os.O_RDONLY )
        total = os.stat(archivo_origen).st_size
        leido = os.read(fdo, 2048)
        print leido
        #print "total leido del archivo: " , len(leido)
        total=leido.split("\n")
    else:
        port = int(sys.argv[1]) # port from argument
        archivo_origen=sys.argv[2]
        print archivo_origen
        fdo = os.open( archivo_origen, os.O_RDONLY )
        total = os.stat(archivo_origen).st_size
        leido = os.read(fdo, 2048)
        print leido
        #print "total leido del archivo: " , len(leido)
        total=leido.split("\n")
        #print total[1]
        hora = time.strftime("%c")
        hora_final = datetime.time(12,30, 0)

        print "la hora de inicio del archivo es " + total[1]

    # INFO DE HOST Y PUERTO.
    host = ''               # EN BLANCO PARA LOCALHOST
    
    print "Proxy Server corriendo en ",host,":",port

    try:
        # CREAMOS EL SOCKET
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #  ASOCIAMOS EL SOCHET AL HOST Y AL PUERTO
        s.bind((host, port))

        # listenning
        s.listen(BACKLOG)
    
    except socket.error, (value, message):
        if s:
            s.close()
        print "No se pudo abrir el socket:", message
        sys.exit(1)

    # OBTIENE LA CONEXION DEL CLIENTE
    while 1:
        conn, client_addr = s.accept()

        # CREAMOS UN HILO PARA MANEJAR LOS REQUEST
        thread.start_new_thread(proxy_thread, (conn, client_addr ,hora, hora_final, total))
        
    s.close()
#************** FIN MAIN  ***************

def printout(type,request,address):
    if "Block" in type or "Blacklist" in type:
        colornum = 91
    elif "Request" in type:
        colornum = 92
    elif "Reset" in type:
        colornum = 93

    print "\033[",colornum,"m",address[0],"\t",type,"\t",request,"\033[0m"

#*******************************************
#********* PROXY_THREAD FUNCION ***************
#  Un hilo que maneja la peticion del browser
#*******************************************
def proxy_thread(conn, client_addr,hora,hora_final,total):

    # OBTENER EL REQUEST DESDE EL BORWSER
    request = conn.recv(MAX_DATA_RECV)
    print request
    # PARSEAMOS LA PRIMER LINEA

    p = urlparse(request)
    print "CON PARSE ES" , p

    first_line = request.split('\n')[0]
    print "primera linea" ,first_line
    # OBTENEMOS LA URL
    url = first_line.split(' ')[1]

    #print "URL ES",url


    x = datetime.datetime.now()
 
    dicdias = {'MONDAY':'Lunes','TUESDAY':'Martes','WEDNESDAY':'Miercoles','THURSDAY':'Jueves', 'FRIDAY':'Viernes','SATURDAY':'Sabado','SUNDAY':'Domingo'}
    anho = x.year
    mes =  x.month
    dia= x.day
 
    fecha = datetime.date(anho, mes, dia)
    var= (dicdias[fecha.strftime('%A').upper()])
    #print var
    #print total[0]
  
    hora_sistema = time.strftime("%X")  #18:50:53
    print "la hora del sistema es"+ hora_sistema
    #print hora_final  
    print total[1]


    if(var=="Martes" and hora_sistema < str (hora_final) and hora_sistema > total[1] ):
        conn.send("HTTP/1.1 200 OK \n\n <h1>Sitio bloqueado</h1>")
        conn.close()
        for i in range(0,len(BLOCKED2)):
            if BLOCKED2[i] in url:
                printout("ListaNegra",first_line,client_addr)
                conn.close()
                sys.exit(1)

    for i in range(0,len(BLOCKED)):
        if BLOCKED[i] in url:
            printout("ListaNegra",first_line,client_addr)
            conn.close()
            sys.exit(1)


    printout("Request",first_line,client_addr)
    # print "URL:",url
    # print
    
    #  BUSCA EL WEBSERVER Y EL PUERTO
    http_pos = url.find("://")          # BUSCA pos DE ://
    if (http_pos==-1):
        temp = url
    else:
        temp = url[(http_pos+3):]       #  OBTIENE EL RESTO DE LA URL
    
    port_pos = temp.find(":")           #  BUSCA LA POSICION DEL PUERTO, SI ES QUE SE DEFINIO ALGUNO

    #  BUSCA EL FIN DEL SERVIDOR WEB
    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)

    webserver = ""
    port = -1
    if (port_pos==-1 or webserver_pos < port_pos):      # PUERTO POR DEFECTO
        port = 80
        webserver = temp[:webserver_pos]
    else:       # specific port
        port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
        webserver = temp[:port_pos]

    try:
        #  CREAMOS EL SOCKET PARA CONECTARNOS
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        s.connect((webserver, port))
        s.send(request)         # ENVIAMOS LA CONSULTA
        
        while 1:
            #  RECIBIMOS LOS DATOS DEL WEBSERVER
            data = s.recv(MAX_DATA_RECV)
            
            if (len(data) > 0):
                #  ENVIAMOS AL BROWSER
                conn.send(data)
            else:
                break
        s.close()
        conn.close()
    except socket.error, (value, message):
        if s:
            s.close()
        if conn:
            conn.close()
        printout("Peer Reset",first_line,client_addr)
        sys.exit(1)
#********** FIN DE LA FUNCION DEL HILO ***********
    
if __name__ == '__main__':
    main()
