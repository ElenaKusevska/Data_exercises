# Based on: https://www.coursera.org/learn/sql-data-science/home/welcome
import ibm_db

# Connection details:
dsn_hostname = "dashdb-txn-sbox-yp-lon02-07.services.eu-gb.bluemix.net" 
dsn_uid = "rzn98758"
dsn_pwd = "02rr8-4st9phd357"

dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_port = "50000"
dsn_protocol = "TCPIP"

# Create the dsn connection string:
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)
print(dsn)

# Create database connection:
try:
    conn = ibm_db.connect(dsn, "", "")
    print ("Connected to database")
except:
    print ("Unable to connect: ", ibm_db.conn_errormsg() )

# Retrieve Metadata for the Database Server:
server = ibm_db.server_info(conn)
print ("DBMS_NAME: ", server.DBMS_NAME)
print ("DBMS_VER:  ", server.DBMS_VER)
print ("DB_NAME:   ", server.DB_NAME)

#Retrieve Metadata for the Database Client / Driver:
client = ibm_db.client_info(conn)
print ("DRIVER_NAME:          ", client.DRIVER_NAME)
print ("DRIVER_VER:           ", client.DRIVER_VER)
print ("DATA_SOURCE_NAME:     ", client.DATA_SOURCE_NAME)
print ("DRIVER_ODBC_VER:      ", client.DRIVER_ODBC_VER)
print ("ODBC_VER:             ", client.ODBC_VER)
print ("ODBC_SQL_CONFORMANCE: ", client.ODBC_SQL_CONFORMANCE)
print ("APPL_CODEPAGE:        ", client.APPL_CODEPAGE)
print ("CONN_CODEPAGE:        ", client.CONN_CODEPAGE)

# Perform some SQL queries:
def Query(query_title, query_comand):
    try:
        ibm_db.exec_immediate(conn, query_comand)
        print(query_title + " complete")
    except Exception as e:
        print("unable to " + query_title)

Query("drop table", "drop table INSTRUCTOR")
Query("create table", "create table INSTRUCTOR(id INTEGER PRIMARY KEY NOT NULL, fname VARCHAR(20), lname VARCHAR(20), city VARCHAR(15), ccode CHAR(10))")
Query("insert", "insert into INSTRUCTOR (id, fname, lname, city, ccode) VALUES (1, 'Elena', 'Kusevska', 'Skopje', 'MK')")
Query("insert", "insert into INSTRUCTOR (id, fname, lname, city, ccode) VALUES (2, 'Some', 'Asshole', 'Some City', 'CC'), (3, 'Another', 'Asshole', 'in Another City', 'CC')")

# Get some info about the database:
def Query_info(query_statement):
    Infos = ibm_db.exec_immediate(conn, query_statement)
    tup = ibm_db.fetch_tuple(Infos)
    while tup != False:
        print(tup)
        tup = ibm_db.fetch_tuple(Infos)
    print ("")
    print("-----------------------------------")

#Query_info("select * from syscat.tables")
Query_info("select TABSCHEMA, TABNAME, CREATE_TIME from SYSCAT.TABLES where TABSCHEMA='RZN98758'")
Query_info("select * from syscat.columns where tabname='INSTRUCTOR'")
Query_info("select distinct(name), coltype, length from sysibm.syscolumns where tbname='INSTRUCTOR'")

# Perform some more queries:
selectQuery = "select * from INSTRUCTOR"
selectStmt = ibm_db.exec_immediate(conn, selectQuery)
while ibm_db.fetch_row(selectStmt) != False:
    print (ibm_db.result(selectStmt, 0), ibm_db.result(selectStmt, "FNAME"), ibm_db.result(selectStmt, 2), ibm_db.result(selectStmt,3),)

#Fetch the Dictionary (for the first row only)
#ibm_db.fetch_both(selectStmt)

Query("update", "update INSTRUCTOR set city='MOOSETOWN' where id=2;")

selectQuery = "select * from INSTRUCTOR"
selectStmt = ibm_db.exec_immediate(conn, selectQuery)
while ibm_db.fetch_row(selectStmt) != False:
   print (ibm_db.result(selectStmt, 0), ibm_db.result(selectStmt, "FNAME"), ibm_db.result(selectStmt, 2), ibm_db.result(selectStmt,3),)

ibm_db.close(conn)
