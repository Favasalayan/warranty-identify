import pyodbc

pyodbc.pooling = True


def get_erp_connection():

    return pyodbc.connect(

        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=example;"
        "DATABASE=example;"
        "UID=example;"
        "PWD=example;"
        "TrustServerCertificate=yes;"
        
    )