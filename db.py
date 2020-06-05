""" db.py
*   Author : Yvain RAYNAUD
*   Date : 05/06/2020
*   Object :   file containing all function dealing with the databases
*              part from https://www.sqlitetutorial.net/sqlite-python/insert/
"""

import sqlite3
from sqlite3 import Error

DATABASE = "drwh.db"

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def resetDB():
    global DATABASE
    connection = create_connection(DATABASE)
    #resetting db content
    cur = connection.cursor()
    cur.execute("DELETE FROM DWH_PATIENT")
    cur.execute("DELETE FROM DWH_PATIENT_IPPHIST")
    cur.execute("DELETE FROM DWH_DOCUMENT")
    connection.commit()
    connection.close()

def insert_patient_ipphist(conn, ipphist):
    """
    Creating a new patient ipphists record
    :param conn:
    :param ipphist (PATIENT_NUM, HOSPITAL_PATIENT_ID, ORIGIN_PATIENT_ID, MASTER_PATIENT_ID, UPLOAD_ID):
    return 
    """
    sql = ''' INSERT INTO DWH_PATIENT_IPPHIST(PATIENT_NUM, HOSPITAL_PATIENT_ID, ORIGIN_PATIENT_ID, MASTER_PATIENT_ID, UPLOAD_ID) 
                        VALUES(?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, ipphist)
    result = cur.lastrowid
    cur.close()
    return result

def insert_patient(conn, patient):
    """
    Creating a new patient   record
    :param conn:
    :param patient (PATIENT_NUM, LASTNAME, FIRSTNAME, BIRTH_DATE, SEX, MAIDEN_NAME, RESIDENCE_ADDRESS, PHONE_NUMBER, ZIP_CODE, RESIDENCE_CITY, DEATH_DATE, RESIDENCE_COUNTRY, DEATH_CODE, UPLOAD_ID):
    return 
    """
    sql = ''' INSERT INTO DWH_PATIENT(PATIENT_NUM, LASTNAME, FIRSTNAME, BIRTH_DATE, SEX, MAIDEN_NAME, RESIDENCE_ADDRESS, PHONE_NUMBER, ZIP_CODE, RESIDENCE_CITY, DEATH_DATE, RESIDENCE_COUNTRY, DEATH_CODE, UPLOAD_ID) 
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, patient)
    result = cur.lastrowid
    cur.close()
    return result

def insert_document(conn, doc):
    """
    Creating new doc record in db
    :param conn:
    :param doc (DOCUMENT_NUM, PATIENT_NUM, DOCUMENT_ORIGIN_CODE, UPDATE_DATE, DISPLAYED_TEXT)
    """
    sql = ''' INSERT INTO DWH_DOCUMENT(DOCUMENT_NUM, PATIENT_NUM, DOCUMENT_ORIGIN_CODE, UPDATE_DATE, DISPLAYED_TEXT)
                        VALUES(?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, doc)
    result = cur.lastrowid
    cur.close()
    return result

def select_patient_id(conn, ipp):
    """
    Query tasks  ipp
    :param conn: the Connection object
    :param ipp:
    :return:
    """
    #conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    cur.execute("SELECT PATIENT_NUM FROM DWH_PATIENT_IPPHIST WHERE HOSPITAL_PATIENT_ID=?", (ipp,))
    rows = cur.fetchall()
    cur.close()
    return rows[0][0] #hospital id is unique ? --- rows is like ((1,),(2,)), rows[0] = (1,) and rows[O][O] = 1
  
