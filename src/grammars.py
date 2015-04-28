chunks = r"""
			
		# Las frases estandar que primero deberiamos detectar.

	 				VERBP: {<VB>+<JJ|UH|RB>*} 
	  				VERBP: }<IN>{
	  				VERBP: }<INP>{
	  				NOUNP: {<DT|NN.*|IN_DT|JJ|CD>+}
	  				NOUNP: {<DT>?<NN.*|IN_DT|JJ|CD>+} 
	  				TIMEP: {<DT>?<TIME|TMP|DATE>}
	  				NOUNP: }<IN>{
	  				NOUNP: }<INP>{
	  				ADVBP: {<RB>+<JJ|VB|WP.*|PR.$>?}								 
	  				PREPP: {<IN>+}  
	  				PLACP: {<INP>+}             
	  				WEBP:  {<DT>?<USER|HTAG|LINK>}
	  				
	  			"""


locations=r"""

	# Podemos envolver las chunks y ahora buscar las mas especificas


	
	LOCATION_EN_ENTRE_Y:<en_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?<entre_.*>}
	LOCATION_Y:{<LOCATION_.*>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?<y_.*><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	

	
	LOCATION_from_0:<desde_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<hacia_.*|hasta_.*|a_.*>
	LOCATION_from_1:<desde_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<a_.*><la_.*><altura_.*>
	
	LOCATION_from_2:<sobre_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<hacia_.*|hasta_.*>
	LOCATION_from_3:<sobre_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<a_.*><la_.*><altura_.*>
	

	LOCATION_from_4:<en_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<hacia_.*|hasta_.*>
	LOCATION_from_5:<en_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<a_.*><la_.*><altura_.*>
	LOCATION_from_6:<en_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<para_.*><superar_.*>
	LOCATION_from_7:<cruce_.*><con_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<hacia_.*|hasta_.*>
	LOCATION_from_8:<cruce_.*><con_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<a_.*><la_.*><altura_.*>
	
	LOCATION_from_9:<de_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<hacia_.*|hasta_.*>
	LOCATION_from_10:<de_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<a_.*><la_.*><altura_.*>
	LOCATION_from_11:<de_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<para_.*><superar_.*|incorporarse_.*>
	

	LOCATION_from_12:<en_.*|sobre_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<desde_.*>
	LOCATION_from_13:{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<sentido_.*|rumbo_.*|direcci.n_.*>
	LOCATION_from_14:{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<mano_.*><a_.*|hacia_.*|al_.*>
	LOCATION_from_15:<despu.s_.*><de_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}

	LOCATION_INSITU_O0:<en_.*|sobre_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<frente_.*|cerca_.*|alrededor_.*|enfrente_.*|detr.s_.*>
	LOCATION_INSITU_D0:<LOCATION_.*>?<frente_.*|cerca_.*|alrededor_.*|enfrente_.*|detr.s_.*><de_.*|del_.*|a_.*|al_.*>?{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}

	LOCATION_to_0:{<LOCATION_.*>?<a_.*><la_.*><altura_.*><de_.*|del_.*>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_to_1:<LOCATION_.*>?<hacia_.*|hasta_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_to_2:{<LOCATION_.*>?<sentido_.*|rumbo_.*|direcci.n_.*><a_.*|al_.*>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_to_3:{<LOCATION_.*>?<mano_.*><a_.*|hacia_.*|al_.*><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}

	LOCATION_INTRO_EVENT_0:{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<presenta_.*|manifiesta_.*|muestra_.*	registra_.*>
	LOCATION_INTRO_EVENT_1:<en_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<el_.*><tr.nsito_.*>
	LOCATION_INTRO_EVENT_2:<circular_.*|retomar_.*><por_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_INTRO_EVENT_3:{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<con_.*><demora_.*|tr.nsito_.*>
	LOCATION_INTRO_EVENT_4:<LOCATION__INTRO_3><o_.*|y_.*>?<por_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_INTRO_EVENT_5:<tr.nsito><.*>?<presenta_.*|manifiesta_.*|muestra_.*	registra_.*>{<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}


"""


events=r"""

	# algunos eventos tipicos


		EVENT_E00:{<.*VERBP><de_.*|por_.*|con_.*>?<.*NOUNP>+(<de_.*PREPP|del_.*PREPP><.*NOUNP>+)?}<en_.*PREPP|sobre_.*PREPP>?<.*B-LOCATION>
		EVENT_E01:{<choque_.*|incendi.*_.*|vuelco_.*|corte.*_.*|cerrada_.*|manifesta_.*|polic.a_.*|accidente_.*|obra_.*|cola_.*|tr.fico_.*|trancad._.*|precauci.n_.*>}
		EVENT_E01:{<lento_.*|r.pido_.*|obstruid._.*|complicado_.*|intens._.*|demora_.*>}
		
		
"""


words=r"""
	
	# direcciones que se reconocen mas bien por palabras que por contexto
		
	LOCATION_1:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<ruta.*NOUNP><(nacional|provincial|n.mero)_.*NOUNP><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}	
	LOCATION_2:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<(parador|bosque|tramo|distribuidor|autov.a|calle|esquina|centro|avenida|kil.metro|Km|autopista|anillo|calzada|colectora|puente|cruce|cruze|circuito|peaje)(s|es)?_.*NOUNP><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_3:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<(rotonda|estaci.n|bulevard|boulevard|perif.rico)_.*NOUNP><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_4:{<el_.*|en_.*|la_.*|los_.*|en_.*|sobre>?<(costanera|barrio|parque|v.aducto|r.o|rio|arroyo|villa|valle|casino)_.*NOUNP>+<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_5:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<(eje_.*|caminio.*_.*|brazo)_.*NOUNP><(central|lateral|principal|puente)_.*NOUNP>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_6:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<monumento_.*NOUNP><a_.*|al_.*|de_.*|del_.*>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_7:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<(municipalidad|municipio|estadio|cine|teatro|peatonal|shopping|hip.dromo|balneario|club|gimnasio)_.*NOUNP><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_8:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<(universidad|campus|instituto|colegio|escuela|biblioteca|colonia|hospital|cl.nica|sanatorio|local)_.*NOUNP><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_9:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<(principal|bajada|entrada|salida|subida|pendiente|encrucijada|cruce)_.*NOUNP><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_10:{<en_.*><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}<el_.*><tr.nsito_.*>
	LOCATION_11:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<ramal_.*NOUNP><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_12:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<casco_.*NOUNP><central_.*NOUNP><de_.*|del_.*>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_13:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<(centro|plaza|localidad|torre|parque|estaci.n|jard.n|playa|carril)_.*NOUNP>+<de_.*|del_.*>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_14:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<(mercado|supermercado|panamericana|almacen|mercadeo)_.*NOUNP><de_.*|del_.*>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_15:{<.*LOCATION>+<de_.*|del_.*|en_.*|sobre>?<B-LOCATION.*>+}
	LOCATION_16:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<distrito_.*NOUNP><federal_.*NOUNP>?<de_.*|del_.*>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_17:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<ciudad_.*NOUNP><aut.noma_.*NOUNP>?<de_.*|del_.*>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_18:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<partido_.*NOUNP><(aut.nom._.*|municipal)_.*NOUNP>?<.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_19:{<san_.*|santa_.*><.*NOUNP>+(<de_.*|del_.*><.*P>+)?}
	LOCATION_20:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<(circuito|iglesia|capilla).*NOUNP><de_.*|del_.*>?<.*NOUNP>+}
	LOCATION_21:{<el_.*|la_.*|las_.*|los_.*|en_.*|sobre>?<ruta.*NOUNP><[0-9]+.*>?}
	LOCATION_22:{<el_.*|la_.*|las_.*|los_.*|en_.*|en_.*|sobre>?<presidente_.*|doctor_.*|general_.*NOUNP><.*NOUNP>+(<de_.*|del_.*><.*NOUNP>+)?}
	LOCATION_23:{<el_.*|la_.*|las_.*|los_.*|en_.*|en_.*|sobre>?<(ruta|eje)_.*NOUNP><[0-9]+_.*NOUNP>}


	"""



clean=r"""

	# no voy a limpiar nada...
"""
