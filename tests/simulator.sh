#!/bin/bash
#Para que funcione correctamente el script se deberá de lanzar desde la carpeta padre del proyecto es decir

#padre:
#   src
#       ...
#   test
#       ...
# Ejemplo: ./simulacion.sh
python3 src/dummy-sensor.py 1   &
python3 src/dummy-switch.py 2   &
python3 src/bridge.py           &
python3 src/controller.py       &
python3 src/rule-engine.py      &


#Ahora están corriendo todos los programas necesarios  para el correcto funcionamiento
#Para comprobar la funcionalidad, deberás de acudir al bot de discord y ejecutar
# añadir sensor 1                                           #añade un sensor(sensor.py)
# añadir actuador 2                                         #añade un actuador(switch.py)
# añadir regla temperatura > 22 2 OFF                       #añade una regla que cuando la temperatura sea mayor que 22 el actuador nº 2 se apagará OFF

