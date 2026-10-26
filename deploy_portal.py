import http.server
import os
import shutil
import subprocess
import zipfile
from email.parser import BytesParser
from email.policy import default

PORT = 8080

class UploadHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = """<!DOCTYPE html>
<html>
<head>
    <title>PromptPad Automated Deployer</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 420px; text-align: center; }
        h2 { margin-top: 0; color: #38bdf8; }
        input[type="file"] { margin: 20px 0; width: 100%; padding: 10px; background: #0f172a; border: 1px dashed #475569; border-radius: 6px; color: #cbd5e1; cursor: pointer; box-sizing: border-box; }
        button { background: #0284c7; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; transition: background 0.2s; }
        button:hover { background: #0369a1; }
        .footer { margin-top: 15px; font-size: 13px; color: #94a3b8; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 PromptPad Uploader</h2>
        <p>Select your <b>promptpad.zip</b> file from your computer to deploy instantly.</p>
        <form action="/" method="post" enctype="multipart/form-data">
            <input type="file" name="zipfile" accept=".zip" required>
            <button type="submit">Upload, Unzip & Push to GitHub</button>
        </form>
        <div class="footer">Codespaces Secure Uploader</div>
    </div>
</body>
</html>
"""
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        content_type = self.headers.get('Content-Type', '')
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        msg = BytesParser(policy=default).parsebytes(f"Content-Type: {content_type}\n\n".encode('utf-8') + body)
        
        zip_data = None
        for part in msg.iter_parts():
            if part.get_param('name', header='content-disposition') == 'zipfile':
                zip_data = part.get_payload(decode=True)
                break
        if not zip_data:
            for part in msg.walk():
                if part.get_content_maintype() != 'multipart' and part.get_filename():
                    zip_data = part.get_payload(decode=True)
                    break
                    
        if zip_data:
            zip_path = "promptpad.zip"
            with open(zip_path, "wb") as f:
                f.write(zip_data)
            
            print("\n📦 Received promptpad.zip via web upload. Processing...")
            if os.path.exists("extracted_temp"):
                shutil.rmtree("extracted_temp")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall("extracted_temp")
            
            extracted_path = "extracted_temp/promptpad"
            if not os.path.exists(extracted_path):
                extracted_path = "extracted_temp"
                
            for item in os.listdir(extracted_path):
                s = os.path.join(extracted_path, item)
                d = os.path.join(".", item)
                if os.path.exists(d):
                    if os.path.isdir(d):
                        shutil.rmtree(d)
                    else:
                        os.remove(d)
                shutil.move(s, d)
                
            for item in os.listdir("extracted_temp"):
                if item == "promptpad":
                    continue
                s = os.path.join("extracted_temp", item)
                d = os.path.join(".", item)
                if not os.path.exists(d):
                    shutil.move(s, d)
                    
            if os.path.exists("extracted_temp"):
                shutil.rmtree("extracted_temp")
            if os.path.exists(zip_path):
                os.remove(zip_path)
                
            subprocess.run(["git", "config", "--global", "user.email", "bot@promptpad.local"], check=True)
            subprocess.run(["git", "config", "--global", "user.name", "PromptPad Bot"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Deploy PromptPad: Automated Web Upload"], check=True)
            push_res = subprocess.run(["git", "push", "origin", "main"])
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            if push_res.returncode == 0:
                success_html = """<!DOCTYPE html>
<html>
<head>
    <title>Success - PromptPad</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); width: 450px; text-align: center; }
        h2 { color: #4ade80; margin-top: 0; }
        a.btn { display: inline-block; background: #22c55e; color: white; text-decoration: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; margin-top: 20px; font-weight: bold; }
        a.btn:hover { background: #16a34a; }
        p { color: #cbd5e1; line-height: 1.5; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🎉 Successfully Deployed!</h2>
        <p>Your files have been unzipped, organized, and pushed directly to your GitHub repository!</p>
        <p><b>Next Step:</b> Complete your live deployment on Vercel.</p>
        <a class="btn" href="https://vercel.com/new" target="_blank">Open Vercel Dashboard →</a>
    </div>
</body>
</html>
"""
                self.wfile.write(success_html.encode('utf-8'))
                print("\n✅ Success! Files uploaded, unzipped, and pushed to GitHub.")
                os._exit(0)
            else:
                self.wfile.write(b"<h2>Push Failed</h2><p>Check terminal for git errors.</p>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No file uploaded.")

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', PORT), UploadHandler)
    print(f"🌐 Uploader portal active!")
    print(f"👉 Look at the bottom right notification popup in VS Code and click 'Open in Browser',")
    print(f"   OR go to the 'Ports' tab in VS Code and click the globe icon next to port 8080.")
    server.serve_forever()
