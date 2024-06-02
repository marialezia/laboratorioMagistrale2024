import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize
import scipy.stats as st

#definisco funzione sinusoidale che voglio fittare
def funzione(x, A, w, phi, z):
    '''
    A = normalizzazione
    w = pulsazione
    phi = fase
    z = offset
    '''
    return A * (np.cos(x*w + phi))**2 + z

def piezo(w, l):
    '''
    w = pulsazione
    l = lunghezza d'onda laser
    '''
    return (w * l)/(2*np.pi)

def piezoErr(w, wErr, l, lErr):
    return np.sqrt((w*lErr)**2+(l*wErr)**2)*0.5/np.pi

laser = 633
laserErr = 6

#associo dei parametri iniziali
pstart = np.array([3.3953, 0.65,1.49,0.95])


#definisco funzione per calcolare il chi2
def chi2(oss, att, ossErr):
    '''
    oss = valori osservati
    att = valori attesi
    ossErr = errore valori osservati
    '''
    chiArr = np.zeros(len(oss))
    return ((att-oss)/ ossErr)**2

#estrapolo dati dal file csv che voglio leggere 
nomeFile = 'C:\\Users\\Mari\\Desktop\\michelson\\dati\\michelsonPasso0.2Prova5Guadagno60.csv'
dati = pd.read_csv(nomeFile)
vEff = dati['voltaggioEffettivo']
mediaArr = dati['media']
mediaErr = dati['erroreMedia']

#valori offset e rumore per calcolare errore sulla tensione misurata
offset= 0.001
noise = 0.0008

#calcolo errore di quantizzazione
erroreADC = 10/2**11/np.sqrt(12)

#associamo al voltaggio effettivo un errore che è proporzionale al valore del voltaggio: con un if controllo valore voltaggio e associo errore
vEffErr = np.zeros(len(vEff))
for i in range(len(vEffErr)):
    if i<20:
        vEffErr[i] = vEff[i] * 0.00015 + 0.0002
    elif i < 200:
        vEffErr[i] = vEff[i] * 0.0002 + 0.0003
    else:
        vEffErr[i] = vEff[i] * 0.00015 + 0.0024
        
#aggiungo in quadratura errori alla tensione misurata legati a offset, rumore e proietto l'errore del voltaggio effettivo
mediaErrTot = np.sqrt(mediaErr**2 + offset**2 + noise**2+vEffErr**2+ erroreADC**2)


#PRIMA PARTE: INTERVALLO UNICO 

#seleziono l'intervallo in quale posso fare il fit
vEff2 = vEff[100:375]
mediaArr2 = mediaArr[100:375]
mediaErr2 = mediaErr[100:375]


#faccio grafico di tutti i dati e di quelli selezionati per evidenziare intervallo selezionato
plt.plot(vEff, mediaArr, '-o', alpha = 0.8, color = 'mediumseagreen', label = 'Dati acquisiti')
plt.plot(vEff2, mediaArr2, '-o', alpha = 0.8, color = 'rebeccapurple', label = 'Intervallo selezionato')
plt.title('Guadagno 60, passo 0.2 V ')
plt.xlabel('Voltaggio Effettivo [V]')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.grid()
plt.legend()
plt.show()


#faccio fit 
parametri, cov = optimize.curve_fit(funzione, vEff2, mediaArr2, p0=[pstart], sigma = mediaErr2)
errParametri = np.sqrt(np.diag(cov))
print('parametri ottimali trovati: \n', 'A: ', parametri[0],' ± ', errParametri[0], '\n w: ', parametri[1],' ± ', errParametri[1], '\n phi: ',parametri[2],' ± ', errParametri[2], '\n z: ',parametri[3],' ± ', errParametri[3])


#faccio grafico funzione fittata e dati originali
mediaFit = funzione(vEff2, parametri[0], parametri[1], parametri[2], parametri[3])
plt.plot(vEff2, mediaFit, '-o', label= 'Fit', alpha = 0.8, color = 'darkorange')
plt.errorbar(vEff2, mediaArr2, yerr= mediaErr2, fmt ='-o', alpha = 0.8, label = 'Dati', color = 'rebeccapurple')
plt.xlabel('Voltaggio Effettivo [V]')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.title('Confronto valori misurati e funzione fittata')
plt.legend()
plt.grid()
plt.show()

#calcolo chi2
chiArr = chi2(mediaArr2, mediaFit, mediaErr2)
chi = np.sum(chiArr)/(len(mediaArr2) -4)
print('\n chi2 = ', chi)

#calcolo della costante piezoelettrica
costPiezo = piezo(parametri[1], laser)
costPiezoErr = piezoErr(parametri[1], errParametri[1], laser, laserErr)

print('costante piezoelettrica trovata = ', costPiezo, ' +- ', costPiezoErr)


#SECONDA PARTE FIT PER DIVERSI INTERVALLI


#definisco degli array con all'interno intervalli diversi per fare fit su piccole zone
arrayVEff = np.array([vEff[100:130], vEff[130:160], vEff[160:190], vEff[190:220], vEff[220:250], vEff[250:280], vEff[280:310], vEff[310:340], vEff[340:370]])
arrayMedia = np.array([mediaArr[100:130], mediaArr[130:160], mediaArr[160:190], mediaArr[190:220], mediaArr[220:250], mediaArr[250:280], mediaArr[280:310], mediaArr[310:340], mediaArr[340:370]])
arrayMediaErr = np.array([mediaErr[100:130], mediaErr[130:160], mediaErr[160:190], mediaErr[190:220], mediaErr[220:250], mediaErr[250:280], mediaErr[280:310], mediaErr[310:340], mediaErr[340:370]])


#faccio grafico di tutti i dati e di tutti gli intervalli diversi
plt.plot(vEff, mediaArr, '-o', label = 'Dati acquisiti', color = 'blue')
plt.plot(arrayVEff[0], arrayMedia[0], '-o', label = 'Intervallo 1: 20-26', alpha = 0.8,  color = 'red')
plt.plot(arrayVEff[1], arrayMedia[1], '-o', label = 'Intervallo 2: 26-32', alpha = 0.8, color = 'darkorange')
plt.plot(arrayVEff[2], arrayMedia[2], '-o', label = 'Intervallo 3: 32-38', alpha = 0.8, color = 'gold')
plt.plot(arrayVEff[3], arrayMedia[3], '-o', label = 'Intervallo 4: 38-44', alpha = 0.8, color = 'yellowgreen')
plt.plot(arrayVEff[4], arrayMedia[4], '-o', label = 'Intervallo 5: 44-50', alpha = 0.8, color = 'forestgreen')
plt.plot(arrayVEff[5], arrayMedia[5], '-o', label = 'Intervallo 6: 50-56', alpha = 0.8, color = 'turquoise')
plt.plot(arrayVEff[6], arrayMedia[6], '-o', label = 'Intervallo 7: 56-62', alpha = 0.8, color = 'teal')
plt.plot(arrayVEff[7], arrayMedia[7], '-o', label = 'Intervallo 8: 62-68', alpha = 0.8, color = 'mediumpurple')
plt.plot(arrayVEff[8], arrayMedia[8], '-o', label = 'Intervallo 9: 68-74', alpha = 0.8, color = 'm')
plt.title('Intervalli selezionati per il fit')
plt.xlabel('Voltaggio Effettivo [V]')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.legend()
plt.grid()
plt.show()

#creo array vuori per riempirli dopo dei parametri e errori parametri dei vari fit per i diversi intervalli
arrayPar = np.ones([10,4])
arrayParErr = np.ones([9,4])
arrayMediaFit = np.ones([9, len(arrayVEff[0])])
arrayChi = np.ones([9])

#faccio ciclo for per fare fit su tutti gli intervalli 
for i in range(len(arrayVEff)):
    parametri, cov = optimize.curve_fit(funzione, arrayVEff[i], arrayMedia[i], p0=[pstart], sigma = arrayMediaErr[i])
    errParametri = np.sqrt(np.diag(cov))
    arrayPar[i] = parametri
    arrayParErr[i] = errParametri
    arrayMediaFit[i] = funzione(arrayVEff[i], parametri[0], parametri[1], parametri[2], parametri[3])
    chiArr = chi2(arrayMedia[i], arrayMediaFit[i], arrayMediaErr[i])
    chi = np.sum(chiArr)/(len(arrayMedia[i]) -4)
    arrayChi[i] = chi


#faccio grafico di tutti i fit e dei dati originali
plt.plot(arrayVEff[0], arrayMediaFit[0], '-o', label = 'Fit intervallo 1: 20-26', alpha = 0.8, linewidth=2, color = 'red')
plt.plot(arrayVEff[1], arrayMediaFit[1], '-o', label = 'Fit intervallo 2: 26-32', alpha = 0.8, linewidth=2,color = 'darkorange')
plt.plot(arrayVEff[2], arrayMediaFit[2], '-o', label = 'Fit intervallo 3: 32-38', alpha = 0.8, linewidth=2,color = 'gold')
plt.plot(arrayVEff[3], arrayMediaFit[3], '-o', label = 'Fit intervallo 4: 38-44', alpha = 0.8, linewidth=2,color = 'yellowgreen')
plt.plot(arrayVEff[4], arrayMediaFit[4], '-o', label = 'Fit intervallo 5: 44-50', alpha = 0.8, linewidth=2,color = 'forestgreen')
plt.plot(arrayVEff[5], arrayMediaFit[5], '-o', label = 'Fit intervallo 6: 50-56', alpha = 0.8,linewidth=2, color = 'turquoise')
plt.plot(arrayVEff[6], arrayMediaFit[6], '-o', label = 'Fit intervallo 7: 56-62', alpha = 0.8, linewidth=2,color = 'teal')
plt.plot(arrayVEff[7], arrayMediaFit[7], '-o', label = 'Fit intervallo 8: 62-68', alpha = 0.8, linewidth=2,color = 'mediumpurple')
plt.plot(arrayVEff[8], arrayMediaFit[8], '-o', label = 'Fit intervallo 9: 68-74', alpha = 0.8, linewidth=2,color = 'm')
plt.errorbar(vEff2, mediaArr2, yerr= mediaErr2, fmt ='-o', alpha = 0.8, label = 'dati', linewidth=3,  color = 'blue', zorder = 1)



plt.xlabel('Voltaggio Effettivo [V]')
plt.ylabel('Voltaggio Fotodiodo [V]')
plt.title('Confronto dati e fit')
plt.legend() 
plt.grid()
plt.show()

#salvo i dati di tutti i parametri che ho ricavato dai vari fit
A = np.ones([9])
AErr = np.ones([9])
w = np.ones([9])
wErr = np.ones([9])
phi = np.ones([9])
phiErr = np.ones([9])
z = np.ones([9])
zErr = np.ones([9])

for i in range(9):
    A[i] = arrayPar[i][0]
    AErr[i] = arrayParErr[i][0]
    w[i] = arrayPar[i][1]
    wErr[i] = arrayParErr[i][1]
    phi[i] = arrayPar[i][2]
    phiErr[i] = arrayParErr[i][2]
    z[i] = arrayPar[i][3]
    zErr[i] = arrayParErr[i][3]
   
#calcolo le costanti piezoelettriche
costArray = piezo(w, laser)
costArrayErr = piezoErr(w, wErr, laser, laserErr)

tabella = pd.DataFrame()
tabella.index = ['20-26', '26-32', '32-38', '38-44', '44-50', '50-56', '56-62', '62-68', '68-74']
tabella['A'] = A
tabella['AErr'] = AErr
tabella['w'] = w
tabella['wErr'] = wErr
tabella['phi'] = phi
tabella['phiErr'] = phiErr
tabella['z'] = z
tabella['zErr'] = zErr
tabella['chi2'] = arrayChi
tabella['costPiezo'] = costArray
tabella['costPiezoErr'] = costArrayErr

tabella.to_csv('parametriFit.csv', index=True)

#riporto in un grafico i valori della pulsazione ottenuti dai vari fit
x = ['20-26', '26-32', '32-38', '38-44', '44-50', '50-56', '56-62', '62-68', '68-74']

wMedia = np.mean(w)
yMedia = np.full(len(x), wMedia)
plt.errorbar(x, w, yerr= wErr, fmt= '-o', color = 'teal', label = 'andamento in funzione del voltaggio')
#plt.errorbar(x, yMedia, yerr= wErr, fmt= '-o', color = 'darkorange', label = 'valore medio')

plt.xlabel('Intervallo voltaggio [V]')
plt.ylabel('Costante piezoelettrica [$nm / V $]')
plt.title('Andamento costante piezoelettrica in funzione del voltaggio')
plt.grid()
plt.show()

