"""
Complete solution
"""


def query_01(connection, column_names):
    # Bouw je query
    query = """
    select t.name, t.yearID, t.HR
    from Teams as t
    order by t.HR desc;
    """

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df



def query_02(connection, column_names, datum_x="1980-01-16"):
    # Bouw je query
    query = """
    select m.nameFirst, m.nameLast, m.birthYear, m.birthMonth, m.birthDay
    from Master as m
    where m.debut > '{}'
    order by m.nameLast asc;
    """.format(
        datum_x
    )

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df


def query_03(connection, column_names):
    # Bouw je query
    query = """
    select distinct m.nameFirst, m.nameLast, t.name
    from Managers as mgr, Teams as t, Master as m
    where   mgr.playerID = m.playerID and 
            mgr.teamID = t.teamID and 
            mgr.yearID = t.yearID and 
            mgr.plyrMgr = 'N'
    order by t.name asc;
    """
    
    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df


def query_03_v_02(connection, column_names):
    # Bouw je query
    query = """
    select  distinct m.nameFirst, m.nameLast, t.name
    from    Managers as mgr, Teams as t, Master as m
    where   mgr.playerID = m.playerID and 
            mgr.teamID = t.teamID and 
            mgr.plyrMgr = 'N'
    order by t.name asc;
    """

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df


# Query 04
def query_04(connection, column_names, league_l="mlb", jaar_x=1980, jaar_y=1990):
    # Bouw je query
    query = """
    SELECT teamID, name, yearID, W, L
    FROM teams AS t
    WHERE   lgID = '{}' AND 
            t.yearID > {}  AND 
            NOT EXISTS (SELECT * 
                        FROM teams AS t2
                        WHERE   t.teamID = t2.teamID AND
                                t.lgID = t2.lgID AND
                                t2.yearID < {})
    ORDER BY teamID ASC, yearID ASC;
    """.format(
        league_l, jaar_x, jaar_y
    )

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df


def query_04_v02(connection, column_names, league_l="mlb", jaar_x=1980, jaar_y=1990):
    # Bouw je query
    query = """
    SELECT teamID, name, yearID, W, L
    FROM teams AS t
    WHERE
        t.lgID = '{}' AND
        EXISTS
            (SELECT * 
             FROM teams AS t3
             WHERE
                 t.teamID = t3.teamID AND
                 t.lgID = t3.lgID AND
                 t3.yearID > {}
            ) AND
        NOT EXISTS
            (SELECT * 
             FROM teams AS t2
             WHERE
                 t.teamID = t2.teamID AND
                 t.lgID = t2.lgID AND
                 t2.yearID < {})

    ORDER BY teamID ASC, yearID ASC;
    """.format(
        league_l, jaar_x, jaar_y
    )

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df


# Query 05
def query_05(connection, column_names):
    # Bouw je query
    query = """
    SELECT p.playerID, p.nameGiven, COUNT(pa.awardID) as pAwards 
    FROM master AS p, awardsplayers AS pa
    WHERE   p.playerID = pa.playerID
            AND EXISTS (SELECT *
                        FROM  awardsmanagers AS ma
                        WHERE p.playerID = ma.playerID)
    GROUP BY playerID
    ORDER BY pAwards DESC, p.playerID DESC;
    """

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df


# Query 06
def query_06(connection, column_names):
    # Bouw je query
    query = """
    SELECT DISTINCT AP1.playerID
    FROM AwardsPlayers as AP1, AwardsPlayers as AP2, AwardsPlayers as AP3
    WHERE   AP1.playerID = AP2.playerID AND 
            AP2.playerID = AP3.playerID AND 
            AP1.yearID = AP2.yearID + 1 AND 
            AP2.yearID = AP3.yearID + 1
    ORDER BY playerID ASC;
    """

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df


# Query 07
def query_07(connection, column_names, jaar_y=1980, manager_x="joske"):
    # Bouw je query
    query = """
    SELECT DISTINCT p.playerID, p.nameFirst, p.nameLast
    FROM master AS p, awardsplayers AS pa, salaries AS s, managers as m
    WHERE   p.playerID = pa.playerID AND
            p.playerID = s.playerID AND
            pa.yearID = {} AND
            s.yearID = pa.yearID AND
            m.yearID = s.yearID AND
            m.playerID = '{}' AND
            m.plyrMgr = 'N' AND
            s.teamID = m.teamID
    ORDER BY p.playerID ASC;
    """.format(
        jaar_y, manager_x
    )

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df


# Query 08
def query_08(connection, column_names):
    # Bouw je query
    query = """
    SELECT M.playerID, M.nameFirst, M.nameLast
    FROM Salaries as S JOIN Master as M on S.PlayerID = M.PlayerID
    GROUP BY playerID
    HAVING AVG(Salary) > (  SELECT AVG(Salary) 
                            FROM Salaries)
    ORDER BY playerID ASC;
    """

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df


# Query 09
def query_09(connection, column_names):

    # Bouw je query
    query = """
    SELECT t.teamID, t.name, MAX(t.yearID), t.W
    FROM teams AS t
    WHERE NOT EXISTS (  SELECT * 
                        FROM teams as t2
                        WHERE   t.teamID = t2.teamID AND 
                                t.yearID != t2.yearID AND
                                t.W < t2.W)
    GROUP BY teamID
    ORDER BY t.W DESC, teamID DESC
    """

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df


# Query 10
def query_10(connection, column_names, jaar_y=1990):
    # Bouw je query
    query = """
    SELECT DISTINCT T.teamId, T.name
    FROM teams as T
    WHERE NOT EXISTS (   SELECT *
                         FROM awardsplayers as AP
                         WHERE   AP.yearID = {} AND
                                 AP.playerID IN (SELECT S.PlayerID
                                                 FROM salaries as S
                                                 WHERE S.yearID = AP.yearID AND
                                                 S.TeamID = T.TeamID)
                     )  
    ORDER BY teamID ASC;
    """.format(
        jaar_y
    )

    # Stap 2 & 3
    res = run_query(connection, query)  # Query uitvoeren
    df = res_to_df(res, column_names)  # Query in DataFrame brengen

    return df
