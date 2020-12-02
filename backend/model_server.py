import torch
import ast
import requests
from flask import flash, redirect, url_for, send_from_directory, Flask, render_template, request
import json;
from utils import *
from model import sentiment
from multiprocessing import Pool
import time

 
num_cores = 6 # how many cores will be used concurrently
app = Flask(__name__)
analyzer = sentiment.Analyzer()



# -------------------------------------------------------------------- #
# classify comments according to sentimental: Positive, Negative, Neutral
# -------------------------------------------------------------------- #
@app.route("/main", methods = ["POST"])
def do_analysis():
    # for processing-time measurement
    start = time.time()

    # get input
    input = generate_dummy_input()
    #data = getdata(request.body)
    #input = data["rawData"]

    korean_input = []
    
    with Pool(processes=num_cores) as pool: # multi-processing
        # separating Korean comments
        for elem in input:
            if is_Korean(elem['textOriginal']):
                korean_input.append(elem)
                input.remove(elem)

        # translate into English
        input = translator(input)

        # extract plain text
        korean_text = pool.map(do_extract, korean_input)
        text = pool.map(do_extract, input)

        # sentiment analysis <-- need to be parallel
        korean_scores = analyzer.analyze_korean_sentences(korean_text)
        scores = analyzer.analyze_sentences(text)

        # classify comments
        positive = []
        negative = []
        neutral = []
        for i in range(len(korean_scores)): # this is O(n).. maybe need to be fixed
            if korean_scores[i] > 0:
                positive.append(korean_input[i])
            elif korean_scores[i] < 0:
                negative.append(korean_input[i])  
            else:
                neutral.append(korean_input[i])
        for i in range(len(scores)): # this is O(n).. maybe need to be fixed
            if scores[i] > 0:
                positive.append(input[i])
            elif scores[i] < 0:
                negative.append(input[i])  
            else:
                neutral.append(input[i])

    # make output
    output = {}
    output['pos'] = positive
    output['neg'] = negative
    output['neu'] = neutral

    # DEBUG print
    print("\n<Positive>")
    print(positive)
    print("\n<Negative>")
    print(negative)
    print("\n<Neutral>")
    print(neutral)
    print("processing time: " + str(time.time()-start))

    return json.dumps(output)
    

# for external access) http://143.248.144.129:8080/
if __name__ == '__main__':
    # options
    host_addr = '0.0.0.0' # broadcast to network
    port_num = 8080
    app.debug == True

    # sentimental classification
    do_analysis()
    
    # run flask server
    #app.run(host = host_addr, port = port_num, threaded = True, debug = app.debug)