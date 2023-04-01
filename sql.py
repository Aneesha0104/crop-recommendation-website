import mysql.connector
conn=mysql.connector.connect(host='localhost',username='root',password='neesha010403',database='crop')
my_cursor=conn.cursor()
username=input("enter username: ")
password=input("enter password: ")
l=(username,password)
flag=0
my_cursor.execute("select * from login ")
output = my_cursor.fetchall()
for i in output:
    if(l==i):
        print(i)
        flag=1
if(flag==0):
    print("login invalid")


print('connection sucessful')

conn.commit()
conn.close()