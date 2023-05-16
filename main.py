class TramaIEEE:
    bandera = None
    longitud = None
    tipo = None
    identificadorDeTrama = None
    cargaUtil = None
    checkSum = None
    checkSumValidated = None

def extraerTrama(string):
    trama = TramaIEEE()
    bandera = string[0:2]
    if bandera != "7E":
        print("No es un comienzo de trama valido")
        return None
    trama.bandera = bandera

    longitud = string[2:6]

    trama.longitud = int(longitud, 16)

    tipo = string[6:8]
    trama.tipo = int(tipo, 16)

    identificador = string[8:10]
    trama.identificadorDeTrama = int(identificador,16)

    carga = string[10:10+ trama.longitud*2 - 4]
    trama.cargaUtil = carga

    inicioDelChecksum = 10 + trama.longitud*2 - 4
    checkSum = string[inicioDelChecksum:inicioDelChecksum + 2]
    trama.checkSum = int(checkSum, 16)
    #Calculo del valor del entero correspondiente a los bytes de la carga
    cargaTotalEntera = 0
    for i in range(0, len(carga) - 1, 2):
        cargaTotalEntera += int(carga[i] + carga[i + 1], 16)

    sumaDeBytes = cargaTotalEntera + trama.identificadorDeTrama + trama.tipo

    checkSumValidated = 0xFF - (sumaDeBytes & 0xFF)
    trama.checkSumValidated = trama.checkSum == checkSumValidated
    return trama
    
def extraerString(string):
    bandera = string[0:2]
    if bandera != "7E":
        print("No es un comienzo de trama valido")
        return 

    longitud = string[2:6]
    tramalongitud = int(longitud, 16)
    inicioDelChecksum = 10 + tramalongitud*2 - 4
    return string[0:inicioDelChecksum + 2]

def imprimirTrama(trama):
    print("bandera ", trama.bandera)
    print("long ", trama.longitud)
    print("tipo ", trama.tipo)
    print("id ", trama.identificadorDeTrama)
    print("carga", trama.cargaUtil)
    print("checkSum", trama.checkSum)
    print("checksum validado ", trama.checkSumValidated)


archivo=open("Tramas_802-15-4.log")
contenido=archivo.read()
tramasLongitudCorrecta = 0
tramasLongitudIncorrecta = 0
tramasConCheckSumInvalido = 0
tramasConCheckSumValido = 0

while contenido != "":
    tramaString = extraerString(contenido)
    trama = extraerTrama(tramaString)

    contenido = contenido[len(tramaString):]
    print(tramaString)
    if contenido[0:2] != "7E" and contenido != "":
            tramasLongitudIncorrecta = tramasLongitudIncorrecta + 1
            nextStart = contenido.find("7E")

            tramaString = contenido[0:nextStart]
            print(tramaString)

            contenido = contenido[nextStart:]
    else:
        tramasLongitudCorrecta = tramasLongitudCorrecta + 1
        if trama.checkSumValidated == True:
            tramasConCheckSumValido = tramasConCheckSumValido + 1
        else:
            tramasConCheckSumInvalido = tramasConCheckSumInvalido + 1

TramasTotales = tramasLongitudCorrecta + tramasLongitudIncorrecta
print("Tramas de longitud correcta ", tramasLongitudCorrecta)
print("Tramas de longitud incorrecta ", tramasLongitudIncorrecta)
print("Tramas con checksum valido ", tramasConCheckSumValido)
print("Tramas con checksum invalido ", tramasConCheckSumInvalido)
print("Tramas totales ", TramasTotales)
