import pandas as pd
import numpy as np
import streamlit as st
from sklearn.utils import shuffle
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity


df=pd.read_csv("zomato_dataset_refined.csv")
df=df.drop("Unnamed: 0",axis=1)

#vec=TfidfVectorizer(analyzer="word",lowercase=False)
#hotels=vec.fit_transform(df["Restaurant Name"])
#hotels=hotels.toarray()

def rate_recom(df,price):

    df=df[df["Prices"]<=price]
    df_new=shuffle(df)
    df_new=df_new.drop(["Dining Rating","Delivery Rating",
                    "Dining Votes","Delivery Votes",
                    "Place Name","City",
                    "Special mentions"],axis=1)
    return df_new

def dine_recom(df,price):

    df=df[df["Dining Rating"]==price]
    df_new=shuffle(df)
    df_new=df_new.drop(["Dining Rating","Delivery Rating",
                    "Dining Votes","Delivery Votes",
                    "Place Name","City",
                    "Special mentions"],axis=1)
    return df_new

def del_recom(df,price):

    df=df[df["Delivery Rating"]==price]
    df_new=shuffle(df)
    df_new=df_new.drop(["Dining Rating",
                    "Dining Votes","Delivery Votes",
                    "Place Name","City",
                    "Special mentions"],axis=1)
    return df_new


st.write("Cuisine Recommender")
st.title("Cuisine recommender based on Zomato")

st.image("logo.png")
st.markdown("Disclaimer: logo from Zomato website")

st.sidebar.title("Zomato Cuisine Recommend")
st.sidebar.text("Developed by Suriya Narayanan")

city=st.selectbox("Enter Your City:",
             ["Hyderabad","Jaipur","Mumbai","Chennai","Bangalore","Ahmedabad","Kolkata","Pune","Kochi","Raipur","Lucknow","New Delhi","Goa","Banaswadi","Ulsoor"])

def get_place(city):
    df_1=df[df["City"]==city]
    pl=df_1["Place Name"].value_counts()
    pl=pl.index
    pl=list(pl)
    return pl
pl=get_place(city)

places=st.selectbox("Select Your Place Name:",pl)

def get_cus(city,places):
    df_1=df[df["City"]==city]
    df_2=df_1[df_1["Place Name"]==places]
    cs=df_2["Cuisine "].value_counts()
    cs=cs.index
    cs=list(cs)
    return cs

cs=get_cus(city,places)

cuisine=st.selectbox("Select Your Cuisine:",cs)

def get_spl(city,places,cs):
    df_1=df[df["City"]==city]
    df_2=df_1[df_1["Place Name"]==places]
    df_3=df_2[df_2["Cuisine "]==cs]
    spl=df_3["Special mentions"].value_counts()
    spl=spl.index
    spl=list(spl)
    #df_4=df_3[df_3["Special mentions"]==spl]
    return spl,df_3

spl,df_2=get_spl(city,places,cuisine)
special=st.selectbox("Special Mentions:",spl)
#st.text()

def ds(spl,df):
    da=df[df["Special mentions"]==spl]
    return da

df_3=ds(special,df_2)

price_per=df_3["Prices"].describe(percentiles=[0.4,0.75])
price_per1=price_per["40%"]

dine_per=df_3["Dining Rating"]
dine_per1=max(dine_per)

del_per=df_3["Delivery Rating"]
del_per1=max(del_per)

if(st.button("Recommend")):
    st.header("Best on rate:")
    rr=rate_recom(df_3,price_per1)
    rr=rr[0:5]
    blankIndex=[''] * len(rr)
    rr.index=blankIndex
    st.table(rr)
    st.header("Best on Dining:")
    dr=dine_recom(df_3,dine_per1)
    dr=dr[0:5]
    blankIndex=[''] * len(dr)
    dr.index=blankIndex
    st.table(dr)
    st.header("Fast Delivery:")
    fr=del_recom(df_3,del_per1)
    fr=fr[0:5]
    blankIndex=[''] * len(fr)
    fr.index=blankIndex
    st.table(fr)
