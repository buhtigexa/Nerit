{ 
"hashtag":
			{	
				"regex":"(?P<hashtag>#[\\wá-úñü0-9Á-ÚÜÑ]+)",
				"replace":"\\g<hashtag>",
				"isolate":"True",
				"post":"HTAG",
				"titleize_regex":"(?P<x>#)(?P<hashtag>[\\wá-úüñ0-9]+)(?P<y>.*)",
				"titleize_replace":"\\g<hashtag>",
				"titleize":"True",
				"not_in_text":"False",
				"clean":"False"


			},

			
"mention":
			{
				"regex":"(?P<user_mentions>@[\\wá-úñü0-9Á-ÚÜÑ]+)",
				"replace":"\\g<user_mentions>",
				"isolate":"True",
				"post":"USER",
				"titleize_regex":"(?P<x>.*@)(?P<user_mentions>[\\wá-úüñ0-9]+)(?P<y>.*)",
				"titleize_replace":"\\g<user_mentions>",
				"titleize":"False",
				"not_in_text":"False",
				"clean":"False"

			},


"link":
		{
				"regex":"(?P<url_shorten>http[s]?.*/[\\w]+)",
				"replace":"\\g<url_shorten>",
				"isolate":"True",
				"post":"LINK",
				"titleize_regex":"(?P<x>.*)(?P<url_shorten>http[s]?.*/[\\w]+$)(?P<y>.*)",
				"titleize_replace":" ",
				"titleize":"False",
				"not_in_text":"False",
				"clean":"False"

		},


"temp":
		{
				"regex":"(?P<hum_tmp_st>[0-9]+)[ ]?(?P<magnitude>[°%\\'\\xc2\\xba\\x25])",
				"replace":"\\g<hum_tmp_st> \\g<magnitude>",
				"isolate":"True",
				"post":"TMP",
				"titleize":"False",
				"not_in_text":"True",
				"clean":"False"

		},


"time_1":
		{

				"regex":"(?P<time_1>[0-9]{1,2}[\\.:]{1}[0-9]{1,2}(pm|p.m|hs|horas|hrs)?(\\.)?)",
				"replace":"\\g<time_1>",
				"isolate":"True",
				"post":"TIME",
				"titleize":"False",
				"not_in_text":"True",
				"clean":"False"



		},

"time_2":
		{
				"regex":"(?P<time_2>[0-9]{1,4}(pm|p.m|am|a.m|hrs|hsr|hs|horas|p. m)(\\.)?)",
				"replace":"\\g<time_2>",
				"isolate":"True",
				"post":"TIME",
				"titleize":"False",
				"not_in_text":"True",
				"clean":"False"
		},

		


"date_1":
		{
				"regex":"(?P<date>^([0-9]{1,2}[/-]{1}[0-9]{1,2}[/-]{1}[0-9]{2,4}|[0-9]{1,2}[/-]{1}[0-9]{1,2})$)",
				"replace":"\\g<date>",
				"isolate":"True",
				"post":"DATE",
				"titleize":"False",
				"not_in_text":"True",
				"clean":"False"
		},




"mixed_words_1":
		{
				"regex":"^(?P<words_1>[a-záüúñ]+)(?P<num_1>[0-9]+)$",
				"replace":"\\g<words_1> \\g<num_1>",
				"isolate":"True",
				"post":"MIX",
				"titleize":"False",
				"not_in_text":"True",
				"clean":"False"
		},



"mixed_words_2":
		
		{
				"regex":"^(?P<num_2>[0-9]+)(?P<words_2>[a-záüúñ]+)$",
				"replace":"\\g<num_2> \\g<words_2>",
				"isolate":"True",
				"post":"MIX",
				"titleize":"False",
				"not_in_text":"True",
				"clean":"False"
		},





"utf_8":
		{
				"regex":"(?P<utf_8>^[\\x00-\\x2F\\x3a-\\x40\\x5b-\\x60\\x7b-\\xc2\\xbf\\xc5\\xbf-\\xd5\\xaf]$)",
				"replace":"",
				"isolate":"False",
				"post":"NO",
				"titleize":"False",
				"not_in_text":"True",
				"clean":"True"

		},

"informationless":
		{
				"regex":"(?P<informationless>^(rt|via|&gt[\\.;]?|ta|\\.\\.\\.|(ja)+|(je)+|(ji)+|(jo)+|(ju)+|(re)+|f|zc|zs|m|zp|gt|reporta[a-z]{0,}|descárgala|descargala|click|clic|ga|ah|oh|uh|vn|via)$)",
				"replace":"",
				"isolate":"False",
				"post":"NO",
				"titleize":"False",
				"not_in_text":"True",
				"clean":"True"
		},

"dirty_words":{

				"regex":"[\u0000-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u00BF\u011A-\u3000]+",
				"replace":" ",
				"isolate":"Default",
				"post":"NO",
				"titleize":"False",
				"not_in_text":"True",
				"clean":"False"
			}
	
}
