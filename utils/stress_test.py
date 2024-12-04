import os
import subprocess
import threading
import time
import random

# Paths to cloned repositories
MODEL_ZOO_PATH = os.path.expanduser("~/hailo_model_zoo")
EXAMPLES_PATH = os.path.expanduser("~/hailo-rpi5-examples")

# List of available demos and scripts
AVAILABLE_DEMOS = [
    f"{EXAMPLES_PATH}/object_detection_demo.py",
    f"{EXAMPLES_PATH}/classification_demo.py",
    f"{MODEL_ZOO_PATH}/eval_scripts/eval_image.py",
    f"{MODEL_ZOO_PATH}/eval_scripts/eval_video.py",
]

# List of arguments for each demo
DEMO_ARGS = {
    f"{EXAMPLES_PATH}/object_detection_demo.py": ["python", f"{EXAMPLES_PATH}/object_detection_demo.py"],
    f"{EXAMPLES_PATH}/classification_demo.py": ["python", f"{EXAMPLES_PATH}/classification_demo.py"],
    f"{MODEL_ZOO_PATH}/eval_scripts/eval_image.py": [
        "python",
        f"{MODEL_ZOO_PATH}/eval_scripts/eval_image.py",
        "--model", "yolov5s",  # Example model name
        "--target", "hailo",
        "--image", "path_to_test_image.jpg",  # Replace with actual image path
    ],
    f"{MODEL_ZOO_PATH}/eval_scripts/eval_video.py": [
        "python",
        f"{MODEL_ZOO_PATH}/eval_scripts/eval_video.py",
        "--model", "mobilenetv2",  # Example model name
        "--target", "hailo",
        "--video", "path_to_test_video.mp4",  # Replace with actual video path
    ],
}


def run_random_demo():
    """Select and execute a random demo at a random interval."""
    while True:
        # Choose a random demo
        demo_script = random.choice(AVAILABLE_DEMOS)
        demo_args = DEMO_ARGS[demo_script]

        print(f"Running demo: {demo_script}")

        try:
            # Run the selected demo
            result = subprocess.run(
                demo_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("Demo Output:", result.stdout)
            if result.stderr:
                print("Demo Error:", result.stderr)
        except Exception as e:
            print("Error during demo execution:", e)

        # Wait for a random interval before running the next demo
        sleep_time = random.randint(10, 30)  # Wait between 10 to 30 seconds
        print(f"Waiting {sleep_time} seconds before running the next demo.")
        time.sleep(sleep_time)


def start_random_demos():
    """Run multiple instances of random demos."""
    threads = []
    num_threads = 3  # Number of parallel demo runners
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
