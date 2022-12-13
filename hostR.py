from flask import Flask, render_template, request
import vessel_math
from capture_ocr import capture_decoder
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/index/')
def hello():
    patient_instance.patient_name = request.form.get("fname")
    return render_template("index.html",
                            name=patient_instance.patient_name)

@app.route('/confirm_data/', methods=['POST'])
def confirm_data_response():
    num = request.form.get("num")
    patient_instance.value_holder(num)
    nu_value = capture_decoder()
    return render_template("index.html", 
                            name=patient_instance.patient_name, 
                            num=nu_value)

@app.route('/read_data/', methods=['POST'])
def read_data_response():
    nu_value = capture_decoder()
    return render_template("index.html", 
                            name=patient_instance.patient_name, 
                            num=nu_value)



if __name__ == '__main__':
    patient_instance = vessel_math.Vessel_math("")
    app.run(debug=True)