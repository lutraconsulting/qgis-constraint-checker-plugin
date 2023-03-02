# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Constraint Checker
                                 A QGIS plugin
 Generate reports of constraints (e.g. planning constraints) applicable to an area of interest.
                              -------------------
        begin                : 2014-03-19
        copyright            : (C) 2014 by Lutra Consulting for Dartmoor National Park Authority
        email                : it@dnpa.gov.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import string
from qgis.core import QgsApplication, QgsAuthMethodConfig, QgsSettings

DEBUG = False


def dbSafe(s):
    """ Returns true if this string is considered safe to use as a DB 
    object, false otherwise """
    
    safeChars = string.digits + string.ascii_letters + '_ '
    
    for char in s:
        if char not in safeChars:
            return False
    return True
        

def get_db_conn_details(conn_name):
    s = QgsSettings()
    s.beginGroup("/PostgreSQL/connections")
    if conn_name not in s.childGroups():
        raise Exception(f"No connection named {conn_name} in QGIS settings!")
    s.endGroup()
    s.beginGroup(f"/PostgreSQL/connections/{conn_name}")
    host = s.value("host", "")
    database = s.value("database", "")
    username = s.value("username", "")
    password = s.value("password", "")
    port = int(s.value("port", 5432))
    authcfg = s.value("authcfg", None)

    if DEBUG:
        print(f"Conn details: {host}, {database}, {username}, {len(password)}, {port}")

    if authcfg:
        conf = QgsAuthMethodConfig()
        auth_manager = QgsApplication.authManager()
        auth_manager.loadAuthenticationConfig(authcfg, conf, True)
        if conf.id():
            username = conf.config("username", "")
            password = conf.config("password", "")

    return host, database, username, password, port
