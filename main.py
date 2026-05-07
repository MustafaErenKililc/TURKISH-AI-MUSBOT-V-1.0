from flask import Flask, render_template_string, request
import requests, webbrowser
from threading import Timer

app = Flask(__name__)

# --- GLOBAL RELEASE V 1.0 ---
# Developed by: Mustafa Eren Kilic

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="mobile-web-app-capable" content="yes">
    <title>MUSBOT AI V 1.0</title>
    <style>
        :root { --neon: #39ff14; --cyber: #00f3ff; }
        body { background: #050505; color: var(--neon); font-family: 'Courier New', monospace; margin: 0; padding: 15px; text-align: center; }
        .terminal { width: 95%; max-width: 650px; height: 380px; border: 2px solid var(--neon); margin: 15px auto; overflow-y: auto; padding: 15px; background: #000; box-shadow: 0 0 20px var(--neon); border-radius: 10px; }
        .line { text-align: left; margin-bottom: 10px; font-size: 0.9em; line-height: 1.4; }
        .config-panel { background: #111; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid var(--cyber); display: inline-block; width: 90%; max-width: 650px; }
        input { background: #000; border: 1px solid var(--neon); color: #fff; padding: 12px; border-radius: 5px; outline: none; margin: 5px; }
        .msg-input { width: 65%; }
        .key-input { width: 85%; border-color: var(--cyber); font-size: 0.8em; }
        button { padding: 12px 20px; background: var(--neon); color: #000; font-weight: bold; border: none; border-radius: 5px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 10px #fff; }
        .bot-tag { color: var(--cyber); font-weight: bold; }
    </style>
</head>
<body>
    <h1 style="margin-top: 10px;">MUSBOT AI <span style="color:white">V 1.0</span></h1>
    <p style="font-size: 0.8em; color: #888; margin-bottom: 20px;">Public Edition | Dev: Mustafa Eren Kilic</p>

    <div class="config-panel">
        <small style="color: var(--cyber);">[SYSTEM] Please enter your Gemini API Key:</small><br>
        <input type="password" id="apiKey" class="key-input" placeholder="Paste your Google API Key here...">
    </div>

    <div class="terminal" id="term">
        <div class="line"><span class="bot-tag">[MUSBOT]:</span> System Online. I am ready to answer any global question. Just enter your API key and ask!</div>
    </div>
    
    <div style="display: flex; justify-content: center; gap: 8px; max-width: 650px; margin: 0 auto; padding-bottom: 20px;">
        <input type="text" id="msgInp" class="msg-input" placeholder="Enter your question..." onkeydown="if(event.key==='Enter') send()">
        <button onclick="send()">SEND</button>
    </div>

    <script>
        function send() {
            let key = document.getElementById('apiKey').value;
            let msg = document.getElementById('msgInp').value;
            let term = document.getElementById('term');
            
            if(!key) { alert("API Key is missing! Please enter your key."); return; }
            if(!msg) return;

            term.innerHTML += "<div class='line'><b>[USER]:</b> " + msg + "</div>";
            document.getElementById('msgInp').value = "";
            term.scrollTop = term.scrollHeight;

            fetch('/ai?q=' + encodeURIComponent(msg) + '&key=' + encodeURIComponent(key))
                .then(r => r.text())
                .then(data => {
                    term.innerHTML += "<div class='line'><span class='bot-tag">[MUSBOT]:</span> " + data + "</div>";
                    term.scrollTop = term.scrollHeight;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): 
    return render_template_string(HTML_TEMPLATE)

@app.route('/ai')
def ai():
    query = request.args.get('q')
    user_key = request.args.get('key')
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={user_key}"
    payload = {"contents": [{"parts": [{"text": f"You are MUSBOT V 1.0, a highly intelligent global AI created by the developer Mustafa Eren Kilic. Answer the user's question clearly and helpfully: {query}"}]}]}
    
    try:
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"API ERROR ({r.status_code}): Please check if your API Key is valid."
    except Exception as e:
        return "CONNECTION ERROR: System could not reach the global brain."

if __name__ == '__main__':
    print(">>> MUSBOT V 1.0 IS LAUNCHING...")
    Timer(1.5, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(port=5000)
