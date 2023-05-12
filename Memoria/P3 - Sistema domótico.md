

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

## Implementación
- La implementación de esta practica ha sido de la siguiente forma:
    > La interfaz con el usuario ha sido programada usando un bot de discord el cual tiene acceso a un servidor privado, al cual se puede acceder mediante este enlace: https://discord.gg/BD5pVcpS
      >Esta interfaz de usuario por comandos acepta una lista de comandos limitada, la cual se detalla a continuación:
    - Añadir sensor:
      - añadir sensor \<id> \
        Ej: añadir sensor 1  

    - Añadir actuador:
      - añadir actuador \<id> \
        Ej: añadir actuador 2  

    - Añadir regla:
        - añadir regla \<parametro> \<operador> \<valor> \<id_actuador> \<accion> \
        Ej: anadir regla temperatura > 26 2 OFF (en español, cuando el parametro temperatura (en este caso del sensor 1) supere el valor 26, establecer el estado del switch 2 a off)

    - Obtener sensor/actuador:
        - obtener <id_sensor/actuador> \
        Ej: obtener 1 (debe devolver el ultimo valor/estado obtenido del sensor/actuador)
- Este bot corre en dos hilos: el primero se encarga de la recepción de mensajes por el servidor, y el segundo se encarga de enviar al servidor los mensajes necesarios que recibe por el controller al que está conectado.
  - La comunicación con el controlador se realiza usando MQTT y es del siguiente modo:
    - Si se añade un sensor, envía un bridge:newsensor:\<id>  
    - Si se añade un actuador, envía un bridge:newactuador:\<id> 
    - Si se añade una regla, envía un bridge:newrule:\<parametro>:\<operador>:\<valor>:\<id_actuador>:\<accion> 
    - Si se quiere obtener un valor de los registros del controlador, se envía un bridge:get:\<id>
      - A este comando el controlador responderá con un mensaje de respuesta, y será recibido por el callback de MQTT del bridge y enviado al servidor para el cliente.
- El controlador, el componente mas complejo del sistema, esta planteado de la siguiente manera:
  - Cuado un mensaje citado anteriormente llega al controlador, hace una llamada la funcion consecuente, ya sea para crear un componente o para obtener un valor
  - Cuando se crea un sensor/actuador, el controlador añade a su diccionario *dict_topics* una entarda tipo \<id>:topic por el cual se podrá comunicar o recibir informacion con el sensor/actuador.
  - Cuando llega una nueva regla, el controlador la añade a un array de raglas *array_reglas*.
    - El controlador cuenta con un hilo que cada segundo manda la lista de reglas al rule_engine para mantenerlo actualizado de reglas nuevas.
  - Si el mensaje es de tipo get dato, consulta el id del controlador que genera el dato en el diccionario *valores* de tipo id:(magnitud:valor) y envía de vuelta la entrada magnitud:valor al bridge para que lo envíe al cliente.
  - Cuando obtiene un mensaje de un sensor o actuador, actualiza su respectiva entrada en el diccionario de *valores* para ese dispositivo y se esta forma guarda el ultimo valor obtenido.
  - Este modulo cuenta con un sistema de persistencia basado en dos funciones, una de volcado y otra de carga del diccionario *dict_topics* y de *array_reglas*. No consideramos necesario guardar los datos de estados y medidiones ya que en cuanto el sistema vuelva al funcionamiento, estos serán resmplazados por los nuevos datos.
  - Cuando el controlador arranca, busca la presencia de un archivo data.json en el directorio raiz, en caso de no encontrarlo inicializa sin estos valores, y cuando se cancela la ejecución del mismo, vuelca el contenido en este mismo archivo para la siguiente ejecución.
- El dummy clock esta diseñado para enviar la hora cada cierto tiempo, dependiendo de como se unicialice. Usa MQTT par comunicarse con el controlador, y su canal se asigna al asignarse el \<id> del dispositivo.
- El dummy sensor usa MQTT par comunicarse con el controlador, y su canal se asigna al asignarse el \<id> del dispositivo. Manda con una frecuencia una medición al controlador.
- El dummy switch esta diseñado para guardar un estado. Usa MQTT para comunicarse con el controlador, y cuando recibe un mensaje tipo "on" o "off", cambia su estado a este.
- El rule engine esta diseñado usando MQTT para comunicarse con el controlador. Este recibe la lista de reglas con una frecuencia de 1s, y con esta actualización de las reglas las comprueba una a una, y si alguna se cumple, notifica al controlador para que actualice el switch correspondiente.
  

## Conclusiones
- Con esta práctica hemos aprendido a programas un sistema domótico completo y funcional, con varios sensores, además de aprender a programar bots de discord para interfaces de usuario.
- Hemos aprendido a usar MQTT para comunicar los distintos componentes del sistema, y a usar hilos para la comunicación entre estos.
- En conclusión, la práctica ha permitido no solo el desarrollo de habilidades técnicas y el conocimiento de nuevas tecnologías, sino también la posibilidad de aplicarlos en la creación de soluciones creativas y personalizadas para la automatización del hogar.

  

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

## Requisitos

Los requisitos de esta practica es crear un sistema domotico usando MQTT como protocolo de comunicación, en nuestro caso Discord para la interfaz de usuario. Poder añadir sensores y actuadores al sistema, poder consultar el estado de estos y de sus mediciones y poder añadir reglas para la automatización de acciones en el sistema.

Se han creado tests en el directorio /test para la comprobación de estos requisitos.

## Casos de uso

Un caso de uso ideal sería el siguiente:
1.  Añadir el bot de discord a un servidor.
2.  Poner un summy_sensor a correr con id = 1
3.  Escribir añadir sensor 1
4.  Poner un dummy_switch a correr con id = 2
3.  Escribir añadir actuador 2
3.  Escribir obtener 1 (obetenemos dato del sensor)
3.  Escribir obtener 2 (obetenemos estado del actuador)
4.  Poner un rule_engine a correr
5.  Escribir anadir regla temperatura > 26 2 ON
6.  Escribir obtener 2 (obetenemos estado del actuador probablemente actualizado por la regla)
7.  Escribir añadir regla temperatura < 26 2 OFF
8.  Poner un dummy_clock a correr con id = 3
9.  Escribir añadir sendor 3 (añadimos el reloj)
10. Escribir obtener 3 (nos devuelve la hora)

Tras al final tendremos un sistema domótico en el cual tenemos un sensor de temperatura (1) y un interruptor de calefacción (2) el cual se pone en ON si la temperatura cae por debajo de 26º, pero que si sube se apaga automaticamente. Tambien podemos consultar la hora al reloj (3). 


## Decisiones

-  ¿Controller y Rule engine han de ser aplicaciones separadas?, ¿por qué?, ¿qué ventajas tiene una y otra opción?¿Cómo se comunican Controller y Rule engine en la opción escogida?
   -  Siendo dos aplicaciones separadas el codigo esta mas compartimentadop y mejor aislado. Nosotros optamos esta opción porque considerabamos que controller ya tenía cierto nivel de complejidad y era mas sencillo instanciar el rule engine por separado.
   -  Nostros usamos MQTT para la comunicación entre las dos aplicaciones. De esta forma se integra en el ecosistema a la perfección. 

- Tiene sentido que alguno de estos componentes compartan funcionalidad?, ¿qué relación hay entre ellos?
  - Bueno, el reloj en practica es como un sensor, y nosotros al añadirlo al sistema domótico lo hacemos igual que si fuera un sensor.

- Cuántas instancias hay de cada componente?
  - Hay, por lo menos:
    - 1 bridge
    - 1 controller
    - 1 rule engine
    - 1 o más dummy-sensor
    - 1 o más dummy-switches
    - 1 dummy-clock (más de uno no tiene sentido porque la hora va a ser la misa)

- Controller y Bridge han de ser aplicaciones separadas?, ¿por qué?, ¿qué ventajas tiene una y otra opción?
  - Según el enunciado deben serlo, y además separadas resulta mas sencillo de depurar. De esta forma el controller puede ser usado con otra interfaz de usuario diferente si así se requiere. El bridge puede modificarse libremente y añadir mas funcionalidaes al sevidor sin peligro de perjudicar al controller.

- Cómo se comunican Controller y Bridge en la opción escogida?
  - Se comunican usando MQTT, estos se subscriben a dos topics de envío/recepción de mensajes al instanciar ambas aplicaciones.



