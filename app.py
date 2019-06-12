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

@app.route('/autores/<id>', methods=["GET"])
def mostrarcomicautores(id):

    datoscomic = datosautores(id)
    nombre = nombreautor(id)
    return render_template("resultadoautores.html", datoscomic=datoscomic, nombre=nombre)

#------------------------------------------------------------------------------------------------------------------------

@app.route('/superheroes', methods=["GET","POST"])
def mostrarheroes():

    if request.method=="GET":
        datos = mostrardatosheroes()
        return render_template("superheroes.html", datos=datos)
    else:
        nombre = request.form.get("nombre")
        heroes = mostrarnombreheroes(nombre)

        return render_template("busquedasuperheroes.html", heroes=heroes)

#------------------------------------------------------------------------------------------------------------------------

@app.route('/superheroes/<id>', methods=["GET"])
def mostrarinformacionheroes(id):

    datosheroes = informacionheroes(id)
    nombre = nombreheroe(id)
    return render_template("resultadosuperheroes.html", datosheroes=datosheroes, nombre=nombre)
        
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

def mostrardatosheroes():

    mikey=os.environ["MiKey"]
    mikeypublica=os.environ["MiKeyPublica"]

    h = hashlib.new("md5",bytes(mikey,"utf-8"))
    hash1=h.hexdigest()
    URL_BASE="http://gateway.marvel.com/v1/public/"

    listadatos=[]

    for i in range(3):
        parametros={
            'offset' : i * 20,
            'ts':'1',
            'apikey': mikeypublica,
            'hash':hash1
        }
        r=requests.get(URL_BASE+"characters",params=parametros)

        if r.status_code == 200:

            datos=r.json()
            for dato in datos['data']['results']:
                if "not" not in dato['thumbnail']['path']:
                    path=(dato['thumbnail']['path'])
                    imagen=(path+"/portrait_medium.jpg")
                    lista = [dato['id'], dato['name'], imagen]
                    listadatos.append(lista)

    return(listadatos)

#------------------------------------------------------------------------------------------------------------------------

def mostrarnombreheroes(nombre):

    mikey=os.environ["MiKey"]
    mikeypublica=os.environ["MiKeyPublica"]

    h = hashlib.new("md5",bytes(mikey,"utf-8"))
    hash1=h.hexdigest()
    URL_BASE="http://gateway.marvel.com/v1/public/"

    listaheroes = []

    variable = nombre.strip()

    parametros={
        'nameStartsWith' : variable,
        'ts':'1',
        'apikey': mikeypublica,
        'hash':hash1
    }

    r=requests.get(URL_BASE+"characters",params=parametros)

    if r.status_code == 200:
        datos=r.json()
        for dic in datos['data']['results']:
            lista = [dic["name"],dic["id"]]
            listaheroes.append(lista)
    
    return listaheroes

#------------------------------------------------------------------------------------------------------------------------

def informacionheroes(id):

    mikey=os.environ["MiKey"]
    mikeypublica=os.environ["MiKeyPublica"]

    h = hashlib.new("md5",bytes(mikey,"utf-8"))
    hash1=h.hexdigest()
    URL_BASE="http://gateway.marvel.com/v1/public/"


    parametros={
        'id' : id,
        'ts':'1',
        'apikey': mikeypublica,
        'hash':hash1
    }

    r=requests.get(URL_BASE+"characters",params=parametros)

    if r.status_code == 200:
        datos=r.json()
        for dic in datos['data']['results']:
            path=(dic['thumbnail']['path'])
            imagen=(path+"/portrait_incredible.jpg")
            lista = [dic["description"],imagen,dic["modified"]]

    return lista

#------------------------------------------------------------------------------------------------------------------------

def nombreheroe(id):

    mikey=os.environ["MiKey"]
    mikeypublica=os.environ["MiKeyPublica"]

    h = hashlib.new("md5",bytes(mikey,"utf-8"))
    hash1=h.hexdigest()
    URL_BASE="http://gateway.marvel.com/v1/public/"

    parametros={
        'id' : id,
        'ts':'1',
        'apikey': mikeypublica,
        'hash':hash1
    }

    r=requests.get(URL_BASE+"characters",params=parametros)

    if r.status_code == 200:
        datos=r.json()
        for dic in datos['data']['results']:
            nombre = dic["name"]
    
    return nombre

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------



app.run('0.0.0.0',int(port), debug=True)















