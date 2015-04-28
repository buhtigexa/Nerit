	
locations=r"""

	# Ajustar los tags de algunas direcciones. P.ej:
	
	# autopista NN  B-LOCATION
    # del IN  I-LOCATION
    # centro NN  B-LOCATION   # aqui comienza una nueva direccion, y no deberia....

	LOCATION_1:{<.*LOCATION>+(<de_.*LOCATION>|<del_.*LOCATION>)<.*B-LOCATION>(<.*I-LOCATION>+)?}
	# rio NN  I-LOCATION
	# de IN  B-PREPP                          # se corta la direccion por presencia de preposicion
	# la DT  B-LOCATION
	# plata NN  I-LOCATION

	LOCATION_2:{<.*LOCATION>+(<de_.*B-PREPP>|<del_.*B-PREPP>)<.*B-LOCATION>(<.*I-LOCATION>+)?}

	# 0 CD  I-LOCATION
    # al IN  B-PREPP                          # preposicion corta la definicion de la distancia...
    # kilometro NN  B-LOCATION

    LOCATION_3:{<.*LOCATION>+<al_.*B-PREPP><kilometro_.*B-LOCATION>(<.*I-LOCATION>+)?}

    # 41 CD  I-LOCATION
	# y CC  O                       # conjuncion me corta la direccion compuesta  ( direccionX y direccionZ)
	# cruze NN  B-NOUNP

	LOCATION_4:{<.*LOCATION>+<y_O><.*B-NOUNP>(<.*I-LOCATION>+)?}

	# suarez NNP I-LOCATION
	# al IN B-PREPP
	# 1010 CD B-LOCATION
 	
 	LOCATION_5:{<.*LOCATION>+<al_.*B-PREPP><[0-9]+.*B-LOCATION>}

"""

clean=r"""
	
	# Aca voy a escribir gramaticas para corregir direcciones que fueron erroneamente detectadas. La idea es limpiar frases.
	# P.ej:
    
    # congreso NN B-LOCATION
	# y CC  I-LOCATION
    # hacia IN  B-PREPP 

	# ruta NN  B-LOCATION

    O_1:<.*LOCATION>+{<y_I-LOCATION>}<.*PREPP>+



"""


