# Evidencia4CDP
Evidencia 4 de Computación Distribuida
En este README especificare uan cosas respecto al codigo y unas cosas que tuve que investigar para resovler algunos problemas que tuve:

-Para empezar ,el dataser que le estoy adjutando tiene mas de 1.5 millones de datos, por lo cual , el tiempo de procesamiento puede superar los 10 minutos. 

-Otro punto importante para la ejecucion del archivo, es que el archivo del dataset este en ambos nodos , el maestro y esclavo en la misma direccion, trate de investigar el por que no se hacia de manera automatica , ya que al tener sh, deberia de hacerlo de manera automatica , me contre que se tenia que usar este comando " ./bin/spark-submit \

   --master yarn \
	 
   --deploy-mode cluster \
	 
   --py-files file1.py,file2.py,file3.zip
	 
   wordByExample.py
	 
"

pero no bastaba para pasarlo de manera correcta, asi que para ejecutar el codigo , se tienen que poner el archivo de dataset en ambos nodos.

Otro punto a resltar que estuve investigando es que a la hora de ejecutar el archivo lo hacia con "python3" , pero aveces me salio errores, pero buscando en internet encotnre este comando " spark-submit nombre_archvio.py", al utilizar el comando "spark-submit", estás enviando el archivo Python especificado, "nombre_archivo.py", al clúster de Spark para que se ejecute. Esto inicia la ejecución de la aplicación de Spark en el clúster distribuido. Con esto me ayudo a que no me diera errores.
Se adjunta el codigo fuente , el dataset y lo necesario para ejecutar el archivo.
Este recomendador esta en python.



