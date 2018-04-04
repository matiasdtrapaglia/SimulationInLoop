# saved as greeting-server.py
import Pyro4
import time
#import json
#import jsonpickle

@Pyro4.behavior(instance_mode="single")
@Pyro4.expose
class p_servidor(object):
    def __init__(self):
        self.dict_dut = {}
        self.status = {"step" : False, "run" : 0, "exit" : False}     #se puede agregar el continuous simulation
        self.dict_len = 1000
        self.lista_entradas = []
###############################################
    def entradas_set(self, lista):
        for i in range(len(lista)):
            self.lista_entradas.append(lista[i])
    @property
    def entradas_get(self):
        return self.lista_entradas
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
    @property
    def exit_get(self):
        return self.status["exit"]
    def exit_set(self, val):
        self.status["exit"] = val
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
    def status_set(self, key, value):
        self.status[key] = value
    def status_get(self, key):
        return self.status[key]
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
    def send_dut(self, dic):
        self.dict_dut = dic.copy()
    @property        
    def dic(self):
        return self.dict_dut
    def dic_set(self, key, value):
        self.dict_dut[key] = value
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-#
    def len_set(self, valor):
        self.dict_len = valor
    @property 
    def dic_len(self):
        return self.dict_len
###############################################    

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()
uri = daemon.register(p_servidor)   # register the greeting maker as a Pyro object
ns.register("servidor.de.variables", uri)

print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
daemon.requestLoop()                   # start the event loop of the server to wait for calls
