from flask import Flask, render_template, request, send_file
import subprocess
import os
import time

app = Flask(__name__, template_folder='templates')

@app.route('/')
def form():
    return render_template('main.html')

@app.route('/browse/')
def browse_certs():
    return render_template('browse.html', certs=get_certs_list())

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    try:
        return send_file("certificates/"+filename)
    except Exception as e:
        return str(e)

@app.route('/output/', methods = ['POST', 'GET'])
def output():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/' to submit form"
    if request.method == 'POST':
        form_output = request.form
        command = request.form.getlist("command")[0]
        p = subprocess.run([command], shell=True, capture_output=True)
        output = pretty_stdout(p.stdout)
        return render_template('output.html', form_output = form_output, output=output)
    
def pretty_stdout(stdout):
    out = stdout.decode("utf-8").split('\n') 
    return out

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
