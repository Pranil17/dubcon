from flask import Flask, redirect, url_for, request, render_template,send_file
import os

app = Flask(__name__)
upload_dir1 = "upload_sub/"
upload_dir2 = "upload_video/"

@app.route('/')
def hello():
    return render_template('homepage.html')

@app.route('/upload',methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return render_template('upload_subs.html')

@app.route('/uploads')
def upload_video():
    return render_template('upload_video.html')



@app.route('/upload_subs', methods=['GET', 'POST'])
def upload_filess():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(upload_dir1,f.filename))
        return redirect(url_for('upload_video'))

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(upload_dir2,f.filename))
        return redirect(url_for("process"))

@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/convert',methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        import combined
        return redirect(url_for("download"))

@app.route('/download')
def download():
    path = "final/final.mp4"
    redirect("http://127.0.0.1:5000/done")
    return send_file(path,as_attachment=True)


@app.route('/done')
def done():
    return redirect(url_for("hello"))


if __name__ == '__main__':
    app.run(debug = True)
