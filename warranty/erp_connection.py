import pyodbc

pyodbc.pooling = True


def get_erp_connection():

    return pyodbc.connect(
        
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=192.168.105.254;"
        "DATABASE=Kakiya_April_18_2023;"
        "UID=Pricecheck;"
        "PWD=hc@123456;"
        "TrustServerCertificate=yes;"
        
    )