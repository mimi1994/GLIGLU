# -*- coding: utf-8 -*-
import csv
import tempfile
import re
import sys
import numpy
import argparse
import os
from os import listdir
from os.path import isfile, join
import pprint

DEBUG = False
VERBOSE = False

#Esto esta en github

# Como indicar que la primera columna es t y la segunda A.
def PreparaCsv(fichero):

    if VERBOSE is True: print fichero

    (fdout,filename) = tempfile.mkstemp()
    #print filename
    try:
        tfile = os.fdopen(fdout,"w")
    except:
        print "Se produjo un error en la preparacion del fichero"

    fdin = open(fichero,"r")

    linea = 1

    for line in fdin:

        if linea == 1:
            line = line[2:]

        if DEBUG is True: print "LINEA: ",line
        line=line.replace('\0','')
        tfile.write(line)
        linea += 1

    tfile.close()
    fdin.close()
    return filename

def Transformaciongliadinasmg(resultadogliadinas, Ve, Vi,peso):
    try:

        resultadogliadinas['omega-gliadinas'] = 0.005*resultadogliadinas['omega-gliadinas']*(Ve/(Vi*peso))
        resultadogliadinas['alfa-gliadinas'] = 0.005*resultadogliadinas['alfa-gliadinas']*(Ve/(Vi*peso))
        resultadogliadinas['gamma-gliadinas'] = 0.005*resultadogliadinas['gamma-gliadinas']*(Ve/(Vi*peso))
        resultadogliadinas['total gliadinas'] = 0.005*resultadogliadinas['total gliadinas']*(Ve/(Vi*peso))
    except Exception:
        print Exception
        print 'Se produjo un error en la transformacion de gliadinas'
        sys.exit()
    return resultadogliadinas

def Transformaciongliadinaspeso(resultadogliadinas, Ve, Vi):
    try:
        resultadogliadinas['omega-gliadinas'] = 0.005*resultadogliadinas['omega-gliadinas']*(Ve/Vi)
        resultadogliadinas['alfa-gliadinas'] = 0.005*resultadogliadinas['alfa-gliadinas']*(Ve/Vi)
        resultadogliadinas['gamma-gliadinas'] = 0.005*resultadogliadinas['gamma-gliadinas']*(Ve/Vi)
        resultadogliadinas['total gliadinas'] = 0.005*resultadogliadinas['total gliadinas']*(Ve/Vi)
    except:
        print 'Se produjo un error en la transformacion de gliadinas'
    return resultadogliadinas

def Transformaciongluteninasmg(resultadogluteninas, Ve, Vi, peso):
    try:
        resultadogluteninas['HMW'] = 0.005*resultadogluteninas['HMW']*(Ve/(Vi*peso))
        resultadogluteninas['LMW'] = 0.005*resultadogluteninas['LMW']*(Ve/(Vi*peso))
        resultadogluteninas['total gluteninas'] = 0.005*resultadogluteninas['total gluteninas']*(Ve/(Vi*peso))
    except:
        print 'Se produjo un error en la tranformacion de gluteninas'
    return resultadogluteninas

def Transformaciongluteninaspeso(resultadogluteninas, Ve, Vi):
    try:
        resultadogluteninas['HMW'] = 0.005*resultadogluteninas['HMW']*(Ve/Vi)
        resultadogluteninas['LMW'] = 0.005*resultadogluteninas['LMW']*(Ve/Vi)
        resultadogluteninas['total gluteninas'] = 0.005*resultadogluteninas['total gluteninas']*(Ve/Vi)
    except:
        print 'Se produjo un error en la transformacion de gluteninas'
    return resultadogluteninas


def gliglu():
    #EL PROGRAMA EMPIEZA AQUI
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--microgramo", help=" Introduzca mg/grano", required="true")
    parser.add_argument("-d", "--directory", help=" Introduzca el directorio", required="true")
    #parser.add_argument("-v", "--volumen", help=" Introduzca el volumen de extraccion", required="true")
    parser.add_argument("-o", "--omegagliadinas", help=" Poner omega-gliadinas de gluteninas en gliadinas Si/No", required="true")
    args = parser.parse_args()



    dirname = args.directory

    onlyfiles = [f for f in listdir(dirname) if isfile(join(dirname, f))]

    listaresultadogliadinas = []
    listaresultadogluteninas = []
    listaGLI = []
    listaGLU = []
    listanoprocesados = []


    for i in range(0, len(onlyfiles)):
        if DEBUG is True: print type(onlyfiles[i])
        temporal = PreparaCsv(os.path.join(dirname,onlyfiles[i]))

        resultadogliadinas = {'Muestra':None, 'omega-gliadinas':0, 'alfa-gliadinas':0, 'gamma-gliadinas':0, 'total gliadinas': 0}
        resultadogluteninas = {'Muestra':None, 'omega-gliadinas':0, 'HMW':0, 'LMW':0, 'total gluteninas':0}
        resultadogliadinaspromedio = {'Muestra':None, 'omega-gliadinas':0, 'alfa-gliadinas':0, 'gamma-gliadinas':0, 'total gliadinas':0}
        resultadogliadinasestadisticos = {'Muestra':None, 'EEomega':0, 'EEalfa':0, 'EEgamma':0, 'EEtotalgliadinas':0 ,'Esperanzaomega':0, 'Esperanzaalfa':0, 'Esperanzagamma':0, 'Esperanzatotalgliadinas':0}
        resultadogluteninaspromedio = {'Muestra':0, 'HMW':0, 'LMW':0, 'total gluteninas':0}
        resultadogluteninasestadisticos = {'Muestra':0, 'EEHMW':0, 'EELMW':0, 'EEtotalgluteninas':0, 'EsperanzaHMW':0, 'EsperanzaLMW':0, 'Esperanzagluteninas':0}
        listaresultadogliadinas = resultadogliadinas
        listaresultadogluteninas = resultadogluteninas
        GLI = re.search('GLI|gli', onlyfiles[i])
        GLU = re.search('GLU|glu', onlyfiles[i])
        Peso = re.search('Peso', onlyfiles[i])

        '''
        REP = re.search('REP', 'repeticion')
        Nombre_muestra = re.search('X259-X330')
        '''

        with open(temporal, 'r') as csvfile:
            reader = csv.reader(csvfile,dialect='excel', delimiter=",")



            matriz = []
            '''
            if GLI or GLU:
            '''
            for row in reader:
                if DEBUG is True: print row
                matriz.append([float(row[0]),float(row[1])])
            '''
            elif Peso:
                for row in reader:
                    print row
                    matriz.append([float(row[1])])
            else:
                pass
            '''

            #Ve = args.volumen
            Ve = 50.0
            peso = 50.0
            Vi = 50.0
            #Vi = 1000/Peso

            if GLI:
                listaGLI.append(onlyfiles[i])
                resultadogliadinas['Muestra'] = onlyfiles[i]
                for row in matriz:
                    if DEBUG is True: print row
                    if row[0] >= 0 and row[0]<= 30:
                        resultadogliadinas['omega-gliadinas'] += row[1]
                    elif row[0] > 30 and row[0] <= 40:
                        resultadogliadinas['alfa-gliadinas'] += row[1]
                    elif row[0] > 40:
                        resultadogliadinas['gamma-gliadinas'] += row[1]
                    else:
                        print 'Se ha producido un error en el proceso matriz-diccionario'
                    resultadogliadinas['total gliadinas'] = resultadogliadinas['omega-gliadinas'] + resultadogliadinas['alfa-gliadinas'] + resultadogliadinas['gamma-gliadinas']
                if DEBUG is True: print resultadogliadinas

                # row[0] no sera igual a resultadogliadinas['Muestra'] porque en el excel donde pongamos el peso no vamos a poner el nombre del archivo en la primera columna, solo el nombre de la muestra


                '''
                if Peso:
                    for row in reader:
                        if row[0] == resultadogliadinas['Muestra']:
                            Peso = row[1]
                '''


                # Transformacion de resultadogliadinas

                if args.microgramo == 'mg':
                    transformaciongliadinasmg = Transformaciongliadinasmg(resultadogliadinas, Ve, Vi, peso)
                    listaGLI.append(resultadogliadinas)
                elif args.microgramo == 'grano':
                    transformaciongliadinaspeso = Transformaciongliadinaspeso(resultadogliadinas, Ve, Vi)
                    listaGLI.append(resultadogliadinas)
                else:
                    print 'Indique una de las dos opciones'
                    sys.exit()
                if DEBUG is True: print resultadogliadinas
            elif GLU:
                listaGLU.append(onlyfiles[i])
                resultadogluteninas['Muestra'] = onlyfiles[i]
                for row in matriz:
                    if DEBUG is True: print row
                    if row[0] < 25:
                        resultadogluteninas['omega-gliadinas'] += row[1]
                    elif row[0] >= 25 and row[0]<= 30:
                        resultadogluteninas['HMW'] += row[1]
                    elif row[0] > 30:
                        resultadogluteninas['LMW'] += row[1]
                    else:
                        print 'Se ha producido un error en el proceso matriz-diccionario'
                    resultadogluteninas['total gluteninas'] = resultadogluteninas['HMW'] + resultadogluteninas['LMW']
                if DEBUG is True: print resultadogluteninas
                # Transformacion de resultadogluteninas
                if args.microgramo == 'mg':
                    transformaciongluteninasmg = Transformaciongluteninasmg(resultadogluteninas, Ve, Vi, peso)
                    listaGLU.append(resultadogluteninas)
                elif args.microgramo == 'grano':
                    transformaciongluteninaspeso = Transformaciongluteninaspeso(resultadogluteninas, Ve, Vi)
                    listaGLU.append(resultadogluteninas)
                else:
                    print 'Indique una de las dos opciones'
                    sys.exit()
                if DEBUG is True: print resultadogluteninas

            else:
                print "No es ni GLU ni GLU"
                listanoprocesados.append(onlyfiles[i])


        os.unlink(temporal)

    pp = pprint.PrettyPrinter(indent=4)
    print "**** NO PROCESADOS ****"
    pp.pprint(listanoprocesados)
    print "**** LISTA GLI ****"
    pp.pprint(listaGLI)
    print "**** LISTA GLU ****"
    pp.pprint(listaGLU)

    if args.omegagliadinas == 'Si':
        for onlyfiles[i] in listaGLU:
            if onlyfiles[i][3:0] == listaGLI(onlyfiles[i][3:0]):
                resultadogliadinas['omega-gliadinas'] += resultadogluteninas['omega-gliadinas']
            else:
                pass
    elif args.omegagliadinas == 'No':
        pass
    else:
        print 'Indique una de las dos opciones'
        sys.exit()

    '''
    arrayGLI = []
    arrayGLU = []

    if # Nombre de muestra coincide y GLI coincide (tres repeticiones):
        arrayGLI = numpy.array([resultadogliadinas])
        promedioomega = numpy.mean(arrayGLI, axis = 1)
        desvestomega = numpy.std(arrayGLI, axis = 1)
        promdeioalfa = numpy.mean(arrayGLI, axis = 2)
        desvestalfa = numpy.std(arrayGLI, axis = 2)
        promediogamma = numpy.mean(arrayGLI, axis = 3)
        desvestgamma = numpy.std(arrayGLI, axis = 3)
        promediototalgliadinas = numpy.mean(arrayGLI, axis = 4)
        desvesttotalgliadinas = numpy.mean(arrayGLI, axis = 4)
        resultadogliadinaspomedio = {'Muestra':None, 'omega-gliadinas': promedioomega, 'alfa-gliadinas': promedioalfa, 'gamma-gliadinas': promediogamma, 'total gliadinas': promediototalgliadinas}
    elif # Nombre de muestra coincide y GLU coincide (tres repeticiones):
        arrayGLU = numpy.array([resultadogluteninas])
        promedioHMW = numpy.mean(arrayGLU, axis = 1)
        desvestHMW = numpy.std(arrayGLU, axis = 1)
        promedioLMW = numpy.mean(arrayGLU, axis = 2)
        desvestLMW = numpy.std(arrayGLU, axis = 2)
        promediototalgluteninas = numpy.mean(arrayGLU, axis = 3)
        desvesttotalgluteninas = numpy.std(arrayGLU, axis = 3)
    '''

    # Crear excel con Muestra, Promedio de cada elemento, estadístico de cada elemento

    #esto se pone al final del procesamiento para borrar el fichero temporal


# Ejecucion de la funcion caesarenc()
if __name__ == "__main__":
	gliglu()
