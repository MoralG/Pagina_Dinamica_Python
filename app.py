# 
# 
# import requests
# import os
# 
# import hashlib
# mikey=os.environ["MiKey"]
# mikeypublica=os.environ["MiKeyPublica"]
# h = hashlib.new("md5",bytes(mikey,"utf-8"))
# 
# hash1=h.hexdigest()
# 
# URL_BASE="http://gateway.marvel.com/v1/public/"
# 
# PrimerNombre="Stan"
# Apellido="Lee"
# 
# parametros={
    # 'firstName':PrimerNombre,
    # 'lastName':Apellido,
    # 'ts':'1',
    # 'apikey': mikeypublica,
    # 'hash':hash1
# }
# 
# r=requests.get(URL_BASE+"creators",params=parametros)
# if r.status_code == 200:
    # datos=r.json()
#    
    # for dic in datos['data']['results'][0]['series']['items']:
        # print(dic['name']
# 




# ---------------------------------------
import os
port=os.environ["PORT"]

from flask import Flask, render_template
app = Flask(__name__)	

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/1')
def articulos():
    return render_template("left-sidebar.html")

@app.route('/2')
def acercade():
    return render_template("no-sidebar.html")


app.run('0.0.0.0',int(port), debug=True)