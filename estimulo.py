import Pyro4 , time, random #, os
from subprocess import call

par_serv = Pyro4.Proxy("PYRONAME:servidor.de.variables")         # get a Pyro proxy to the current proyect

if (par_serv.exit_get == True):
    par_serv.exit_set(False)
    time.sleep(1)
        
keys_entradas = []
keys_salidas = []
keys_constantes = []

#TO DO:
#   - Anadir una indicacion de tiempo de simulacion transcurrido
#   - Se puede agregar la opcion de cambiar una variable continuamente, viendo resultados
#   - Se puede agregar la opcion de cargar "waves" de una variable desde un bloc de notas, con cada espacio o enter como un step configuragle
#   - Guardar configuracion de puertos en archivo de texto con el nombre del dut en cuestion.
#   - Agregar indicador de [frozen] o stand-by para indicar si los valores que se muestran son los actuales.

dic_dut = {}
        
    
while par_serv.exit_get == False :
    print "par_serv.dic len: %d != par_serv.dic_len: %d" %(len(par_serv.dic), par_serv.dic_len)
    while len(par_serv.dic) != par_serv.dic_len :
        time.sleep(2)
        print "%d != %d" %(len(par_serv.dic), par_serv.dic_len)
    
    keys = par_serv.dic.keys()
    keys_puertos = par_serv.dic.keys()
############################################################################
    for i in range(len(keys)):
        call("clear")
        print("Puertos sin clasificar del DUT".center(60,'-'))
        for puerto in keys_puertos:
            print "%s  " % puerto ,
        
        print "\n\n"," Inputs del DUT ".center(60,'-')
        for entrada in keys_entradas:
            print "%s  " % entrada ,
        
        print "\n\n"," Outputs del DUT ".center(60,'-')
        for salida in keys_salidas:
            print "%s  " % salida ,
            
        print "\n\n"," Constantes del DUT ".center(60,'-')
        for ctte in keys_constantes:
            print "%s  " % ctte ,
        
        print "\n\n"
        clasif = raw_input ("La variable %s es Input (I), Output (O) o Constante (C)? \n (I/O/C) ? " % keys[i])
        if clasif == "I" :
            keys_entradas.append(keys[i])
        elif clasif == "O":
            keys_salidas.append(keys[i])
        else :
            keys_constantes.append(keys[i])
        keys_puertos.pop(keys_puertos.index(keys[i]))
############################################################################
    dic_dut = par_serv.dic.copy()
    par_serv.entradas_set(keys_entradas)
    
    opcion = ""
    valor = 0
    while 1:
        call("clear")
        print "\n\n"," Inputs del DUT ".center(60,'-')
        for entrada in keys_entradas:
            print "%s  = %s | ".rjust(5) % (entrada, dic_dut[entrada]) ,
        print "\n\n"," Outputs del DUT ".center(60,'-')
        for salida in keys_salidas:
            print "%s  = %s | ".rjust(5) % (salida, dic_dut[salida]) ,
        print "\n\n"," Constantes del DUT ".center(60,'-')
        for ctte in keys_constantes:
            print "%s  = %s | ".rjust(5) % (ctte, dic_dut[ctte]) ,
            print "\n"
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
        print("- Escriba \".salir\" para cerrar la simulacion.\n- Escriba \".step\" para avanzar la simulacion una unidad de tiempo (10nS).\n- Escriba \".run\" para correr la simulacion un tiempo a establecerse.\n\n")
        
        opcion = raw_input (" Ingrese la variable de entrada que desea modificar: ")
        if opcion == ".salir":
            par_serv.exit_set(True)
            break
        elif opcion == ".step":
            par_serv.status_set("step", True)
            while par_serv.status_get("step") == True :
                time.sleep(0.3)
            dic_dut = par_serv.dic.copy()
        elif opcion == ".run":
            tiempo = raw_input("\nIngrese el tiempo en nS que desea avanzar en la simulacion: ")
            par_serv.status_set("run", tiempo)
            while par_serv.status_get("run") != 0 :
                time.sleep(0.3)
            dic_dut = par_serv.dic.copy()
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
        for entrada in keys_entradas:
            if opcion == entrada:
                valor = raw_input("Ingrese el valor que desea introducir en %s : " % entrada)
                dic_dut[entrada] = valor
                par_serv.dic_set(entrada, valor)
        
