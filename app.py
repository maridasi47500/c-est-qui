from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=request.form

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename

        one_user = query_db("insert into user (username,pic,country_id,phone,email,password,fm) values (:username,:pic,:country_id,:phone,:email,:password,:fm)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','pic','country_id','phone','email','password','fm']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user")
    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user")


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','pic','country_id','phone','email','password','fm']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','pic','country_id','phone','email','password','fm']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=request.form

        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")
    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_personne", methods=["GET","POST"])
def add_one_personne():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=request.form

        one_user = query_db("insert into personne (name,fm) values (:name,:fm)",hey)
        user = query_db('select * from personne')

        return render_template("personneform.html", personnes=user, one_user=one_user, the_title="add new personne")
    user = query_db('select * from personne')
    one_user = query_db("select * from personne limit 1", one=True)
    return render_template("personneform.html", personnes=user, one_user=one_user, the_title="add new personne")

@app.route("/add_one_secrets", methods=["GET","POST"])
def add_one_secrets():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=request.form

        uploaded_file = request.files['pic']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/photos', uploaded_file.filename))

        hey["pic"]=uploaded_file.filename

        one_user = query_db("insert into secrets (personne_id,user_id,pic,info_or_gossip) values (:personne_id,:user_id,:pic,:info_or_gossip)",hey)
        user = query_db('select * from secrets')

        return render_template("secretsform.html", secretss=user, one_user=one_user, the_title="add new secrets")
    user = query_db('select * from secrets')
    one_user = query_db("select * from secrets limit 1", one=True)
    return render_template("secretsform.html", secretss=user, one_user=one_user, the_title="add new secrets")

