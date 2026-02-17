from flask import Flask, request, render_template_string
from flask_mail import Mail, Message
from Topsis_Ishita_102317254.topsis import topsis
import os
import sys
sys.path.append(os.path.abspath(".."))
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASS")
app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]
print("MAIL_USERNAME =", app.config["MAIL_USERNAME"])



mail = Mail(app)


HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>TOPSIS Web Service</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100vh;
      background: #0f1117;
      display: flex; align-items: center; justify-content: center;
      font-family: 'Segoe UI', system-ui, sans-serif;
      color: #e2e8f0; padding: 2rem;
    }
    .card {
      background: #1a1d27; border: 1px solid #2d3148;
      border-radius: 16px; padding: 2.5rem;
      width: 100%; max-width: 500px;
      box-shadow: 0 25px 60px rgba(0,0,0,0.5);
    }
    .header { text-align: center; margin-bottom: 2rem; }
    .badge {
      display: inline-block;
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      color: white; font-size: 0.7rem; font-weight: 700;
      letter-spacing: 0.12em; text-transform: uppercase;
      padding: 0.3rem 0.85rem; border-radius: 999px; margin-bottom: 1rem;
    }
    h1 { font-size: 1.75rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.4rem; }
    .subtitle { font-size: 0.875rem; color: #64748b; }
    .divider { height: 1px; background: #2d3148; margin: 1.75rem 0; }
    .form-group { margin-bottom: 1.25rem; }
    label {
      display: block; font-size: 0.8rem; font-weight: 600; color: #94a3b8;
      letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.5rem;
    }
    .hint { font-size: 0.75rem; color: #475569; margin-top: 0.35rem; }
    input[type="text"], input[type="email"] {
      width: 100%; background: #0f1117; border: 1px solid #2d3148;
      border-radius: 8px; padding: 0.65rem 0.9rem;
      font-size: 0.9rem; color: #e2e8f0; outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    input[type="text"]:focus, input[type="email"]:focus {
      border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
    }
    input::placeholder { color: #3d4460; }
    .file-drop {
      position: relative; border: 2px dashed #2d3148; border-radius: 10px;
      padding: 2rem 1rem; text-align: center; cursor: pointer;
      transition: border-color 0.2s, background 0.2s;
    }
    .file-drop:hover, .file-drop.dragover {
      border-color: #6366f1; background: rgba(99,102,241,0.05);
    }
    .file-drop input[type="file"] {
      position: absolute; inset: 0; opacity: 0;
      cursor: pointer; width: 100%; height: 100%;
    }
    .file-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
    .file-drop-text { font-size: 0.85rem; color: #64748b; }
    .file-drop-text span { color: #818cf8; font-weight: 600; }
    .file-name { margin-top: 0.5rem; font-size: 0.8rem; color: #6366f1; font-weight: 600; display: none; }
    button[type="submit"] {
      width: 100%; padding: 0.8rem;
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      border: none; border-radius: 8px; color: white;
      font-size: 0.95rem; font-weight: 600; cursor: pointer;
      margin-top: 0.5rem; transition: opacity 0.2s, transform 0.15s;
    }
    button[type="submit"]:hover { opacity: 0.9; transform: translateY(-1px); }
    .footer-note { text-align: center; margin-top: 1.5rem; font-size: 0.75rem; color: #334155; }
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="badge">Decision Analysis</div>
      <h1>TOPSIS</h1>
      <p class="subtitle">Technique for Order of Preference by Similarity to Ideal Solution</p>
    </div>
    <div class="divider"></div>
    <form action="/topsis" method="post" enctype="multipart/form-data">
      <div class="form-group">
        <label>Dataset (CSV)</label>
        <div class="file-drop" id="fileDrop">
          <input type="file" name="file" accept=".csv" required id="fileInput"/>
          <div class="file-icon">📂</div>
          <div class="file-drop-text"><span>Choose file</span> or drag & drop</div>
          <div class="file-name" id="fileName"></div>
        </div>
        <p class="hint">CSV with alternatives as rows. First column = name, rest = criteria.</p>
      </div>
      <div class="form-group">
        <label>Weights</label>
        <input type="text" name="weights" placeholder="e.g. 1,1,2,1" required />
        <p class="hint">Comma-separated numeric weights for each criterion.</p>
      </div>
      <div class="form-group">
        <label>Impacts</label>
        <input type="text" name="impacts" placeholder="e.g. +,+,-,+" required />
        <p class="hint">Use <code style="color:#818cf8">+</code> (higher is better) or <code style="color:#818cf8">-</code> (lower is better) per criterion.</p>
      </div>
      <div class="form-group">
        <label>Email</label>
        <input type="email" name="email" placeholder="you@example.com" required />
        <p class="hint">Results will be sent to this address as a CSV attachment.</p>
      </div>
      <button type="submit">Run TOPSIS &rarr;</button>
    </form>
    <p class="footer-note">Results are processed server-side and emailed directly to you.</p>
  </div>
  <script>
    const input = document.getElementById('fileInput');
    const label = document.getElementById('fileName');
    const drop  = document.getElementById('fileDrop');
    input.addEventListener('change', () => {
      if (input.files.length) { label.textContent = '✓ ' + input.files[0].name; label.style.display = 'block'; }
    });
    drop.addEventListener('dragover', e => { e.preventDefault(); drop.classList.add('dragover'); });
    drop.addEventListener('dragleave', () => drop.classList.remove('dragover'));
    drop.addEventListener('drop', e => {
      e.preventDefault(); drop.classList.remove('dragover');
      if (e.dataTransfer.files.length) {
        input.files = e.dataTransfer.files;
        label.textContent = '✓ ' + e.dataTransfer.files[0].name; label.style.display = 'block';
      }
    });
  </script>
</body>
</html>
"""

SUCCESS_HTML = """
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/><title>Result Sent</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{min-height:100vh;background:#0f1117;display:flex;align-items:center;justify-content:center;font-family:'Segoe UI',system-ui,sans-serif;color:#e2e8f0}
  .card{background:#1a1d27;border:1px solid #2d3148;border-radius:16px;padding:3rem 2.5rem;max-width:420px;width:90%;text-align:center;box-shadow:0 25px 60px rgba(0,0,0,.5)}
  .icon{font-size:3rem;margin-bottom:1.25rem}
  h2{font-size:1.5rem;font-weight:700;color:#f1f5f9;margin-bottom:.6rem}
  p{font-size:.9rem;color:#64748b;margin-bottom:2rem}
  a{display:inline-block;padding:.7rem 2rem;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:8px;color:white;font-weight:600;font-size:.9rem;text-decoration:none;transition:opacity .2s}
  a:hover{opacity:.88}
</style></head>
<body><div class="card">
  <div class="icon">✅</div>
  <h2>Results Sent!</h2>
  <p>Your TOPSIS analysis is complete. Check your inbox for the ranked CSV attachment.</p>
  <a href="/">Run Another Analysis</a>
</div></body></html>
"""
ERROR_HTML = """
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/><title>Error</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{min-height:100vh;background:#0f1117;display:flex;align-items:center;justify-content:center;font-family:'Segoe UI',system-ui,sans-serif;color:#e2e8f0}
  .card{background:#1a1d27;border:1px solid #3d1f1f;border-radius:16px;padding:3rem 2.5rem;max-width:460px;width:90%;text-align:center;box-shadow:0 25px 60px rgba(0,0,0,.5)}
  .icon{font-size:3rem;margin-bottom:1.25rem}
  h2{font-size:1.5rem;font-weight:700;color:#fca5a5;margin-bottom:.6rem}
  .error-box{background:#1f0f0f;border:1px solid #3d1f1f;border-radius:8px;padding:.85rem 1rem;font-size:.85rem;color:#f87171;margin:1.25rem 0 2rem;text-align:left;word-break:break-word}
  a{display:inline-block;padding:.7rem 2rem;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:8px;color:white;font-weight:600;font-size:.9rem;text-decoration:none;transition:opacity .2s}
  a:hover{opacity:.88}
</style></head>
<body><div class="card">
  <div class="icon">⚠️</div>
  <h2>Something went wrong</h2>
  <div class="error-box">{{ error }}</div>
  <a href="/">Try Again</a>
</div></body></html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/topsis", methods=["POST"])
def run_topsis():
    try:
        file = request.files["file"]
        weights = request.form["weights"]
        impacts = request.form["impacts"]
        email = request.form["email"]

        weights_list = weights.split(",")
        impacts_list = impacts.split(",")

        if len(weights_list) != len(impacts_list):
            raise Exception("Weights and impacts count must match")

        for i in impacts_list:
            if i not in ['+', '-']:
                raise Exception("Impacts must be + or -")

        input_file = "input.csv"
        output_file = "result.csv"

        file.save(input_file)

        topsis(input_file, weights, impacts, output_file)

        msg = Message(
            subject="TOPSIS Result",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )
        msg.body = "TOPSIS result attached."

        with open(output_file, "rb") as f:
            msg.attach("result.csv", "text/csv", f.read())

        mail.send(msg)
        print("MAIL SENT FUNCTION CALLED SUCCESSFULLY")


        os.remove(input_file)
        os.remove(output_file)

        return render_template_string(SUCCESS_HTML)

    except Exception as e:
        return render_template_string(ERROR_HTML, error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
