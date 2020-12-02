from google_trans_new import google_translator  

# input : { id: string, authorDisplayName: string, authorProfileImageUrl: string, textOriginal: string}
#    do : translate the original text into English
# output:  
def translator(comment):
    text = comment['textOriginal']
    translator = google_translator()  
    translate_text = translator.translate(text,lang_tgt='en')  
    comment['textOriginal'] = translate_text

    # DEBUG print
    print(translate_text)

    return comment


if __name__ == "__main__":
    test_comment = { 'id': '222', 'authorDisplayName': 'zinuok', 'authorProfileImageUrl': 'https://', 'textOriginal': 'こんにちは'}
    translator(test_comment)