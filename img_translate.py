import streamlit as st
import numpy as np
import matplotlib as plt
from pylab import rcParams
import cv2
import easyocr
from IPython.display import Image
import PIL
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from langdetect import detect
from PIL import ImageDraw,Image, ImageFont, ImageDraw, ImageEnhance, ImageFont
def app():

	language_d ={"Telugu" : "te","Vietnamese" : "vi","Lithuanian" : "lt","French": "fr","Thai": "th","Czech" : "cs","Bengali" : "bn",
    "Spanish": "es","Russian": "ru",'Urdu':'ur','Latvian':'lv','Italian':'it','Swahili':'sw','Ukrainian':'uk','Korean':'ko','English':'en', 
    'Romanian':'ro','Nepali':'ne','Indonesian':'id','Marathi': 'mr','Arabic': 'ar','Hindi' : 'hi','German': 'de','Persian': 'fa', 'Estonian': 'et', 
    'Polish': 'pl','Swedish': 'sv',"Portugese":"pt","Turkish": "tr","Afrikaans":"af","Tamil":"ta","Dutch":"nl","Tagalog":"tl","Slovenian":"sl"}
	class imgt:

		def draw_boxes(self,image, bounds, color='green', width=3):
			draw = ImageDraw.Draw(image)
			for bound in bounds:
				p0, p1, p2, p3 = bound[0]
				draw.line([*p0, *p1, *p2, *p3, *p0], fill='green', width=3)
			return image
		def text_wrap(self,text,font,max_width):
			lines = []
			# If the text width is smaller than the image width, then no need to split
			# just add it to the line list and return
			if font.getsize(text)[0]  <= max_width:
				lines.append(text)
			else:
				#split the line by spaces to get words
				words = text.split(' ')
				i = 0
				# append every word to a line while its width is shorter than the image width
				while i < len(words):
					line = ''
					while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
						line = line + words[i]+ " "
						i += 1
					if not line:
						line = words[i]
						i += 1
					lines.append(line)
			return lines

	reader = ""
	langs = list(language_d.keys())
	st.subheader("The Languages currently supported are : ")
	st.info(langs)
	langs.insert(0,"Not selected yet")
	st.subheader('Language you need to convert: ')
	language = st.selectbox("Select",langs)
	if language == "Not selected yet":
		st.warning("Language not selected yet")
	else:
		ln = "Language Selected is : " + language
		st.info(ln)
		reader = easyocr.Reader([language_d[language]])
		#defining reader object with required languages
	st.write("Please upload the image")
	img = st.file_uploader('Upload an image')
	if img is not None:
		rcParams['figure.figsize'] = 8,16
		st.image(img)
		#display raw output data
		output = reader.readtext(img.name)
		output_txt = [elem[1] for elem in output]
		st.subheader("Text read from input image : ")
		st.success(output_txt)
		x = []
		y = []
		for i in range(len(output)):
		  x.append(output[i][0][0][0])
		  x.append(output[i][0][2][0])
		  y.append(output[i][0][0][1])
		  y.append(output[i][0][2][1])

		min_x = min(x)
		max_x = max(x)
		min_y = min(y)
		max_y = max(y)
		#function to draw box on the image
		im = PIL.Image.open(img.name)
		draw = ImageDraw.Draw(im)
		ig = imgt()
		# st.image(ig.draw_boxes(im, output))
		model_name = "facebook/mbart-large-50-many-to-many-mmt"
		model = MBartForConditionalGeneration.from_pretrained(model_name)
		listToStr = ' '.join([str(elem) for elem in output_txt]) 
		text = [listToStr]
		out_list =[]
		lang_dictionary = {"sv":"sv_SE","fi":"fi_FI","hi":"hi_IN","ro":"ro_RO","ko":"ko_KR","sl":"sl_SI","mr":"mr_IN","pt":"pt_XX",
	    "de":"de_DE","en":"en_XX","fa": "fa_IR","th": "th_TH","mk": "mk_MK","pl": "pl_PL","en": "en_XX","ru": "ru_RU","lv": "lv_LV",
	    "bn": "bn_IN","et": "et_EE","af": "af_ZA","he":"he_IL","tl":"tl_XX","hr":"hr_HR","ml":"ml_IN","es":"es_XX","it":"it_IT",
	    "nl":"nl_XX","ar":"ar_AR","tr":"tr_TR","ta":"ta_IN","te" : "te_IN","fr" : "fr_XX","ne" : "ne_NP","lt" : "lt_LT","ur" : "ur_PK",
	    "uk" : "uk_UA","sw" : "sw_KE","cs" : "cs_CZ","gu" : "gu_IN"}
		for i in text:
			lang = lang_dictionary[language_d[language]]
			tokenizer = MBart50TokenizerFast.from_pretrained(model_name, src_lang = lang)
			encoded_text = tokenizer(i, return_tensors="pt")
			generated_tokens = model.generate(**encoded_text, forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"])
			out = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
			out = str(out).strip('][\'')
			out_list.append(out)
		font = ImageFont.truetype("arial.ttf", 25)
		source_img = Image.open(img.name).convert("RGBA")
		draw = ImageDraw.Draw(source_img)
		colors = source_img.getpixel((int(min_x-10),int(min_y-10))) 
		draw.rectangle(((min_x, min_y), (max_x, max_y)), fill=colors)
		st.subheader("Converted text is : ")
		st.success(out_list[0])
		lines = ig.text_wrap(out_list[0],font,max_x-min_x-20)
		y = min_y+15
		x = min_x+15
		line_height = 35
		for line in lines:
			draw.text((x,y), line, font=font) 
			y = y + line_height
		st.subheader("After trying to replace original image with converted text : ")
		st.image(source_img)
	else:
		st.warning("No file has been chosen yet")

