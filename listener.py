from flask import Flask, request
import subprocess, os.path
app = Flask(__name__)

dagsfolder = open('dagsfolder.cfg', encoding = 'utf-8').readline().strip()
token = open('token.cfg', encoding = 'utf-8').readline().strip()

@app.route('/update', methods=['POST'])
def update():
    data = dict(request.headers)
    if not 'Token' in data or data['Token'] != token:
        return {'status': 'Unauthorized'}, 401
    if not '.git' in os.listdir(dagsfolder):
        return {'status': 'Not Found'}, 404
    subprocess.run(['git', 'reset', '--hard', 'HEAD'], cwd = dagsfolder)
    subprocess.run(['git', 'pull'], cwd = dagsfolder)
    return {'status': 'OK'}, 200

@app.route('/cleanall', methods=['POST'])
def cleanall():
    data = dict(request.headers)
    if not 'Token' in data or data['Token'] != token:
        return {'status': 'Unauthorized'}, 401
    subprocess.run(['rm', '-rf', os.path.join(dagsfolder)])
    subprocess.run(['mkdir', dagsfolder])
    return {'status': 'OK'}, 200

@app.route('/connect', methods=['POST'])
def connect():
    data = dict(request.headers)
    if not 'Token' in data or data['Token'] != token:
        return {'status': 'Unauthorized'}, 401
    if len(os.listdir(dagsfolder)) > 0:
        return {'status': 'Conflict'}, 409
    url = data['Url']
    subprocess.run(['git', 'clone', url, '.', '--config', 'core.sshCommand=ssh -i ~/.ssh/keyset'], cwd = dagsfolder)
    return {'status': 'OK'}, 200

@app.route('/sslkey', methods=['GET'])
def getSSLKey():
    data = dict(request.headers)
    if not 'Token' in data or data['Token'] != token:
        return {'status': 'Unauthorized'}, 401
    fullkey = open('/root/.ssh/keyset.pub', encoding = 'utf-8').readline()
    return fullkey.strip(), 400

if __name__ == "__main__":
    app.run(host = '0.0.0.0')