import torch
from flask import Flask
from utils import *
from model import sentiment
from multiprocessing import Pool

app = Flask(__name__)
num_cores = 6

# test function
@app.route("/")
def model_api():
    return "<h1>Jae-young loves So-young!</h1>"

# classify comments according to sentimental: Positive, Negative, Neutral
@app.route("/main")
def do_analysis():
    # get input
    input = generate_dummy_input()

    # translate into English
    input = translator(input)

    # extract plain text
    with Pool(num_cores) as pool:
        text = pool.map(do_extract, input)

    # sentiment analysis
    analyzer = sentiment.Analyzer()
    scores = analyzer.analyze_sentences(text)

    # classify comments

    print(scores)
    

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
