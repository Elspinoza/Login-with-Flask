from config import db
from app import app
from flask import render_template, request, session, redirect, flash, Blueprint
from flask_bcrypt import Bcrypt
from models.users import User

bcrypt = Bcrypt(app)

Authentification = Blueprint('authentification', __name__)


################################# HOME PAGE #####################################

@app.route('/')
def home():
    return render_template('home.html', title = 'Home page')        


################################# DASHBOARD #####################################

@app.route('/dashboard')
def index():

    #Verifier si l'utilisateur s'est authentifier ou pas

    if not session.get('user_id'):
        return redirect('/login')
    
    # Verifier si l'utilisateur est active en session ou pas

    if session.get('user_id'):
        id = session["user_id"]

    users = User.query.get(id)

    return render_template('index.html', title = 'Dashboard', users = users)




################################# PAGE D'INSCRIPTION #####################################

@app.route('/signup', methods = ['POST','GET'])
def signup():

    #Verifier si l'utilisateur s'est authentifier ou pas

    if session.get('user_id'):
        return redirect('/dashboard')
    
    if request.method == 'POST':

        # Recuperation des donnees entrer depuis le formulaire
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verification des valeurs s'ils sont remplie ou pas
        if name == "" or email == "" or password == "" :

            # Retourne d'un message flash
            flash ('Please fill the field', 'danger')

            return redirect('/signup')
        
        else:

            # Verification de l'adresse email s'il existe deja dans le base de donnee
            existEmail = User.query.filter_by(email = email).first()

            # Verification de l'adresse email (si l'adresse exist deja...)
            if existEmail:

                flash ('Email already exist', 'danger')
                return redirect('/signup')
            
            else:

                # Faire un mot de passe de hachage
                hash_password = bcrypt.generate_password_hash(password)

                # Creaction d'une instance de la class User
                data = User(name=name,email=email,password=hash_password)

                # Enregistrement dana la base de donnee
                db.session.add(data)

                # Validation de la base de donnees
                db.session.commit()

                # Retourne d'un message flash
                flash ('Account Create successfully', 'success')

                # Renvoi de la page de connexion
                return redirect('/login')
        
    return render_template('signup.html', title = 'Signup Page')



################################# PAGE DE CONNEXION #####################################

@app.route('/login', methods = ['POST', 'GET'])
def login():

    # Authentification de l'utilisateur a l'instant

    if session.get('user_id'):
        return redirect ('/dashboard')
    
    # Verifier s'il s'agit d'un post ou pas
    if request.method == 'POST':

        # Recuperation des valeur depuis le formulaire 
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifier si les champs ne sont pas vide
        if email == '' and password == '':

            # Envoi d'un message flash
            flash('Please fill the field','danger')

            return redirect('/login')
        
        else:

            # Recuperation de l'utilsateur par son adresse emaail
            users = User.query.filter_by(email=email).first()

            # Verifier si l'utilisateur exit et la comparaison du mot de passe s'il est valable
            if users and bcrypt.check_password_hash(users.password,password):

                # Stocker le nom et le id dans la session
                session['user_id']=users.id
                session['name']=users.name

                # Renvoi de la page home Page
                flash('Login Successfully','success')

                return redirect('/dashboard')
            else:
                flash('Invalid Email and Password','danger')
                return redirect('/login')
    else:
        return render_template('login.html',title='Login Page')



################################# DECONNEXION #####################################

@app.route('/logout')
def logout():

    # session.pop('user_id',None)
    # session.pop('name',None)

    session['user_id'] = None
    session['name'] = None
    return redirect('/')




