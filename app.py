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
def mostrarautores():

    if request.method=="GET":
        autores = mostrarautores()
        print(autores)
        return render_template("autores.html",autores=autores)    
    else:
        nombre = request.form.get("nombre")
        datoscomic = datosautores(nombre)
        print(nombre)
    
    return render_template("resultadoautores.html", datoscomic=datoscomic, nombre=nombre)

#------------------------------------------------------------------------------------------------------------------------

@app.route('/comic/<id>', methods=["GET","POST"])
def mostrarcomic(id):

    if request.method=="GET":
        return render_template("comic.html",id=id)

#------------------------------------------------------------------------------------------------------------------------

@app.route('/comic', methods=["GET","POST"])
def mostrarcomics():

    if request.method=="GET":
        return render_template("comic.html",id=id)

#------------------------------------------------------------------------------------------------------------------------

@app.route('/superheroes', methods=["GET","POST"])
def mostrarheroes():

    if request.method=="GET":
        imagenes = imagenesheroes()
        return render_template("superheroes.html", imagenes=imagenes)    
        
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

def datosautores(nombre):
    
    mikey=os.environ["MiKey"]
    mikeypublica=os.environ["MiKeyPublica"]

    lista = []
    listadatos = []

    h = hashlib.new("md5",bytes(mikey,"utf-8"))
    hash1=h.hexdigest()
    URL_BASE="http://gateway.marvel.com/v1/public/"

    parametros={
        'fullName' : nombre,
        'ts':'1',
        'apikey': mikeypublica,
        'hash':hash1
    }
    r=requests.get(URL_BASE+"creators",params=parametros)

    if r.status_code == 200:
        datos=r.json()
        for dic in datos['data']['results'][0]['series']['items']:


            URL_BASE = dic.get('resourceURI')

            parametros={
                'ts':'1',
                'apikey': mikeypublica,
                'hash':hash1
            }

            r=requests.get(URL_BASE,params=parametros)

            if r.status_code == 200:
                datos1=r.json()
                imagen=(datos1['data']['results'][0]['thumbnail']['path']+"/portrait_incredible.jpg")
                nombre=(datos1['data']['results'][0]['title'])
                ids=(datos1['data']['results'][0]['id'])
                lista = [imagen,nombre,ids]
                listadatos.append(lista)
    print(listadatos)
    return listadatos

#------------------------------------------------------------------------------------------------------------------------

def mostrarautores():
    
    mikey=os.environ["MiKey"]
    mikeypublica=os.environ["MiKeyPublica"]

    listautores = []

    h = hashlib.new("md5",bytes(mikey,"utf-8"))
    hash1=h.hexdigest()
    URL_BASE="http://gateway.marvel.com/v1/public/"

    for valor in range(10):

        parametros={
            'offset' : valor * 20,
            'ts':'1',
            'apikey': mikeypublica,
            'hash':hash1
        }
        r=requests.get(URL_BASE+"creators",params=parametros)

        if r.status_code == 200:
            datos=r.json()
            for dic in datos['data']['results']:
                nombre = (dic['fullName'])
                listautores.append(nombre)

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





