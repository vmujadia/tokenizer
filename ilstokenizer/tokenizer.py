import ilstokenizer._tokenizer_ils as _tokenizer_ils

def tokenize(sentence, to_lower=False):
    if to_lower:
        sentence = sentence.lower()
    sentence = sentence.split()
    return " ".join(_tokenizer_ils.tokenize(sentence))

def tokenize_text(text, to_lower=False):
    if to_lower:
        text = text.lower()
    #text = text.split()
    return _tokenizer_ils.tokenize_text(text)
