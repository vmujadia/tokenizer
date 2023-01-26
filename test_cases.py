from ilstokenizer import tokenizer


text = "पीड़िता के पिता की मौत के बाद मामले में सीबीआई जांच बैठी थी तो डॉ . प्रशांत पर लापरवाही का आरोप लगा था । वह जिला अस्पताल की इमर्जेंसी में ईएमओ पद पर तैनात थे । उस समय एक वीडियो वायरल हुआ था , जिसमें वह हंसते हुए दिख रहे थे । सीबीआई की जांच रिपोर्ट पर उन्हें 12 अप्रैल 2018 को निलंबित कर दिया गया था । 9 महीने बाद वह बहाल हुए और फतेहपुर जिला अस्पताल में तैनाती हुई । शहर कोतवाली क्षेत्र के मोतीनगर निवासी डॉ . प्रशांत उपाध्याय फतेहपुर जिला अस्पताल के ब्लड बैंक में कार्यरत थे । 1918 - ज्येष्ठ संगीतकार सी . रामचंद्र यांचा जन्म ."

print (tokenizer.tokenize_text(text, language='hin'))

text = "The primary sensor has 1.25 - micron pixels and an f / 1.8 aperture . The actress said that she is ' disturbed as a parent ' because ' the world is on fire quite literally. ' She also asserted that she fears for her child ' s future as she looks out at the world today ."

print (tokenizer.tokenize_text(text, language='eng'))
#print (tokenizer.tokenize("my name is ram."))
