# -*- coding: utf-8 -*-
"""GEN_CORR (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DL51goypRkpXtVzMKSUqwOeHV0nKy7kz
"""

#!pip  install georasters



#from bs4 import BeautifulSoup
#from google.colab import drive
#from google.colab import files
import pandas as pd
import seaborn as sns
import georasters as gr
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import requests
import tifffile as tiff
import io
import dateutil.parser
import datetime
import time

#Cette fonction permet de récupérer une donnée particulière pour un temps précis avec un run donné; cette fonction sera appelé plusieurs fonctions avec des paramètres qui varient
import json
headers={"Authorization":"Bearer ya29.a0ARrdaM969lg6n3wcXCbCidpIqEsotZEYdwxG43hsuR87EBtZArYVr885mt6h6pmFHzTwmF8Hfs9_S21eRMeJ_q0NAxS_OIsJx5Oje4l2bXq4Xh_gfrDOFyI-OXPlXhzwQmrtwtOltIc4a7mB05wjl8tuC3PO"}

def getexc(model,CoverageId,date_run,date_prev,lat,long,height):
    if height==None:
      url="https://geoservices.meteofrance.fr/api/__KZEzsd-e_dya8FrIBhfOuk8lblARc7UN__/{}?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&format=image/tiff&coverageId={}{}&subset={}&subset={}&subset={}".format(model,CoverageId,date_run,date_prev,lat,long)
    else:
      url="https://geoservices.meteofrance.fr/api/__KZEzsd-e_dya8FrIBhfOuk8lblARc7UN__/{}?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&format=image/tiff&coverageId={}{}&subset={}&subset={}&subset={}&subset={}".format(model,CoverageId,date_run,date_prev,lat,long,height)
    with open('test.tiff', 'wb') as f:
      ret = requests.get(url, stream=True)
    #print(ret.status_code)
      for data in ret.iter_content(1024):
          f.write(data)
    data = gr.from_file('test.tiff')
    data_df=data.to_pandas()
    T1=(date_run,date_prev)
    T2=data_df[data_df.iloc[:,3].astype('str').str.startswith('5.15') & data_df.iloc[:,4].astype('str').str.startswith('43.63')]['value'].to_list()[0]
    return T1,T2

jour=14

L=["2021-10-{}T00:00:00Z".format(jour),"2021-10-{}T03:00:00Z".format(jour),"2021-10-{}T06:00:00Z".format(jour),"2021-10-{}T09:00:00Z".format(jour),"2021-10{}T12:00:00Z".format(jour),"2021-10-{}T15:00:00Z".format(jour),"2021-10-{}T18:00:00Z".format(jour),"2021-10-{}T21:00:00Z".format(jour)]

#Paramètres généraux: Ce sont les paramètres qu'on doit donner à la fonction getexc, les listes créées vont servir de stockage de données mais avec une seule fonction, on aura besoin que d'une seule liste
model="MF-NWP-HIGHRES-AROME-001-FRANCE-WCS"
long="long(-22.539481000530827,23.591206784516856)"
lat="lat(31.89645994765944,60.64827366410191)"
CoverageId_T="TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___"
CoverageId_V="WIND_SPEED__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___"
CoverageId_NH="HIGH_CLOUD_COVER__GROUND_OR_WATER_SURFACE___"
CoverageId_NM="MEDIUM_CLOUD_COVER__GROUND_OR_WATER_SURFACE___"
CoverageId_NB="LOW_CLOUD_COVER__GROUND_OR_WATER_SURFACE___"
height_T="height(2)"
height_V="height(10)"
date_run=L[0]
date_prev="time(2021-07-18T08:00:00Z)"
T=[]
T_dates=[]
V=[]
V_dates=[]
NH=[]
NH_dates=[]
NM=[]
NM_dates=[]
NB=[]
NB_dates=[]

Hour_prev=L[0]
date_run=Hour_prev
def getdata(model,CoverageId,date_run,date_prev,lat,long,height):
    #Température
    p=0
    T=[]
    T_dates=[]
    for j in range(1):
      d = dateutil.parser.parse(date_run)
      hours=p
      hours_added = datetime.timedelta(hours = hours)
      q=d+hours_added
      date_run=q.strftime('%Y-%m-%dT%H:%M:%SZ')
      p=p+3
      for i in range(3):
        d = dateutil.parser.parse(date_run)
        if height==None:
          hours=i+1
        else:
          hours=i
        hours_added = datetime.timedelta(hours = hours)
        q=d+hours_added
        date_prev="time({})".format(q.strftime('%Y-%m-%dT%H:%M:%SZ'))
        try:
          T1,T2=getexc(model,CoverageId,date_run,date_prev,lat,long,height)
        except Exception as e:
            print(e)
            print('Restarting!')
            time.sleep(20)
            #continue
            try:
              T1,T2=getexc(model,CoverageId,date_run,date_prev,lat,long,height)
            except Exception as e:
              print(e)
              print('Restarting!')
              time.sleep(20)
              try:
                T1,T2=getexc(model,CoverageId,date_run,date_prev,lat,long,height)
              except Exception as e:
                print(e)
                print('Restarting!')
                time.sleep(20)
                try:
                  T1,T2=getexc(model,CoverageId,date_run,date_prev,lat,long,height)
                except Exception as e:
                  print(e)
                  print('Restarting!')
                  time.sleep(20)
                  continue
        T_dates.append(T1)
        T.append(T2)
    return T_dates, T

#getdata(model,CoverageId_T,date_run,date_prev,lat,long,height_T)

def GetAllData(annee, jour):
        #Paramètres généraux: Ce sont les paramètres qu'on doit donner à la fonction getexc, les listes créées vont servir de stockage de données mais avec une seule fonction, on aura besoin que d'une seule liste
    model="MF-NWP-HIGHRES-AROME-001-FRANCE-WCS"
    long="long(-22.539481000530827,23.591206784516856)"
    lat="lat(31.89645994765944,60.64827366410191)"
    CoverageId_T="TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___"
    CoverageId_V="WIND_SPEED__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___"
    CoverageId_NH="HIGH_CLOUD_COVER__GROUND_OR_WATER_SURFACE___"
    CoverageId_NM="MEDIUM_CLOUD_COVER__GROUND_OR_WATER_SURFACE___"
    CoverageId_NB="LOW_CLOUD_COVER__GROUND_OR_WATER_SURFACE___"
    height_T="height(2)"
    height_V="height(10)"
    #date_run=L[0]
    date_prev="time(2021-07-18T08:00:00Z)"
    T=[]
    T_dates=[]
    V=[]
    V_dates=[]
    NH=[]
    NH_dates=[]
    NM=[]
    NM_dates=[]
    NB=[]
    NB_dates=[]
    L=["{}-10-{}T00:00:00Z".format(annee,jour),"{}-10-{}T03:00:00Z".format(annee,jour),"{}-10-{}T06:00:00Z".format(annee,jour),"{}-10-{}T09:00:00Z".format(annee,jour),"{}-10-{}T12:00:00Z".format(annee,jour),"{}-10-{}T15:00:00Z".format(annee,jour),"{}-10-{}T18:00:00Z".format(annee,jour),"{}-10-{}T21:00:00Z".format(annee,jour)]
    for i in range(len(L)):
      date_run=L[i]
      K_dates, K=getdata(model,CoverageId_T,date_run,date_prev,lat,long,height_T)
      for j in range(len(K)):
        T.append(K[j])
        T_dates.append(K_dates[j])

      K_dates, K=getdata(model,CoverageId_V,date_run,date_prev,lat,long,height_V)
      for j in range(len(K)):
        V.append(K[j])
        V_dates.append(K_dates[j])

      K_dates, K=getdata(model,CoverageId_NH,date_run,date_prev,lat,long,height=None)
      for j in range(len(K)):
        NH.append(K[j])
        NH_dates.append(K_dates[j])

      K_dates, K=getdata(model,CoverageId_NM,date_run,date_prev,lat,long,height=None)
      for j in range(len(K)):
        NM.append(K[j])
        NM_dates.append(K_dates[j])

      K_dates, K=getdata(model,CoverageId_NB,date_run,date_prev,lat,long,height=None)
      for j in range(len(K)):
        NB.append(K[j])
        NB_dates.append(K_dates[j])
    Neb_df=pd.DataFrame()
    Neb_df['dates']=NB_dates
    Neb_df['NH_val']=NH
    Neb_df['NM_val']=NM
    Neb_df['NB_val']=NB
    Neb_df.to_excel("Neb{}.xlsx".format(jour), sheet_name='Nébulosité')
    Ne_df=pd.DataFrame()
    Ne_df['dates']=T_dates
    Ne_df['T_val']=T
    Ne_df['V_val']=V
    Ne_df.to_excel("Temp_vi{}.xlsx".format(jour), sheet_name='Temp_Vit')
    para={"name":"Temp_vi{}.xlsx".format(jour)}
    files={
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open("Temp_vi{}.xlsx".format(jour), "rb")
    }
    r=requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", headers=headers, files=files)
    return 'perfect'

GetAllData(2021,15)