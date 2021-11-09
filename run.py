import os
from app import create_app
# Debug Checking
if os.environ.get('DEBUG') is None:
    os.environ["DEBUG"] = "True"
if os.environ.get('TESTING') is None:
    os.environ["TESTING"] = "False"

if os.environ.get('TESTING') == "False":
    app = create_app()
    app.run(host="0.0.0.0", port=3000, debug=os.environ["DEBUG"])
else:
    print("TESTING flag set to not False, cannot run.")