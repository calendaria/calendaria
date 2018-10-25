from app.util import date_utils
from unidecode import unidecode

def create_export_data(indate, lang):
	data = []
	display_order = [
		# title, key, quad left, quad right (None or False for blank row)
		({'en' :'Step', 'es': 'Paso'}, 'steps', 3, 2),
		({'en': 'Quadrant', 'es': 'Cuadrante'}, 'quads', 3, 2),
		({'en': 'Round Day', 'es': 'Dia Vuelta'}, 'round_days', 3, 2),
		({'en': 'Date', 'es': 'Fecha'}, 'dates_str', 3, 2),
		({'en': 'Week Number', 'es': 'Semana nro'}, 'week_nbr', 3, 2),
		({'en': 'Week Day', 'es': 'Dia de Semana'}, 'weekday', 3, 2),
		({'en': 'Day Number', 'es': 'Frec+'}, 'day_nbr', 3, 2),
		({'en': 'Negative Frequency', 'es': 'Frec-'}, 'freq_neg', 3, 2),
		({'en': 'GAP', 'es': 'GAP'}, 'gap', 3, 2),
		({'en': 'GAP Date', 'es': 'Fecha GAP'}, 'gap_date_str', 3, 2),
		({'en': 'Fifth Stage', 'es': '5ta'}, 'fs', 3, 2),
		({'en': 'AU', 'es': 'Eje 258'}, 'au', 3, 2),
		({'en': 'CG', 'es': 'CG'}, 'cg', 3, 2),
		({'en': 'DGC', 'es': 'DGC'}, 'cg_tot_days', 3, 2),
		([None]),
		({'en' :'Step', 'es': 'Paso'}, 'steps', 1, 4),
		({'en': 'Quadrant', 'es': 'Cuadrante'}, 'quads', 1, 4),
		({'en': 'Round Day', 'es': 'Dia Vuelta'}, 'round_days', 1, 4),
		({'en': 'Date', 'es': 'Fecha'}, 'dates_str', 1, 4),
		({'en': 'Week Number', 'es': 'Semana nro'}, 'week_nbr', 1, 4),
		({'en': 'Week Day', 'es': 'Dia de Semana'}, 'weekday', 1, 4),
		({'en': 'Day Number', 'es': 'Frec+'}, 'day_nbr', 1, 4),
		({'en': 'Negative Frequency', 'es': 'Frec-'}, 'freq_neg', 1, 4),
		({'en': 'GAP', 'es': 'GAP'}, 'gap', 1, 4),
		({'en': 'GAP Date', 'es': 'Fecha GAP'}, 'gap_date_str', 1, 4),
		({'en': 'Fifth Stage', 'es': '5ta'}, 'fs', 1, 4),
		({'en': 'AU', 'es': 'Eje 258'}, 'au', 1, 4),
		({'en': 'CG', 'es': 'CG'}, 'cg', 1, 4),
		({'en': 'DGC', 'es': 'DGC'}, 'cg_tot_days', 1, 4),
	]
	# Append the headers of the file
	if 'es' in lang.lower():
	    lang = 'es'
	    date_title = ['Fecha:', indate.strftime('%d-%b-%Y')]
	    quad_title = ['Cuadrante:', date_utils.quadrant(indate)]
	    round_title = ['Vuelta:', date_utils.quadrant(indate)]
	    data.append(date_title)
	    data.append(quad_title)
	    data.append(round_title)
	    data.append([])
	    data.append([])
	    data.append(['Valores de la vuelta para la fecha:'])
	    data.append([])
	else:
	    lang = 'en'
	    date_title = ['Date:', indate.strftime('%d-%b-%Y')]
	    quad_title = ['Quadrant:', date_utils.quadrant(indate)]
	    round_title = ['Round:', date_utils.quadrant(indate)]
	    data.append(date_title)
	    data.append(quad_title)
	    data.append(round_title)
	    data.append([])
	    data.append([])
	    data.append(['Round values for date:'])
	    data.append([])
	# Now the quad values
	quads = date_utils.quadrant_vals(indate)
	for vals in display_order:
		if not vals[0]:
			data.append([])
		else:
			title = vals[0][lang]
			key = vals[1]
			ql = 'q' + str(vals[2])
			qr = 'q' + str(vals[3])
			row_vals_l = [str(i) for i in quads[ql][key]]
			row_vals_r = [str(i) for i in quads[qr][key]]
			row_vals_lu = [unidecode(j) for j in row_vals_l]
			row_vals_ru = [unidecode(j) for j in row_vals_r]
			row = [title] + row_vals_lu + [''] + row_vals_ru
			data.append(row)
	return data

