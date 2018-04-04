#!/bin/bash
#Ejecutar servidor de nombres, servidor, cliente y make de cocotb

konsole -e pyro4-ns
sleep 3
konsole -e python server.py
sleep 2
konsole -e make COCOTB_REDUCED_LOG_FMT=1
konsole -e python estimulo.py
