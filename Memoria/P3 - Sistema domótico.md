

P3 - Sistema domótico

Tabla de contenidos

1. [Introduccion]
2. [Objetivos de aprendizaje]
3. [Funcionalidad]

En esta práctica se va a implementar un sistema domótico para el hogar con dispositivos IoT.

Un sistema de domótica de hogar permite conectar distintos tipos de dispositivos como interruptores, sensores o motores para realizar acciones cotidianas como encender una luz, medir una temperatura o subir una persiana. Estos sensores y actuadores se usan en conjunto con reglas que permiten hacer cosas como: "encender la luz de la puerta al anochecer", "cerrar las persianas al pulsar un bot n", "encender la caldera si la temperatura baja de 21 grados", etc.

Existen mœltiples protocolos para comunicación IoT abiertos e incluso algunos fabricantes implementan el suyo propietario, pero en este caso nos centraremos en MQTT, de los más usados.


Hemos utilizado un bot de discord para la comunicación con los dispositivos IoT

La aplicación consta de los siguientes ficheros

Dispositivos IoT:

- Sensores
- Interruptores
- Relojes

Broker MQTT Mosquitto:

- Controller Gestión del sistema general: lee mensajes del broker, llama al Rule engine y realiza acciones sobre los dispositivos a través del broker.

Persistencia:

- Almacena la informaci n de los dispositivos registrados y las reglas.

Rule engine:

- Entidad que, ante un evento, comprueba las reglas y lanza acciones

Bridge:

- Aplicación puente que comunica la aplicación web con Discord


Discord:

- Es una plataforma que soporta, entre otras cosas, la creaci n de salas de chat de texto, v deo y audio

Y los siguientes actores:

Dispositvo IoT (device).

- Publican sus cambios de estado y pueden recibir acciones a realizar usando MQTT

Controlador (controller):

- Recibe y env a mensajes a los dispositivos IoT usando MQTT. Permite gestionar los dispositivos

Traductor (bridge):

- Recibe eventos y los traduce a acciones para el bot. Recibe acciones del bot y las traduce a acciones sobre los dispositivos.   Bot

- Publica mensajes en Discord y recibe acciones


Controlador:

- Es un suscriptor y publicador en MQTT para recibir los cambios de estado y realizar cambios en los dispositivos. Persiste los cambios en los dispositivos y genera eventos.

- Permite recibir acciones a realizar sobre los dispositivos IoT

Rule engine:

- Permite gestionar las reglas del sistema, recibir eventos y comprobar las reglas para realizar acciones


Opción Discord

- Bridge

  - Hace de traductor entre la integraci n con Discord y el sistema. EstarÆ conectado con Discord para poder recibir acciones y para publicar cambios de estado.

- Bot

  - Recibe los mensajes de acciones y publica mensajes en la sala para la que estÆ con�gurada. Broker MQTT

Usaremos Mosquitto, el broker MQTT más ligero y popular

Implementación
- ###############################

Conclusiones
- ###############################

3 Funcionalidad

1) Gestión de dispositivos IoT: se tiene que poder aæadir un dispositivo con su identificador, tipo, editar y borrar

- Para añadir un dispositivo, dependiendo de la opción escogida, se podrá hacer externamente creando el fichero y notificando al sistema que se ha añadido un nuevo dispositivo

2) Gestión de reglas básicas: dado-cuando-entonces para los disparadores soportaremos los operadores ==, > y <

- Bastará con definir un formato textual que el sistema tratará p.ej. "si sala mayor que 25 enciende caldera"Configuración del sistema: conexión MQTT, topics por defecto, persistencia, contraseñas para API

3) Registro de un dispositivo: mediate su id, si está registrado se procesan sus mensajes y se pueden realizar acciones sobre él. En caso contrario se rechazan.

4) Un dispositivo puede:
   1. comunicar un cambio de estado
   2. Recibir una acción si lo soporta

Conectar con el broker MQTT

Generar eventos internos

Comprobar reglas para ver si un evento encaja y se desencadena una acci n Realizar acciones sobre dispositivos Cambiar el estado de un interruptor

Discord

1. Gestionar credenciales de API Discord
2. Publicar cambios de estado en una sala a travØs del bot
3. Consultar, añadir, editar y borrar reglas
4. Recibir acciones sobre un dispositivo a travØs del bot
5. Enviar eventos como mensajes a una sala

Limitaciones

- Un dispositivo en sí no tiene persistencia, al arrancar elige un estado y lo comunica

- Los eventos que se comprueban contra las reglas son ef meros, si el rule engine cae y se recupera, no procesa eventos antiguos

Requisitos

###############################

Casos de uso

###############################

Decisiones

-  ¿Controller y Rule engine han de ser aplicaciones separadas?, ¿por qué?, ¿qué ventajas tiene una y otra opción?¿Cómo se comunican Controller y Rule engine en la opción escogida?

- Tiene sentido que alguno de estos componentes compartan funcionalidad?, ¿qué relación hay entre ellos?

- Cuántas instancias hay de cada componente?

- Controller y Bridge han de ser aplicaciones separadas?, ¿por qué?, ¿qué ventajas tiene una y otra opción?

- Cómo se comunican Controller y Bridge en la opción escogida?

#############################
