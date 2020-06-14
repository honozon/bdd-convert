# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:52:08 2020

@author: mchonozon
"""
    
import pandas as pd 

def crea_bdd_iltass(file1, file2, output):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    df = pd.concat([df1,df2])
    
    aggregat = df.groupby(['Année', 'Mois','Produit','Business', 'Titre Programme', 'Chaine', u'Thématique Simba', 'Format', 'Device', 'Environnement'])['Sessions'].sum().to_frame('Sessions').reset_index()
    diff = abs(df.groupby(['Année','Mois'])['Sessions'].sum().sum() - aggregat.groupby(['Année','Mois'])['Sessions'].sum().sum())
    
    if(diff<2):
        aggregat.to_excel(output,  index=False)
        print('Tout a bien marché !')
    else :
        print('La somme des sessions est beaucoup trop grande, elle vaut :' +str(diff))

from flask import Flask  
from flask import render_template
from flask import request
from flask import send_file
#from werkzeug.utils import secure_filename

def secure_filename(filename):
    return filename

import os
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(".", "tmp")
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return True # '.' in filename and  filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello():  
    data = "<b>Hello, World</b>a"
    return render_template('index.html', data=data)

@app.route("/resultatbdd", methods=['POST'])
def resultatbdd():
    #fichier1 = "BDDPY01.xlsx"
   # fichier2 = "2019_cumul_decembre.xlsx"
    fichier1 =  request.files['file1']
    fichier2 =  request.files['file2']
    
    if fichier1 and allowed_file(fichier1.filename) and fichier2 and allowed_file(fichier2.filename):

        file1=os.path.join(app.config['UPLOAD_FOLDER'], "file1")
        fichier1.save(file1)
        file2=os.path.join(app.config['UPLOAD_FOLDER'], "file2")
        fichier2.save(file2)

        resultat=os.path.join(app.config['UPLOAD_FOLDER'], "test.xlsx")
        crea_bdd_iltass(file1, file2, resultat)
        try:
            return send_file(resultat, attachment_filename='resultatbdd.xlsx')
        
        except Exception as e:
            return str(e)
    else:
        return "no files"

# run the application

if __name__ == "__main__":  
    app.run(host='0.0.0.0',debug=True,port=os.getenv("PORT", 8080))
    
