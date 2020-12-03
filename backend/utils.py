from model import sentiment
from google_trans_new import google_translator  
from multiprocessing import Pool
import re
import ast

"""
util functions used for model server
"""

# how many cores will be used concurrently
num_cores = 6


# -------------------------------------------------------------------- #
# input : data from client
#    do : decode the data in utf-8
# output: decoded data
# -------------------------------------------------------------------- #
def getdata(data):
    return ast.literal_eval(data.decode("utf-8"))


# -------------------------------------------------------------------- #
# input : None
#    do : generate dummy inputs
# output: generated list of dummy inputs
# -------------------------------------------------------------------- #
def generate_dummy_input():
    l = []
    # Korean
    l.append({ 'id': '1', 'authorDisplayName': 'A', 'authorProfileImageUrl': 'https://', 'textOriginal': '연기는 별로지만 재미 하나는 진짜 끝내줌!'})
    l.append({ 'id': '2', 'authorDisplayName': 'B', 'authorProfileImageUrl': 'https://', 'textOriginal': '주연배우가 아깝다. 총체적 난국...'})
    l.append({ 'id': '3', 'authorDisplayName': 'D', 'authorProfileImageUrl': 'https://', 'textOriginal': '매우 화가 난다'})
    # English
    l.append({ 'id': '4', 'authorDisplayName': 'C', 'authorProfileImageUrl': 'https://', 'textOriginal': 'What a beautiful contents!'})
    l.append({ 'id': '5', 'authorDisplayName': 'C', 'authorProfileImageUrl': 'https://', 'textOriginal': 'what the hell'})
    return l


# -------------------------------------------------------------------- #
# input : string
#    do : check if Korean is included.
# output: Boolean
# -------------------------------------------------------------------- #
def is_Korean(str):
    return len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', str)) > 0


# -------------------------------------------------------------------- #
# extractor body function
# -------------------------------------------------------------------- #
def do_extract(comment):
    return comment['textOriginal']


# -------------------------------------------------------------------- #
# translator body function
# -------------------------------------------------------------------- #
def do_translate(comment):
    # comment = { id: string, authorDisplayName: string, authorProfileImageUrl: string, textOriginal: string}
    translator = google_translator()
    comment['textOriginal'] = translator.translate(comment['textOriginal'],lang_tgt='en')
    return comment
# -------------------------------------------------------------------- #
# input : comment which includes original text in any language
#    do : translate the original text into English
# output: comment which includes translated text in English
# -------------------------------------------------------------------- #
def translator(comment_list):
    if len(comment_list) == 0:
        return []
    pool = Pool(processes=num_cores)
    trans_list = pool.map(do_translate, comment_list)
    pool.close()
    pool.join()
    return trans_list