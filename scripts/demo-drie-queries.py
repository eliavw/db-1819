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
