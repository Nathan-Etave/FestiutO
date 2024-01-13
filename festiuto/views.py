import random
from flask import jsonify, render_template, session, redirect, url_for, request
from flask_wtf import FlaskForm
import scipy as sp
from wtforms import BooleanField, DateField, DateTimeField, EmailField, HiddenField, IntegerField, SelectField, StringField, SubmitField, TelField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from festiuto import app, csrf
from festiuto import requetes
from sqlalchemy import inspect

class AjouterArtisteForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    groupe = SelectField('groupe', choices=[(groupe.idG, groupe.nomG) for groupe in requetes.get_groupes()], validators=[DataRequired()])
    submit = SubmitField("ajouter l'artiste")

    def get_information(self):
        nom = self.nom.data
        prenom = self.prenom.data
        groupe = self.groupe.data
        return nom, prenom, groupe
    
class AjouterGroupeForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    style = SelectField('groupe', choices=[(style.idS, style.nomS) for style in requetes.get_styles()], validators=[DataRequired()])
    submit = SubmitField("ajouter le groupe")

    def get_information(self):
        nom = self.nom.data
        description = self.description.data
        style = self.style.data
        return nom, description, style

class RechercheGroupeForm(FlaskForm):
    search = StringField('Recherche')
    submit = SubmitField('rechercher')

    def get_search(self):
        return None if self.search.data == "" else self.search.data
    
class RechercheForm(FlaskForm):
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
    tel = TelField('telephone', validators=[DataRequired()])
    quantite = IntegerField('quantite', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('ajouter au panier')
    next = HiddenField()

    def get_information(self):
        tel = self.tel.data
        quantite = self.quantite.data
        return (tel, quantite)
    
    def get_days(self):
        monday = self.monday.data
        tuesday = self.tuesday.data
        wednesday = self.wednesday.data
        thursday = self.thursday.data
        friday = self.friday.data
        saturday = self.saturday.data
        sunday = self.sunday.data
        return (monday, tuesday, wednesday, thursday, friday, saturday, sunday)

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
    if 'user' in session:
        favori = requetes.is_favori(session['user'][0],id)
        
        return render_template(
            'groupe.html',
            id = id,
            artistes = artistes,
            groupe = groupe,
            concerts_associated = concerts_associated,
            groupes_related = groupes_related,
            favori = favori
        )
    else:
        return render_template(
                'groupe.html',
                id = id,
                artistes = artistes,
                groupe = groupe,
                concerts_associated = concerts_associated,
                groupes_related = groupes_related,
            )
    

@app.route('/ajouter-favori/<int:id>',methods=['GET','POST'])
def ajouter_fav(id:int):
    requetes.ajouter_favori(session['user'][0],id)
    return redirect(url_for('groupe',id=id))

@app.route('/supprimer_favori/<int:id>',methods=['GET','POST'])
def supprimer_fav(id:int):
    requetes.supprimer_favori(session['user'][0],id)
    return redirect(url_for('groupe',id=id))

@app.route('/config-billet/<int:id>',methods=['GET','POST'])
def config_billet(id):
    f = BilletForm()
    if f.validate_on_submit():
        data = f.get_information()
        days = f.get_days()
        if id == 1:
            if days.count(True) == 1:
                date_d = ""
                date_f = ""
                for day in range(len(days)):
                    if days[day] is True:
                        date_d = f"2024-05-{day+13}"
                        date_f = f"2024-05-{day+13}"
                requetes.insert_billet(id,session['user'][0],date_d,date_f, data[1])
                return redirect(url_for('home'))
            else:
                return render_template(
                    'config_billet.html',
                    BilletForm = f,
                    id = id,
                    error = "Vous devez choisir au moins un jour"
                )
        elif id == 2:
            if days.count(True) == 2:
                indexs = list()
                for day in range(len(days)):
                    if days[day] is True: indexs.append(day)
                date_d = f"2024-05-{indexs[0]+13}"
                date_f = f"2024-05-{indexs[1]+13}"
                requetes.insert_billet(id,session['user'][0],date_d,date_f, data[1])
                return redirect(url_for('home'))
            else:
                return render_template(
                    'config_billet.html',
                    BilletForm = f,
                    id = id,
                    error = "Vous devez choisir au moins deux jours"
                )
        else:
            requetes.insert_billet(id,session['user'][0],"2024-05-13","2023-04-19",data[1])
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
                session['user'] = (user.idU,user.idR,user.nomU)
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

@app.route('/add-user',methods=['GET','POST'])
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
        'about.html',
        groupes = requetes.get_groupes()
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

@app.route('/favoris',methods=['GET','POST'])
def favoris():
    return render_template(
        'favoris.html',
        favoris = requetes.get_favoris(session['user'][0])
    )

@app.route('/billets',methods=['GET','POST'])
def billets():
    data_billets,total = requetes.get_billets_with_idU(session['user'][0])
    print(data_billets)
    return render_template(
        'billets.html',
        billets = data_billets,
        total = total
    )

@app.route('/informations',methods=['GET','POST'])
def informations():
    return render_template(
        'informations.html',
        informations = requetes.get_user(session['user'][0])
    )

@app.route('/module-admin',methods=['GET','POST'])
def admin():
    return render_template(
        'admin.html'
    )

@app.route('/groupe-management',methods=['GET','POST'])
def groupe_management():
    f = RechercheForm()
    if f.validate_on_submit():
        search = f.get_search()
        print(search)
        if search != None:
            return render_template(
                'module_administrateur/groupe_management.html',
                groupes = requetes.get_groupes_with_search(search),
                RechercheForm = f,
                nb_resultat = len(requetes.get_groupes_with_search(search))
            )
    return render_template(
        'module_administrateur/groupe_management.html',
        groupes = requetes.get_groupes(),
        RechercheForm = f,
        nb_resultat = len(requetes.get_groupes())
    )

@app.route('/ajouter_groupe',methods=['GET','POST'])
def ajouter_groupe():
    f = AjouterGroupeForm()
    return render_template(
        'module_administrateur/ajouter_groupe.html',
        AjouterGroupeForm = f
    )

@app.route('/ajouter_groupe_submit',methods=['GET','POST'])
def ajouter_groupe_submit():
    nom = request.form.get('nom')
    style = request.form.get('style')
    description = request.form.get('description')
    requetes.insert_groupe(nom,style,description)
    return redirect(url_for('groupe_management'))

@app.route('/supprimer-groupe/<int:id>',methods=['GET','POST'])
def supprimer_groupe(id:int):
    requetes.delete_groupe(id)
    return redirect(url_for('groupe_management'))

@app.route('/artiste-management',methods=['GET','POST'])
@csrf.exempt
def artiste_management():
    f = RechercheForm()
    if f.validate_on_submit():
        search = f.get_search()
        if search != None:
            return render_template(
                'module_administrateur/artiste_management.html',
                artistes = requetes.get_artiste_with_search(search),
                RechercheForm = f,
                nb_resultat = len(requetes.get_artiste_with_search(search))
            )

    return render_template(
        'module_administrateur/artiste_management.html',
        artistes = requetes.get_artistes(),
        RechercheForm = f,
        nb_resultat = len(requetes.get_artistes())
    )

@app.route('/ajouter_artiste',methods=['GET','POST'])
def ajouter_artiste():
    f = AjouterArtisteForm()
    return render_template(
        'module_administrateur/ajouter_artiste.html',
        AjouterArtisteForm = f
    )

@app.route('/ajouter_artiste_submit',methods=['GET','POST'])
def ajouter_artiste_submit():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    groupe = request.form.get('groupe')
    requetes.insert_artiste(nom, prenom, groupe)
    return redirect(url_for('artiste_management'))

@app.route('/supprimer-artiste/<int:id>',methods=['GET','POST'])
def supprimer_artiste(id:int):
    requetes.delete_artiste(id)
    return redirect(url_for('artiste_management'))

@app.route('/spectateur-management',methods=['GET','POST'])
def spectateur_management():
    return render_template(
        'module_administrateur/spectateur_management.html',
        spectateurs = requetes.get_spectateurs()
    )

@app.route('/hebergement-management',methods=['GET','POST'])
def hebergement_management():
    return render_template(
        'module_administrateur/hebergement_management.html',
        hebergements = requetes.get_hebergements()
    )

@app.route('/billet-management',methods=['GET','POST'])
def billet_management():
    return render_template(
        'module_administrateur/billet_management.html',
        billets = requetes.get_billets()
    )

@app.route('/ajouter-concert',methods=['GET','POST'])
def ajouter_concert():
    return render_template(
        'module_administrateur/ajouter_concert.html'
    )