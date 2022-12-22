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
    try:
        selected_vessel = patient_instance.vessels[patient_instance.temp_vessel_tracker]
        vessel_index = patient_instance.temp_vessel_tracker
    except:
        vessel_index = patient_instance.temp_vessel_tracker - 1
        selected_vessel = patient_instance.vessels[vessel_index]
    return render_template("index.html", 
                            selected_vessel = selected_vessel,
                            vessels = patient_instance.vessels,
                            name = patient_instance.patient_name, 
                            num = patient_instance.temp_discovered_value_holder, 
                            current_vessel_values = patient_instance.vessel_values[vessel_index][1])

@app.route('/confirm_data/', methods=['POST'])
def confirm_data_response():
    patient_instance.value_holder()         #this is where it broke
    patient_instance.temp_discovered_value_holder = capture_decoder()
    try:
        selected_vessel = patient_instance.vessels[patient_instance.temp_vessel_tracker]
        vessel_index = patient_instance.temp_vessel_tracker
    except:
        vessel_index = patient_instance.temp_vessel_tracker - 1
        selected_vessel = patient_instance.vessels[vessel_index]
    return render_template("index.html", 
                            selected_vessel = selected_vessel,
                            vessels = patient_instance.vessels,
                            name = patient_instance.patient_name, 
                            num = patient_instance.temp_discovered_value_holder, 
                            current_vessel_values = patient_instance.vessel_values[vessel_index][1])

@app.route('/read_data/', methods=['POST'])
def read_data_response():
    if patient_instance.patient_name == "":
        patient_instance.patient_name = request.form.get("fname")
    patient_instance.temp_discovered_value_holder = capture_decoder()
    try:
        selected_vessel = patient_instance.vessels[patient_instance.temp_vessel_tracker]
        vessel_index = patient_instance.temp_vessel_tracker
    except:
        vessel_index = patient_instance.temp_vessel_tracker - 1
        selected_vessel = patient_instance.vessels[vessel_index]
    return render_template("index.html", 
                            selected_vessel = selected_vessel,
                            vessels = patient_instance.vessels,
                            name = patient_instance.patient_name, 
                            num = patient_instance.temp_discovered_value_holder, 
                            current_vessel_values = patient_instance.vessel_values[vessel_index][1])

@app.route('/results/', methods=['GET','POST'])
def results():
    patient_instance.macro_vessel_calculations()
    return render_template("results.html", 
                            macro_vessel_values = patient_instance.macro_vessel_results, 
                            name=patient_instance.patient_name)

@app.route('/print_data/', methods=['GET','POST'])
def print_data():
    patient_instance.bvg_2_csv_file()
    return render_template("index.html", 
                            name=patient_instance.patient_name)

if __name__ == '__main__':
    patient_instance = vessel_math.Vessel_math()
    app.run(debug=True)