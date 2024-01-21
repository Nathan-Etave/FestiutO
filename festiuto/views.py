import datetime
import random
from re import T
from flask import jsonify, render_template, session, redirect, url_for, request
from festiuto import app, csrf
from festiuto import requetes
from festiuto.forms import *
from sqlalchemy import inspect

@app.route('/',methods=['GET','POST'])
@csrf.exempt
def home():
    """Méthode de la page d'accueil
    """
    f = RechercheGroupeForm()
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "aout","septembre", "octobre", "novembre", "décembre"],
    search = f.get_search()
    if search != None:
        return render_template(
            'home.html',
            mois = mois,
            RechercheGroupeForm = f,
            concerts = requetes.Concert.Get.get_concerts_with_search(search)
        )
    
    # Génération aléatoire de concert
    idCs = set()
    all_idC = requetes.Concert.Get.get_concerts_idC()
    while len(idCs) < 8: idCs.add(all_idC[random.randint(0,len(all_idC)-1)][0])
    concerts = []
    for id in idCs:
        concerts.append(requetes.Concert.Get.get_concerts_with_id(id))

    return render_template  (
        'home.html',
        mois = mois,
        RechercheGroupeForm = f,
        concerts = concerts
    )

@app.route('/billeterie')
def billeterie():
    """Méthode de la page de billeterie
    """
    return render_template(
        'billeterie.html'
    )

@app.route('/programme')
def programme():
    """Méthode de la page du programme
    """
    monday_concerts = requetes.Concert.Get.get_concerts_by_day(13)
    tuesday_concerts = requetes.Concert.Get.get_concerts_by_day(14)
    wednesday_concerts = requetes.Concert.Get.get_concerts_by_day(15)
    thursday_concerts = requetes.Concert.Get.get_concerts_by_day(16)
    friday_concerts = requetes.Concert.Get.get_concerts_by_day(17)
    saturday_concerts = requetes.Concert.Get.get_concerts_by_day(18)
    sunday_concerts = requetes.Concert.Get.get_concerts_by_day(19)
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
    """Méthode de la page d'un groupe

    Args:
        id (int): id du groupe
    """
    groupe = requetes.Groupe.Get.get_groupe_with_idG(id)
    artistes = requetes.Artiste.Get.get_artistes_with_idG(id)
    concerts_associated = requetes.Concert.Get.get_concerts_with_idG(id)
    activites_associated = requetes.Activites.Get.get_activites_with_idG(id)
    groupes_related = requetes.Groupe.Get.get_groupe_related(id)
    images = requetes.Photo.Get.get_images_with_idG(id)
    if 'user' in session and not session['user'][1] == 1:
        favori = requetes.Favoris.Boolean.is_favori(session['user'][0],id)
        
        return render_template(
            'groupe.html',
            id = id,
            artistes = artistes,
            groupe = groupe,
            concerts_associated = concerts_associated,
            activites_associated = activites_associated,
            groupes_related = groupes_related,
            favori = favori,
            images = images
        )
    elif 'user' in session and session['user'][1] == 1:
        return render_template(
            'groupe.html',
            id = id,
            artistes = artistes,
            groupe = groupe,
            concerts_associated = concerts_associated,
            activites_associated = activites_associated,
            groupes_related = groupes_related,
            images = images,
            admin=True
        )
    else:
        return render_template(
            'groupe.html',
            id = id,
            artistes = artistes,
            groupe = groupe,
            concerts_associated = concerts_associated,
            activites_associated = activites_associated,
            groupes_related = groupes_related,
            images = images
        )
    

@app.route('/ajouter-favori/<int:id>',methods=['GET','POST'])
def ajouter_fav(id:int):
    """Méthode pour ajouter un favori

    Args:
        id (int): id du groupe
    """
    requetes.Favoris.Insert.ajouter_favori(session['user'][0],id)
    return redirect(url_for('groupe',id=id))

@app.route('/supprimer_favori/<int:id>',methods=['GET','POST'])
def supprimer_fav(id:int):
    requetes.Favoris.Delete.supprimer_favori(session['user'][0],id)
    return redirect(url_for('groupe',id=id))

@app.route('/config-billet/<int:id>',methods=['GET','POST'])
def config_billet(id):
    """Méthode pour configurer un billet

    Args:
        id (int): id du type de billet
    """
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
                requetes.Billet.Insert.insert_billet(id,session['user'][0],date_d,date_f, data[1])
                return redirect(url_for('billets'))
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
                requetes.Billet.Insert.insert_billet(id,session['user'][0],date_d,date_f, data[1])
                return redirect(url_for('billets'))
            else:
                return render_template(
                    'config_billet.html',
                    BilletForm = f,
                    id = id,
                    error = "Vous devez choisir au moins deux jours"
                )
        else:
            requetes.Billet.Insert.insert_billet(id,session['user'][0],"2024-05-13","2023-04-19",data[1])
            return redirect(url_for('billets'))

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
        roles = requetes.Role.Get.get_roles(),
        RegisterForm = RegisterForm()
    )

@app.route('/add-user',methods=['GET','POST'])
def add_user():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    mail = request.form.get('mail')
    mdp = requetes.Utilisateur.Insert.hasher_mdp(request.form.get('mdp'))
    mdpConfirm = requetes.Utilisateur.Insert.hasher_mdp(request.form.get('mdpConfirm'))
    if mdp == mdpConfirm:
        requetes.Utilisateur.Insert.insert_user(mail, prenom, nom, mdp)
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
        groupes = requetes.Groupe.Get.get_groupes()
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
    concerts = requetes.Concert.Get.get_concerts_with_search(search_term)
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
        favoris = requetes.Favoris.Get.get_favoris(session['user'][0])
    )

@app.route('/panier',methods=['GET','POST'])
def billets():
    data_billets,total = requetes.Billet.Get.get_billets_with_idU(session['user'][0])
    return render_template(
        'billets.html',
        billets = data_billets,
        total = total
    )

@app.route('/informations',methods=['GET','POST'])
def informations():
    return render_template(
        'informations.html',
        informations = requetes.Utilisateur.Get.get_user(session['user'][0])
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
        if search != None:
            return render_template(
                'module_administrateur/groupe_management.html',
                groupes = requetes.Groupe.Get.get_groupes_with_search(search),
                RechercheForm = f,
                nb_resultat = len(requetes.Groupe.Get.get_groupes_with_search(search))
            )
    return render_template(
        'module_administrateur/groupe_management.html',
        groupes = requetes.Groupe.Get.get_groupes(),
        RechercheForm = f,
        nb_resultat = len(requetes.Groupe.Get.get_groupes())
    )

@app.route('/modifier_groupe/<int:id>',methods=['GET','POST'])
def modifier_groupe(id):
    f = ModifierGroupeForm()
    groupe = requetes.Groupe.Get.get_groupe_with_idG(id)
    f.style.default = groupe.STYLEMUSICAL.idS
    f.description.default = groupe.GROUPE.descriptionG
    f.process()
    return render_template(
        'module_administrateur/modifier_groupe.html',
        groupe = groupe,
        ModifierGroupeForm = f
    )

@app.route('/modifier_groupe_submit/<int:id>',methods=['GET','POST'])
def modifier_groupe_submit(id):
    nom = request.form.get('nom')
    style = request.form.get('style')
    files = [f for f in request.files.getlist('images') if f.filename != '']
    description = request.form.get('description')
    requetes.Groupe.Update.update_groupe(id, nom, style, description, files)
    return redirect(url_for('groupe_management'))

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
    requetes.Groupe.Insert.insert_groupe(nom,style,description)
    return redirect(url_for('groupe_management'))

@app.route('/supprimer-groupe/<int:id>',methods=['GET','POST'])
def supprimer_groupe(id:int):
    requetes.Concert.Delete.delete_concert_with_idG(id)
    requetes.Activites.Delete.delete_activites_with_idG(id)
    requetes.Artiste.Delete.delete_artistes_with_idG(id)
    requetes.Loger.Delete.delete_revervation_with_idG(id)
    requetes.Favoris.Delete.delete_favoris_with_idG(id)
    requetes.Photo.Delete.delete_photos_with_idG(id)
    requetes.Groupe.Delete.delete_groupe(id)
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
                artistes = requetes.Artiste.Get.get_artiste_with_search(search),
                RechercheForm = f,
                nb_resultat = len(requetes.Artiste.Get.get_artiste_with_search(search))
            )

    return render_template(
        'module_administrateur/artiste_management.html',
        artistes = requetes.Artiste.Get.get_artistes(),
        RechercheForm = f,
        nb_resultat = len(requetes.Artiste.Get.get_artistes())
    )

@app.route('/modifier_artiste/<int:id>',methods=['GET','POST'])
def modifier_artiste(id):
    f = ModifierArtisteForm()
    artiste = requetes.Artiste.Get.get_artiste_with_idA(id)
    f.groupe.default = artiste.idG
    f.process()
    return render_template(
        'module_administrateur/modifier_artiste.html',
        artiste = artiste,
        ModifierArtisteForm = f
    )

@app.route('/modifier_artiste_submit/<int:id>',methods=['GET','POST'])
def modifier_artiste_submit(id):
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    groupe = request.form.get('groupe')
    requetes.Artiste.Update.update_artiste(id,nom,prenom,groupe)
    return redirect(url_for('artiste_management'))

@app.route('/ajouter_artiste',methods=['GET','POST'])
def ajouter_artiste():
    f = AjouterArtisteForm()
    f.groupe.choices = [(groupe.idG, groupe.nomG) for groupe in requetes.Groupe.Get.get_groupes()]
    return render_template(
        'module_administrateur/ajouter_artiste.html',
        AjouterArtisteForm = f
    )

@app.route('/ajouter_artiste_submit',methods=['GET','POST'])
def ajouter_artiste_submit():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    groupe = request.form.get('groupe')
    requetes.Artiste.Insert.insert_artiste(nom, prenom, groupe)
    return redirect(url_for('artiste_management'))

@app.route('/supprimer-artiste/<int:id>',methods=['GET','POST'])
def supprimer_artiste(id:int):
    requetes.Artiste.Delete.delete_artiste(id)
    return redirect(url_for('artiste_management'))

@app.route('/concert-management',methods=['GET','POST'])
def concert_management():
    f = RechercheForm()
    if f.validate_on_submit():
        search = f.get_search()
        if search != None:
            return render_template(
                'module_administrateur/concert_management.html',
                groupes = requetes.Groupe.Get.get_groupes_with_search(search),
                RechercheForm = f,
                nb_resultat = len(requetes.Groupe.Get.get_groupes_with_search(search))
            )
    return render_template(
        'module_administrateur/concert_management.html',
        groupes = requetes.Groupe.Get.get_groupes(),
        RechercheForm = f,
        nb_resultat = len(requetes.Groupe.Get.get_groupes())
    )

@app.route('/modifier_groupe_activites/<int:id>',methods=['GET','POST'])
def modifier_groupe_activites(id):
    f = AjouterActivitesForm()
    groupe = requetes.Groupe.Get.get_groupe_with_idG(id)
    if f.validate_on_submit():
        data = f.get_information()
        datetimeDeb = datetime.datetime.combine(data[3], data[4])
        datetimeFin = datetime.datetime.combine(data[5], data[6])
        requetes.Activites.Insert.insert_activite(id,data[0],data[1],data[2],datetimeDeb,datetimeFin,data[-1])
        return redirect(url_for('concert_management'))
    return render_template(
        'module_administrateur/modifier_groupe_activites.html',
        AjouterActivitesForm = f,
        groupe = groupe
    )

@app.route('/modifier_groupe_concert/<int:id>',methods=['GET','POST'])
def modifier_groupe_concert(id):
    f = AjouterConcertForm()
    groupe = requetes.Groupe.Get.get_groupe_with_idG(id)
    concerts = requetes.Concert.Get.get_concerts_with_idG(id)
    if f.validate_on_submit():
        data = f.get_information()
        datetimeDeb = datetime.datetime.combine(data[1], data[2])
        datetimeFin = datetime.datetime.combine(data[3], data[4])
        requetes.Concert.Insert.insert_concert(id,data[0],datetimeDeb,datetimeFin,data[5],data[6],data[7])
        return redirect(url_for('concert_management'))
    return render_template(
        'module_administrateur/modifier_groupe_concert.html',
        groupe = groupe,
        concerts = concerts,
        AjouterConcertForm = f
    )

@app.route('/spectateur-management',methods=['GET','POST'])
@csrf.exempt
def spectateur_management():
    f = RechercheForm()
    if f.validate_on_submit():
        search = f.get_search()
        if search != None:
            return render_template(
                'module_administrateur/spectateur_management.html',
                spectateurs = requetes.Utilisateur.Get.get_spectateurs_with_search(search),
                RechercheForm = f,
                nb_resultat = len(requetes.Utilisateur.Get.get_spectateurs_with_search(search))
            )

    return render_template(
        'module_administrateur/spectateur_management.html',
        spectateurs = requetes.Utilisateur.Get.get_spectateurs(),
        RechercheForm = f,
        nb_resultat = len(requetes.Utilisateur.Get.get_spectateurs())
    )

@app.route('/ajouter_spectateur',methods=['GET','POST'])
def ajouter_spectateur():
    f = RegisterForm()
    return render_template(
        'module_administrateur/ajouter_spectateur.html',
        RegisterForm = f
    )

@app.route('/ajouter_spectateur_submit',methods=['GET','POST'])
def ajouter_spectateur_submit():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    mail = request.form.get('mail')
    mdp = requetes.Utilisateur.Insert.hasher_mdp(request.form.get('mdp'))
    mdpConfirm = requetes.Utilisateur.Insert.hasher_mdp(request.form.get('mdpConfirm'))
    if mdp == mdpConfirm:
            requetes.Utilisateur.Insert.insert_user(mail, prenom, nom, mdp)
            return redirect(url_for('spectateur_management'))
    else:
        return render_template(
            'module_administrateur/ajouter_spectateur.html',
            RegisterForm = RegisterForm()
        )

@app.route('/supprimer-spectateur/<int:id>',methods=['GET','POST'])
def supprimer_spectateur(id:int):
    requetes.Billet.Delete.delete_billet_by_idU(id)
    requetes.Utilisateur.Delete.delete_user(id)
    return redirect(url_for('spectateur_management'))

@app.route('/hebergement-management',methods=['GET','POST'])
def hebergement_management():
    f = RechercheForm()
    if f.validate_on_submit():
        search = f.get_search()
        if search != None:
            return render_template(
                'module_administrateur/hebergement_management.html',
                hebergements = requetes.Hebergement.Get.get_hebergements_with_search(search),
                RechercheForm = f,
                nb_resultat = len(requetes.Hebergement.Get.get_hebergements_with_search(search))
            )
    return render_template(
        'module_administrateur/hebergement_management.html',
        hebergements = requetes.Hebergement.Get.get_hebergements(),
        RechercheForm = f,
        nb_resultat = len(requetes.Hebergement.Get.get_hebergements())
    )

@app.route('/ajouter-hebergement',methods=['GET','POST'])
def ajouter_hebergement():
    f = AjouterHebergement()
    if f.validate_on_submit():
        data = f.get_information()
        requetes.Hebergement.Insert.insert_hebergement(data[0],data[1],data[2])
        return redirect(url_for('hebergement_management'))
    return render_template(
        'module_administrateur/ajouter_hebergement.html',
        AjouterHebergement = f
    )

@app.route('/modifier-hebergement/<int:id>',methods=['GET','POST'])
def modifier_hebergement(id):
    hebergement = requetes.Hebergement.Get.get_hebergement_with_idH(id)
    reservations = requetes.Loger.Get.get_lodging_with_idH(id)
    return render_template(
        'module_administrateur/modifier_hebergement.html',
        hebergement = hebergement,
        reservations = reservations
    )

@app.route('/ajouter-groupe-hebergement/<int:id>',methods=['GET','POST'])
def ajouter_groupe_hebergement(id):
    f = RechercheForm()
    if f.validate_on_submit():
        search = f.get_search()
        if search != None:
            return render_template(
                'module_administrateur/ajouter_groupe_hebergement.html',
                idH = id,
                groupes = requetes.Groupe.Get.get_groupes_with_search(search),
                RechercheForm = f,
                nb_resultat = len(requetes.Groupe.Get.get_groupes_with_search(search))
            )
    return render_template(
        'module_administrateur/ajouter_groupe_hebergement.html',
        groupes = requetes.Groupe.Get.get_groupes(),
        idH = id,
        RechercheForm = f,
        nb_resultat = len(requetes.Groupe.Get.get_groupes())
    )
@app.route('/billet-management',methods=['GET','POST'])
def billet_management():
    return render_template(
        'module_administrateur/billet_management.html',
        billets = requetes.Billet.Get.get_billets()
    )

@app.route('/ajouter-concert',methods=['GET','POST'])
def ajouter_concert():
    return render_template(
        'module_administrateur/ajouter_concert.html'
    )

@app.route('/config-reservation/<int:idH>/<int:idG>',methods=['GET','POST'])
def config_reservation(idG, idH):
    f = ConfigReservationForm()
    if f.validate_on_submit():
        data = f.get_information()
        requetes.Loger.Insert.insert_reservation(idH,idG,data[0],data[1])
        return redirect(url_for('modifier_hebergement',id=idH))
    return render_template(
        'module_administrateur/config_reservation.html',
        idG = idG,
        idH = idH,
        ConfigReservationForm = f
    )

@app.route('/instrument_management/<int:id>',methods=['GET','POST'])
def instrument_management(id):
    artiste = requetes.Artiste.Get.get_artiste_with_idA(id)
    instrument_idA = requetes.Instrument.Get.get_instrument_with_idA(id)
    instruments = requetes.Instrument.Get.get_instruments()
    f = AjouterInstrument()
    for instrument_2 in instrument_idA:
        for instrument in instruments:
            if instrument.idI == instrument_2.idI:
                instruments.remove(instrument)
    f.instrument.choices = [(instrument.idI, instrument.nomI) for instrument in instruments]
    if f.validate_on_submit():
        requetes.Instrument.Insert.insert_instrument(id,f.get_information())
        return redirect(url_for('instrument_management',id=id))
    f.process()
    return render_template(
        'module_administrateur/instrument_management.html',
        artiste = artiste,
        instrument_idA = instrument_idA,
        instruments = instruments,
        AjouterInstrument = f
    )

@app.route('/supprimer_instrument/<int:idA>/<int:idI>',methods=['GET','POST'])
def supprimer_instrument(idA,idI): 
    requetes.Instrument.Delete.delete_instrument(idA,idI)
    return redirect(url_for('instrument_management',id=idA))

@app.route('/decrementer-billet',methods=['GET','POST'])
@csrf.exempt
def decrementer_billet():
    json = request.get_json()
    billet = requetes.Billet.Get.get_billet_by_idB(json['idB'])
    if billet is None or not requetes.Billet.Boolean.is_user_billet(session['user'][0], billet.idB):
        return jsonify(-1, -1)
    else:
        return jsonify(requetes.Billet.Delete.remove_billet_from_panier(billet.idU, billet.idT, billet.dateDebB, billet.dateFinB), requetes.Billet.Get.get_prix_billet(billet.idT), billet.idT, billet.idU, str(billet.dateDebB), str(billet.dateFinB))

@app.route('/incrementer-billet',methods=['GET','POST'])
@csrf.exempt
def incrementer_billet():
    json = request.get_json()
    billet = requetes.Billet.Get.get_billet_by_idB(json['idB'])
    if billet is None or not requetes.Billet.Boolean.is_user_billet(session['user'][0], billet.idB):
        return jsonify(-1, -1)
    else:
        return jsonify(requetes.Billet.Insert.add_billet_to_panier(billet.idU, billet.idT, billet.dateDebB, billet.dateFinB), requetes.Billet.Get.get_prix_billet(billet.idT))
    
@app.route('/incrementer-nouveau-billet',methods=['GET','POST'])
@csrf.exempt
def incrementer_nouveau_billet():
    json = request.get_json()
    return jsonify(requetes.Billet.Insert.add_billet_to_panier(session['user'][0], json['idT'], json['dateD'], json['dateF']), requetes.Billet.Get.get_prix_billet(json['idT']))
