"""
Contains basic functions, also implemented in the notebooks themselves.
"""
import mysql.connector
import getpass      # Package om een paswoordveldje te genereren.
import pandas as pd # Populaire package voor data-verwerking


def verbind_met_GB(username, hostname, gegevensbanknaam, password=None):
    """
    Maak verbinding met een externe gegevensbank

    Parameters
    ----------

    username:           str
                        Username van de gebruiker
    hostname            str
                        Naam van de host. In het geval van lokale server 'localhost'
    gegevensbanknaam    str
                        Naam van de gegevensbank
    password            str, None
                        Wachtwoord kan al meegegeven worden. Indien niet, wordt
                        een wachtwoordveldje gegenereerd waar de gebruiker het
                        kan ingeven.
    Returns
    -------
    connection          connection object
                        Dit is het soort object dat wordt teruggeven door
                        connect() methods van packages die voldoen aan de DB-API

    """

    if password is None:
        password = getpass.getpass()  # Genereer vakje voor wachtwoord in te geven
    else:
        password = password

    connection = mysql.connector.connect(host=hostname,
                                         user=username,
                                         passwd=password,
                                         db=gegevensbanknaam)
    return connection


def run_query(connection, query):
    """
    Voer een query uit op een bestaande connection.

    Geeft het resultaat van de query terug.

    Parameters
    ----------
    connection      connection object
                    Dit is het soort object dat wordt teruggeven door
                    connect() methods van packages die voldoen aan de DB-API
    query           str
                    SQL-query geschreven als een gewone string

    Returns
    -------

    """

    # Maak een cursor en voer query uit
    cursor = connection.cursor()
    cursor.execute(query)

    # Haal het resultaat op
    res = cursor.fetchall()

    return res


def res_to_df(query_result, column_names):
    """
    Zet ruwe output van een query om naar een DataFrame met gegeven kolomnamen.

    Let op: Het resultaat van de query moet dus exact evenveel kolommen bevatten
    als kolomnamen die je meegeeft. Als dit niet het geval is, is dit een indicatie
    dat je oplossing fout is. (Gezien wij de kolomnamen van de oplossing al cadeau doen)

    Parameters
    ----------
    query_result:
                    Resultaat van een uitgevoerde query zoals dat gegeven wordt
                    door cursor.fetchall()
    column_names    list
                    Lijst van kolomnamen voor het resulterende DataFrame

    Returns
    -------
    df:             pd.DataFrame
                    DataFrame dat het resultaat bevat.

    """

    df = pd.DataFrame(query_result, columns=column_names)
    return df