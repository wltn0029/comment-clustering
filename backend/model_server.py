
from flask import Flask

app = Flask(__name__)



@app.route("/")
def model_api():
    return "<h1>TEST!</h1>"



if __name__ == '__main__':
    # options
    #host_addr = "192.168.0.100"
    host_addr = '0.0.0.0'
    port_num = 8080
    app.debug == True

    # run flask server
    app.run(host = host_addr, port = port_num, threaded = True, debug = app.debug)
