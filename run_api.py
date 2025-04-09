import subprocess

subprocess.run(["python", "-m", "uvicorn", "api.main:app", "--reload"])
