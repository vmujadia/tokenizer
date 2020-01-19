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

def tokenize_text(text):
    sentences = re.findall('.*?।|.*?\n', text + '\n', re.UNICODE)
    proper_sentences = list()
    for index, sentence in enumerate(sentences):
        if sentence.strip() != '':
            list_tokens = tokenize(sentence.split())
            end_sentence_markers = [index + 1 for index, token in enumerate(
                list_tokens) if token in ['?', '۔', '؟', '।', '!', '|', '.']]
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
    return " ".join(proper_sentences)

