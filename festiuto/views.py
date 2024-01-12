import random
from flask import jsonify, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, DateTimeField, EmailField, HiddenField, IntegerField, SelectField, StringField, SubmitField, TelField, PasswordField
from wtforms.validators import DataRequired
from festiuto import app, csrf
from festiuto import requetes
from sqlalchemy import inspect

class RechercheGroupeForm(FlaskForm):
    search = StringField('Recherche')
    submit = SubmitField('rechercher')

    def get_search(self):
        return None if self.search.data == "" else self.search.data

class BilletForm(FlaskForm):
    monday = BooleanField('lundi')
    tuesday = BooleanField('mardi')
    wednesday = BooleanField('mercredi')
    thursday = BooleanField('jeudi')
    friday = BooleanField('vendredi')
    saturday = BooleanField('samedi')
    sunday = BooleanField('dimanche')
    tel = TelField('Téléphone', validators=[DataRequired()])
    submit = SubmitField('commander')
    next = HiddenField()

    def get_information(self):
        monday = self.monday.data
        tuesday = self.tuesday.data
        wednesday = self.wednesday.data
        thursday = self.thursday.data
        friday = self.friday.data
        saturday = self.saturday.data
        sunday = self.sunday.data
        tel = self.tel.data
        return (monday, tuesday, wednesday, thursday, friday, saturday, sunday, tel)
    
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
        mdp = requetes.get_mdp_by_email(self.email.data)
        if user is None:
            return None
        passwd = requetes.hasher_mdp(self.password.data)
        return user if passwd == mdp else None

class RegisterForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    mail = StringField('email', validators=[DataRequired()])
    mdp = PasswordField('password', validators=[DataRequired()])
    mdpConfirm = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("s'enregistrer")
    next = HiddenField()

    def get_information(self):
        nom = self.nom.data
        prenom = self.prenom.data
        mail = self.mail.data
        mdp = requetes.hasher_mdp(self.mdp.data)
        mdpConfirm = requetes.hasher_mdp(self.mdpConfirm.data)
        return nom, prenom, mail, mdp, mdpConfirm

@app.route('/',methods=['GET','POST'])
@csrf.exempt
def home():
    f = RechercheGroupeForm()
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "aout","septembre", "octobre", "novembre", "décembre"],
    search = f.get_search()
    if search != None:
        print("pas none")
        return render_template(
            'home.html',
            mois = mois,
            RechercheGroupeForm = f,
            concerts = requetes.get_concerts_with_search(search)
        )
    
    # Génération aléatoire de concert
    idCs = set()
    all_idC = requetes.get_concerts_idC()
    while len(idCs) < 8: idCs.add(all_idC[random.randint(0,len(all_idC)-1)][0])
    concerts = []
    for id in idCs:
        concerts.append(requetes.get_concerts_with_id(id))

    return render_template  (
        'home.html',
        mois = mois,
        RechercheGroupeForm = f,
        concerts = concerts
    )

@app.route('/billeterie')
def billeterie():
    return render_template(
        'billeterie.html'
    )

@app.route('/programme')
def programme():
    monday_concerts = requetes.get_concerts_by_day(13)
    tuesday_concerts = requetes.get_concerts_by_day(14)
    wednesday_concerts = requetes.get_concerts_by_day(15)
    thursday_concerts = requetes.get_concerts_by_day(16)
    friday_concerts = requetes.get_concerts_by_day(17)
    saturday_concerts = requetes.get_concerts_by_day(18)
    sunday_concerts = requetes.get_concerts_by_day(19)
    # à optimiser
    concerts_day = [monday_concerts, tuesday_concerts, wednesday_concerts, thursday_concerts, friday_concerts, saturday_concerts, sunday_concerts]
    days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

    return render_template(
        'programme.html',
        concerts_day = concerts_day,
        len_day = len(concerts_day),
        days = days
    )

@app.route('/groupe/<int:id>',methods=['GET','POST'])
def groupe(id:int):
    groupe = requetes.get_groupe_with_idG(id)
    artistes = requetes.get_artistes_with_idG(id)
    concerts_associated = requetes.get_concerts_with_idG(id)
    groupes_related = requetes.get_groupe_related(id)
    
    return render_template(
        'groupe.html',
        id = id,
        artistes = artistes,
        groupe = groupe,
        concerts_associated = concerts_associated,
        groupes_related = groupes_related
    )

@app.route('/config-billet/<int:id>',methods=['GET','POST'])
def config_billet(id):
    f = BilletForm()
    if f.validate_on_submit():
        data = f.get_information()
        if id == 1:
            if data.count(True) != 1:
                return render_template(
                    'config_billet.html',
                    BilletForm = f,
                    id = id,
                    error = "Vous devez choisir au moins un jour"
                )
            else:
                for day in range(len(data[0:-2])):
                    if data[day] is True:
                        dated = f"2023-07-{day+13}"
                        datef = f"2023-07-{day+13}"
                requetes.insert_billet(id,session['user'][0],dated,datef)
                return redirect(url_for('home'))
        elif id == 2:
            if data.count(True) != 2:
                return render_template(
                    'config_billet.html',
                    BilletForm = f,
                    id = id,
                    error = "Vous devez choisir au moins deux jours"
                )
            else:
                for day in range(len(data[0:-2])):
                    if data[day] is True:
                        dated = f"2023-07-{day+13}"
                        datef = f"2023-07-{day+13}"
                requetes.insert_billet(id,session['user'][0],dated,datef)
                return redirect(url_for('home'))
        else:
            for day in range(len(data[0:-2])):
                if data[day] is True:
                    dated = f"2023-07-{day+13}"
                    datef = f"2023-07-{day+13}"
            requetes.insert_billet(id,session['user'][0],dated,datef)
            return redirect(url_for('home'))

    return render_template(
        'config_billet.html',
        BilletForm = f,
        id = id
    )

@app.route('/login',methods=['GET','POST'])
def login():
    f = LoginForm()
    if f.validate_on_submit():
        try:
            user = f.get_authenticated_user()
            if user != None:
                session['user'] = (user.idU,user.idR)
                print("session : ",session['user'])
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

@app.route('/add_user',methods=['GET','POST'])
def add_user():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    mail = request.form.get('mail')
    mdp = requetes.hasher_mdp(request.form.get('mdp'))
    mdpConfirm = requetes.hasher_mdp(request.form.get('mdpConfirm'))
    if mdp == mdpConfirm:
        requetes.insert_user(mail, prenom, nom, mdp)
        return redirect(url_for('login'))
    else:
        return render_template(
            'register.html',
            erreur = "Les mots de passes ne correspondent pas, veuillez réessayer.",
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

@app.route('/search',methods=['GET','POST'])
@csrf.exempt
def search():
    def serialize_concert(concert_tuple):
        concert, groupe, stylemusical = concert_tuple
        return {
            'concert': {attr: str(getattr(concert, attr)) for attr in inspect(concert).attrs.keys()},
            'groupe': {attr: str(getattr(groupe, attr)) for attr in inspect(groupe).attrs.keys()},
            'stylemusical': {attr: str(getattr(stylemusical, attr)) for attr in inspect(stylemusical).attrs.keys()},
        }
    search_term = request.get_json()['search_term']
    concerts = requetes.get_concerts_with_search(search_term)
    if search_term == "":
        random_concerts = set()
        while len(random_concerts) < 8: random_concerts.add(concerts[random.randint(0,len(concerts)-1)])
        concerts = random_concerts
    serialized_concerts = [serialize_concert(concert) for concert in concerts]
    return jsonify(serialized_concerts)