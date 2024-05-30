from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    dns_name = request.form['dns_name']
    ip_address = request.form['ip_address']
    port = request.form['port']
    commit_message = request.form['commit_message']
    action = request.form['action']

    template_path = 'nginx/sites-available/mysite.template.conf'
    output_path = f'nginx/sites-available/{dns_name}.conf'

    # Membaca template dan mengganti placeholder
    with open(template_path, 'r') as template_file:
        config_content = template_file.read()
    
    config_content = config_content.replace('$dnsname', dns_name)
    config_content = config_content.replace('$ipaddress', ip_address)
    config_content = config_content.replace('$port', port)

    # Menulis konfigurasi baru ke file
    with open(output_path, 'w') as output_file:
        output_file.write(config_content)

    # Jika tombol "Generate and Push" ditekan, lakukan git commit dan push
    if action == "Generate and Push":
        os.system('git add .')
        os.system(f'git commit -m "{commit_message}"')
        os.system('git push origin main')

    return f'Config for {dns_name} generated successfully!'

if __name__ == '__main__':
    app.run(debug=True)
