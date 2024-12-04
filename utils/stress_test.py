import os
import subprocess
import threading
import time
import random

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

def run_random_demo():
    """Select and execute a random demo at a random interval."""
    while True:
        # Choose a random demo
        demo_name, demo_args = random.choice(list(AVAILABLE_DEMOS.items()))

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
        sleep_time = random.randint(10, 30)  # Wait between 10 to 30 seconds
        print(f"Waiting {sleep_time} seconds before running the next demo.")
        time.sleep(sleep_time)

def start_random_demos():
    """Run multiple instances of random demos."""
    threads = []
    num_threads = 2  # Number of parallel demo runners
    for _ in range(num_threads):
        t = threading.Thread(target=run_random_demo)
        t.daemon = True
        t.start()
        threads.append(t)

    # Keep the main thread alive
    while True:
        time.sleep(1)

if __name__ == '__main__':
    start_random_demos()
