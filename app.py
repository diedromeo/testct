from flask import Flask, request, send_file, render_template_string
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # project base path
DOCS_FOLDER = os.path.join(BASE_DIR, "docs")
FLAG_FILE = os.path.join(BASE_DIR, "flag.txt")

# Ensure docs folder exists
os.makedirs(DOCS_FOLDER, exist_ok=True)

# Create sample docs if not already there
if not os.path.exists(os.path.join(DOCS_FOLDER, "welcome.txt")):
    with open(os.path.join(DOCS_FOLDER, "welcome.txt"), "w") as f:
        f.write("""==============================
Acme Corp - Employee Onboarding
==============================

Welcome to Acme Corp, a leader in innovative technology solutions.

This portal is designed to give employees secure access to internal documentation,
policies, and procedures.""")

if not os.path.exists(os.path.join(DOCS_FOLDER, "secret.txt")):
    with open(os.path.join(DOCS_FOLDER, "secret.txt"), "w") as f:
        f.write("""==============================
Acme Corp - Confidential NDA
==============================

This document is classified. Sharing its content without written approval
is strictly prohibited.""")

# Create the flag file outside docs folder
if not os.path.exists(FLAG_FILE):
    with open(FLAG_FILE, "w") as f:
        f.write("ctf7{path_traversal_master}")

@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Acme Corp - Document Portal</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #eef1f5; margin: 0; padding: 0; }
            header { background-color: #004085; color: white; padding: 20px; text-align: center; }
            .container { max-width: 900px; margin: 40px auto; background: white; padding: 30px; border-radius: 8px;
                         box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
            h1 { color: #004085; }
            select, button { padding: 10px; font-size: 14px; border-radius: 4px; border: 1px solid #ccc; margin-top: 10px; }
            button { background-color: #004085; color: white; cursor: pointer; }
            button:hover { background-color: #002752; }
            footer { text-align: center; font-size: 12px; color: #777; margin-top: 20px; }
        </style>
    </head>
    <body>
        <header>
            <h1>Acme Corp - Internal Document Viewer</h1>
        </header>
        <div class="container">
            <h1>Available Internal Documents</h1>
            <p>Please select a document to view. All access is monitored for compliance.</p>
            <select id="docSelect">
                <option value="welcome.txt">Welcome Document</option>
                <option value="secret.txt">Confidential NDA</option>
            </select>
            <br>
            <button onclick="viewDoc()">View Document</button>
        </div>
        <footer>
            &copy; 2025 Acme Corp - Internal Systems Division
        </footer>
        <script>
            function viewDoc() {
                const file = document.getElementById('docSelect').value;
                window.location.href = '/view?file=' + encodeURIComponent(file);
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/view")
def view_file():
    file = request.args.get("file", "")

    # Block direct access to flag.txt
    if os.path.basename(file) == "flag.txt":
        return "<b>Access Denied:</b> Restricted file"

    try:
        # Vulnerable logic: start in docs folder, allow traversal
        target_path = os.path.abspath(os.path.join(DOCS_FOLDER, file))

        # Allow any file that exists (even outside docs)
        if os.path.exists(target_path):
            return send_file(target_path)

        return "<b>Error:</b> File not found"
    except Exception as e:
        return f"<b>Error:</b> {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
