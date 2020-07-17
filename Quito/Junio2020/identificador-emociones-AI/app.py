# -*- coding: utf-8 -*-
"""
Created on Mon May 17 14:01:12 2020
@author:    Ximena Celi
"""
import os
from flask import Flask, render_template, request
#from werkzeug import secure_filename
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./audios"


dirpath = os.getcwd()
nombrepath = os.path.normpath(dirpath)
pathAudios = nombrepath + os.sep + 'audios' + os.sep
pathModelos = nombrepath + os.sep + 'modelos' + os.sep

print("dirpath: "+dirpath)
print("pathAudios: "+pathAudios)
print("pathModelos: "+pathModelos)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/upload", methods=['POST'])
def uploader():
	if request.method == "POST":
		f = request.files['archivo']
		filename = secure_filename(f.filename)
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return render_template('index.html', archivoSubido=' Archivo subido exitosamente')

@app.route('/predecir',methods=['POST'])
def predecir():
    genero = "Femenino"
    estadoAnimo = "Alegre"
    return render_template('index.html', resultado='Es de género {}'.format(genero)+" y su estado de ánimo es {}".format(estadoAnimo))



if __name__ == "__main__":
    app.run(debug=True)
 #     app.run()

