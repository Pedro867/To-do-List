from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return redirect(url_for('login'))
                    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "Faz login"
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)