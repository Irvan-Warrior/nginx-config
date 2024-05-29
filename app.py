from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        dns_name = request.form['dns_name']
        ip_address = request.form['ip_address']
        port = request.form['port']

        template_path = 'nginx/sites-available/mysite.template.conf'
        output_path = f'nginx/sites-available/{dns_name}.conf'

        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        output_content = template_content.replace('$dnsname', dns_name).replace('$ipaddress', ip_address).replace('$port', port)

        with open(output_path, 'w') as output_file:
            output_file.write(output_content)
        
        symlink_path = f'nginx/sites-enabled/{dns_name}.conf'
        if os.path.islink(symlink_path) or os.path.exists(symlink_path):
            os.remove(symlink_path)
        os.symlink(os.path.abspath(output_path), os.path.abspath(symlink_path))

        return f'Configuration for {dns_name} generated successfully!'
    except KeyError as e:
        return f'Missing form field: {e}', 400
    except FileNotFoundError:
        return f'Error: Template file not found at {template_path}', 404
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
