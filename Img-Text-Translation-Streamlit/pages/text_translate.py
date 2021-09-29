import streamlit as st
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from langdetect import detect
def app():
	lang_dictionary = {"sv":"sv_SE","fi":"fi_FI","hi":"hi_IN","ro":"ro_RO","ko":"ko_KR","sl":"sl_SI","mr":"mr_IN","pt":"pt_XX",
    "de":"de_DE","en":"en_XX","fa": "fa_IR","th": "th_TH","mk": "mk_MK","pl": "pl_PL","ru": "ru_RU","lv": "lv_LV",
    "bn": "bn_IN","et": "et_EE","af": "af_ZA","he":"he_IL","tl":"tl_XX","hr":"hr_HR","ml":"ml_IN","es":"es_XX","it":"it_IT",
    "nl":"nl_XX","ar":"ar_AR","tr":"tr_TR","ta":"ta_IN","te" : "te_IN","fr" : "fr_XX","ne" : "ne_NP","lt" : "lt_LT","ur" : "ur_PK",
    "uk" : "uk_UA","sw" : "sw_KE","cs" : "cs_CZ","gu" : "gu_IN"}

	orig_name = {"sv":"Swedish","fi":"Finnish","hi":"Hindi","ro":"Romanian","ko":"Korean","sl":"Slovenian","mr":"Marathi","pt":"Portugese",
    "de":"German","en":"English","fa": "Persian","th": "Thai","mk": "Macedonian","pl": "Polish","ru": "Russian","lv": "Latvian",
    "bn": "Bengali","et": "Estonian","af": "Afrikaans","he":"Hebrew","tl":"Tagalog","hr":"Croatian","ml":"Malayalam","es":"Spanish","it":"Italian",
    "nl":"Dutch/Flemish","ar":"Arabic","tr":"Turkish","ta":"Tamil","te" : "Telugu","fr" : "French","ne" : "Nepali","lt" : "Lithuanian","ur" : "Urdu",
    "uk" : "Ukrainian","sw" : "Swahili","cs" : "Czech","gu" : "Gujarati"}

	st.subheader("The Languages currently supported are : ")
	st.info(list(orig_name.values()))

	inp = st.text_input("Enter text that you want to translate to english")
	if ((inp is not None) and (st.button("TRANSLATE"))):

		model_name = "facebook/mbart-large-50-many-to-many-mmt"
		model = MBartForConditionalGeneration.from_pretrained(model_name)
		r = detect(inp)
		st.subheader("LANGUAGE DETECTED IS ")
		st.info(orig_name[r])
		lang = lang_dictionary[r]
		tokenizer = MBart50TokenizerFast.from_pretrained(model_name, src_lang = lang)
		encoded_text = tokenizer(inp, return_tensors="pt")
		if r =="en":
			st.warning("Text is already in ENGLISH")
		else:
			generated_tokens = model.generate(**encoded_text, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])
			out = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
			out = str(out).strip('][\'')
			st.success("TRANSLATED!")
			st.subheader("TRANSLATED TEXT")
			st.write(out)
	else:
		st.warning("Please enter text for translating")
