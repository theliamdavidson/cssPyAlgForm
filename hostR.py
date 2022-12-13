from flask import Flask, render_template, request
import vessel_math
from capture_ocr import capture_decoder
import logging
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/index/')
def hello():
    fname = request.form.get("fname")
    return render_template("index.html",
                            name=fname)

@app.route('/confirm_data/', methods=['POST'])
def confirm_data_response():
    fname = request.form.get("fname")
    num = request.form.get("num")
    patient_instance.value_holder(num)
    nu_value = capture_decoder()
    for values in nu_value:
        try:
            float(values) + 1.0
            return render_template("index.html", 
                            name=fname, 
                            num=nu_value)
        except TypeError:
            logging.info("not the value %s", values)
    return render_template("index.html", 
                            name=fname, 
                            num=nu_value)

@app.route('/read_data/', methods=['POST'])
def read_data_response():
    fname = request.form.get("fname")
    nu_value = capture_decoder()
    for slices, values in enumerate(nu_value):
        try:
            float(nu_value[slices]) + 1.0
            return render_template("index.html", 
                            name=fname, 
                            num=nu_value[slices])
        except:
            logging.info("not the value %s", values)
    return render_template("index.html", 
                            name=fname, 
                            num=nu_value)



if __name__ == '__main__':
    patient_instance = vessel_math.Vessel_math("DavidsonLiam")
    app.run(debug=True)