from sqlalchemy import text
from festiuto import cnx

def test():
    try:
        result = cnx.execute(text("select * from FESTIVAL;"))
        result = result.first()
        return result
    except:
        print("erreur de l'id")
        raise

