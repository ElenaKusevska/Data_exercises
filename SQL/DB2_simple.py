# Create database connection - simple
import ibm_db

dsn = "DATABASE=BLUDB;HOSTNAME=dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=pwz45036;PWD=pnzb63zjv4xsmw^d;"
try:
    conn = ibm_db.connect(dsn, "", "")
    print ("Connected to database")
except:
    print ("Unable to connect: ", ibm_db.conn_errormsg() )

#Retrieve Metadata for the Database Server
server = ibm_db.server_info(conn)

print ("DBMS_NAME: ", server.DBMS_NAME)
print ("DBMS_VER:  ", server.DBMS_VER)
print ("DB_NAME:   ", server.DB_NAME)

#Retrieve Metadata for the Database Client / Driver
client = ibm_db.client_info(conn)

print ("DRIVER_NAME:          ", client.DRIVER_NAME)
print ("DRIVER_VER:           ", client.DRIVER_VER)
print ("DATA_SOURCE_NAME:     ", client.DATA_SOURCE_NAME)
print ("DRIVER_ODBC_VER:      ", client.DRIVER_ODBC_VER)
print ("ODBC_VER:             ", client.ODBC_VER)
print ("ODBC_SQL_CONFORMANCE: ", client.ODBC_SQL_CONFORMANCE)
print ("APPL_CODEPAGE:        ", client.APPL_CODEPAGE)
print ("CONN_CODEPAGE:        ", client.CONN_CODEPAGE)

ibm_db.close(conn)
