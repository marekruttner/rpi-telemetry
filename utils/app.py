from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly
import plotly.express as px
import json
import subprocess
import os

app = Flask(__name__, template_folder='templates')

# Define DEMO_ARGS first
EXAMPLES_PATH = os.path.expanduser("~/hailo-rpi5-examples")

DEMO_ARGS = {
    "Object Detection": f"{EXAMPLES_PATH}/basic_pipelines/detection.py",
    "Pose Estimation": f"{EXAMPLES_PATH}/basic_pipelines/pose_estimation.py",
    "Instance Segmentation": f"{EXAMPLES_PATH}/basic_pipelines/instance_segmentation.py",
    # Add more demos as needed
}

# Global variable to keep track of the stress test process
stress_test_process = None

# Initialize stress_test_options after DEMO_ARGS is defined
stress_test_options = {
    'num_threads': 2,
    'demos': list(DEMO_ARGS.keys()),
    'min_interval': 10,
    'max_interval': 30,
}

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

    return render_template(
        'index.html',
        graphs=graphs,
        stress_test_running=stress_test_running,
        stress_test_options=stress_test_options,
        available_demos=DEMO_ARGS
    )

@app.route('/start_stress_test', methods=['POST'])
def start_stress_test():
    global stress_test_process, stress_test_options
    if stress_test_process is None or stress_test_process.poll() is not None:
        # Get options from form
        num_threads = int(request.form.get('num_threads', 2))
        selected_demos = request.form.getlist('demos')
        min_interval = int(request.form.get('min_interval', 10))
        max_interval = int(request.form.get('max_interval', 30))

        # Update stress test options
        stress_test_options = {
            'num_threads': num_threads,
            'demos': selected_demos,
            'min_interval': min_interval,
            'max_interval': max_interval,
        }

        # Build command to start stress_test.py with arguments
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stress_test.py')
        cmd = ['python3', script_path,
               '--num_threads', str(num_threads),
               '--min_interval', str(min_interval),
               '--max_interval', str(max_interval)]
        for demo in selected_demos:
            cmd.extend(['--demos', demo])

        # Start the stress test process
        stress_test_process = subprocess.Popen(cmd, cwd=os.path.dirname(script_path))
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
