from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly
import plotly.express as px
import json
import subprocess
import os

app = Flask(__name__, template_folder='templates')

# Global variable to keep track of the stress test process
stress_test_process = None

@app.route('/')
def index():
    # Read the telemetry data
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'telemetry_log.csv')
    df = pd.read_csv(log_file)

    # Ensure the Timestamp is in datetime format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Generate graphs
    fig_cpu = px.line(df, x='Timestamp', y='CPU_Usage', title='CPU Usage Over Time')
    fig_temp = px.line(df, x='Timestamp', y='CPU_Temp', title='CPU Temperature Over Time')
    fig_ram = px.line(df, x='Timestamp', y='RAM_Usage', title='RAM Usage Over Time')
    fig_proc = px.line(df, x='Timestamp', y='Processes', title='Number of Running Processes Over Time')

    # Convert figures to JSON
    graphs = {
        'cpu': json.dumps(fig_cpu, cls=plotly.utils.PlotlyJSONEncoder),
        'temp': json.dumps(fig_temp, cls=plotly.utils.PlotlyJSONEncoder),
        'ram': json.dumps(fig_ram, cls=plotly.utils.PlotlyJSONEncoder),
        'proc': json.dumps(fig_proc, cls=plotly.utils.PlotlyJSONEncoder)
    }

    # Check if stress test is running
    stress_test_running = stress_test_process is not None and stress_test_process.poll() is None

    return render_template('index.html', graphs=graphs, stress_test_running=stress_test_running)

@app.route('/start_stress_test', methods=['POST'])
def start_stress_test():
    global stress_test_process
    if stress_test_process is None or stress_test_process.poll() is not None:
        # Start the stress test process
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stress_test.py')
        stress_test_process = subprocess.Popen(['python', script_path], cwd=os.path.dirname(script_path))
    return redirect(url_for('index'))

@app.route('/stop_stress_test', methods=['POST'])
def stop_stress_test():
    global stress_test_process
    if stress_test_process is not None and stress_test_process.poll() is None:
        # Terminate the stress test process
        stress_test_process.terminate()
        stress_test_process.wait()
        stress_test_process = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
