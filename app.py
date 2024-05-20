from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    dnsname = request.form['dnsname']
    ipaddress = request.form['ipaddress']
    port = request.form['port']
    
    # Lakukan apa yang Anda butuhkan dengan nilai-nilai ini
    # Misalnya, simpan ke dalam file atau kirim ke server

    return "Configuration updated successfully!"

if __name__ == '__main__':
    app.run(debug=True)
