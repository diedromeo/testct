from flask import Flask, request, send_file, render_template_string
import os

app = Flask(__name__)

DOCS_FOLDER = "docs"
FLAG_FILE = "flag.txt"

# Make sure docs folder exists
os.makedirs(DOCS_FOLDER, exist_ok=True)

# Create sample docs
with open(os.path.join(DOCS_FOLDER, "welcome.txt"), "w") as f:
    f.write("""==============================
Acme Corp - Employee Onboarding
==============================

Welcome to Acme Corp, a leader in innovative technology solutions.

This portal is designed to give employees secure access to internal documentation,
policies, and procedures.

Guidelines:
-----------
1. Use the Document Portal only for work-related files.
2. Do not attempt to access or modify system files.
3. Confidentiality is critical — sharing internal documents outside the company
   is strictly prohibited.
4. Report suspicious activity to the IT Security Team.

Note:
-----
All access is monitored for compliance with company security policies.
Unauthorized access to restricted files may result in disciplinary action.

For assistance, contact:
helpdesk@acmecorp.internal

Stay safe and secure!
- Acme Corp Security Team
""")

with open(os.path.join(DOCS_FOLDER, "secret.txt"), "w") as f:
    f.write("""==============================
Acme Corp - Confidential NDA
==============================

This document is classified. Sharing its content without written approval
from Acme Corp Legal Department is strictly prohibited.

All employees must agree to:
- Not disclose proprietary information
- Not share client data outside Acme Corp
- Not duplicate internal technical documentation

Breach of this NDA will result in immediate termination and legal action.

Document Ref: NDA-INT-2025
""")

# Create the flag file OUTSIDE docs folder
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
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                margin: 0;
                padding: 0;
            }
            header {
                background-color: #1a73e8;
                color: white;
                padding: 20px;
                text-align: center;
            }
            .container {
                max-width: 900px;
                margin: 40px auto;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                font-size: 24px;
                color: #333;
            }
            select, button {
                padding: 10px;
                margin-top: 10px;
                font-size: 14px;
                border-radius: 4px;
                border: 1px solid #ccc;
            }
            button {
                background-color: #1a73e8;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background-color: #1557b0;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>Acme Corp - Internal Document Viewer</h1>
        </header>
        <div class="container">
            <h1>Select a document to view</h1>
            <select id="docSelect">
                <option value="welcome.txt">Welcome Document</option>
                <option value="secret.txt">Confidential NDA</option>
            </select>
            <br>
            <button onclick="viewDoc()">View Document</button>
        </div>
        <script>
            function viewDoc() {
                const file = document.getElementById('docSelect').value;
                // Redirect so ?file= appears in browser URL
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

    # Block direct request to flag.txt
    if os.path.basename(file) == "flag.txt":
        return "<b>Access Denied:</b> Restricted file"

    try:
        # Check inside docs folder first
        file_path = os.path.join(DOCS_FOLDER, file)
        if os.path.exists(file_path):
            return send_file(file_path)

        # Intentionally vulnerable: allow path traversal
        return send_file(file)
    except Exception as e:
        return f"<b>Error:</b> {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
