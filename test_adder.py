# Simple tests for an adder module
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.result import TestFailure
from adder_model import adder_model
import random
import inspect
import logging
import Pyro4
import time

@cocotb.test()
def adder_basic_test(dut):
    """Test for 5 + 10"""
    dut._discover_all()                     #  IMPORTANTE 
    par_serv = Pyro4.Proxy("PYRONAME:servidor.de.variables") 

    if (par_serv.exit_get == True):
        par_serv.exit_set(False)
        time.sleep(1)
        
############################## Funciones ###################################
    def enviar_dut(dut, ps, keys): 
        dic = {}
        dut._discover_all()                 #  IMPORTANTE 
        for key in keys:
            dic[key] = str(dut._sub_handles[key])
        ps.send_dut(dic)
    #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
    def recibir_dut(dut, dic, keys_entradas):
        for entrada in keys_entradas:
            exec "dut.%s = %s" % (entrada, dic[entrada]) in globals(), locals()
    #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
    def ports_send(dut, ps, keys):
        ps.len_set(len(keys))
        for key in keys:
            ps.dic_set(key, str(dut._sub_handles[key]))    
############################################################################  

    par_serv.reset()
    
    keys = dut._sub_handles.keys()
    ports_send(dut, par_serv, keys)

    lista_constantes = []
    lista_senales = []
    lista_modif = []
    
    
    for key in keys:
        if dut._sub_handles[key]._type == "GPI_MODULE":
            pass                                            ###################### TO DO jerarquias ##############################
        elif dut._sub_handles[key]._type == "GPI_REGISTER":
            lista_senales.append(key)
        else:    #GPI_PARAMETER
            lista_constantes.append(key)
    
    par_serv.lista_set("sig", lista_senales)
    par_serv.lista_set("ctte", lista_constantes)
    
    dut.log.setLevel(logging.DEBUG)                         # al dope
   
    #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
    while True:
        time.sleep(0.3)
        if par_serv.status_get("clk") != "":
            cocotb.fork(Clock(dut._sub_handles[par_serv.status_get("clk")], 10).start())
            break
        if par_serv.status_get("sync") == False :
            break
    
    #yield RisingEdge(dut.CLK)
    #cocotb.log.info("wep")
    #yield RisingEdge(dut.CLK)
    #cocotb.log.info("wap")
    
    #yield Timer(10)
    #cocotb.log.info("wep")
    #yield Timer(10)
    #cocotb.log.info("wap")
    
    
    while par_serv.exit_get == False :
        lista_modif = []
        disparo = []
        while par_serv.status_get("run") == "idle":
            time.sleep(0.2)   
            if par_serv.exit_get == True :
                break
        lista_modif = par_serv.lista_get("modif")
        state = par_serv.status_get("run")
        if state == "step" :
            recibir_dut(dut, par_serv.dic, lista_modif)
            if par_serv.status_get("sync") ==  True:
                yield RisingEdge(dut._sub_handles[par_serv.status_get("clk")])
            else:
                yield Timer(10)
            enviar_dut(dut, par_serv, keys)
            par_serv.status_set("run", "idle")
        elif state == "go":
            tiempo = par_serv.status_get("time")
            if "clock" in par_serv.lista_get("event"):
                clk_count = par_serv.status_get("count")
            #monit = par_serv
            check = []
            estado={}
            while len(disparo)==0:
                recibir_dut(dut, par_serv.dic, lista_modif)
                if "clock" in par_serv.lista_get("event"):
                    clk_count  -=1
                    if clk_count <= 0:
                        disparo.append("clock")
                    yield RisingEdge(dut._sub_handles[par_serv.status_get("clk")])
                elif "time" in par_serv.lista_get("event"):
                    if len(par_serv.lista_get("event")) >1 :
                        yield Timer(tiempo)
                        disparo = "time"
                    elif tiempo <= 10:
                        disparo.append("clock")
                        yield Timer(tiempo)
                    elif tiempo > 10:
                        tiempo -= 10
                        yield Timer(10)
                else:
                    yield Timer(10)
                if "reg" in par_serv.lista_get("event"):
                    if len(check) == 0:
                        check = par_serv.var_state_get.keys()
                        dut._discover_all()
                    for element in check:
                        estado[element] = dut._sub_handles[element] #no se si estado es necesario
                        if estado[element] == parv_serv.var_state_get(element):
                            disparo.append("reg")
                    
                    
                    #disparo = "time"
            #yield Timer(par_serv.status_get("time"))
            par_serv.status_set("disparo", disparo)
            #dut._discover_all()  
            enviar_dut(dut, par_serv, keys)
            par_serv.status_set("run", "idle")

    if par_serv.exit_get == True:
        par_serv.reset()
