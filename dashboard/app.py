import os
import json
import sys
from flask import Flask, render_template, request, jsonify

# Add project root to path to import config
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
import config

app = Flask(__name__)

SCANS_DIR = config.SCANS_PATH

@app.route('/')
def index():
    scans = []
    if os.path.exists(SCANS_DIR):
        for filename in os.listdir(SCANS_DIR):
            if filename.endswith(".json"):
                # info_HOST.json
                # info_exploitation_scan_HOST.json
                host = filename.replace(".json", "")
                type_ = "Service Scan"
                if "exploitation" in filename:
                    type_ = "Exploitation Scan"
                    host = host.replace("info_exploitation_scan_", "")
                else:
                    host = host.replace("info_", "")

                filepath = os.path.join(SCANS_DIR, filename)
                try:
                    with open(filepath) as f:
                        data = json.load(f)
                        scans.append({
                            "filename": filename,
                            "host": host,
                            "type": type_,
                            # Add timestamp if file stat?
                            "timestamp": os.path.getmtime(filepath)
                        })
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    pass

    # Sort by timestamp desc
    scans.sort(key=lambda x: x["timestamp"], reverse=True)
    return render_template('index.html', scans=scans)

@app.route('/scan/<filename>')
def view_scan(filename):
    # Security check to prevent path traversal
    if ".." in filename or "/" in filename:
         return "Invalid filename", 400

    filepath = os.path.join(SCANS_DIR, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath) as f:
                data = json.load(f)
            return render_template('scan.html', data=data, filename=filename)
        except Exception as e:
            return f"Error reading file: {e}", 500
    return "Scan not found", 404

if __name__ == '__main__':
    print(f"Starting dashboard. Scans directory: {SCANS_DIR}")
    # Disable debug mode for production/submission
    app.run(host='0.0.0.0', port=5000, debug=False)
