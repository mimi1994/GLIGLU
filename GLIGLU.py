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
import xlsxwriter

DEBUG = False
VERBOSE = False
OMEGAGLIADINAS = False

#Variables locales
Ve = 0.0

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

def Transformaciongliadinasgrano(resultadogliadinas, Ve, Vi):
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
        resultadogluteninas['omega-gliadinas'] = 0.005*resultadogluteninas['omega-gliadinas']*(Ve/(Vi*peso))
        resultadogluteninas['HMW'] = 0.005*resultadogluteninas['HMW']*(Ve/(Vi*peso))
        resultadogluteninas['LMW'] = 0.005*resultadogluteninas['LMW']*(Ve/(Vi*peso))
        resultadogluteninas['total gluteninas'] = 0.005*resultadogluteninas['total gluteninas']*(Ve/(Vi*peso))
    except:
        print 'Se produjo un error en la tranformacion de gluteninas'
    return resultadogluteninas

def Transformaciongluteninasgrano(resultadogluteninas, Ve, Vi):
    try:
        resultadogluteninas['omega-gliadinas'] = 0.005*resultadogluteninas['omega-gliadinas']*(Ve/Vi)
        resultadogluteninas['HMW'] = 0.005*resultadogluteninas['HMW']*(Ve/Vi)
        resultadogluteninas['LMW'] = 0.005*resultadogluteninas['LMW']*(Ve/Vi)
        resultadogluteninas['total gluteninas'] = 0.005*resultadogluteninas['total gluteninas']*(Ve/Vi)
    except:
        print 'Se produjo un error en la transformacion de gluteninas'
    return resultadogluteninas

def Variables():
    peso = float(peso)
    Vi = 1000/peso
    return Ve, Vi, peso

def gliglu():
    #EL PROGRAMA EMPIEZA AQUI
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--microgramo", help=" Introduzca mg/grano", required="true")
    parser.add_argument("-d", "--directory", help=" Introduzca el directorio", required="true")
    parser.add_argument("-v", "--volumen", help=" Introduzca el volumen de extraccion", dest='Ve', action='store', required="true")
    parser.add_argument("-o", "--omegagliadinas", help=" Poner omega-gliadinas de gluteninas en gliadinas", dest='OMEGAGLIADINAS',action='store_true',default=False)
    parser.add_argument('--debug', help='Habilitar depuracion', dest='DEBUG', action='store_true',default=False)
    args = parser.parse_args()


    dirname = args.directory

    onlyfiles = [f for f in listdir(dirname) if isfile(join(dirname, f))]

    listaGLIonlyfiles = []
    listaGLUonlyfiles = []
    listaGLI = []
    listaGLU = []
    listanoprocesados = []

    resultadogliadinas = {'Muestra':None, 'omega-gliadinas':0, 'alfa-gliadinas':0, 'gamma-gliadinas':0, 'total gliadinas': 0}
    resultadogluteninas = {'Muestra':None, 'omega-gliadinas':0, 'HMW':0, 'LMW':0, 'total gluteninas':0}
    resultadogliadinaspromedio = {'Muestra':None, 'omega-gliadinas':0, 'alfa-gliadinas':0, 'gamma-gliadinas':0, 'total gliadinas':0}
    resultadogliadinasestadisticos = {'Muestra':None, 'EEomega':0, 'EEalfa':0, 'EEgamma':0, 'EEtotalgliadinas':0 ,'IComega':0, 'ICalfa':0, 'ICgamma':0, 'ICtotalgliadinas':0}
    resultadogluteninaspromedio = {'Muestra':0, 'HMW':0, 'LMW':0, 'total gluteninas':0}
    resultadogluteninasestadisticos = {'Muestra':0, 'EEHMW':0, 'EELMW':0, 'EEtotalgluteninas':0, 'ICHMW':0, 'ICLMW':0, 'ICgluteninas':0}


    for i in onlyfiles:
        if DEBUG: print type(onlyfiles[i])
        temporal = PreparaCsv(os.path.join(dirname,onlyfiles[i]))

        GLI = re.search('GLI|gli', onlyfiles[i])
        GLU = re.search('GLU|glu', onlyfiles[i])
        HAVEPESO = re.search('peso', onlyfiles[i])

        '''
        REP = re.search('REP', 'repeticion')
        Nombre_muestra = re.search('X259-X330')
        '''

        with open(temporal, 'r') as csvfile:
            reader = csv.reader(csvfile,dialect='excel', delimiter=",")


            matriz = []
            for row in reader:
                if DEBUG is True: print row
                matriz.append([float(row[0]),float(row[1])])


            if GLI:
                listaGLIonlyfiles.append(onlyfiles[i])
                resultadogliadinas['Muestra'], extension = os.path.splitext(onlyfiles[i]) # Menos los símbolos
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


                # Transformacion de resultadogliadinas

                for i in onlyfiles:
                    if HAVEPESO:
                        for row in reader:
                            if row[0] == resultadogliadinas['Muestra'][3:]:
                                peso = float(row[1])

                Variables()

                if args.microgramo == 'mg':
                    transformaciongliadinas = Transformaciongliadinasmg(resultadogliadinas, Ve, Vi, peso)
                    listaGLI.append(transformaciongliadinas)
                elif args.microgramo == 'grano':
                    transformaciongliadinas = Transformaciongliadinasgrano(resultadogliadinas, Ve, Vi)
                    listaGLI.append(transformaciongliadinas)
                else:
                    print 'Indique una de las dos opciones'
                    sys.exit()
                if DEBUG is True: print resultadogliadinas
            elif GLU:
                listaGLUonlyfiles.append(onlyfiles[i])
                resultadogluteninas['Muestra'], extension = os.path.splitext(onlyfiles[i])
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
                for i in onlyfiles:
                    if HAVEPESO:
                        for row in reader:
                            if row[0] == resultadogluteninas['Muestra'][3:]:
                                peso = float(row[1])

                Variables()
                if args.microgramo == 'mg':
                    transformaciongluteninas = Transformaciongluteninasmg(resultadogluteninas, Ve, Vi, peso)
                    listaGLU.append(transformaciongluteninas)
                    if DEBUG is True: print transformaciongluteninas
                elif args.microgramo == 'grano':
                    transformaciongluteninas = Transformaciongluteninasgrano(resultadogluteninas, Ve, Vi)
                    listaGLU.append(transformaciongluteninas)
                    if DEBUG is True: print transformaciongluteninas
                else:
                    print 'Indique una de las dos opciones'
                    sys.exit()

            else:
                print "No es ni GLU ni GLU"
                listanoprocesados.append(onlyfiles[i])


        os.unlink(temporal)

    pp = pprint.PrettyPrinter(indent=4)
    print "**** NO PROCESADOS ****"
    pp.pprint(listanoprocesados)
    print "**** LISTA GLI ****"
    pp.pprint(listaGLIonlyfiles)
    print "**** LISTA GLU ****"
    pp.pprint(listaGLUonlyfiles)

    if OMEGAGLIADINAS is True:
        for a in listaGLU:
            for b in listaGLI:
                if transformaciongluteninas['Muestra']('GLI' + a[3:]) == transformaciongliadinas['Muestra']:
                    transformaciongliadinas['omega-gliadinas'] += transformaciongluteninas['omega-gliadinas']

    print transformaciongliadinas
    print transformaciongluteninas


    arrayGLI = []
    arrayGLU = []

    for i in listaGLI:
        for a in listaGLI:
            if transformaciongliadinas['Muestra'][0:7] == transformaciongliadinas['Muestra'][0:7]:
                arrayGLI = numpy.array([transformaciongliadinas])
                promedioomega = numpy.mean(arrayGLI, axis = 1)
                desvestomega = numpy.std(arrayGLI, axis = 1)
                promdeioalfa = numpy.mean(arrayGLI, axis = 2)
                desvestalfa = numpy.std(arrayGLI, axis = 2)
                promediogamma = numpy.mean(arrayGLI, axis = 3)
                desvestgamma = numpy.std(arrayGLI, axis = 3)
                promediototalgliadinas = numpy.mean(arrayGLI, axis = 4)
                desvesttotalgliadinas = numpy.mean(arrayGLI, axis = 4)
                # Error estandar
                eeomega = desvestomega/(3)^(1/2)
                eealfa = desvestalfa/(3)^(1/2)
                eegamma = desvestgamma/(3)^(1/2)
                eetotalgliadinas = desvesttotalgliadinas/(3)^(1/2)
                # Intervalo de confianza
                icomega = 1.96*(desvestomega/(3)^(1/2))
                icalfa = 1.96*(desvestalfa/(3)^(1/2))
                icgamma = 1.96*(desvestgamma/(3)^(1/2))
                ictotalgliadinas = 1.96*(desvesttotalgliadinas/(3)^(1/2))
                resultadogliadinaspomedio = {'Muestra':transformaciongliadinas['Muestra'], 'omega-gliadinas': promedioomega, 'alfa-gliadinas': promedioalfa, 'gamma-gliadinas': promediogamma, 'total gliadinas': promediototalgliadinas}
                resultadogliadinasestadisticos = {'Muestra':transformaciongliadinas['Muestra'], 'EEomega': eeomega, 'EEalfa': eealfa, 'EEgamma': eegamma, 'EEtotalgliadinas': eetotalgliadinas, 'IComega': icomega, 'ICalfa': icalfa, 'ICgamma': icgamma, 'ICtotalgliadinas': ictotalgliadinas}

    for a in listaGLU:
        for a in listaGLU:
            if transformaciongluteninas['Muestra'][0:7] == transformaciongluteninas['Muestra'][0:7]:
                arrayGLU = numpy.array([transformaciongluteninas])
                promedioHMW = numpy.mean(arrayGLU, axis = 1)
                desvestHMW = numpy.std(arrayGLU, axis = 1)
                promedioLMW = numpy.mean(arrayGLU, axis = 2)
                desvestLMW = numpy.std(arrayGLU, axis = 2)
                promediototalgluteninas = numpy.mean(arrayGLU, axis = 3)
                desvesttotalgluteninas = numpy.std(arrayGLU, axis = 3)
                # Error estandar
                eeHMW = desvestHMW/(3)^(1/2)
                eeLMW = desvestLMW/(3)^(1/2)
                eetotalgluteninas = desvesttotalgluteninas/(3)^(1/2)
                # Intervalo de confianza
                icHMW = 1.96*(desvestHMW/(3)^(1/2))
                icLMW = 1.96*(desvestLMW/(3)^(1/2))
                ictotalgluteninas = 1.96*(desvesttotalgluteninas/(3)^(1/2))
                resultadogluteninaspromedio = {'Muestra':transformaciongluteninas['Muestra'], 'HMW': promedioHMW, 'LMW': promedioLMW, 'total gluteninas': promediototalgluteninas}
                resultadogluteninasestadisticos = {'Muestra':transformaciongluteninas['Muestra'], 'EEHMW': eeHMW, 'EELMW': eeLMW, 'EEtotalgluteninas': eetotalgluteninas, 'ICHMW': icHMW, 'ICLMW': icLMW, 'ICtotalgluteninas': ictotalgluteninas}


    workbook = xlswriter.Workbook('GLIGLU.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    for a in listaGLI:
        for key in resultadogliadinaspromedio.keys():
            col += 1
            if a == 0:
                worksheet.write(row, col, key)
            for item in resultadogliadinaspromedio[key]:
                worksheet.write(row +1, col, item)
                col += 1
        for key in resultadogliadinasestadisticos.key():
            col += 1
            worksheet.write(row, col, key)
            for item in resultadogliadinasestadisticos[key]:
                worksheet.write(row +1, col, item)
                col += 1
    for b in listaGLU:
        for key in resultadogluteninaspromedio.keys():
            col += 1
            if b == 0:
                worksheet.write(row, col, key)
            for item in resultadogluteninaspromedio[key]:
                worksheet.write(row +1, col, item)
                col += 1
        for key in resultadogluteninasestadisticos.key():
            col += 1
            worksheet.write(row, col, key)
            for item in resultadogluteninasestadisticos[key]:
                worksheet.write(row +1, col, item)
                col  += 1

    workbook.close()

    # Crear excel con Muestra, Promedio de cada elemento, estadístico de cada elemento

    #esto se pone al final del procesamiento para borrar el fichero temporal


# Ejecucion de la funcion caesarenc()
if __name__ == "__main__":
	gliglu()
