import os
from typing import Any, Union
import requests
import operator
import re
import nltk
from flask import Flask, render_template, request , redirect
from flask_mysqldb import MySQL
from stop_words import STOP_WORDS_CACHE, STOP_WORDS_DIR
from collections import Counter
from bs4 import BeautifulSoup
import mysql.connector


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'mobilye'

mysql = MySQL(app)



@app.route('/', methods=['GET', 'POST'])
def index():
    return "<h1> Distance Reading Archive</h1><p>"


@app.route('/default/<path:mypath>')
@app.route('/default/<int:param>')
@app.route('/default/<string:family>')
@app.route('/default', defaults={''})
@app.route('/default')
@app.route('/default/<name>', methods=['GET', 'POST'])
def default(name=0,param=0,family=0, mypath=0):
    resp = ""
    language = request.args.get('language')
    fremework=request.args.get('fremework')
    website=request.args.get('website')
    name=request.args.get('name')
    family=request.args.get('family')
    firstname=request.args.get('firstname')
    lastname=request.args.get('lastname')
    age=request.args.get('age')

    if name:
        resp = resp + name + " "
    if param:
        resp = resp + str(param)  + " "
    if family:
        resp = resp + family + " "
    if mypath:
        resp = resp + mypath + " "
    if language:
        resp = resp + language + " "
    if fremework:
         resp = resp + fremework + " "
    if website:
         resp = resp + website + " "
    if firstname:
          resp = resp + firstname + " "
    if lastname:
          resp = resp + lastname + " "
    if age:
          resp=resp + age + " "

    with open('save_data.txt', "a+") as f:
        f.write(resp)
        f.write('\n')
        f.close()

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO  `mobilye`.`save_data_2`(result) VALUES (%s)", (resp,))
    mysql.connection.commit()

    return '''<h1>the resp is : {}.</h1>
           '''.format(resp)### , mycursor.rowcount   <h1>the record inserted is {}. <h1>


@app.route('/query_example')
def query_example():
    language = request.args.get('language')
    fremework = request.args.get('fremework')
    website = request.args.get('website')
    name = request.args.get('name')
    family = request.args.get('family')
    firstname =  request.args.get('firstname')
    lastname = request.args.get('lastname')
    age = request.args.get('age')
    return '''<h1>The fremework is : {}</h1>
            <h1>The language is : {}</h1>
            <h1>The website is : {}</h1>
             <h1>The name is : {} </h1>
             <h1>The family is : {} </h1>
             <h1>The firstname is : {} </h1>
             <h1>The lastname is : {} </h1>
             <h1>The age is : {} </h1>
                '''.format(language, fremework, website,name,family,firstname,lastname, age)


@app.route('/form_example', methods=['POST', "GET"])
def form_exampl():
    if request.method == 'POST':
        language=request.form.get('language')
        freamework = request.form['freamework']
        return '''<h1>This is post request </h1>
                <h1>The  language is {}.</h1>
                 <h1>The  freamework is {}.</h1>'''.format(language, freamework)
    else:
        pass
    return '''<form method='POST'>
    Language <input type="test" name="langusge">
    Framework <input type="test" name="framework">
    <input type="submit" name"Submit">
    </form>'''

# {
#     "language" : "Python",
#     "framework" : "Flask",
#     "website" : "scots",
#     "version_info" : {
#         "python" : 3.7,
#         "flask" : 1.0
#         },
#     "example" : ["query", "form", "json"],
#     "boolean_test" : "true"
# }


@app.route('/json_example', methods=['POST', "GET"])
def json_example():
    req_data = request.get_json()
    language = req_data['language']
    python_version = req_data['version_info']['python']
    example = req_data['examples'][0]

# @app.route('/my_route')
# def my_route():
#     page=request.args.get('page', default=1, type=int)
#     filter=request.args.get('filter', default='*', type=str)
#     # urlstring = request.query_string
#     # method = request.method
#     url = request.url
#     base_url= request.base_url
#     # url_charset = request.url_charset
#     url_root = request.url_root
#     rule = str(request.url_rule)
#     host_url = request.host_url
#     args = request.args
#     form = request.form
#     # host= request.host
#     # script_root = request.script_root
#     # path = request.path
#     full_path = request.full_path
#     resp = url.rsplit('/', 1)[-1]
#     print("page = " + page)
#     print("filter = " + filter)


# @app.route("/users")
# @app.route("/post")
# @app.route("/bookmarks")
# @app.route("/<target>")
# def category_browser(target = ""):
#     if(target != "" and target not in ['categories']):
#         return render_template("404.html")
#     else:
#         return render_template("view.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)