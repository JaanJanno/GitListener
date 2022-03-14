from flask import Flask, request
import subprocess, os.path
app = Flask(__name__)

dagsfolder = open('dagsfolder.cfg', encoding = 'utf-8').readline().strip()
token = open('token.cfg', encoding = 'utf-8').readline().strip()

@app.route('/update', methods=['POST'])
def update():
    data = dict(request.form)
    if 'token' in data and data['token'] != token:
        return {'status': 'Unauthorized'}, 401
    dirs = os.listdir(dagsfolder)
    for e in dirs:
        dir =  os.path.join(dagsfolder, e)
        if os.path.isdir(dir):
            subprocess.run(['git', 'reset', '--hard', 'HEAD'], cwd = dir)
            subprocess.run(['git', 'pull'], cwd = dir)
    return {'status': 'OK'}, 200

@app.route('/cleanall', methods=['POST'])
def cleanall():
    data = dict(request.form)
    if 'token' in data and data['token'] != token:
        return {'status': 'Unauthorized'}, 401
    dirs = os.listdir(dagsfolder)
    for e in dirs:
        dir =  os.path.join(dagsfolder, e)
        if os.path.isdir(dir):
            subprocess.run(['git', 'reset', '--hard', 'HEAD'], cwd = dir)
            subprocess.run(['git', 'clean', '-f', '-d'], cwd = dir)
            subprocess.run(['git', 'pull'], cwd = dir)
    return {'status': 'OK'}, 200

@app.route('/connect', methods=['POST'])
def connect():
    data = dict(request.form)
    if 'token' in data and data['token'] != token:
        return {'status': 'Unauthorized'}, 401
    subprocess.run(['git', 'clone', data['url']], cwd = dagsfolder)
    return {'status': 'OK'}, 200

@app.route('/sslkey', methods=['GET'])
def getSSLKey():
    data = dict(request.form)
    if 'token' in data and data['token'] != token:
        return {'status': 'Unauthorized'}, 401
    fullkey = open('/root/.ssh/keyset.pub', encodiing = 'utf-8').readline()
    return fullkey.strip(), 400

if __name__ == "__main__":
    app.run(host = '0.0.0.0')