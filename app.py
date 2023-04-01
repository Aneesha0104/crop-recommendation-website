from flask import Flask,render_template, request, url_for
import mysql.connector

import pandas as pd 
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
df = pd.read_csv("C:\\Users\\anees\\OneDrive\\Documents\\sem 4\\MLT\\excercises\\ml cia2\\Crop_recommendation.csv")
    
def crop_recommend(d,final):
    global df
    
    d=pd.DataFrame([d])
    df = pd.concat([df, d], axis=0, ignore_index=True)
    
    df_last=final.iloc[[-1],]
    
    cos_sim=cosine_similarity(df_last,final)
    df_cos_sim = pd.DataFrame(cos_sim)
    cos_scores = sorted(list(enumerate(cos_sim[0])),key=lambda x:x[1], reverse = True)
    s_idx  =[i[0] for i in cos_scores]
    s_scores =[i[1] for i in cos_scores]
    
    df_similar = pd.DataFrame(columns=["label", "Similarity"])
    df_similar["label"] = df.loc[s_idx, "label"]
    df_similar["Similarity"] = s_scores
    df_similar=df_similar.loc[(df_similar.label !='')]
    df_similar=df_similar.drop_duplicates(subset='label', keep="first")
    
    df_similar_N = df_similar.iloc[0:5,:]
    df_similar_N.reset_index(inplace = True)
    pred = df_similar_N['label'].values.tolist()
    
    return pred                   
     
def pred(li):
    
    df1=df.iloc[:,:-1]
    df2=df.iloc[:,-1]
    from sklearn import preprocessing
    label_encoder = preprocessing.LabelEncoder()
    df2= label_encoder.fit_transform(df2)
    df2=pd.DataFrame(data=df2)
    final=pd.concat([df1,df2],axis=1,ignore_index=True)
    a=crop_recommend(li,final)
    return a

 
app = Flask(__name__)
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="neesha010403",
        database="crop"
        )
cursor = mydb.cursor()

@app.route('/')
def form():
    return render_template('home.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
     
    if request.method == 'POST':

        username = request.form.get("username")
        password = request.form.get("password")
        l=(username,password)
        flag=0
        cursor.execute("select * from login ")
        output = cursor.fetchall()
        for i in output:
            if(l==i):
                print(i)
                flag=1
        if(flag==0):
             return ("invalid username or password")
        else:
            return render_template('form.html')
        
        
    else:
        return render_template('login.html')
        
 
@app.route('/form', methods = ['POST', 'GET'])
def quiz():
    if request.method == 'GET':
        return render_template('form.html')
     
    if request.method == 'POST':
        N = float(request.form.get("N"))
        P = float (request.form.get("P"))
        K = float (request.form.get("K"))
        temperature=float (request.form.get("temperature"))
        humidity= float (request.form.get("humidity"))
        ph = float ( request.form.get("ph"))
        rainfall = float(request.form.get("rainfall"))
       
        li=[[N,P,K,temperature,humidity,ph,rainfall]]
        result=pred(li)
        st=''
        for i in result:
            st=st+','+i
        return ("The crops that we recommend are:\n"+st)

    return render_template("form.html")

        
app.run(host='localhost', port=5000)

'''@app.route("/register",methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate the form data
        if not username:
            print('Please enter a username')
            return render_template('register.html')
        if not password:
            print('Please enter a password')
            return render_template('register.html')

        # Check if the username is already taken
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM login WHERE username = %s', (username,))
        user = cur.fetchone()
        if user:
            print('That username is already taken')
            return render_template('register.html')

        # Insert the new user into the database
        cur.execute('INSERT INTO login (username, password) VALUES (%s, %s)', (username, password))
        mysql.connection.commit()
        cur.close()

        print('Registration successful')
        return render_template('login.html')

    return render_template('register.html')'''
