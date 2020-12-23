import mysql.connector as mariadb
from datetime import datetime
from datetime import date
#import pytz

DB_DATABASE = "ChallanMasterDatabase"



def connect_databse():
    
    '''This will create the connection to database''' 

    try:
        conn = mariadb.connect(user = "root" , password= "", database = DB_DATABASE)
        cur = conn.cursor()
        
    except Exception as err:

        cur = conn = None
        print("error while connecting the database : {0}".format(err))
        print("oops connect db failed") 

    return cur, conn    


def create_database():
    
    conn = None
    cur = None

    try:
        status = True
        conn = mariadb.connect(user = "root" , host = " localhost", password= "") 
        cur = conn.cursor()

        ''' Create database Challan '''

        sql_command = "CREATE DATABASE IF NOT EXISTS {0}".format(DB_DATABASE)

        cur.execute(sql_command)

    except Exception as err:    
        print("ERROR {0}".format(err))
        status = False
        print("oops create_db  failed")

    finally:
        if conn is not None:
            cur.close()
            conn.close()
    return status


def init_db():

    ''' This function will initilize the database i.e will create the tables '''

    conn = None
    
    try:
        # Create the database
        database_status = create_database()

        if database_status:
            cur, conn = connect_databse()

            cur.execute('''CREATE TABLE IF NOT EXISTS Challans (
                           TicketNumber INTEGER PRIMARY KEY AUTO_INCREMENT,
                           Time TEXT NOT NULL,
                           Date TEXT NOT NULL,
                           VehicleNumber TEXT NOT NULL)
                        ''')


            conn.commit()
            
    except Exception as err:

        print("DB error {0}".format(err))         
        print("oops init_db failed")

    finally:
        if conn is not None:
            cur.close()
            conn.close()
    return               

def addChallan(date, time, VehicleNumber):


    ''' This function will add challan's information '''


    status = message = " Success"

    try:
        sql_query = "INSERT INTO Challans (Date, Time, VehicleNumber) VALUES ('{0}', '{1}', '{2}')".format(date, 
        time, VehicleNumber)

        cur, conn = connect_databse()

        cur.execute(sql_query)
        conn.commit()
    except Exception as err:
        print("database error {0}".format(err))
        print("oops addchallan failed")
            
    finally:

        if conn is not None:
            cur.close()
            conn.close()
    return status, message


def updateChallans(date, time, VehicleNumber, TicketNumber):

    ''' This function will update the subnet information '''

    status = message = "success"

    try:

        sql_query = " UPDATE Challans SET Date = '{0}', Time = '{1}', VehicleNumber = '{2}' WHERE TicketNumber =  '{3}'".format(date,time, VehicleNumber,TicketNumber)
        cur, conn = connect_databse()
        cur.execute(sql_query)
        conn.commit()
    except Exception as err:
        print("database error {0}".format(err))
        status = "Fail"
        message = "Database update error {0}".format(err)
        print("oops updateChallan failed")
    finally:
        if conn is not None:
            cur.close()
            conn.close()

    return status,  message  