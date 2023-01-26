# lang = 0 for all languages other than Urdu, lang = 1 for Urdu
import re
import argparse
import os
from string import punctuation


punctuations = set(punctuation) - {'?', '۔', '؟', '।', '!', '|', '.'}

token_specification = [
    ('datemonth',
     r'^(0?[1-9]|1[012])[-\/\.](0?[1-9]|[12][0-9]|3[01])[-\/\.](1|2)\d\d\d$'),
    ('monthdate',
     r'^(0?[1-9]|[12][0-9]|3[01])[-\/\.](0?[1-9]|1[012])[-\/\.](1|2)\d\d\d$'),
    ('yearmonth',
     r'^((1|2)\d\d\d)[-\/\.](0?[1-9]|1[012])[-\/\.](0?[1-9]|[12][0-9]|3[01])'),
    ('EMAIL1', r'([\w\.])+@(\w)+\.(com|org|co\.in)$'),
    ('url1', r'(www\.)([-a-z0-9]+\.)*([-a-z0-9]+.*)(\/[-a-z0-9]+)*/i'),
    ('url', r'/((?:https?\:\/\/|www\.)(?:[-a-z0-9]+\.)*[-a-z0-9]+.*)/i'),
    ('BRACKET', r'[\(\)\[\]\{\}]'),       # Brackets
    ('NUMBER', r'^(\d+)([,\.]\d+)*(\w)*'),  # Integer or decimal number
    ('ASSIGN', r'[~:]'),          # Assignment operator
    ('END', r'[;!_]'),           # Statement terminator
    ('EQUAL', r'='),   # Equals
    ('OP', r'[+*\/\-]'),    # Arithmetic operators
    ('QUOTES', r'[\"\'‘’]'),          # quotes
    ('Fullstop', r'(\.+)$'),
    ('ellips', r'\.(\.)+'),
    ('HYPHEN', r'[-+\|+]'),
    ('Slashes', r'[\\\/]'),
    ('COMMA12', r'[,%]'),
    ('hin_stop', r'।'),
    ('quotes_question', r'[”\?]'),
    ('hashtag', r'#')
]
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex)


def tokenize(list_s):
    tkns = []
    for wrds in list_s:
        wrds_len = len(wrds)
        initial_pos = 0
        end_pos = 0
        while initial_pos <= (wrds_len - 1):
            mo = get_token.match(wrds, initial_pos)
            if mo is not None and len(mo.group(0)) == wrds_len:
                tkns.append(wrds)
                initial_pos = wrds_len
            else:
                match_out = get_token.search(wrds, initial_pos)
                if match_out is not None:
                    end_pos = match_out.end()
                    if match_out.lastgroup == "NUMBER":
                        aa = wrds[initial_pos:(end_pos)]
                    else:
                        aa = wrds[initial_pos:(end_pos - 1)]
                    if aa != '':
                        tkns.append(aa)
                    if match_out.lastgroup != "NUMBER":
                        tkns.append(match_out.group(0))
                    initial_pos = end_pos
                else:
                    tkns.append(wrds[initial_pos:])
                    initial_pos = wrds_len
    return tkns

# only for Hindi and fullstop
ignore_sentence_end_list = ['डॉ','Pvt','Ltd','Co','Ph','Rs',"उदा","eVnY","eVl","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX","XXX","XL","L","LX","LXX","LXXX","XC","C","D","M","Adj","Adm","Adv","Asst","Ave","Bldg","Brig","Bros","Capt","Cmdr","Col","Comdr","Con","Corp","Cpl","Dr","Ens","Gen","Gov","Govt","Hon","Hosp","Insp","Lt","Maj","Messrs","Mlle","Mme","Mr","Mrs","Ms","Msgr","Op","Ord","Pfc","Ph","Prof","Pvt","Rep","Reps","Res","Rev","Rt","Sen","Sens","Sgt","Sr","St","Supt","Surg","v","vs","किमी","किग्रा","श्रीमती","क","का","कि","की","कु","कू","के","कै","को","कौ","कं","कँ","कृ","ख","खा","खि","खी","खु","खू","खे","खै","खो","खौ","खं","खँ","खृ","ग","गा","गि","गी","गु","गू","गे","गै","गो","गौ","गं","गँ","गृ","ग्र","ग्रा","घ","घा","घि","घी","घु","घू","घे","घै","घो","घौ","घं","घँ","घृ","च","चा","चि","ची","चु","चू","चे","चै","चो","चौ","चं","चँ","चृ","च्र","च्रा","छ","छा","छि","छी","छु","छू","छे","छै","छो","छौ","छं","छँ","छृ","ज","जा","जि","जी","जु","जू","जे","जै","जो","जौ","जं","जँ","जृ","ज्र","ज्रा","झ","झा","झि","झी","झु","झू","झे","झै","झो","झौ","झं","झँ","झृ","ञ","ञा","ञि","ञी","ञु","ञू","ञे","ञै","ञो","ञौ","ञं","ञँ","ञृ","ट","टा","टि","टी","टु","टू","टे","टै","टो","टौ","टं","टँ","टृ","ट्र","ट्रा","ठ","ठा","ठि","ठी","ठु","ठू","ठे","ठै","ठो","ठौ","ठं","ठँ","ठृ","ड","डा","डि","डी","डु","डू","डे","डै","डो","डौ","डं","डँ","डृ","डॉ","ढ","ढा","ढि","ढी","ढु","ढू","ढे","ढै","ढो","ढौ","ढं","ढँ","ढृ","ण","णा","णि","णी","णु","णू","णे","णै","णो","णौ","णं","णँ","णृ","त","ता","ति","ती","तु","तू","ते","तै","तो","तौ","तं","तँ","तृ","थ","थि","थु","थू","थै","थो","थौ","थं","थँ","थृ","थ्र","थ्रा","द","दा","दि","दी","दु","दू","दे","दै","दो","दौ","दं","दँ","दृ","द्र","द्रा","दॉ","ध","धा","धि","धी","धु","धू","धे","धै","धो","धौ","धं","धँ","धृ","ध्र","ध्रा","न","ना","नि","नी","नु","नू","ने","नै","नो","नौ","नं","नँ","नृ","प","पा","पि","पी","पु","पू","पे","पै","पो","पौ","पं","पँ","पृ","फ","फा","फि","फी","फु","फू","फे","फै","फो","फौ","फं","फँ","फृ","फ्र","फ्रा","ब","बा","बि","बी","बु","बू","बे","बै","बो","बौ","बं","बँ","बृ","ब्र","ब्रा","भ","भा","भि","भी","भु","भू","भे","भै","भो","भौ","भं","भँ","भृ","भ्र","भ्रा","म","मा","मि","मी","मु","मू","मे","मै","मो","मौ","मं","मँ","मृ","य","या","यि","यी","यु","यू","ये","यै","यो","यौ","यं","यँ","यृ","र","रा","रि","री","रु","रू","रे","रै","रो","रौ","रं","रँ","रृ","ल","ला","लि","ली","लु","लू","ले","लै","लो","लौ","लं","लँ","लृ","व","वा","वि","वी","वु","वू","वे","वै","वो","वौ","वं","वँ","वृ","व्र","व्रा","श","शा","शि","शी","शु","शू","शे","शै","शो","शौ","शं","शँ","शृ","स","सा","सि","सी","सु","सू","से","सै","सो","सौ","सं","सँ","सृ","ष","षा","षि","षी","षु","षू","षे","षै","षो","षौ","षं","षँ","षृ","ह","हा","हि","ही","हु","हू","हे","हौ","हं","हँ","हृ","क्ष","क्षा","क्षि","क्षी","क्षु","क्षू","क्षे","क्षै","क्षो","क्षौ","क्षं","क्षँ","क्षृ","त्र","त्रा","त्रि","त्री","त्रु","त्रू","त्रे","त्रै","त्रो","त्रौ","त्रं","त्रँ","त्रृ","ज्ञ","ज्ञा","ज्ञि","ज्ञी","ज्ञु","ज्ञू","ज्ञे","ज्ञै","ज्ञो","ज्ञौ","ज्ञं","ज्ञँ","ज्ञृ","श्र","श्रा","श्रि","श्री","श्रु","श्रू","श्रे","श्रै","श्रो","श्रौ","श्रं","श्रँ","श्रृ","प्र","प्रा","प्रि","प्री","प्रु","प्रू","प्रे","प्रै","प्रो","प्रौ","प्रं","प्रँ","प्रृ","क्र","क्रा","क्रि","क्री","क्रु","क्रू","क्रे","क्रै","क्रो","क्रौ","क्रं","क्रँ","क्रृ","अ","आ","इ","ई","उ","ऊ","ए","ऐ","ओ","औ","अं","अँ","ऋ","ऍ","ऑ","ए","बी","सी","डी","ई","एफ","एफ़","जी","एच","आई","आइ","जे","ज़े","के","एल","एम","एन","ओ","पी","क्यू","क्यु","आर","एस","टी","यू","यु","वी","डब्लू","डब्ल्यू","डब्ल्यु","एक्स","वाइ","वाई","जैड","जेड","ज़ैड","ज़ेड"]
threshold = {'eng':1, 'hin':1}
def tokenize_text(text, language='eng'):
    sentences = re.findall('.*?।|.*?\n', text + '\n', re.UNICODE)
    proper_sentences = list()
    for index, sentence in enumerate(sentences):
        if sentence.strip() != '':
            list_tokens = tokenize(sentence.split())
            end_sentence_markers = []
            
            for index, token in enumerate(list_tokens):
                if token in ['?', '۔', '؟', '।', '!', '|', '.'] and list_tokens[index-1] not in ignore_sentence_end_list:
                    if index>0 and len(list_tokens)<index and list_tokens[index-1].isdigit() and list_tokens[index+1].isdigit():
                        pass
                    else:
                        if language!='eng':
                            #print (language, token, list_tokens[index-1], len(list_tokens[index-1]), threshold.get(language,1))
                            if token=='.' and len(list_tokens[index-1])>threshold.get(language,1):
                                end_sentence_markers.append(index + 1)
                        else:
                            end_sentence_markers.append(index + 1)
            
            #end_sentence_markers = [index + 1 for index, token in enumerate(
            #    list_tokens) if token in ['?', '۔', '؟', '।', '!', '|', '.'] and list_tokens[index-1] not in ignore_sentence_end_list]
            updated_sentence_markers = list()
            false_flag = False
            true_start = 0
            for start, end in zip(end_sentence_markers, end_sentence_markers[1:]):
                if end - start > 2:
                    if not false_flag and not true_start:
                        updated_sentence_markers.append(start)
                    else:
                        updated_sentence_markers.append(true_start)
                        true_start = 0
                        false_flag = False
                else:
                    false_flag = True
                    true_start = start
            updated_sentence_markers += [len(list_tokens)]
            if len(list_tokens) >= 2 and \
                    list_tokens[-1] in punctuations and len(updated_sentence_markers) and \
                    list_tokens[updated_sentence_markers[-1] - 1] == list_tokens[-2]:
                updated_sentence_markers[-1] += 2
            if len(updated_sentence_markers) > 0:
                end_sentence_markers_with_sentence_end_positions = [
                    0] + updated_sentence_markers
                sentence_boundaries = list(zip(
                    end_sentence_markers_with_sentence_end_positions, end_sentence_markers_with_sentence_end_positions[1:]))
                for start, end in sentence_boundaries:
                    individual_sentence = ' '.join(list_tokens[start: end])
                    proper_sentences.append(individual_sentence)
            else:
                proper_sentences.append(' '.join(list_tokens))
    return proper_sentences

