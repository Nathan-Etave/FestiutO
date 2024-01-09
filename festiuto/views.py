from flask import render_template
from flask_wtf import FlaskForm
from wtforms import DateField, DateTimeField, EmailField, HiddenField, IntegerField, SelectField, StringField, SubmitField, TelField, PasswordField
from wtforms.validators import DataRequired
from festiuto import app #, db
from festiuto import requetes

class BilletForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    tel = TelField('Téléphone', validators=[DataRequired()])
    date_d = DateField('Date de réservation', validators=[DataRequired()])
    date_f = DateField('Date de réservation', validators=[DataRequired()])
    submit = SubmitField('commander')
    next = HiddenField()
    
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('se connecter')
    next = HiddenField()

class RegisterForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    # choices = [('professeur', 'Professeur'), ('gestionnaire', 'Gestionnaire'), ('laborantin', 'Laborantin')]
    # statut = SelectField('ComboBox', choices=choices)
    next = HiddenField()

@app.route('/')
def index():
    return render_template(
        'home.html',
        mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "aout","septembre", "octobre", "novembre", "décembre"],
        concerts = requetes.get_all_concerts()[0:8]
    )

@app.route('/billeterie')
def billeterie():
    return render_template(
        'billeterie.html'
    )

@app.route('/programme')
def programme():
    return render_template(
        'programme.html'
    )

@app.route('/concert/<int:id>',methods=['GET','POST'])
def concert(id:int):
    return render_template(
        'concert.html',
        idC = id,
        data_concert = requetes.get_groupe_by_idC(id)
    )

@app.route('/config-billet/<int:id>',methods=['GET','POST'])
def config_billet(id):
    return render_template(
        # f = BilletForm()
        'config_billet.html',
        BilletForm = BilletForm(),
        id = id
    )

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template(
        'login.html',
        LoginForm = LoginForm()
    )

@app.route('/register',methods=['GET','POST'])
def register():
    return render_template(
        'register.html',
        RegisterForm = RegisterForm()
    )

@app.route('/about',methods=['GET','POST'])
def about():
    return render_template(
        'about.html'
    )