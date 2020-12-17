from flask import Flask, render_template, url_for, redirect, send_from_directory, send_file
import flask
import os
import os.path, time
from parse_size import ParseSize
from pathlib import Path
from os import listdir
from os.path import isfile, join
from flask_ngrok import run_with_ngrok as ngrok

root_fol = "/static/shared"
app = Flask(__name__)
ngrok(app)

def scanFiles(mypath):
    file_li = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #return file_li
    return os.listdir(mypath)
    
def scanFilename(filelist, mypath):
    li = []
    for file in filelist:
        li.append(Path(mypath+"/" + file).resolve().stem)
    return li

def getExtension(path):
    li = []
    file_list = scanFiles(os.getcwd() + path )
    file_names = scanFilename(file_list, path)
    for i in range(len(file_list)):
        if file_list[i][len(file_names[i])+1:].upper() != "":
            li.append(file_list[i][len(file_names[i])+1:].upper())
        else:
            li.append("FOLDER")
    return li
    
def modification_date(file_list, path):
    mod_time = []
    for file in file_list:
       mod_time.append(time.strftime('%m/%d/%Y', time.localtime(os.path.getmtime(path + "/" + file))))
    return mod_time   

def getSize(file_list, path):
    li = []
    for file in file_list:
        li.append(ParseSize(os.stat(os.getcwd() + "/" + path + "/" + file).st_size))
    return li  

@app.route('/')
def root():
    file_list = scanFiles(os.getcwd() + root_fol)
    file_names = scanFilename(file_list, root_fol)
    file_sizes = getSize(file_list, root_fol)
    mod_time = modification_date(file_list, os.getcwd() + root_fol)
    extension_list = getExtension(root_fol)
    return render_template("DASHBOARD.JRNL", file_list = file_list, mod_time = mod_time, file_names = file_names, ext = extension_list, sizes = file_sizes)

@app.route('/', defaults={'path': 'root'})
@app.route('/<path:path>')
def serve_path(path):
    try:
        file_list = scanFiles(os.getcwd() + root_fol + "/" + path)
        file_names = scanFilename(file_list, root_fol + "/" + path)
        file_sizes = getSize(file_list, root_fol + "/" + path)
        mod_time = modification_date(file_list, os.getcwd() + root_fol + "/" + path)
        extension_list = getExtension(root_fol + "/" + path)
    except Exception as e:
        return e
    return render_template("FOLDER.JRNL", file_list = file_list, mod_time = mod_time, file_names = file_names, ext = extension_list, sizes = file_sizes, path = path)

@app.route('/xget&path=<path:path>&fname=<fname>')
def downloadFile(path, fname):
    if path == "root":
        path = ""
    return send_file(os.getcwd() + root_fol + "/" + str(path) + "/" + fname, as_attachment=True)
    
if __name__ == "__main__":
    #app.run(debug=True, host="0.0.0.0", port=9999)
    app.run()
 
