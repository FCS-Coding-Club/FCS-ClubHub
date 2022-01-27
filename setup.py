import subprocess

# This file just runs commands in the shell to update and download all dependencies
subprocess.run(["pip", "install", "-U", "pip"])
subprocess.run(["pip", "install", "poetry"])
subprocess.run(["poetry", "shell"])
subprocess.run(["poetry", "install"])
subprocess.run(["git", "submodule", "update", "--init", "--recursive"])  
print("Setup Complete")