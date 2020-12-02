import torch
import ast
import requests
from flask import flash, redirect, url_for, send_from_directory, Flask, render_template, request
import json;
from utils import *
from model import sentiment
from multiprocessing import Pool

import time

app = Flask(__name__)
num_cores = 6

def getdata(data):
    return ast.literal_eval(data.decode("utf-8"))


# classify comments according to sentimental: Positive, Negative, Neutral
@app.route("/main", methods = ["POST", "GET"])
def do_analysis():
    if request.method != 'POST':
        return

    # get input
    #input = generate_dummy_input()
    data = getdata(request.data)
    input = data["input"]
    
    # translate into English
    input = translator(input)

    # extract plain text
    with Pool(num_cores) as pool: # multi-processing
        text = pool.map(do_extract, input)

    # sentiment analysis
    analyzer = sentiment.Analyzer()
    scores = analyzer.analyze_sentences(text)

    # classify comments
    positive = []
    negative = []
    neutral = []
    for i in range(len(scores)): # this is O(n).. maybe need to be fixed
        if scores[i] > 0:
            positive.append(input[i])
        elif scores[i] < 0:
            negative.append(input[i])  
        else:
            neutral.append(input[i])
    output = {}
    output['pos'] = positive
    output['neg'] = negative
    output['neu'] = neutral
    print(output)

    return json.dumps(output)
    

# for external access) http://143.248.144.129:8080/
if __name__ == '__main__':
    # options
    host_addr = '0.0.0.0' # broadcast to network
    port_num = 8080
    app.debug == True

    # sentimental classification
    #do_analysis()
    
    # run flask server
    app.run(host = host_addr, port = port_num, threaded = True, debug = app.debug)
