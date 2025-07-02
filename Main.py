from flask import Flask, render_template, url_for, redirect, session, send_from_directory, request
from account import signup, login
import secrets
import os
from werkzeug.utils import secure_filename
from Downloader import download_audio_function,download_video_function

app = Flask(__name__)
app.secret_key = secrets.token_hex(1024)

# Load config
server_conf = [line.strip().split('=') for line in open('server_conf.txt','r').readlines() 
             if line[0] != '#' and line.strip() != '']
server_conf_dict = {e[0]: e[1] for e in server_conf}

# Ensure directories exist
os.makedirs(server_conf_dict['MEDIA_DIR'], exist_ok=True)
os.makedirs(server_conf_dict['STORAGE_DIR'], exist_ok=True)

def get_user_folder():
    """Returns path to the current user's storage folder"""
    if 'username' not in session:
        return None
    user_folder = os.path.join(server_conf_dict['STORAGE_DIR'], session['username'])
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

# Routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method.lower() == 'post':
        username = request.form.get('username')
        passwd = request.form.get('password')
        if signup(username, passwd):
            session['username'] = username
            return redirect(url_for('dashboard')) 
        return 'Signup failed'
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method.lower() == 'post':
        if login(request.form.get('username'), request.form.get('password')):
            session['username'] = request.form.get('username')
            return redirect(url_for('dashboard'))
        return 'Login failed'
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    user_folder = get_user_folder()
    files = os.listdir(user_folder) if user_folder else []
    return render_template('dashboard.html', files=files)

@app.route('/media')
def media():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('media.html', files=os.listdir(server_conf_dict['MEDIA_DIR']))

@app.route('/media/<filename>')
def download_file(filename):
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return send_from_directory(server_conf_dict['MEDIA_DIR'], filename)

@app.route('/files/<filename>')
def serve_user_file(filename):
    if 'username' not in session:
        return redirect(url_for('login_page'))
    user_folder = get_user_folder()
    return send_from_directory(user_folder, filename)

@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    user_folder = get_user_folder()
    if not user_folder:
        return "Error: User folder not found", 400
    
    # Debug print to verify uploads
    print(f"\n=== UPLOAD DEBUG ===")
    print(f"User: {session.get('username')}")
    print(f"Files received: {[f.filename for f in request.files.getlist('files')]}")
    
    for file in request.files.getlist('files'):
        if file.filename:
            filename = secure_filename(file.filename)
            dest_path = os.path.join(user_folder, filename)
            file.save(dest_path)
            print(f"Saved to: {dest_path}")
    
    # Force refresh with cache control
    response = redirect(url_for('dashboard'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'server.ico')

@app.route('/download_media',methods=['GET','POST'])
def download_videos():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    if request.method.lower() == 'post':
        url = request.form.get('url')
        data_format = request.form.get('format')
        if data_format == 'audio':
            download_audio_function(url)
        elif data_format == 'video':
            download_video_function(url)
        return redirect(url_for('media'))
        
    return render_template('download_media.html')

if __name__ == '__main__':
    if server_conf_dict['HOST'].lower() == 'true':
        app.run(host='0.0.0.0', port=int(server_conf_dict['PORT']))
    else:
        app.run(port=int(server_conf_dict['PORT']))


##TODO: Next time See what to do about the online buffer and also the game server (MC)
