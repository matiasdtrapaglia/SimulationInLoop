# saved as greeting-server.py
import Pyro4
import time


@Pyro4.behavior(instance_mode="single")
@Pyro4.expose
class p_servidor(object):
    def __init__(self):
        self.dict_dut = {}
        self.status = {"run": "idle" , "exit":False , "sync":True , "time":10 , "clk": "", "count" : 0}     #
        self.dict_len = 1000
        self.lista_sig = []
        self.lista_constantes = []
        self.lista_modif = []
        self.lista_eventos = []
        self.lista_monit = []
        self.lista_disp = []
        #self.lista_check = []
        self.var_state = {}
###############################################
    def reset(self):
        self.dict_dut.clear()
        self.status = {"run": "idle" , "exit":False , "sync":True , "time":10 , "clk": "", "count" : 0}     #
        self.dict_len = 1000
        self.lista_sig = []
        self.lista_constantes = []
        self.lista_modif = []
        self.lista_eventos = []
        self.lista_monit = []
        self.lista_disp = []
        #self.lista_check = []
        self.var_state.clear()
    def lista_set(self, nombre , lista):
        if nombre == "sig" :
            for signal in lista:
                self.lista_sig.append(signal)
        elif nombre == "ctte":
            for ctte in lista:
                self.lista_constantes.append(ctte)
        elif nombre == "modif":
            self.lista_modif = []
            for key in lista:
                self.lista_modif.append(key)
        elif nombre == "event":
            self.lista_eventos = []
            for key in lista:
                self.lista_eventos.append(key)
        elif nombre == "mon" :
            self.lista_monit = []
            for key in lista:
                self.lista_monit.append(key)
        elif nombre == "disp" :
            for key in lista:
                self.lista_disp.append(key)
        #elif nombre == "check" :
            #for key in lista:
                #self.lista_check.append(key)
    def lista_get(self, cual):
        if cual=="sig":
            return self.lista_sig
        elif cual=="ctte":
            return self.lista_constantes
        elif cual=="modif":
            return self.lista_modif
        elif cual=="event":
            return self.lista_eventos
        elif cual=="mon":
            return self.lista_monit
        elif cual=="disp":
            return self.lista_disp
        #elif cual=="check":
            #return self.lista_check
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
    def var_state_set(self, key, value):
        self.var_state[key] = value
    #def var_state_get(self, key):
        #return self.var_state[key]
    @property
    def var_state_get(self):
        return var_state
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
