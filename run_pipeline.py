import subprocess
import sys


pipeline_steps = [
    ("Transform", "src/transform/clean_shop.py"),
    ("Load", "src/load/load_shop_sqlite.py"),
    ("Analytics", "src/analytics/analyze_shop.py"),
]


for step_name, script_path in pipeline_steps:
    print(f"\n{'=' * 50}")
    print(f"Running step: {step_name}")
    print(f"{'=' * 50}")

    subprocess.run(
        [sys.executable, script_path],
        check=True,
    )


print("\nPipeline completed successfully.")