import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize
import scipy.stats as st

def funzione(x, A, w, phi, z):
    return A * np.sin(x*w + phi) + z

def chi2(oss, att, ossErr):
    chiArr = np.zeros(len(oss))
    return ((att-oss)/ ossErr)**2



nomeFile1 = 'C:\\Users\\Mari\\Desktop\\michelson\\datiLaser\\fotodiodoProva1Guadagno60.csv'
nomeFile2= 'C:\\Users\\Mari\\Desktop\\michelson\\datiLaser\\fotodiodoProva2Guadagno60.csv'
nomeFile3 = 'C:\\Users\\Mari\\Desktop\\michelson\\datiLaser\\fotodiodoProva4Guadagno60.csv'
nomeFile4= 'C:\\Users\\Mari\\Desktop\\michelson\\datiLaser\\fotodiodoProva5Guadagno60.csv'
nomeFile5 = 'C:\\Users\\Mari\\Desktop\\michelson\\datiLaser\\fotodiodoProva6Guadagno60.csv'
nomeFile6= 'C:\\Users\\Mari\\Desktop\\michelson\\datiLaser\\fotodiodoProva7Guadagno60.csv'

dati1 = pd.read_csv(nomeFile1)
vEff1 = dati1['voltaggioEffettivo'][2:]
mediaArr1 = dati1['media']
mediaErr1 = dati1['erroreMedia']

dati2 = pd.read_csv(nomeFile2)
vEff2 = dati2['voltaggioEffettivo'][2:]
mediaArr2 = dati2['media']
mediaErr2 = dati2['erroreMedia']

dati3 = pd.read_csv(nomeFile3)
vEff3 = dati3['voltaggioEffettivo'][2:]
mediaArr3 = dati3['media']
mediaErr3 = dati3['erroreMedia']

dati4 = pd.read_csv(nomeFile4)
vEff4 = dati4['voltaggioEffettivo'][2:]
mediaArr4 = dati4['media']
mediaErr4 = dati4['erroreMedia']

dati5 = pd.read_csv(nomeFile5)
vEff5 = dati5['voltaggioEffettivo'][2:]
mediaArr5 = dati5['media']
mediaErr5 = dati5['erroreMedia']

dati6 = pd.read_csv(nomeFile6)
vEff6 = dati6['voltaggioEffettivo'][2:]
mediaArr6 = dati6['media']
mediaErr6 = dati6['erroreMedia']

x = range(len(mediaArr1))
plt.plot(mediaArr1, '-o', color = 'teal')
plt.xlabel('Campionamenti')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.grid()
plt.title('Fluttuazioni laser prova 1')
plt.show()

plt.plot(mediaArr2, '-o', color = 'teal')
plt.xlabel('Campionamenti')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.grid()
plt.title('Fluttuazioni laser prova 2')
plt.show()

plt.plot(mediaArr3, '-o', color = 'teal')
plt.xlabel('Campionamenti')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.grid()
plt.title('Fluttuazioni laser prova 3')
plt.show()

plt.plot(mediaArr4, '-o', color = 'teal')
plt.xlabel('Campionamenti')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.grid()
plt.title('Fluttuazioni laser prova 4')
plt.show()

plt.plot(mediaArr5, '-o', color = 'teal')
plt.xlabel('Campionamenti')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.grid()
plt.title('Fluttuazioni laser prova 5')
plt.show()

plt.plot(mediaArr6, '-o', color = 'teal')
plt.xlabel('Campionamenti')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.grid()
plt.title('Fluttuazioni laser prova 6')
plt.show()

devStd1 = np.std(mediaArr1)
devStd2 = np.std(mediaArr2)
devStd3 = np.std(mediaArr3)
devStd4 = np.std(mediaArr4)
devStd5 = np.std(mediaArr5)
devStd6 = np.std(mediaArr6)

media1 = np.mean(mediaArr1)
media2 = np.mean(mediaArr2)
media3 = np.mean(mediaArr3)
media4 = np.mean(mediaArr4)
media5 = np.mean(mediaArr5)
media6 = np.mean(mediaArr6)

devArr = np.array([devStd1, devStd2, devStd3, devStd4, devStd5, devStd6])
mediaArr = np.array([media1, media2, media3, media4, media5, media6])
df = pd.DataFrame()
df['medie'] = mediaArr
df['deviazioni'] = devArr
df.to_csv('fluttuazioni.csv')
