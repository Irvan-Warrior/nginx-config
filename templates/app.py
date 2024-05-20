from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    dnsname = request.form['dnsname']
    ipaddress = request.form['ipaddress']
    port = request.form['port']

    with open('nginx/sites-available/mysite.template.conf', 'r') as template_file:
        config_content = template_file.read()
        config_content = config_content.replace('{{ dnsname }}', dnsname)
        config_content = config_content.replace('{{ ipaddress }}', ipaddress)
        config_content = config_content.replace('{{ port }}', port)

    config_path = f'nginx/sites-available/{dnsname}.conf'
    with open(config_path, 'w') as config_file:
        config_file.write(config_content)

    # Trigger deployment
    os.system(f'bash scripts/deploy.sh {dnsname}.conf')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
