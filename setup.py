from os import environ
import subprocess

# This file just runs commands in the shell to update and download all dependencies
if "REPL_ID" not in environ:
    subprocess.run(["pip", "install", "-U", "pip"])
    subprocess.run(["pip", "install", "poetry"])
    subprocess.run(["poetry", "shell"])
    subprocess.run(["poetry", "check"])
subprocess.run(["git", "submodule", "update", "--init", "--recursive"])  
print("Setup Complete")