from flask import Flask, render_template, request
import vessel_math
import capture_ocr
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
    return render_template("index.html")

@app.route('/confirm_data/', methods=['POST'])
def response():
    fname = request.form.get("fname")
    num = request.form.get("num")
    patient_instance.value_holder(num)
    nu_value = capture_ocr.capture_decoder()
    return render_template("index.html", 
                            name=fname, 
                            num=nu_value)
@app.route('/read_data/', methods=['POST'])
def response():
    fname = request.form.get("fname")
    nu_value = capture_ocr.capture_decoder()
    return render_template("index.html", 
                            name=fname, 
                            num=nu_value)



if __name__ == '__main__':
    patient_instance = vessel_math.Vessel_math("DavidsonLiam")
    app.run(debug=True)