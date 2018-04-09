import Pyro4 , time, random #, os
from subprocess import call

par_serv = Pyro4.Proxy("PYRONAME:servidor.de.variables")         # get a Pyro proxy to the current proyect

if (par_serv.exit_get == True):
    par_serv.exit_set(False)
    time.sleep(1)
        
keys_monit = []
keys_modif = []
keys_constantes = []

#TO DO:
#   - Anadir una indicacion de tiempo de simulacion transcurrido
#   - Se puede agregar la opcion de cambiar una variable continuamente, viendo resultados
#   - Se puede agregar la opcion de cargar "waves" de una variable desde un bloc de notas, con cada espacio o enter como un step configuragle
#   - Guardar configuracion de puertos en archivo de texto con el nombre del dut en cuestion.
#   - Agregar indicador de [frozen] o stand-by para indicar si los valores que se muestran son los actuales.

dic_dut = {}
        
#par_serv.reset()
while par_serv.exit_get == False :
    print "par_serv.dic len: %d != par_serv.dic_len: %d" %(len(par_serv.dic), par_serv.dic_len)
    while len(par_serv.dic) != par_serv.dic_len :
        time.sleep(2)
        print "%d != %d" %(len(par_serv.dic), par_serv.dic_len)
    
    keys= par_serv.dic.keys()
    keys_ctte = par_serv.lista_get("ctte")
    keys_sig = par_serv.lista_get("sig")
    
############################################################################

    print "\n\n"
    var = ""
    while var.lower() != ".ready":
        call("clear")
        print("Senales del DUT".center(60,'-'))
        for sig in keys_sig:
            print "%s  " % sig ,
                    
        print "\n\n"," Constantes del DUT ".center(60,'-')
        for ctte in keys_constantes:
            print "%s  " % ctte ,
            
        print "\n\n"," Variables to monitor ".center(60,'-')
        for key in keys_monit:
            print "%s  " % key ,
        
        print "\n\n"
        var = raw_input ("- Ingrese de a una las variables que desea mantener visibles; luego \".ready\" para continuar con la simulacion. (\".all\" para mostrarlas todas, \".salir\" para abandonar la simulacion).\n Input: ")
        if var.lower() ==".all":
            for elem in keys_sig:
                if (elem in keys_monit)==False:
                    keys_monit.append(elem)
            break
        elif var.lower() == ".salir":
            par_serv.exit_set(True)
        elif (var in keys_sig) == True:
            keys_monit.append(var)
            keys_sig.remove(var)
        elif (var in keys_constantes) == True:
            keys_monit.append(var)
            keys_constantes.remove(var)
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#  
    dic_dut = par_serv.dic.copy()
    call("clear")
    print "\n\n"," Variables monitoreadas del DUT ".center(60,'-')
    for key in keys_monit:
        print "%s  = %s | ".rjust(5) % (key, dic_dut[key]) ,
    print "\n\n"
    while par_serv.exit_get == False:
        opcion = raw_input ("- La simulacion posee clock?\n(S/N) ")
        if opcion.lower() == "s":
            par_serv.status_set("sync", True)
            var = ""
            while(var in par_serv.lista_get("sig"))==False:
                var = raw_input ("\n- Ingrese el nombre de la variable que funciona como clock: ")
            par_serv.status_set("clk", var)
            break
        if opcion.lower() == "n":
            par_serv.status_set("sync", False)
            break
        
            
############################################################################

    opcion = ""
    valor = 0
    modo = ""
    eventos = []
    
    while par_serv.exit_get == False:
        call("clear")
        while par_serv.status_get("run") != "idle" :
            time.sleep(0.2)     
        dic_dut.clear()
        dic_dut = par_serv.dic.copy()
        
        
        keys_modif = []
        var = ""
        #modo 
        while (var != ".ready") and (var != ".run") and (par_serv.exit_get == False):
            call("clear")
            print "\n\n"," Monitoreo del DUT ".center(60,'-')
            for key in keys_monit:
                print "%s  = %s | ".rjust(5) % (key, dic_dut[key]) ,
            print "\n\n"
            var = raw_input ("- Ingrese variable a modificar, \".ready\" para continuar a la seccion eventos, \".run\" para avanzar la simulacion o \".salir\" para abandonar la simulacion.\n  ")
            if var.lower() == ".run" :
                if (modo == "") and (len(eventos)==0):
                    modo = "step"                    
            elif var.lower() == ".salir":
                par_serv.exit_set(True)
            elif var in keys :  
                keys_modif.append(var)
                valor = raw_input ("\n- Ingrese el valor\n ")
                dic_dut[var] = valor
                par_serv.dic_set(var, valor)
                
        par_serv.lista_set("modif", keys_modif)
        
        disparo = ""
        monit = []
        while par_serv.exit_get == False :
            if modo == "step":
                modo = ""
                par_serv.status_set("run", "step")
                break
            elif  var == ".run":
                break
            call("clear")
            print "\n\n"," Monitoreo del DUT ".center(60,'-')
            for key in keys_monit:
                print "%s  = %s | ".rjust(5) % (key, dic_dut[key]) ,
            print "\n\n"
            print "\n\n"," Seteo de eventos ".center(60,'-')
            print "\nEventos ya configurados: "
            if "Bit" in eventos:
                print "\nCambio de bit: "
                for var in monit:
                    print var ,
            if "time" in eventos:
                print "\nTime: %d seg." % par_serv.status_get("time")
            if "clock" in eventos:
                print "\nClock: %d ciclos." % par_serv.status_get("count")
            opcion = raw_input("\nElejir eventos o modos de ejecucion:\n (Reg, Bit, Clock, Time, .ready, .borrar, .salir ")
            if opcion.lower() == "time" :
                if ("time" in eventos) == False:
                    eventos.append("time")
                valor = 0.0
                while int(valor) == 0 :
                    valor = raw_input("\nIngresar el tiempo que desea correr la ejecucion\n")
                    par_serv.status_set("time", int(valor))  
                
                
            elif opcion.lower() == "bit":
                nombre = ""
                while nombre == "":
                    nombre = raw_input("\nIngrese el nombre del bit a monitorear cambios: ")
                monit.append(nombre)
                val = 0
                val = int(raw_input("\nIngrese el valor de interes del registro a monitorear cambios: "))
                par_serv.var_state_set(nombre, val) #fijarse si nombre es key
                if ("bit" in eventos) == False:
                    eventos.append("bit")
            elif opcion.lower() == "reg":
                nombre = ""
                while nombre == "":
                    nombre = raw_input("\nIngrese el nombre del registro a monitorear cambios: ")
                monit.append(nombre)
                val = 0
                while val == 0:
                    val = int(raw_input("\nIngrese el valor de interes del registro a monitorear cambios: "))
                par_serv.var_state_set(nombre, val) #fijarse si nombre es key
                if ("reg" in eventos) == False:
                    eventos.append("reg")
            elif opcion.lower() == "clock":
                val = int(raw_input("\nIngrese la cantidad de pulsos de reloj que desea correr: "))
                par_serv.status_set("count", val)
                if ("clock" in eventos) == False:
                    eventos.append("clock")
            elif opcion.lower() == ".ready" :
                par_serv.status_set("run", "go")
                break
            elif opcion.lower() == ".borrar":
                eventos = []
                monit = []
            elif opcion.lower() == ".salir":
                par_serv.exit_set(True)
        #par_serv.lista_set("check", monit)  
        #for var in monit:
            #par_serv.var_state_set(var, 0)
            
        par_serv.lista_set("event", eventos)

        
