import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import re
import time
#from abydos.phonetic import *
from scipy.signal import savgol_filter
#pe = FONEM()


def countvowels(string):
    num_vowels=0
    num_consonants=0
    string=string.replace(' ','')
    for char in string:
        if char in 'AEIOUYÀÂÆÉÈÊËÎÏÔŒÙÛÜŸ':
           num_vowels += 1
        if char in 'ÇBCDFGHJKLMNPQRSTVWXZ':
           num_consonants += 1  
    return num_vowels/(num_consonants+num_vowels)


## examples de garçons
prenomcible=['MEHDI',['ANSELME','ANSHELME','ANSHELM'],['DOMINIC','DOMINIQUE'],'LUDOVIC','PIERRE',['ÉRIC','ERIC'],'VINCENT',['JEAN-PIERRE','JEAN PIERRE'],'ROBIN',['JONATHAN','JONNATHAN','JOHNATHAN','JOHNATAN','JONNATAN'],['ANDREW','ANDRÉ']]
#prenomcible=[['VIRGIL','VIRGYL','VIRGILE','VIRGYLE'],'YURI']
#prenomcible=['ROBIN','ALEXANDRE','SIMON','YURI','MAX','SATURNIN',['ELZEAR','ÉLZÉAR','ELZÉAR','ELZÉARD','ELZEARD'],'AUBIN']
sexe=1

#prenomcible=['BRUNO','GÉRALD','ÉRIC','PAP','SÉBASTIEN','OLIVIER','DAMIEN','MARC','STANISLAS']
#prenomcible=['BRUNO','GÉRALD','ÉRIC','PAPA','SÉBASTIEN','OLIVIER','DAMIEN','MARC','STANISLAS']
#sexe=1


## examples de filles (à décommenter)
#prenomcible=['SALMA',['LAURIE','LORIE','LAURI','LORI','LAURY','LORY','LORRY','LORRI'],['ESTHÈRE','ESTHER','ESTER','ESTÈR','ESTÈRE'],['REBECCA','REBECA'],['CHRISTINA','CRISTINA'],['JANA','JANNA'],'ALICE',['EYA','ÉYA','EYIA','ÉYIA','EIA','ÉIA']]
#prenomcible=[['LEIA','LEYA'],['CLEMENTINE','CLÉMENTINE'],['JOSÉPHINE','JOSEPHINE']]
#prenomcible=[['JASMINE'],['SUZANNE'],['JUDITH','JUDIT'],['MARLENE','MARLÈNE'],['LOUISE'],['MARIE'],['ROXANNE','ROXAN'],['THALIA']]
#prenomcible=['CATHERINE','AMÉLIE','BRIGITTE','SYLVIE','YAËL','AGNÈS']
#sexe=2

#importer CSV de l'INSEE fichier csv
df= pd.read_csv(r'C:\Users\PIALL\OneDrive - Vaisala Oyj\perso\prénoms\nat2019.csv', sep=';')
# j'enlève les Nan
df = df.dropna()


dfgars=df[df["sexe"]==1]
dffille=df[df["sexe"]==2]

df=df[df["sexe"]==sexe]


## je trace les graphs de ma liste (/!\ gars ou filles)
fig = plt.figure(1)
ax = fig.gca()
ax.set_yscale('log')

#je boucle sur ma liste de prénom
for pren in prenomcible:
    linsize=2

    if len(pren[0])==1:
        
        subdf=df[df["preusuel"]==pren]
        subdf = subdf.drop(subdf[subdf["annais"]=='XXXX'].index)

    else:        
        
        subdf = []
        for subpren in pren:
            subsubdf=df[df["preusuel"]==subpren]
            subsubdf = subsubdf.drop(subsubdf[subsubdf["annais"]=='XXXX'].index)
            subdf.append(subsubdf)
        subdf = pd.concat(subdf)
        subdf=subdf.drop(['preusuel'], axis=1)
        subdf=subdf.groupby(by="annais").sum()
        subdf = subdf.reset_index()    
    subdf["annais"] = pd.to_numeric(subdf["annais"])
    subdf=subdf.sort_values(by=['annais'])

    xx=[int(i) for i in subdf.annais.tolist()]
    yy=[int(i) for i in subdf.nombre.tolist()]
    print(pren)
    print(str(subdf["annais"].iloc[-1])+':'+str(subdf["nombre"].iloc[-1]))
    plt.plot(xx,yy, label=pren,linewidth=linsize, linestyle='-', marker='o') # plotting t, a separately


plt.grid(b=True, which='both', color='#D3D3D3', linestyle='dashdot')
plt.xlabel('Année')
plt.ylabel('Nb d''occurence')
plt.legend()
plt.show()


## prenoms uniques et tailles des prénoms

uniquegars=[]
uniquefille=[]
mean_lengthgars=[]
mean_lengthfille=[]
mean_vowelratio_gars=[]
mean_vowelratio_fille=[]
std_lengthgars=[]
std_lengthfille=[]
std_vowelratio_gars=[]
std_vowelratio_fille=[]
firstbyyear=[]
for ann in xx:
    print(ann)
    uniquegars.append(dfgars[dfgars["annais"]==str(ann)]["preusuel"].nunique())
    uniquefille.append(dffille[dffille["annais"]==str(ann)]["preusuel"].nunique())
    mean_lengthgars.append(dfgars[dfgars["annais"]==str(ann)]["preusuel"].apply(len).mean())
    mean_lengthfille.append(dffille[dffille["annais"]==str(ann)]["preusuel"].apply(len).mean())
    mean_vowelratio_gars.append(dfgars[dfgars["annais"]==str(ann)]["preusuel"].apply(countvowels).mean())
    mean_vowelratio_fille.append(dffille[dffille["annais"]==str(ann)]["preusuel"].apply(countvowels).mean())
    
    std_lengthgars.append(dfgars[dfgars["annais"]==str(ann)]["preusuel"].apply(len).std())
    std_lengthfille.append(dffille[dffille["annais"]==str(ann)]["preusuel"].apply(len).std())
    std_vowelratio_gars.append(dfgars[dfgars["annais"]==str(ann)]["preusuel"].apply(countvowels).std())
    std_vowelratio_fille.append(dffille[dffille["annais"]==str(ann)]["preusuel"].apply(countvowels).std())


fig, ax = plt.subplots(1, 3)

ax[0].plot(xx,uniquegars, label='gars',linewidth=linsize,  color='#1B2ACC', marker='o')
ax[0].plot(xx,uniquefille, label='filles',linewidth=linsize,  color='#CC4F1B', marker='o')
ax[0].set_xlabel('Année')
ax[0].set_xlim([1900,2019])
ax[0].set_ylabel('prénoms uniques')
ax[0].grid(b=True, which='both', color='#D3D3D3', linestyle='dashdot')
ax[0].legend()

ax[1].plot(np.array(xx), np.array(mean_lengthfille), label='gars',  color='#1B2ACC')
ax[1].fill_between(np.array(xx), np.array(mean_lengthfille)-np.array(std_lengthfille)/2, np.array(mean_lengthfille)+np.array(std_lengthfille)/2,  alpha=0.5, edgecolor='#1B2ACC', facecolor='#089FFF')
ax[1].plot(np.array(xx), np.array(mean_lengthgars), label='filles',  color='#CC4F1B')
ax[1].fill_between(np.array(xx), np.array(mean_lengthgars)-np.array(std_lengthgars)/2, np.array(mean_lengthgars)+np.array(std_lengthgars)/2,  alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
ax[1].set_xlabel('Année')
ax[1].set_xlim([1900,2019])
ax[1].set_ylabel('Nombre de lettres par prénoms')
ax[1].grid(b=True, which='both', color='#D3D3D3', linestyle='dashdot')
ax[1].legend()


ax[2].plot(np.array(xx), np.array(mean_vowelratio_fille), label='gars', color='#1B2ACC')
ax[2].fill_between(np.array(xx), np.array(mean_vowelratio_fille)-np.array(std_vowelratio_fille)/2, np.array(mean_vowelratio_fille)+np.array(std_vowelratio_fille)/2,  alpha=0.5, edgecolor='#1B2ACC', facecolor='#089FFF')
ax[2].plot(np.array(xx), np.array(mean_vowelratio_gars), label='filles',  color='#CC4F1B')
ax[2].fill_between(np.array(xx), np.array(mean_vowelratio_gars)-np.array(std_vowelratio_gars)/2, np.array(mean_vowelratio_gars)+np.array(std_vowelratio_gars)/2,  alpha=0.5, edgecolor='#CC4F1B', facecolor='#FF9848')
ax[2].set_xlabel('Année')
ax[2].set_xlim([1900,2019])
ax[2].set_ylabel('Ratio de Voyelles dans le prénom')
ax[2].grid(b=True, which='both', color='#D3D3D3', linestyle='dashdot')
ax[2].legend()

plt.show()


## matrix de phonem : clustering des familles de prénoms (en chantier)


df=dffille
df['phonem'] = df.preusuel.apply(lambda name: pe.encode(name))

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(xx, yy, linestyle='-', marker='o')
line2, = ax.plot(xx, yy, linestyle='-')
ax.grid(b=True, which='both', color='#D3D3D3', linestyle='dashdot')
ax.set_yscale('log')
ax.set_xlim([1900,2019])
ax.set_ylim([1,1e4])

b=[]
for phon in df.phonem.unique():
    pren=df[df["phonem"]==phon]['preusuel'].unique().tolist()
    if len(pren[0])==1:

        subdf=df[df["preusuel"]==pren]
        subdf = subdf.drop(subdf[subdf["annais"]=='XXXX'].index)
    else:
        print('double prénom')
        subdf = []
        for subpren in pren:
            subsubdf=df[df["preusuel"]==subpren]
            subsubdf = subsubdf.drop(subsubdf[subsubdf["annais"]=='XXXX'].index)
            subdf.append(subsubdf)
        subdf = pd.concat(subdf)
        subdf=subdf.drop(['preusuel'], axis=1)
        subdf=subdf.groupby(by="annais").sum()
        subdf = subdf.reset_index()
    subdf["annais"] = pd.to_numeric(subdf["annais"])
    subdf=subdf.sort_values(by=['annais'])

    yy=[int(i) for i in subdf.nombre.tolist()]
    if len(yy)>3:
        print(pren)
        xx=[int(i) for i in subdf.annais.tolist()]
        windowslength=min([9 ,max([2,round(np.floor(len(xx) / 2) * 2 - 1)])])
        yhat = savgol_filter(yy, windowslength, min([3, windowslength-1]))
        line1.set_xdata(xx)
        line1.set_ydata(yy)
        line2.set_xdata(xx)
        line2.set_ydata(yhat)
        ax.set_title(phon)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(1)
        # np.vstack((a,np.asarray(b,object)))
