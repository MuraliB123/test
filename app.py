import os
from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)

@app.route('/')
def index():
    report_available = os.path.exists('report.json')
    print(report_available)
    return render_template('form.html', report_available=report_available)

@app.route('/detect-drift', methods=['POST'])
def detect_drift():
    src_db_url = request.form['src_db_url']
    src_db_username = request.form['src_db_username']
    src_db_password = request.form['src_db_password']
    ref_db_url = request.form['ref_db_url']
    ref_db_username = request.form['ref_db_username']
    ref_db_password = request.form['ref_db_password']
    db_objects = request.form.getlist('db_objects') 

    db_objects_str = ','.join(db_objects)  

    # Construct the Liquibase diff command
    liquibase_command = (
        f'liquibase diff '
        f'--url="{src_db_url}" '
        f'--username="{src_db_username}" '
        f'--password="{src_db_password}" '
        f'--reference-url="{ref_db_url}" '
        f'--reference-username="{ref_db_username}" '
        f'--reference-password="{ref_db_password}" '
        f'--output-file="output.txt" '
        f'--diff-types="{db_objects_str}"'
    )

    
    print(liquibase_command)

    # os.system(liquibase_command)
    # or
    # import subprocess
    # subprocess.run(liquibase_command, shell=True)

    with open('report.json', 'w') as f:
        f.write('{"status": "success", "message": "Drift detected"}')
    
    report_available = os.path.exists('report.json')
    print(report_available)
    return render_template('form.html',report_available=report_available)

@app.route('/download-report')
def download_report():
    return send_file('report.json', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
