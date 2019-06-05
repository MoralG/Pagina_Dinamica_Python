# ---------------------------------------

from flask import Flask, render_template,request, abort
import requests
import hashlib
import os
port=os.environ["PORT"]

from flask import Flask, render_template
app = Flask(__name__)	

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

@app.route('/')
def inicio():
    return render_template("index.html")

#------------------------------------------------------------------------------------------------------------------------

@app.route('/autores', methods=["GET","POST"])
def mostrardatosautores():

    if request.method=="GET":
        return render_template("autores.html")    
    else:
        nombre = request.form.get("nombre")
        autores = mostrarautores(nombre)
        
        return render_template("busquedaautores.html", autores=autores)

#------------------------------------------------------------------------------------------------------------------------

@app.route('/autores/<id>', methods=["GET","POST"])
def mostrarcomicautores(id):

    if request.method=="GET":
        
        datoscomic = datosautores(id)
        nombre = nombreautor(id)
        return render_template("resultadoautores.html", datoscomic=datoscomic, nombre=nombre)

#------------------------------------------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------------------------------------------

@app.route('/superheroes', methods=["GET","POST"])
def mostrarheroes():

    if request.method=="GET":
        imagenes = imagenesheroes()
        return render_template("superheroes.html", imagenes=imagenes)    
        
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

def nombreautor(ids):

    mikey=os.environ["MiKey"]
    mikeypublica=os.environ["MiKeyPublica"]

    lista = []
    listadatos = []

    h = hashlib.new("md5",bytes(mikey,"utf-8"))
    hash1=h.hexdigest()
    URL_BASE="http://gateway.marvel.com/v1/public/"

    listadatos=[]

    parametros={
        'id' : ids,
        'ts':'1',
        'apikey': mikeypublica,
        'hash':hash1
    }

    r=requests.get(URL_BASE+"creators",params=parametros)
    
    if r.status_code == 200:
        
        datos=r.json()
        nombre = datos['data']['results'][0]["fullName"]
    return nombre

#------------------------------------------------------------------------------------------------------------------------

def datosautores(ids):
    
    mikey=os.environ["MiKey"]
    mikeypublica=os.environ["MiKeyPublica"]

    lista = []
    listadatos = []

    h = hashlib.new("md5",bytes(mikey,"utf-8"))
    hash1=h.hexdigest()
    URL_BASE="http://gateway.marvel.com/v1/public/"

    listadatos=[]

    parametros={
        'ts':'1',
        'apikey': mikeypublica,
        'hash':hash1
    }

    r=requests.get(URL_BASE+"creators/"+ids+"/comics",params=parametros)

    if r.status_code == 200:
        datos=r.json()

        for dic in datos['data']['results']:
            url = (dic["thumbnail"]["path"]+"/portrait_xlarge.jpg")
            lista = [dic["title"], url, dic["id"], dic]
            listadatos.append(lista)

        return listadatos

#------------------------------------------------------------------------------------------------------------------------

def mostrarautores(variable):
    
    mikey=os.environ["MiKey"]
    mikeypublica=os.environ["MiKeyPublica"]

    listautores = []

    h = hashlib.new("md5",bytes(mikey,"utf-8"))
    hash1=h.hexdigest()
    URL_BASE="http://gateway.marvel.com/v1/public/"


    nombre1=variable
    
    
    if " " in variable:
        nombre1 = variable.split()[0]
        nombre2 = variable.split()[1]
        
        parametros={
            'lastName' : nombre2,
            'ts':'1',
            'apikey': mikeypublica,
            'hash':hash1
        }
        r=requests.get(URL_BASE+"creators",params=parametros)
    
        if r.status_code == 200:
            datos=r.json()
    
            for dic in datos['data']['results']:
            
                lista = [dic["fullName"],dic["id"]]
                listautores.append(lista)
    
    #-------------------
    
    parametros={
        'firstName' : nombre1,
        'ts':'1',
        'apikey': mikeypublica,
        'hash':hash1
    }
    r=requests.get(URL_BASE+"creators",params=parametros)
    
    if r.status_code == 200:
        datos=r.json()
    
        for dic in datos['data']['results']:
            
            lista = [dic["fullName"],dic["id"]]
            listautores.append(lista)
    
    #-------------------
    
    parametros={
        'lastName' : nombre1,
        'ts':'1',
        'apikey': mikeypublica,
        'hash':hash1
    }
    r=requests.get(URL_BASE+"creators",params=parametros)
    
    if r.status_code == 200:
        datos=r.json()
    
        for dic in datos['data']['results']:
            lista = [dic["fullName"],dic["id"]]
            listautores.append(lista)
    
    return listautores

#------------------------------------------------------------------------------------------------------------------------

def imagenesheroes():

    listaimagen=[]

    for ids in range(1,10):

        URL_BASE=("https://superheroapi.com/api/2434277406632758/%d/image" % ids)


        peticion=requests.get(URL_BASE)
        datos=peticion.json()
        listaimagen.append(datos["url"])

    return(listaimagen)

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

app.run('0.0.0.0',int(port), debug=True)





