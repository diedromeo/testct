from flask import Flask, request, send_file, render_template_string
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_FOLDER = os.path.join(BASE_DIR, "docs")
FLAG_FILE = os.path.join(BASE_DIR, "flag.txt")

os.makedirs(DOCS_FOLDER, exist_ok=True)

# Sample docs
if not os.path.exists(os.path.join(DOCS_FOLDER, "welcome.txt")):
    with open(os.path.join(DOCS_FOLDER, "welcome.txt"), "w") as f:
        f.write("Welcome to Acme Corp - Employee Onboarding")

if not os.path.exists(os.path.join(DOCS_FOLDER, "secret.txt")):
    with open(os.path.join(DOCS_FOLDER, "secret.txt"), "w") as f:
        f.write("Acme Corp - Confidential NDA")

# Flag outside docs
if not os.path.exists(FLAG_FILE):
    with open(FLAG_FILE, "w") as f:
        f.write("ctf7{path_traversal_master}")

@app.route("/")
def index():
    return render_template_string("""
    <h1>Acme Corp - Internal Document Viewer</h1>
    <select id="docSelect">
        <option value="welcome.txt">Welcome Document</option>
        <option value="secret.txt">Confidential NDA</option>
    </select>
    <button onclick="viewDoc()">View Document</button>
    <script>
        function viewDoc() {
            const file = document.getElementById('docSelect').value;
            window.location.href = '/view?file=' + encodeURIComponent(file);
        }
    </script>
    """)

@app.route("/view")
def view_file():
    file = request.args.get("file", "")

    # Block direct flag access
    if os.path.basename(file) == "flag.txt":
        return "<b>Access Denied:</b> Restricted file"

    # Special fake traversal mapping
    if file.replace("\\", "/").endswith("../../../flag.txt"):
        return send_file(FLAG_FILE)

    # Serve from docs folder normally
    safe_path = os.path.join(DOCS_FOLDER, file)
    if os.path.exists(safe_path):
        return send_file(safe_path)

    return "<b>Error:</b> File not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
