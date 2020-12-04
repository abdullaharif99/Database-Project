import cx_Oracle
import pandas as pd

"""
Some quick start guides:
* cx_Oracle 8: https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html
* pandas: https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
"""
# TODO change path of Oracle Instant Client to yours
cx_Oracle.init_oracle_client(lib_dir = "./instantclient_19_9")

# TODO change credentials
# Connect as user "user" with password "mypass" to the "CSC423" service
# running on lawtech.law.miami.edu
connection = cx_Oracle.connect(
    "username", "password", "lawtech.law.miami.edu/CSC_423")
cursor = connection.cursor()

queries = ["""Select c.clientNo, c.fname
From Client c, Services s
Where c.clientNo In (select clientNo from Services where day='Wednesday')
""",
"""
Select COUNT(Distinct r.equipmentID) 
From services s, requires r 
Where s.clientNo=2 And r.serviceID=s.serviceID
""",
"""
Select count(r.equipmentid)
From services s, requires r 
Where s.day='Friday' AND r.serviceID=s.serviceID
""",
"""
Select serviceID
From performs
Where empno=2

""",
"""
Select COUNT(Distinct r.equipmentID)
From requires r, performs p
Where r.serviceID In( select serviceID from performs where empNo=2) 
"""]


for q in queries:
    cursor.execute(q)

    # get column names from cursor
    columns = [c[0] for c in cursor.description]

    # print(len(cursor.description))
    # fetch data
    data = cursor.fetchall()
    # bring data into a pandas dataframe for easy data transformation
    df = pd.DataFrame(data, columns = columns)
    print(df) # examine
    print(df.columns)
    # print(df['FIRST_NAME']) # example to extract a column

cursor.close()

