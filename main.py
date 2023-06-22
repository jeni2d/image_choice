import os, shutil

from flask import Flask, render_template, redirect, url_for


# PATH = 'c:/video/1/'
# RESULT_PATH = 'c:/video/images/'
PATH = 'photos/'
RESULT_PATH = 'result/'

class Files:
    __slots__ = (
        'files_name',
        'file_index'
    )

    def __init__(self):
        self.files_name = []
        self.file_index = 0

        self.fill_files_name()

    def fill_files_name(self):
        for root, dirs, files in os.walk(PATH):
            for filename in files:
                if filename.endswith('.jpg'):
                    self.files_name.append(os.path.join(root.split('/')[-1],filename))
                
    @property
    def file_name(self) -> str:
        # print(self.files_name[self.file_index])
        return self.files_name[self.file_index]

    def next_step(self):
        if self.file_index != len(self.files_name)-1:
            self.file_index += 1

files = Files()

app = Flask(__name__, static_folder="/home/admin/photos/")

@app.route("/", methods=["GET"])
def hello_world():
    return redirect(url_for('main'))

@app.route("/main", methods=["GET"])
def main():
    return render_template('index.html', path=PATH, file_name=files.file_name)

@app.route("/empty", methods=["GET"])
def empty():
    return render_template('empty.html')

@app.route("/yes", methods=["GET"])
def yes():

    try:
        file_path = PATH + files.file_name
        try:
            os.mkdir(os.path.join(RESULT_PATH,file_path.split('/')[-2]))
        except FileExistsError:
            pass
        shutil.copyfile(file_path, os.path.join(RESULT_PATH, file_path.split('/')[-2], file_path.split('/')[-1]))
        os.remove(file_path)
        files.next_step()
        return redirect(url_for('main'))
    except FileNotFoundError:
        return redirect(url_for('empty'))
        
@app.route("/no", methods=["GET"])
def no():
    
    try:
        file_path = PATH + files.file_name
        os.remove(file_path)
        files.next_step()
        return redirect(url_for('main'))
    except FileNotFoundError:
        return redirect(url_for('empty'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")