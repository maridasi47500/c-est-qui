# -*- coding: utf-8 -*-

import sys
import os
print(sys.argv[1])


filename=sys.argv[1].lower()
myclass=(filename).capitalize()
modelname=(filename).capitalize()
marouteget="\"/%s\"" % filename
maroutenew="\"/%s_new\"" % filename
maroutecreate="\"/%s_create\"" % filename
marouteget2="\\\"/%s\\\"" % filename
myhtml="my"+filename+"html"
myfavdirectory=filename
index = 2 
createtable=""
columns="("
formhtml="<form method=\"POST\">"
values="("
mysession="["
myparam=","
items=sys.argv
referencesstr=""
requestfiles="""
"""
while index < (len(items)):

    try:
      print(index, items[index])
      hasfile=""
      references=""
      paramname=items[index]
      if ":file" in paramname: 
          hasfile="yes"
      if ":references" in paramname: 
          references="yes"
      paramname=items[index].replace(":file","").replace(":references","")
      print(items[(index+1)])
    except:
      myparam=""
    index += 1
    myfieldtype="text"
    if hasfile == "yes":
      myfieldtype="file"
      requestfiles+="""
        uploaded_file = request.files['{paramname}']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["{paramname}"]=uploaded_file.filename
"""


    if referencesstr == "yes":
        references+=", tousles{paramname}=tousles{paramname}".format(paramname=paramname)
        formhtml+="<div class=\"field\"><label for=\"somefield{paramname}\">{paramname}</label><input type=\"{mytype}\" id=\"somefield{paramname}\" name=\"{paramname}\"/></div>".format(myparam=myparam,paramname=paramname,mytype=myfieldtype)
    else:
        formhtml+="<div class=\"field\"><label for=\"somefield{paramname}\">{paramname}</label><select id=\"somefield{paramname}\" name=\"{paramname}\">".format(myparam=myparam,paramname=paramname,mytype=myfieldtype)
        formhtml+="{% for some{paramname} in tousles{paramname} %}".format(myparam=myparam,paramname=paramname,mytype=myfieldtype)
        formhtml+="<option value={{ some"+paramname+"['id'] }}">{{ some"+paramname+"['name'] }}</option>{% endif %}"
        formhtml+="</select></div>"
    mysession+="'{paramname}'{myparam}".format(myparam=myparam,paramname=paramname)
    columns+="{paramname}{myparam}".format(myparam=myparam,paramname=paramname)
    values+=":{paramname}{myparam}".format(myparam=myparam,paramname=paramname)
    createtable+="""        {paramname} text{myparam}
    """.format(myparam=myparam,paramname=paramname)
columns+=")"
values+=")"
mysession+=")"
mystr="""create table if not exists {filename}(
        id integer primary key autoincrement,
"""
mystr+=createtable

mystr+="""                );
"""
selectall= "select * from {filename}"

delete="""delete from {filename} where id = ?",(myid,)"""
selectone="""select * from {filename} where id = ?",(myid,)"""
addone="""@app.route("/add_one_{filename}", methods=["GET","POST"])
def add_one_{filename}():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=request.form"""
addone+=requestfiles

addone+="""
        one_user = query_db("insert into {filename} {columns} values {values}",hey)
        user = query_db('select * from {filename}')
"""
if filename == "user":
    addone+="""
        last_user = query_db("select * from {filename} where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in {mysession}:
            session[x]=hey[x]

"""
addone+="""
        return render_template("{filename}form.html", {filename}s=user, one_user=one_user, the_title="add new {filename}")
    user = query_db('select * from {filename}')
    one_user = query_db("select * from {filename} limit 1", one=True)
    return render_template("{filename}form.html", {filename}s=user, one_user=one_user, the_title="add new {filename}")

"""
if filename == "user":
    addone+="""
@app.route("/{filename}_sign_out", methods=["GET","POST"])
def {filename}_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in {mysession}:
            session[x]=""
        return redirect("/")


@app.route("/{filename}_log_in", methods=["GET","POST"])
def {filename}_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from {filename} where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in {mysession}:
                session[x]=hey[x]
        except:
            return render_template("{filename}login.html")
    return render_template("{filename}login.html")
"""


with open("app.py", "a") as myfile:
    myfile.write(addone.format(filename=filename,columns=columns,values=values))
with open("schema.sql", "a") as myfile:
    myfile.write(mystr.format(filename=filename))
with open("templates/hey.html", "a") as myfile:
    myfile.write("<a href=\"/add_one_{filename}\"> add one {filename}</a>".format(filename=filename))


with open("templates/"+filename+"form.html", "w") as myfile:
    myfile.write("{% extends 'base.html' %}{% block content %}"+formhtml.format(filename=filename)+"<div class=\"actions\"><input type=\"submit\"/></div></form>" + "{% for x in "+filename+"s %}{{"+ "x[\""+items[2]+"\"] }}{% endfor %}"+"{% endblock %}{% block liens %}<a href=\"/\">bienvenue</a>"+"<a href=\"/add_one_{filename}\"> add one {filename}</a>".format(filename=filename)+"{% endblock %}")


if filename == "user":
    with open("templates/"+filename+"login.html", "w") as myfile:
        myfile.write("{% extends 'base.html' %}{% block content %}<h1>signin</h1><form method=\"POST\"><div><label>username</label><input name=\"username\"/><div><label>username</label><input name=\"password\" type=\"password\"/></div><div class=\"actions\"><input type=\"submit\"/></div></form>" + "{% for x in "+filename+"s %}{{"+ "x[\""+items[2]+"\"] }}{% endfor %}"+"{% endblock %}{% block liens %}<a href=\"/\">bienvenue</a>"+"<a href=\"/add_one_{filename}\"> s'inscrire (add one {filename})</a>".format(filename=filename)+"{% endblock %}")
    
