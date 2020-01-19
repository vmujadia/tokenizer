import ilstokenizer._tokenizer_ils as _tokenizer_ils

def tokenize(sentence):
    return _tokenizer_ils.tokenize(sentence)

def tokenize_text(text):
    return _tokenizer_ils.tokenize_text(text)
