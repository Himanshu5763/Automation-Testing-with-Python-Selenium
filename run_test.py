import os
import sys
import subprocess
import webbrowser

def get_base_path():
    """Returns the base path depending on whether it's running as a script or executable."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.dirname(__file__))

def run_behave_tests():
    base_path = get_base_path()
    project_root = os.path.abspath(os.path.join(base_path, ".."))  # Moves one level up from dist

    # Adjust paths to point outside dist
    artifacts_path = os.path.join(project_root, "test_artifacts")
    results_dir = os.path.join(artifacts_path, "results")
    features_dir = os.path.join(project_root, "features")  # Ensure features are outside dist
    steps_dir = os.path.join(project_root, "steps")        # Ensure steps are outside dist

    print(f"🔍 Running Behave tests in: {features_dir}")
    print(f"📁 Storing results in: {results_dir}")

    os.makedirs(results_dir, exist_ok=True)

    env = os.environ.copy()
    env['PYTHONPATH'] = os.pathsep.join([
        base_path,
        os.path.join(base_path, "utilities"),
        os.path.join(base_path, "configurations"),
        steps_dir  # Add steps directory to PYTHONPATH
    ])

    # Ensure Behave runs from the correct directory
    subprocess.run([
        "behave",
        "-f", "allure_behave.formatter:AllureFormatter",
        "-o", results_dir,
        "features"  # Ensure this is relative to project_root, not dist
    ], check=True, env=env, cwd=project_root)  # Set cwd to project_root

def generate_allure_report():
    allure_bat = r"C:\Program Files\allure-2.32.0\bin\allure.bat"
    base_path = get_base_path()
    project_root = os.path.abspath(os.path.join(base_path, ".."))
    
    artifacts_path = os.path.join(project_root, "test_artifacts")
    results_dir = os.path.join(artifacts_path, "results")
    report_dir = os.path.join(artifacts_path, "allure-report")

    print("📊 Generating Allure report...")

    os.makedirs(report_dir, exist_ok=True)

    subprocess.run([
        allure_bat,
        "generate", results_dir,
        "--clean",
        "--single-file",
        "-o", report_dir
    ], check=True)

    report_file = os.path.abspath(os.path.join(report_dir, "index.html"))
    print(f"✅ Report generated at: {report_file}")
    webbrowser.open(f"file:///{report_file}")

def main():
    run_behave_tests()
    generate_allure_report()
    print("🎉 Tests completed. Allure report is now open.")
    print("📦 All results and reports are saved in 'test_artifacts' folder outside of dist.")

if __name__ == "__main__":
    main()
