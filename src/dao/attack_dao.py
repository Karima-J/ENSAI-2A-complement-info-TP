# from typing import List, Optional
from dao.type_attack_dao import TypeAttackDAO
from utils.singleton import Singleton
from dao.db_connection import DBConnection
from business_object.attack.abstract_attack import AbstractAttack
from business_object.attack.attack_factory import AttackFactory


class AttackDao(metaclass=Singleton):
    def add_attack(self, attack: AbstractAttack) -> bool:
        """
        Add an attack to the database
        """
        created = False

        # Get the id type
        id_attack_type = TypeAttackDAO().find_id_by_label(attack.type)
        if id_attack_type is None:
            return created

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tp.attack (id_attack_type, attack_name,        "
                    " power, accuracy, element, attack_description)             "
                    "VALUES                                                     "
                    "(%(id_attack_type)s, %(name)s, %(power)s, %(accuracy)s,    "
                    " %(element)s, %(description)s)                             "
                    "RETURNING id_attack;",
                    {
                        "id_attack_type": id_attack_type,
                        "name": attack.name,
                        "power": attack.power,
                        "accuracy": attack.accuracy,
                        "element": attack.element,
                        "description": attack.description,
                    },
                )
                res = cursor.fetchone()
        if res:
            attack.id = res["id_attack"]
            created = True

        return created

    def find_attack_by_id(self, id: int) -> AbstractAttack:
        """renvoie l attaque avec l ID donné ou si l attaque n est pas trouvée None"""
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                 "
                    "  FROM tp.attack a                    "
                    "  JOIN tp.attack_type at2  "
                    "  ON a.id_attack_type = at2.id_attack_type            "
                    " WHERE id_attack = %(id_attack)s ",
                    {"id_attack": id},
                )
                res = cursor.fetchone()
        attack = AttackFactory.instantiate_attack(res["attack_type_name"], res["id_attack"],
                                                  res["power"], res["attack_name"],
                                                  res["attack_descritpion"], res["accuracy"],
                                                  res["element"])
        return attack


if __name__ == "__main__":
    # Pour charger les variables d'environnement contenues dans le fichier .env
    import dotenv
    from business_object.attack.physical_attack import PhysicalFormulaAttack

    dotenv.load_dotenv(override=True)

    # Création d'une attaque et ajout en BDD
    mon_attaque = PhysicalFormulaAttack(
        power=50,
        name="chatouille",
        description="guili-guilis",
        accuracy=90,
        element="Normal",
    )

    succes = AttackDao().add_attack(mon_attaque)
    print("Attack created in database : " + str(succes))
