import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def readData(path):
  f = open(path, "r")
  data = f.read()
  f.close()
  return data

@app.route('/hw-python/config', methods=['GET'])
def hw_python_config():
  return readData("hw-python/config.json")

@app.route('/hw-cpp/config', methods=['GET'])
def hw_cpp_config():
  return readData("hw-cpp/config.json")

@app.route('/hw-cpp/config', methods=['GET'])
def hw_cpp_config():
  return readData("hw-cpp/config.json")

app.run(host='0.0.0.0', port=30033)
