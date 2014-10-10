from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/answer", methods=["GET"])
def answer():
    query = request.args.get('q')
    return render_template("answer.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
