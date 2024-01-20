from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import Table

engine = create_engine("mysql+pymysql://lavenant_fest:lavenant@mysql-lavenant.alwaysdata.net/lavenant_3")
# engine = create_engine("mysql+pymysql://etave:etave@servinfo-maria/DBetave")
Base = automap_base()
Base.prepare(autoload_with=engine)
metadata = MetaData()
Session = sessionmaker(bind=engine)

ACTIVITE_ANNEXE = Base.classes.ACTIVITEANNEXE
ARTISTE = Base.classes.ARTISTE
BILLET = Base.classes.BILLET
CONCERT = Base.classes.CONCERT
FAVORIS = Table('FAVORIS', metadata, autoload_with=engine)
FESTIVAL = Base.classes.FESTIVAL
GROUPE = Base.classes.GROUPE
HEBERGEMENT = Base.classes.HEBERGEMENT
IMAGER_GROUPE = Table('IMAGER_GROUPE', metadata, autoload_with=engine)
INSTRUMENT = Base.classes.INSTRUMENT
JOUER = Table('JOUER', metadata, autoload_with=engine)
LIEU = Base.classes.LIEU
LOGER = Base.classes.LOGER
PHOTO = Base.classes.PHOTO
RESEAU_SOCIAL = Base.classes.RESEAUSOCIAL
RESEAU_SOCIAL_GROUPE = Table('RESEAUSOCIAL_GROUPE', metadata, autoload_with=engine)
RESERVATION_ACTIVITE_ANNEXE = Base.classes.RESERVATION_ACTIVITEANNEXE
RESERVATION_CONCERT = Base.classes.RESERVATION_CONCERT
ROLE_UTILISATEUR = Base.classes.ROLEUTI
STYLE_MUSICAL = Base.classes.STYLEMUSICAL
TYPE_BILLET = Base.classes.TYPEBILLET
UTILISATEUR = Base.classes.UTILISATEUR
VIDEO = Base.classes.VIDEO
VIDEO_GROUPE = Table('VIDEO_GROUPE', metadata, autoload_with=engine)
