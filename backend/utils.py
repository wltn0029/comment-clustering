from model import sentiment
from google_trans_new import google_translator  
from multiprocessing import Pool

"""
util functions used for model server
"""

# how many cores will be used
num_cores = 6



def generate_dummy_input():
    l = []
    l.append({ 'id': '1', 'authorDisplayName': 'A', 'authorProfileImageUrl': 'https://', 'textOriginal': '私は非常に満足している'})
    l.append({ 'id': '2', 'authorDisplayName': 'B', 'authorProfileImageUrl': 'https://', 'textOriginal': 'これはあまりにも悲しい'})
    l.append({ 'id': '3', 'authorDisplayName': 'C', 'authorProfileImageUrl': 'https://', 'textOriginal': 'これは中立的な文章である'})
    return l


def do_extract(comment):
    return comment['textOriginal']

# translator body function
def do_translate(comment):
    # comment = { id: string, authorDisplayName: string, authorProfileImageUrl: string, textOriginal: string}
    translator = google_translator()
    comment['textOriginal'] = translator.translate(comment['textOriginal'],lang_tgt='en')

    return comment

# input : comment which includes original text in any language
#    do : translate the original text into English
# output: comment which includes translated text in English
def translator(comment_list):
    pool = Pool(num_cores)
    trans_list = pool.map(do_translate, comment_list)
    pool.close()
    pool.join()

    # DEBUG print
    #print(trans_list)

    return trans_list
