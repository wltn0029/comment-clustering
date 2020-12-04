import torch
import ast
import requests
from flask import flash, redirect, url_for, send_from_directory, Flask, render_template, request 
from flask_cors import CORS
from math import *
import json;
from utils import *
from model import sentiment
from multiprocessing import Pool
import time
from OpenSSL import SSL
import numpy as np
import gc

 
num_cores = 2 # 6 how many cores will be used concurrently
batch_size = 5 # 10
analyzer = sentiment.Analyzer()

# for flask
app = Flask(__name__)
CORS(app)

@app.route("/test", methods = ["GET", "POST"])
def test():
    return "<h1>Test Message.<h1>"

# -------------------------------------------------------------------- #
# classify comments according to sentimental: Positive, Negative, Neutral
# -------------------------------------------------------------------- #
@app.route("/main", methods = ["POST"])
def do_analysis():
    # garbage collection
    gc.collect()
    torch.cuda.empty_cache()

    # for processing-time measurement
    start = time.time()

    # get input
    #input = generate_dummy_input()
    data = getdata(request.data)
    input = data["rawData"]
    input_len = len(input)
    """
    # DEBUG print
    print("< raw input >")
    print(data)
    print("< parsed >")
    print(input)
    return
    """

    with Pool(processes=num_cores) as pool: # multi-processing
        # separating Korean comments
        korean_input = []
        other_input = []
        for e in input:
            if is_Korean(e['textOriginal']):
                korean_input.append(e)
            else:
                other_input.append(e)

        # translate into English
        input = translator(other_input)

        # extract plain text
        korean_text = pool.map(do_extract, korean_input)
        text = pool.map(do_extract, input)

        # sentiment analysis <-- need to be parallel
        korean_scores = []
        scores = []
        for i in range(ceil(len(korean_text)/batch_size)):
            start = batch_size*i
            result = analyzer.analyze_korean_sentences(korean_text[start:start+batch_size])
            if i == ceil(len(korean_text)/batch_size)-1:
                for j in range(batch_size-len(result)):
                    result.append(-2) # dummy value
            korean_scores.append(result)
        for i in range(ceil(len(text)/batch_size)):
            start = batch_size*i
            result = analyzer.analyze_sentences(text[start:start+batch_size])
            if i == ceil(len(text)/batch_size)-1:
                for j in range(batch_size-len(result)):
                    result.append(-2) # dummy value
            scores.append(result)
        korean_scores = np.array(korean_scores).flatten()
        scores = np.array(scores).flatten()

        # neutral handle: using python library

        # classify comments
        positive = []
        negative = []
        neutral = []
        for i in range(len(korean_text)): # this is O(n).. maybe need to be fixed
            if korean_scores[i] > 0:
                positive.append(korean_input[i])
            elif korean_scores[i] < 0:
                negative.append(korean_input[i])  
            else:
                neutral.append(korean_input[i])
        for i in range(len(text)): # this is O(n).. maybe need to be fixed
            if scores[i] > 0:
                positive.append(input[i])
            elif scores[i] < 0:
                negative.append(input[i])  
            else:
                neutral.append(input[i])

    # make output
    output_len = len(positive)+len(negative)+len(neutral)
    print("input: ")
    print(input_len)
    print("output: ")
    print(output_len)
    output = {}
    output['pos'] = positive
    output['neg'] = negative
    output['neu'] = neutral

    # DEBUG print
    """
    print("\n<Positive>")
    print(positive)
    print("\n<Negative>")
    print(negative)
    print("\n<Neutral>")
    print(neutral)
    print("processing time: " + str(time.time()-start))
    print("-----------------------")
    print(json.dumps(output, ensure_ascii=False))
    print("-----------------------")
    """
    
    # for english and korean
    return json.dumps(output, ensure_ascii=False)


    #return json.dumps(output)
    

# for external access) http://143.248.144.129:8080/
if __name__ == '__main__':
    # options
    #host_addr = '0.0.0.0' # broadcast to network
    host_addr = '127.0.0.1' # localhost
    port_num = 8080
    app.debug == True
    #context = ('certificate/future.crt', 'certificate/future.key') # for HTTPS

    # run flask server: sentimental classification
    app.run(host = host_addr, port = port_num, threaded = True, debug = app.debug)
    #app.run(host = host_addr, port = port_num, ssl_context=context, threaded = True, debug = app.debug)