import torch
from model import sentiment
from google_trans_new import google_translator  

# comment = { id: string, authorDisplayName: string, authorProfileImageUrl: string, textOriginal: string}

# input : comment which includes original text in any language
#    do : translate the original text into English
# output: comment which includes translated text in English
def translator(comment):
    text = comment['textOriginal']
    translator = google_translator()  
    translate_text = translator.translate(text,lang_tgt='en')  
    comment['textOriginal'] = translate_text

    # DEBUG print
    print(translate_text)

    return comment


def model():
    # evalation
    analyzer = sentiment.Analyzer()
    sample_text = ["I am so happy", "This is so sad ..", "This is a neutral sentence."]
    out = analyzer.analyze_sentences(sample_text)
    print(out)

if __name__ == "__main__":
    test_comment = { 'id': '222', 'authorDisplayName': 'zinuok', 'authorProfileImageUrl': 'https://', 'textOriginal': 'こんにちは'}
    #translator(test_comment)

    model()
