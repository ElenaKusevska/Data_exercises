# Based on: https://www.coursera.org/learn/sql-data-science/home/welcome
# https://www.coursera.org/learn/sql-data-science/ungradedLti/pCr6A/hands-on-lab-1-connecting-to-a-database-instance
import ibm_db
import pandas
import ibm_db_dbi

# DSN Connection details:
dsn_hostname = "dashdb-txn-sbox-yp-lon02-06.services.eu-gb.bluemix.net" 
dsn_uid = "pwz45036"
dsn_pwd = "pnzb63zjv4xsmw^d"

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

# Connection for pandas:
pconn = ibm_db_dbi.Connection(conn)

# query statement to retrieve all rows in INSTRUCTOR table:
selectQuery = "select * from INSTRUCTOR"

# retrieve the query results into a pandas dataframe:
pdf = pandas.read_sql(selectQuery, pconn)

#print just the LNAME for the first row in the pandas data frame:
print(pdf.LNAME[0])

#print the entire data frame:
print(pdf)

# print the shape of the data frame:
print(pdf.shape)


ibm_db.close(conn)
