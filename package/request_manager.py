from __future__ import annotations

import pandas as pd
import pyodbc

REQUEST_TYPE_SELECT = "SELECT"
REQUEST_DISTINCT = "DISTINCT"
REQUEST_WHERE = "WHERE"
REQUEST_AND = "AND"
REQUEST_OR = "OR"


class Condition:
    """Documentation
    Cette classe représente une condition dans une requete
    """

    def __init__(self, value: str, operator: str = "AND") -> None:
        self.sub_cond: list[Condition] = []
        self.value: str = value
        self.operator: str = operator
        pass

    def add_condition(self, cond: Condition):
        """Documentation
        Permet d'ajouter des conditions emboitées
        """
        self.sub_cond.append(cond)
        return self

    def __str__(self) -> str:
        """Documentation
        Renvoie la condition en forme
        """
        out: str = " "

        out += self.operator
        out += " ( "
        out += self.value
        out += " "

        for cond in self.sub_cond:
            out += str(cond)

        out += ")"

        return out


class Request:
    def __init__(self, type: str = REQUEST_TYPE_SELECT, distinct: bool = False) -> None:
        self.type = type
        self.conditions: list[Condition] = []
        self.is_distinct = distinct
        self.selector: list[(str, str)] = []
        self.tables: list[(str, str)] = []
        self.order: str = ""

    def add_table(self, table, alias=None) -> Request:
        """Documentation
        Ajoute une table et son alias

        Parametre:
            Table: Nom de la table a ajouter,
            Alias: Alias de la table
        """
        self.tables.append((table, alias))

        return self

    def add_selector(self, selector: str, alias=None) -> Request:
        """Documentation
        Ajoute une selection par exemple * pour faire un select *

        Parametre:
            selector: chaine de caractere correspondant a la colonne a sélectionner

        """
        self.selector.append((selector, alias))

        return self

    def add_condition(self, cond: Condition) -> Request:
        """Documenetaion
        rajoute une condition de la forme {operator} {valeur}
                                            and         type = eau

        Parametre:
            Value: une condition ex: "type = eau"
            operator: and/or pour le calcul
        """
        if type(cond) != Condition:
            raise "ERROR - Ce n'est pas un type condition"

        self.conditions.append(cond)

        return self

    def set_order_by(self, ordre: str) -> Request:
        self.order = " ORDER BY " + ordre
        return self

    def reset_order_by(self) -> Request:
        self.order = ""
        return self

    def run(self, connexion: pyodbc.Connection) -> pd.DataFrame:
        print(str(self))
        return pd.read_sql_query(str(self), connexion)

    def __str__(self) -> str:
        out: str = ""
        out += self.type
        out += " "

        if self.is_distinct:
            out += REQUEST_DISTINCT
            out += " "

        out += self.selector[0][0]
        if self.selector[0][1] is not None:
            out += " " + self.selector[0][1]
        for select, alias in self.selector[1:]:
            out += ", "
            out += select
            if alias is not None:
                out += " " + alias

        out += " from "
        out += self.tables[0][0]
        if self.tables[0][1] is not None:
            out += " "
            out += self.tables[0][1]

        for table, alias in self.tables[1:]:
            out += ", "
            out += table
            if alias is not None:
                out += " " + alias

        if len(self.conditions) > 0:
            out += " where 1=1"
        for cond in self.conditions:
            out += str(cond)

        out += self.order

        # out += ";"
        return out


if __name__ == "__main__":
    test = Condition("type = 'eau'", "and").add_condition(
        Condition("type = 'gaz'", "or")
    )
    test2 = Condition("test = 'toilette'", "and").add_condition(
        Condition("test = 'toilette2'", "or")
    )

    # print(test)

    rq = (
        Request()
        .add_selector("client.ID", "groupe")
        .add_table("Test.dbo.historique", "histo")
        .add_table("TABLE2222222222", "tab2")
        .add_condition(test)
        .add_condition(test2)
    )

    print(rq)