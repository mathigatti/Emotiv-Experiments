from psychopy import visual, core, event, gui, data
from random import shuffle,randint
from psychopy.tools.filetools import fromFile, toFile
import datetime
import os
import time
import gtk
from gonogo import *

def main():
    # Info de la sesion
    expInfo = {NAME:'nombre', BIRTHDATE:'DD/MM/AA', HAND:'mano', EXPERIMENT_TYPE:'conductual',OPERATOR:''}

    # Presento cuadro para rellenar
    dlg = gui.DlgFromDict(expInfo, title='Formulario')
    if not(dlg.OK):
        core.quit()
    else:
        fileName = expInfo[NAME]
        if not os.path.exists('./Datos/' + fileName):
            os.makedirs('./Datos/' + fileName)
        dataFile = open('./Datos/' + fileName + '/' + str(datetime.date.today()) + '_' +fileName+'.csv', 'a')
        nombreEDF = './Datos/' + fileName + "/" + str(datetime.date.today()) + '_' + fileName
        texto = expInfo[NAME] + '; ' + str(datetime.datetime.now()) + '; ' + expInfo[BIRTHDATE] + '; ' + expInfo[HAND] + '; ' + expInfo[EXPERIMENT_TYPE] + '; ' + expInfo[OPERATOR]
    dataFile.write(texto)

    ##########################
    ##  Parametros Pantalla ##
    ##########################
    res = [gtk.gdk.screen_width(), gtk.gdk.screen_height()]
    pantCompleta = True

    #win = visual.Window(res, monitor="Mi Monitor", units="pix",  color=gris, colorSpace='hex', fullscr=pantCompleta)
    win = visual.Window(res,units="pix",  color=gris, colorSpace='hex', fullscr=pantCompleta, monitor = "testMonitor")
    win.setMouseVisible(False)

    ###########################################
    ## Inicializo parametros del experimento ##
    ###########################################
    proporcion = 0.7
    pruebas = 30
    Nsess = 12

    # Tiempos
    #StimDur = 0.184
    #ISI = 0.986
    StimDur = 0.404
    ISI = 0.986

    ponermarcas  = []
    if expInfo[EXPERIMENT_TYPE] == EMOTIV:
        from multiprocessing import Process, Queue
        import guardar
        q_marcas = Queue()
        p = Process(target = guardar.save_data, args=(nombreEDF, q_marcas, ))
        p.start()
        ponermarcas = 1
    elif expInfo[EXPERIMENT_TYPE] == TRADITIONAL_EEG:
        from parallel import Parallel # Version sugerida por Fede (ver mail 02/08/2016)
        #from psychopy import parallel
        # BIOSEMI
        #q_marcas=parallel.ParallelPort(address=u'/dev/parport0')
        #q_marcas=parallel.PParallelDLPortIO(address=888) # Chequear que este bien la direccion del puerto paralelo
        q_marcas = Parallel() # Version sugerida por Fede (ver mail 02/08/2016)
        q_marcas.setData(0) # Solo para asegurarse de que arranque con todos los pins abajo
        ponermarcas = 2
    elif expInfo[EXPERIMENT_TYPE] == CONDUCTUAL:
        q_marcas = 1
        ponermarcas = 0



    cond = pacman
    stimuli = [pacmanImage,"./estimulo/fantasma_naranja.png", "./estimulo/fantasma_rosado.png", "./estimulo/fantasma_verde.png", "./estimulo/fantasma_azul.png"]
    pantalla_inicio = "./estimulo/pantini_pacman.png"
    run_training(win, proporcion, 10, 6, StimDur, ISI,res,gris,negro,blanco,stimuli,pantalla_inicio)
    run_experiment(dataFile, win, proporcion, pruebas, Nsess, StimDur, ISI, q_marcas, ponermarcas,res,gris,negro,blanco,stimuli,pantalla_inicio,cond)

    cond = angry
    stimuli = [birdImage,"./estimulo/cerdo_naranja.png", "./estimulo/cerdo_rosado.png", "./estimulo/cerdo_verde.png", "./estimulo/cerdo_azul.png"]
    pantalla_inicio = "./estimulo/pantini_angry.png"
    run_training(win, proporcion, 10, 6, StimDur, ISI,res,gris,negro,blanco,stimuli,pantalla_inicio)
    run_experiment(dataFile, win, proporcion, pruebas, Nsess, StimDur, ISI, q_marcas, ponermarcas,res,gris,negro,blanco,stimuli,pantalla_inicio,cond)


if __name__ == "__main__":
    main()
