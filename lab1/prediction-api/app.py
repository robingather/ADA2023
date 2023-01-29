from flask import Flask, request

from diabetes_predictor import DiabetesPredictor

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/diabetes_predictor/', methods=['POST']) # path of the endpoint. Except only HTTP POST request
def predict_str():
    # the prediction input data in the message body as a JSON payload
    prediction_inout = request.get_json()
    return dp.predict_single_record(prediction_inout)


dp = DiabetesPredictor()
app.run(host='0.0.0.0', port=5000)
