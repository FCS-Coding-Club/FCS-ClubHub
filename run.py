import os
from app import app
# Debug Checking
if os.environ.get('DEBUG') is None:
    os.environ["DEBUG"] = "True"
# TODO: Unit Testing?

# Run App
app.run(host="0.0.0.0", port=5000, debug=os.environ["DEBUG"])
