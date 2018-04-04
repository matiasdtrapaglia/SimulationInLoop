# Simple tests for an adder module
import cocotb
from cocotb.triggers import Timer
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
############################################################################
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
    keys = dut._sub_handles.keys()
    ports_send(dut, par_serv, keys)
    # RECORDAR SETEAR VALORES INICIALES
    # ojo con los parametros iniciales, de ser necesario, pedir elejir las cctes
    
    lista_entradas = []
    while len(par_serv.entradas_get) == 0:
        time.sleep(0.3)
    for entrada in par_serv.entradas_get:
        lista_entradas.append(entrada)
    
    dut.log.setLevel(logging.DEBUG)
   
    while par_serv.exit_get == False :
        time.sleep(0.2)
        if par_serv.status_get("step") == True :
            recibir_dut(dut, par_serv.dic, lista_entradas)
            yield Timer(10)
            enviar_dut(dut, par_serv, keys)
            par_serv.status_set("step", False)
        elif par_serv.status_get("run") != 0:
            recibir_dut(dut, par_serv.dic, lista_entradas)
            yield Timer(int(par_serv.status_get("run")))
            enviar_dut(dut, par_serv, keys)
            par_serv.status_set("run", 0)
