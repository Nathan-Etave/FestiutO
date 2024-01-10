from flask import render_template, session, redirect, url_for, request
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

    def get_authenticated_user(self):
        """
        Récupère l'utilisateur authentifié.

        Cette méthode récupère l'utilisateur authentifié en utilisant l'adresse e-mail fournie.
        Elle vérifie également si le mot de passe fourni correspond au mot de passe enregistré pour cet utilisateur.

        Returns:
            L'utilisateur authentifié si l'adresse e-mail et le mot de passe sont valides, sinon None.
        """
        user = requetes.get_user_by_email(self.email.data)
        print(user)
        mdp = requetes.get_mdp_by_email(self.email.data)
        if user is None:
            return None
        passwd = requetes.hasher_mdp(self.password.data)
        print(mdp)
        print(passwd)
        # print(str(mdp)+" == "+str(passwd))
        return user if passwd == mdp else None

class RegisterForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    mail = StringField('email', validators=[DataRequired()])
    mdp = PasswordField('password', validators=[DataRequired()])
    mdpConfirm = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("s'enregistrer")
    next = HiddenField()

@app.route('/',methods=['GET','POST'])
def home():
    return render_template(
        'home.html',
        mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "aout","septembre", "octobre", "novembre", "décembre"],
        concerts = requetes.get_all_concerts()
    )

@app.route('/billeterie')
def billeterie():
    return render_template(
        'billeterie.html'
    )

@app.route('/programme')
def programme():
    return render_template(
        'programme.html',
        concerts = requetes.get_all_concerts()
    )

@app.route('/concert/<int:id>',methods=['GET','POST'])
def concert(idC:int):
    return render_template(
        'concert.html',
        idC = idC,
        data_concert = requetes.get_groupe_by_idC(idC)
    )

@app.route('/config-billet/<int:id>',methods=['GET','POST'])
def config_billet(id):
    return render_template(
        'config_billet.html',
        BilletForm = BilletForm(),
        id = id
    )

@app.route('/login',methods=['GET','POST'])
def login():
    f = LoginForm()
    if f.validate_on_submit():
        try:
            print("test",f.get_authenticated_user())
            idU, nomU, prenomU, mailU, idR = f.get_authenticated_user()
            user = idU, nomU, prenomU, mailU, idR
            if user != None:
                idUt = user[0]
                session['user'] = user
                return redirect(url_for('home'))
        except:
            return render_template(
                'login.html',
                LoginForm = f
            )
    return render_template(
        'login.html',
        LoginForm = f
    )

@app.route('/register',methods=['GET','POST'])
def register():
    return render_template(
        'register.html',
        roles = requetes.get_roles(),
        RegisterForm = RegisterForm()
    )

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/profil',methods=['GET','POST'])
def profil():
    return render_template(
        'profil.html'
    )

@app.route('/about',methods=['GET','POST'])
def about():
    return render_template(
        'about.html'
    )