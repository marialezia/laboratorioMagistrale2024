import pyvisa
import time
import matplotlib.pyplot as plt
import nidaqmx
import time
import sys
from datetime import datetime
import pandas as pd
import numpy as np

time.sleep(10)
now = datetime.now()

current_time = now.strftime("%Y-%B-%d_%H-%M-%S")

#codice per collegarsi ad alimentatore e sistema di acquisizione
rm = pyvisa.ResourceManager()
inst=rm.open_resource('GPIB0::18::INSTR')

inst.write(':SENS:FUNC "CURR"')
inst.write(":OUTP:STAT 1")


if len(sys.argv)<2 :
    print("Scivi almeno un parametro (passo del volt)")
    print("Parametri opzionali:")
    print("                    2) Numero di campioni per canale")
    print("                    3) Tempo che aspetto")
    print("                    4) Numero prova")
    print("                    5) guadagno")
    sys.exit(0)

passo =float(sys.argv[1])
try: 
    nCampioni =int(sys.argv[2])
except:
    nCampioni=1
try: 
    tAttesa =float(sys.argv[3])
except:
    tAttesa =1

#determino il numero di elementi per costruire l'array dividendo il voltaggio massimo che voglio dare (125) per il passo di ogni quanto vario il voltaggio
nElementiArray = int(125/passo)

#creo array dei voltaggi creando prima un array di zeri e poi riempiendo l'array con voltaggi da 0 a 125, con il passo che ho messo come parametro
voltaggio = np.zeros(nElementiArray)
for i in range(nElementiArray):
    voltaggio[i] = i*passo


mediaArray =[]# np.zeros(nElementiArray)
voltaggioEffettivo = [] #np.zeros(nElementiArray)
mediaErr = np.empty(0)
numeroProva = str(sys.argv[4])
guadagno = str(sys.argv[5])


#codice per creare un grafico che si modifichi ogni punto che prendo 
plt.ion()
fig = plt.figure()
axes = plt.gca()
axes.set_autoscaley_on(True)
axes.set_autoscalex_on(True)
linee = axes.plot(voltaggioEffettivo, mediaArray, 'ro-', label='ch0',linewidth=1)

#codice per acquisizione dati: mi collego al canale    
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0",terminal_config=nidaqmx.constants.TerminalConfiguration.RSE)

    #ciclo nell'array dei voltaggi che impone al generatore di imporre il voltaggio che ho nell'array
    for i in range(len(voltaggio)):

        #scrivo il voltaggio sull'alimentatore e aspetto il tempo tAttesa (parametro che ho chiesto) prima di leggere i dati successivi
        inst.write(("SOUR:VOLT %f" % (voltaggio[i])))
        time.sleep(tAttesa)
        
        #leggo dati (data, voltaggio effettivo)
        dataAlimentatore=inst.query(':READ? "defbuffer1", DATE, SOUR, READ')

        #ripeto la misura della tensione misurata, un numero di volte pare a nCampioni (parametro inserito), salvo i dati in un array e poi faccio la media
        mes = task.read(number_of_samples_per_channel=nCampioni)
        mean = 0.
        mediaErr = np.append(mediaErr, np.std(mes))

        for samp in mes:
            mean += samp/nCampioni
        
        #aggiungo la tensione media all'array con tutte le tensioni
        mediaArray.append(mean)

        #estrapolo voltaggio effettivo dal dato acquisito prima (dataAlimentatore che è una stringa con data e voltaggio effettivo separati da una virgola) e lo aggiungo all'array con tutti i voltaggi effettivi
        x = dataAlimentatore.split(",")
        voltaggioEffettivo.append(float(x[1]))

        #aggiorno grafico aggiungendo dati
        linee[0].set_xdata(voltaggioEffettivo)
        linee[0].set_ydata(mediaArray)
        axes.relim()
        axes.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.savefig('grafico'+ str(passo)+ 'Prova' + numeroProva + 'Guadagno' + guadagno + '.png')


        
#riazzero l'alimentatore e aspetto tempo di 10 s prima di spegnere
inst.write("SOUR:VOLT 0")
time.sleep(10)
inst.query(':READ? "defbuffer1", DATE, SOUR, READ')
inst.write(":OUTP:STAT 0")

#salvo dati raccolti in un file csv
tabella = pd.DataFrame()
tabella['voltaggioEffettivo'] = voltaggioEffettivo
tabella['media'] = mediaArray
tabella['erroreMedia'] = mediaErr
print(tabella)
nome = 'michelsonPasso'+ str(passo)+ 'Prova' + numeroProva + 'Guadagno' + guadagno + '.csv'

tabella.to_csv(nome, index=False)


