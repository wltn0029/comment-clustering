from flask import Flask

app = Flask(__name__)

@app.route("/")
def model_api():
    return "<h1>Jae-young loves So-young!</h1>"



# for external access) http://143.248.144.129:8080/
if __name__ == '__main__':
    # options
    host_addr = '0.0.0.0' # broadcast to network
    port_num = 8080
    app.debug == True

    # run flask server
    app.run(host = host_addr, port = port_num, threaded = True, debug = app.debug)
