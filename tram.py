###########################################################################################################
#  TramBot, no necesitas más, ya nunca volveras a llegar tarde, no volveras a perder ese tram. 
# 
#
#    Desing By DVerdejo and Secury
#
# **Escribir tu TOKEN y debes tener el archivo paradas.json en el mismo directorio que este bot para que funcione//
#Ultima actualizacion por verdejus 23:50-18/10/2017
###########################################################################################################
#⌚️
#📌
import telegram.ext, requests, re, time, json

#
# Funcion Inicial para el comando /start 
#
#  Saluda respondiendo por el username o name del usuario y diciendo que hago
#
def start(bot,update):
    #username de quien manda el mensaje para saludar
    name=update.message.from_user.name
    
    update.message.reply_text('Hola '+ name +' soy TramBot escribe /help para obtener ayuda.')


#
# Funcion de Ayuda para el comando /help
#
#  Mostrar ayuda detallada de cada comando
#
def help(bot,update):
    update.message.reply_text('Ayuda:\n/start - Saludo del bot.\n/paradas - Paradas disponibles.\n/times Origen Destino - Horarios de hoy.\n/timesto Origen Destino HInicio HFin - Horarios en un intervalo de tiempo, formato de hora XX:XX.\n/help - Muestra la ayuda.')




#
# Funcion TimesToday: devuelve el horario completo de salidas de una parada de tram a 
#  otra parada destino con fecha actual.
#
# [*] USO: /times Bulevar-del-Pla Alicante-Luceros 
#
def timestoday(bot,update,args):

    #Validacion de argumentos, solo recibe origen y destino
    if (len(args) == 2):

        #Obtengo la fecha actual
        today = time.strftime("%x")

        #Cargo el json de las paradas y sus respectivos codigos
        leer = json.loads(open('./paradas.json').read())

        #Valida si existe el argumento 1 (origen) y el argumento 2 (destino)
        numid = leer.get(str.lower(args[0]), 'Nothing')
        numid2 = leer.get(str.lower(args[1]), 'Nothing')
        
        #Compruebo que el origen y el destino sean distintos
        if(args[0]==args[1]):
            update.message.reply_text('Error.\nEl origen y destino coinciden!')
        else:

            #Valida si ha encontrado la codificacion de la parada de origen y destino
            if((numid in "Nothing") or (numid2 in "Nothing")):
                update.message.reply_text("Error en las paradas.\nEs posible que haya errores en los nombres de las paradas")
            else:
			
                #Construyo y realizo la peticion con los datos correspondientes
                payload = {
				'origen': numid,
				'aceptar': '0',
				'key': '0',
				'destino': numid2,
				'fecha': today,
				'hini': '00:00',
				'hfin': '23:59',
				'calcular': '1'
                }
                r = requests.post("http://www.tramalicante.es/horarios.php", data=payload)

                #Scrapeo cada valor de la tabla de horarios
                cadatd = re.findall("<td>(\d+:\d+)</td>", r.text)

                total=''
                numero1='-1'
                numero0='-1'
                #Mando el horario de la forma: en una linea la hora y en la siguiente todas las
                #veces que sale en esa hora, y asi con todas las horas.
                for hora in cadatd:
                    #imprime horas por grupos de hora
                    if(hora[0]==numero0 and hora[1]==numero1):
                       
                        total=(total+hora+' ')
                    #detecta cuando tiene que pasar a la siguiente hora
                    else:
                        #Detectar transbordo
                        if(numero0*10+numero1 > hora[0]*10+hora[1]):
                            total=total+'\n\nTRANSBORDOOOR\n'
                        
                        numero0=hora[0]
                        numero1=hora[1]
                        total=(total+'\n'+'⌚️'+numero0+numero1+'\n'+'📌'+hora+' ')

                update.message.reply_text('Salidas desde '+str.lower(args[0])+' a '+str.lower(args[1])+ ' :'+total)

    else:
        update.message.reply_text("Error en los parametros.\nUso /times Origen Destino")

# Funcion TimesIntervalo: devuelve el horario de salidas de una estacion origen a una destino en un intervalo de horas
# establecido por el usuario (como argumento 2 y 3)
#
# [*] USO: /timesto Bulevar-del-Pla-Alicante-Luceros 7 9
#
#
def timesintervalo(bot,update,args):

    if(len(args) == 4):

        #Cambiar ubicacion del JSON **************************************************
        leer = json.loads(open('./paradas.json').read())
        
        #Valida si existe el argumento 1 (origen) y el argumento 2 (destino)
        numid = leer.get(str.lower(args[0]), 'Nothing')
        numid2 = leer.get(str.lower(args[1]), 'Nothing')

        #Compruebo que el origen y el destino sean distintos
        if(args[0]==args[1]):
            update.message.reply_text('Error.\nEl origen y destino coinciden!')
        
        else:
            #Comprobacion del formato de hora correcto
            if(len(args[2])==5 and len(args[3])==5 and args[2][2]==':'and args[3][2]==':'and args[2][0].isdigit() and args[2][1].isdigit() and args[2][3].isdigit() and args[2][4].isdigit() and args[3][0].isdigit() and args[3][1].isdigit()and args[3][3].isdigit() and args[3][4].isdigit()):
	    	
                #Valida si ha encontrado la codificacion de la parada de origen y destino
                if((numid in "Nothing") or (numid2 in "Nothing")):
                    update.message.reply_text("Error en las paradas.\nEs posible que haya errores en los nombres de las paradas")
                else:
                    h1=args[2][0]*1000+args[2][1]*100+args[2][3]*10+args[2][4]
                    h2=args[3][0]*1000+args[3][1]*100+args[3][3]*10+args[3][4]
                    if(h1<h2):
			
                        today = time.strftime("%x")
                
                        #Hora inicio y final
                        hinicio = args[2]
                        hfinal = args[3]


                
                        #Construyo y realizo la peticion con los datos correspondientes y los intervalos
                        payload = {
				'origen': numid,
				'aceptar': '0',
				'key': '0',
				'destino': numid2,
				'fecha': today,
				'hini': hinicio,
				'hfin': hfinal,
				'calcular': '1'
                        }
                        r = requests.post("http://www.tramalicante.es/horarios.php", data=payload)

                        #Scrapeo cada valor de la tabla de horarios
                        cadatd = re.findall("<td>(\d+:\d+)</td>", r.text)

                        total=''
                        numero1='-1'
                        numero0='-1'
                        #Mando el horario de la forma: en una linea la hora y en la siguiente todas las
                        #veces que sale en esa hora, y asi con todas las horas.
                
                        for hora in cadatd:
                            #imprime horas por grupos de hora
                            if(hora[0]==numero0 and hora[1]==numero1):
                       
                                total=(total+hora+' ')
                            #detecta cuando tiene que pasar a la siguiente hora
                            else:
                                #Detectar transbordo
                                if(numero0*10+numero1 > hora[0]*10+hora[1]):
                                    total=total+'\n\nTRANSBORDOOOR\n'
                            
                                numero0=hora[0]
                                numero1=hora[1]
                                total=(total+'\n'+'⌚️'+numero0+numero1+'\n'+'📌'+hora+' ')
                        
                        if(total==''):
                            update.message.reply_text('Lo siento, no sale ningun tram en el intervalo horario indicado.')
                        else:
                            update.message.reply_text('Salidas desde '+str.lower(args[0])+' a '+str.lower(args[1])+ ' de '+hinicio+ ' a '+hfinal+ ':'+total)
                    else:
                        update.message.reply_text('Error.\nLa hora de inicio debe ser menor que la hora de fin.')
            else:
                update.message.reply_text('El intervalo de horas es incorrecto, debe cumplir este formato: XX:XX')
    else:
        update.message.reply_text('Error en los argumentos.\nUso: /timesto Origen Destino Hora1 Hora2')

#
# Funcion paradas:lista el nombre de todas las paradas
# [*]USO: /paradas
#
#
def paradas(bot, update):
    
    #cargo el json de las paradas
    leer = json.loads(open('./paradas.json').read())
    
    total='📌'
    for parada in leer:

        total=(total+parada+'\n'+'📌')
    temp=len(total)
    total=total[:temp -1] 
    update.message.reply_text('Paradas disponibles:\n'+total)

######################################
# Funcion principal 		     #
######################################
def main():
    #Cambiar token***********************************************************************
    updater = telegram.ext.Updater('TOKEN')
    dp = updater.dispatcher

    dp.add_handler(telegram.ext.CommandHandler("start",start))
    dp.add_handler(telegram.ext.CommandHandler("help",help))
    dp.add_handler(telegram.ext.CommandHandler("times",timestoday,pass_args=True))
    dp.add_handler(telegram.ext.CommandHandler("timesto",timesintervalo,pass_args=True))
    dp.add_handler(telegram.ext.CommandHandler("paradas",paradas))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()	
