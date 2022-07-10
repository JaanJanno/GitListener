from flask import Flask, request
import subprocess, os.path
app = Flask(__name__)

dagsfolder = open('/home/airflow/GitListener/dagsfolder.cfg', encoding = 'utf-8').readline().strip()
token = open('/home/airflow/GitListener/token.cfg', encoding = 'utf-8').readline().strip()

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
    subprocess.call(['rm', '-rf', dagsfolder])
    subprocess.call(['mkdir', dagsfolder])
    return {'status': 'OK'}, 200

@app.route('/connect', methods=['POST'])
def connect():
    data = dict(request.headers)
    if not 'Token' in data or data['Token'] != token:
        return {'status': 'Unauthorized'}, 401
    if len(os.listdir(dagsfolder)) > 0:
        return {'status': 'Conflict'}, 409
    url = data['Url']
    if '@' in url:
        host = url.split('@')[1].split(':')[0]
        if not os.path.exists('/home/airflow/.ssh/known_hosts'):
            subprocess.run(['touch', '/home/airflow/.ssh/known_hosts'])
        content = '\n' + '\n'.join(open('/home/airflow/.ssh/known_hosts').readlines())
        if not ('\n' + host + ' ') in content:
            with open('/home/airflow/.ssh/known_hosts', "a") as outfile:
                subprocess.run(['ssh-keyscan', host], stdout = outfile)
    subprocess.run(['git', 'clone', url, '.', '--config', 'core.sshCommand=ssh -i ~/.ssh/keyset'], cwd = dagsfolder)
    return {'status': 'OK'}, 200

@app.route('/sslkey', methods=['GET'])
def getSSLKey():
    data = dict(request.headers)
    if not 'Token' in data or data['Token'] != token:
        return {'status': 'Unauthorized'}, 401
    fullkey = open('/home/airflow/.ssh/keyset.pub', encoding = 'utf-8').readline()
    return fullkey.strip(), 200

if __name__ == "__main__":
    app.run(host = '0.0.0.0')