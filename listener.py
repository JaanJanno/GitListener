from flask import Flask, request
import subprocess, os.path
app = Flask(__name__)

dagsfolder = open('dagsfolder.cfg', encoding = 'utf-8').readline().strip()

@app.route('/update', methods=['POST'])
def update():
    dirs = os.listdir(dagsfolder)
    for e in dirs:
        dir =  os.path.join(dagsfolder, e)
        if os.path.isdir(dir):
            subprocess.run(['git', 'reset', '--hard', 'HEAD'], cwd = dir)
            subprocess.run(['git', 'pull'], cwd = dir)
    return {'status': 'success'}, 200

@app.route('/cleanall', methods=['POST'])
def cleanall():
    dirs = os.listdir(dagsfolder)
    for e in dirs:
        dir =  os.path.join(dagsfolder, e)
        if os.path.isdir(dir):
            subprocess.run(['git', 'reset', '--hard', 'HEAD'], cwd = dir)
            subprocess.run(['git', 'clean', '-f', '-d'], cwd = dir)
            subprocess.run(['git', 'pull'], cwd = dir)
    return {'status': 'success'}, 200

@app.route('/connect', methods=['POST'])
def connect():
    data = dict(request.form)
    subprocess.run(['git', 'clone', data['url']], cwd = dagsfolder)
    return {'status': 'success'}, 200

if __name__ == "__main__":
    app.run(host = '0.0.0.0')