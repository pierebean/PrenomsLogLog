import pandas as pd
import epitran
import os
from pathlib import Path
import numpy as np
import math
import matplotlib.pyplot as plt
import re
import time


## examples de garçons
prenomcible=[['ANSELME','ANSHELME','ANSHELM'],['DOMINIC','DOMINIQUE'],'LUDOVIC','PIERRE',['ÉRIC','ERIC'],'VINCENT',['JEAN-PIERRE','JEAN PIERRE'],'ROBIN',['JONATHAN','JONNATHAN','JOHNATHAN','JOHNATAN','JONNATAN'],['KEVIN','KÉVIN'],['JEAN-MARIE','JEAN MARIE'],'VADIM']

sexe=1

#importer CSV de l'INSEE fichier json
df= pd.read_csv(r'C:\Users\PIALL\OneDrive - Vaisala Oyj\perso\prénoms\nat2019.csv', sep=';')
# j'enlève les Nan
df = df.dropna()


## examples de filles (à décommenter)
# prenomcible=['SALMA',['LAURIE','LORIE','LAURI','LORI','LAURY','LORY','LORRY','LORRI'],['ESTHÈRE','ESTHER','ESTER','ESTÈR','ESTÈRE'],['REBECCA','REBECA'],['CHRISTINA','CRISTINA'],['JANA','JANNA'],'ALICE',['EYA','ÉYA','EYIA','ÉYIA','EIA','ÉIA']]
#
# sexe=2

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
        print(pren)
        subdf=df[df["preusuel"]==pren]
        subdf = subdf.drop(subdf[subdf["annais"]=='XXXX'].index)

    else:
        print('double prénom')
        print(pren)
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
    plt.plot(xx,yy, label=pren,linewidth=linsize, linestyle='-', marker='o') # plotting t, a separately


plt.grid(b=True, which='both', color='#D3D3D3', linestyle='dashdot')
plt.xlabel('Année')
plt.ylabel('Nb d''occurence')
plt.legend()
plt.show()


## prenoms uniques et tailles des prénoms
from abydos.phonetic import *

pe = FONEM()

uniquegars=[]
uniquefille=[]
mean_lengthgars=[]
mean_lengthfille=[]
firstbyyear=[]
for ann in xx:
    print(ann)
    uniquegars.append(dfgars[dfgars["annais"]==str(ann)]["preusuel"].nunique())
    uniquefille.append(dffille[dffille["annais"]==str(ann)]["preusuel"].nunique())
    mean_lengthgars.append(dfgars[dfgars["annais"]==str(ann)]["preusuel"].apply(len).mean())
    mean_lengthfille.append(dffille[dffille["annais"]==str(ann)]["preusuel"].apply(len).mean())

fig, ax = plt.subplots(1, 2)

ax[0].plot(xx,uniquegars, label='gars',linewidth=linsize, linestyle='-', marker='o')
ax[0].plot(xx,uniquefille, label='filles',linewidth=linsize, linestyle='-', marker='o')
ax[0].set_xlabel('Année')
ax[0].set_ylabel('prénoms uniques')
ax[0].grid(b=True, which='both', color='#D3D3D3', linestyle='dashdot')
ax[0].legend()

ax[1].plot(xx,mean_lengthgars, label='gars',linewidth=linsize, linestyle='-', marker='o')
ax[1].plot(xx,mean_lengthfille, label='filles',linewidth=linsize, linestyle='-', marker='o')
ax[1].set_xlabel('Année')
ax[1].set_ylabel('Nombre de lettres par prénoms')
ax[1].grid(b=True, which='both', color='#D3D3D3', linestyle='dashdot')
ax[1].legend()

plt.show()


## matrix de phonem : clustering des familles de prénoms (en chantier)

# plt.ion()
# fig = plt.figure()
# ax = fig.add_subplot(111)
# line1, = ax.plot(1, 1)
# df['phonem'] = df.preusuel.apply(lambda name: pe.encode(name))
# b=[]
# for pren in df.phonem.unique():
#
#     subdf=df[df["phonem"]==pren]
#     subdf = subdf.drop(subdf[subdf["annais"]=='XXXX'].index)
#     subdf["annais"] = pd.to_numeric(subdf["annais"])
#     subdf=subdf.sort_values(by=['annais'])
#     yy=[int(i) for i in subdf.nombre.tolist()]
#     if len(yy)>3:
#         print(pren)
#         xx=[int(i) for i in subdf.annais.tolist()]
#         # a = np.array([[pren,yy]], dtype=object)
#         line1.set_xdata(xx)
#         line1.set_ydata(yy)
#         fig.canvas.draw()
#         fig.canvas.flush_events()
#         time.sleep(1)
#         # np.vstack((a,np.asarray(b,object)))
