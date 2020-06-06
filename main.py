"""" main.py
*   Author : Yvain RAYNAUD
*   Date : 05/06/2020
*   Object : main file for code "defi code"
"""

import sqlite3
import pandas as pd
import numpy as np
import glob
from datetime import date

import db 
import readFile
import regex

UPLOAD_ID = 0 #based on upload
PATIENT_NUM = 0 #based on the last PATIENT_NUM in DB TODO
DATABASE = "drwh.db"


def importXlsxIntoDb(input):
    """
    Read and process data stored in input excel file then inject entry in DB
    :param input: -> input path from this file
    """
    #import global variable
    global UPLOAD_ID
    global PATIENT_NUM
    global DATABASE

    connection = db.create_connection(DATABASE)

    xlsx = pd.read_excel(input)

    #looping on each row
    print(" - Importing data in DB", end = '')
    for index, row in xlsx.iterrows(): #index is needed
        if (pd.isna(row['DATE_MORT']) == False):
            DEATH_DATE = row['DATE_MORT']
            DEATH_CODE = 1
        else :
            DEATH_DATE = None #insert null in db
            DEATH_CODE = 0
        #insert in client
        db.insert_patient_ipphist(connection, (PATIENT_NUM, row['HOSPITAL_PATIENT_ID'], "export_patient.xlsx", 0, UPLOAD_ID))
        

        if (pd.isna(row['NOM_JEUNE_FILLE']) == False):
            MAIDEN_NAME = row['NOM_JEUNE_FILLE']
        else:
            MAIDEN_NAME = None
        db.insert_patient(connection, (PATIENT_NUM, row['NOM'], row['PRENOM'], row['DATE_NAISSANCE'], row['SEXE'], MAIDEN_NAME, row['ADRESSE'], row['TEL'], row['CP'], row['VILLE'], DEATH_DATE, row['PAYS'], DEATH_CODE, UPLOAD_ID))
        PATIENT_NUM = PATIENT_NUM + 1
        UPLOAD_ID = UPLOAD_ID + 1
        if (index % 100 == 0):
            print(".", end = '')
    #commit the changes to db			
    connection.commit()
    #close the connection
    connection.close()
    print("\n")

def getDocumentQuery(text, DOCUMENT_ORIGIN_CODE, file, pathFolder, extension):
    """
        Returning query from text as tuple
        format : (documentId, patient_num, DOCUMENT_ORIGIN_CODE, DOCUMENT_DATE, date.today().strftime("%m/%d/%y"), text, AUTHOR)
    """
    DOCUMENT_DATE = regex.getDateDoc(text)
    #getting probable author
    AUTHOR = regex.getAuthor(text)
    strModif = file[len(pathFolder):-len(extension)] #getting rid of path and extension
    documentName = strModif.split("_")
    patientIpp = documentName[0]
    documentId = documentName[1]
    #get patient id from patientIpp
    conn = db.create_connection(DATABASE)
    patient_num = db.select_patient_id(conn, patientIpp.lstrip('0')) #removing leading 0 causing troubles in select
    conn.close()
    return (documentId, patient_num, DOCUMENT_ORIGIN_CODE, DOCUMENT_DATE, date.today().strftime("%m/%d/%y"), text, AUTHOR)

def pdfProcessing():
    """
    Read and process all pdf file situated in "./fichiers source/" then inject it in the document table
    """
    global DATABASE
    DOCUMENT_ORIGIN_CODE = "DOSSIER_PATIENT"

    pathFolder = "fichiers source/"
    extension = ".pdf"
    pdfFileArrayPath = glob.glob(pathFolder + "*" + extension)
    print(" - Processing pdf", end="")
    index = 0
    for file in pdfFileArrayPath:
        text = readFile.readPdfFile(file)
        query = getDocumentQuery(text, DOCUMENT_ORIGIN_CODE, file, pathFolder, extension)
        conn = db.create_connection(DATABASE)
        db.insert_document(conn, query)

        #commit the changes to db
        conn.commit()
        #close the connection
        conn.close()
        
        print(".", end = '')
        index = index + 1
    print("\n")

def docxProcessing():
    """
    Read and process all docx file situated in "./fichiers source/" then inject it in the document table
    """
    DOCUMENT_ORIGIN_CODE = "RADIOLOGIE_SOFTWARE"
    global DATABASE

    pathFolder = "fichiers source/"
    extension = ".docx"
    docxFileArrayPath = glob.glob(pathFolder + "*" + extension)
    print(" - Processing docx", end="")
    index = 0
    for file in docxFileArrayPath:
        text = readFile.readDocxFile(file)
        query = getDocumentQuery(text, DOCUMENT_ORIGIN_CODE, file, pathFolder, extension)
        conn = db.create_connection(DATABASE)
        db.insert_document(conn, query)
        #commit the changes to db			
        conn.commit()
        #close the connection
        conn.close()
        
        print(".", end = '')
        index = index + 1
    print("\n")

def main():
    db.resetDB()
    importXlsxIntoDb("fichiers source/export_patient.xlsx")
    pdfProcessing()
    docxProcessing()




if __name__ == '__main__':
    main()