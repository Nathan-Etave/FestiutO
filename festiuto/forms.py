from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, DateField, HiddenField, IntegerField, SelectField, StringField, SubmitField, TelField, PasswordField, TextAreaField, TimeField
from wtforms.validators import DataRequired, NumberRange
from festiuto import requetes

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

class AjouterInstrument(FlaskForm):
    instrument = SelectField('instruments', validators=[DataRequired()])
    submit = SubmitField("ajouter l'instrument")

    def get_information(self):
        instrument = self.instrument.data
        return instrument

class ModifierArtisteForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    groupe = SelectField('groupe', choices=[(groupe.idG, groupe.nomG) for groupe in requetes.get_groupes()], validators=[DataRequired()])
    submit = SubmitField("modifier l'artiste")

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

class ModifierGroupeForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    images = FileField('images', validators=[FileAllowed(['jpeg', 'jpg'])])
    style = SelectField('groupe', choices=[(style.idS, style.nomS) for style in requetes.get_styles()], validators=[DataRequired()])
    submit = SubmitField("modifier le groupe")

    def get_information(self):
        nom = self.nom.data
        description = self.description.data
        style = self.style.data
        return nom, description, style
    
class AjouterActivitesForm(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    lieu = SelectField('lieu', choices=[(lieu.idL, lieu.nomL) for lieu in requetes.get_lieux()], validators=[DataRequired()])
    dateDeb = DateField('dateDeb', validators=[DataRequired()])
    heureDeb = TimeField('heureDeb', validators=[DataRequired()])
    dateFin = DateField('dateFin', validators=[DataRequired()])
    heureFin = TimeField('heureFin', validators=[DataRequired()])
    estPublique = BooleanField('estPublique')
    submit = SubmitField("ajouter l'activité")

    def get_information(self):
        nom = self.nom.data
        description = self.description.data
        lieu = self.lieu.data
        dateDeb = self.dateDeb.data
        heureDeb = self.heureDeb.data
        dateFin = self.dateFin.data
        heureFin = self.heureFin.data
        estPublique = self.estPublique.data
        return nom, description, lieu, dateDeb, heureDeb, dateFin, heureFin, estPublique

class RechercheGroupeForm(FlaskForm):
    search = StringField('Recherche')
    submit = SubmitField('rechercher')

    def get_search(self):
        return None if self.search.data == "" else self.search.data
    
class AjouterHebergement(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    addresse = StringField('addresse', validators=[DataRequired()])
    nbPlace = IntegerField('nbPlace', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField("ajouter l'hébergement")

    def get_information(self):
        nom = self.nom.data
        addresse = self.addresse.data
        nbPlace = self.nbPlace.data
        return nom, addresse, nbPlace

class AjouterConcertForm(FlaskForm):
    lieu = SelectField('lieu', choices=[(lieu.idL, lieu.nomL) for lieu in requetes.get_lieux()], validators=[DataRequired()])
    dateDeb = DateField('dateDeb', validators=[DataRequired()])
    heureDeb = TimeField('heureDeb', validators=[DataRequired()])
    dateFin = DateField('dateFin', validators=[DataRequired()])
    heureFin = TimeField('heureFin', validators=[DataRequired()])
    dureeMontage = TimeField('dureeMontage', validators=[DataRequired()])
    dureeDemontage = TimeField('dureeDemontage', validators=[DataRequired()])
    estGratuit = BooleanField('estGratuit')
    submit = SubmitField("ajouter le concert")

    def get_information(self):
        lieu = self.lieu.data
        dateDeb = self.dateDeb.data
        heureDeb = self.heureDeb.data
        dateFin = self.dateFin.data
        heureFin = self.heureFin.data
        dureeMontage = self.dureeMontage.data
        dureeDemontage = self.dureeDemontage.data
        estGratuit = self.estGratuit.data
        return lieu, dateDeb, heureDeb, dateFin, heureFin, dureeMontage, dureeDemontage, estGratuit
    
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

class ConfigReservationForm(FlaskForm):
    dateD = DateField('dateD', validators=[DataRequired()])
    dateF = DateField('dateF', validators=[DataRequired()])
    submit = SubmitField("ajouter l'hébergement")
    next = HiddenField()

    def get_information(self):
        dateD = self.dateD.data
        dateF = self.dateF.data
        return (dateD, dateF)

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
    submit = SubmitField("créer le compte")
    next = HiddenField()

    def get_information(self):
        nom = self.nom.data
        prenom = self.prenom.data
        mail = self.mail.data
        mdp = requetes.hasher_mdp(self.mdp.data)
        mdpConfirm = requetes.hasher_mdp(self.mdpConfirm.data)
        return nom, prenom, mail, mdp, mdpConfirm