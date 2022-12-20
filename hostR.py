from flask import Flask, render_template, request
import vessel_math
from capture_ocr import capture_decoder
app = Flask(__name__)


@app.route('/')
def home():
    patient_instance.__init__()
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/index/')
def hello():
    patient_instance.patient_name = request.form.get("fname")
    return render_template("index.html",
                            name=patient_instance.patient_name)

@app.route('/update_vessel', methods=['POST','GET'])
def change_current_vessel():  
    patient_instance.temp_vessel_tracker = patient_instance.vessels.index(request.form['vessel'])
    patient_instance.temp_discovered_value_holder = capture_decoder()
    return render_template("index.html", 
                            vessels = patient_instance.vessels,
                            name=patient_instance.patient_name, 
                            num=patient_instance.temp_discovered_value_holder)

@app.route('/confirm_data/', methods=['POST'])
def confirm_data_response():
    patient_instance.value_holder()
    patient_instance.temp_discovered_value_holder = capture_decoder()
    return render_template("index.html", 
                            vessels = patient_instance.vessels,
                            name = patient_instance.patient_name, 
                            num = patient_instance.temp_discovered_value_holder)

@app.route('/read_data/', methods=['POST'])
def read_data_response():
    if patient_instance.patient_name == "":
        patient_instance.patient_name = request.form.get("fname")
    patient_instance.temp_discovered_value_holder = capture_decoder()
    return render_template("index.html", 
                            vessels = patient_instance.vessels,
                            name = patient_instance.patient_name, 
                            num = patient_instance.temp_discovered_value_holder)

@app.route('/print_data/', )
def print_data():
    patient_instance.bvg_2_csv_file()
    return render_template("index.html", 
                            name=patient_instance.patient_name)

if __name__ == '__main__':
    patient_instance = vessel_math.Vessel_math()
    app.run(debug=True)