import ilstokenizer._tokenizer_ils as _tokenizer_ils

def tokenize(sentence):
    sentence = sentence.split()
    return " ".join(_tokenizer_ils.tokenize(sentence))

def tokenize_text(text):
    text = text.split()
    return " ".join(_tokenizer_ils.tokenize_text(text))
