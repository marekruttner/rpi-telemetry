import os
import subprocess
import threading
import time
import random
import argparse

# Path to the cloned repository
EXAMPLES_PATH = os.path.expanduser("~/hailo-rpi5-examples")

# List of available demos and their arguments
AVAILABLE_DEMOS = {
    "Object Detection": [
        "python3",
        f"{EXAMPLES_PATH}/basic_pipelines/detection.py"
    ],
    "Pose Estimation": [
        "python3",
        f"{EXAMPLES_PATH}/basic_pipelines/pose_estimation.py"
    ],
    "Instance Segmentation": [
        "python3",
        f"{EXAMPLES_PATH}/basic_pipelines/instance_segmentation.py"
    ],
    "Object Detection USB": [
        "python3",
        f"{EXAMPLES_PATH}/basic_pipelines/detection.py",
        "--input", "dev/video8"  # Replace with actual input source
    ],
    "Pose Estimation USB": [
        "python3",
        f"{EXAMPLES_PATH}/basic_pipelines/pose_estimation.py",
        "--input", "dev/video8"  # Replace with actual input source
    ],
    "Instance Segmentation USB": [
        "python3",
        f"{EXAMPLES_PATH}/basic_pipelines/instance_segmentation.py",
        "--input", "dev/video8"  # Replace with actual input source
    ],
    # Add more demos as needed
}

def run_random_demo(selected_demos, min_interval, max_interval):
    """Select and execute a random demo at a random interval."""
    while True:
        # Choose a random demo from selected demos
        demo_script = random.choice(selected_demos)
        demo_args = AVAILABLE_DEMOS[demo_script]
        demo_name = os.path.basename(demo_script)

        print(f"Running demo: {demo_name}")

        try:
            # Run the selected demo
            result = subprocess.run(
                demo_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"{demo_name} Output:", result.stdout)
            if result.stderr:
                print(f"{demo_name} Error:", result.stderr)
        except Exception as e:
            print(f"Error during {demo_name} execution:", e)

        # Wait for a random interval before running the next demo
        sleep_time = random.randint(min_interval, max_interval)
        print(f"Waiting {sleep_time} seconds before running the next demo.")
        time.sleep(sleep_time)

def start_random_demos(num_threads, selected_demos, min_interval, max_interval):
    """Run multiple instances of random demos."""
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=run_random_demo, args=(selected_demos, min_interval, max_interval))
        t.daemon = True
        t.start()
        threads.append(t)

    # Keep the main thread alive
    while True:
        time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stress Test with Hailo AI Demos')
    parser.add_argument('--num_threads', type=int, default=2, help='Number of parallel demo runners')
    parser.add_argument('--demos', nargs='+', choices=list(AVAILABLE_DEMOS.keys()), default=list(AVAILABLE_DEMOS.keys()), help='List of demos to run')
    parser.add_argument('--min_interval', type=int, default=10, help='Minimum interval between demos in seconds')
    parser.add_argument('--max_interval', type=int, default=30, help='Maximum interval between demos in seconds')
    args = parser.parse_args()

    selected_demos = args.demos
    start_random_demos(args.num_threads, selected_demos, args.min_interval, args.max_interval)