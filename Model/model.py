import numpy as np
import pandas as pd
import joblib
import pymysql
import phe
from phe import paillier

#dataset = pd.read_csv("glass.csv")

#database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="connectwithpython")
cursor = connection.cursor()

# queries for retrievint all rows
retrive_X = "Select RI,Na,Mg,Al,Si,K,Ca,Ba,Fe from glass_db;"

#executing the quires
cursor.execute(retrive_X)
X = cursor.fetchall()

retrive_Y = "Select Type from glass_db;"

#executing the quires
cursor.execute(retrive_Y)
Y = cursor.fetchall()

pubkey, privkey = paillier.generate_paillier_keypair(n_length=90)
X=np.asarray(X)
encrypted_number_list = [[pubkey.encrypt(int(j)) for j in i] for i in X]
encrypted_number_array = np.array(encrypted_number_list)
x_list = [[(j.ciphertext()) for j in i] for i in encrypted_number_array]
X_array = np.array(x_list)
X = pd.DataFrame(X_array, columns= ['RI','Na','Mg','Al','Si','K','Ca','Ba','Fe'])
X = np.nan_to_num(X)


#X = dataset.iloc[:,:-1]
#Y = dataset.iloc[:,9]

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.20, random_state=42)

from sklearn.preprocessing import StandardScaler
sc_x=StandardScaler()
X_train=sc_x.fit_transform(X_train)
X_test=sc_x.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
cls = RandomForestClassifier(criterion='entropy',n_estimators=300,random_state=42)
cls.fit(X_train, Y_train)

print(X_train)


print('ACCURACY is ',cls.score(X_test,Y_test)*100,'%')

#save the model to disk
filename = 'finalized_RFmodel.sav'
joblib.dump(cls, filename)