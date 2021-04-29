from flask import Flask, redirect, url_for, request, render_template
import GenearteFiles
app = Flask(__name__)


@app.route("/")
def Main():
    return render_template("home.html", img=url_for('static', filename='sergi.png'))


@app.route("/search", methods=['POST', "GET"])
def search():
    if request.method == "GET":
        if(request.args.get("search") == "Search"):
            return "Search"
        if(request.args.get("generate") == "Generate Files"):
            files = GenearteFiles.Files(3, 6)
            return "Generate Files"
    """------------------------------------------------------------"""
    if request.method == "POST":
        if("search" in request.form.keys()):
            return "HELLO SEARCH"
        elif("generate" in request.form.keys()):
            files = GenearteFiles.Files(3, 6)
            return "HELLO generate"


if __name__ == "__main__":
    app.run(debug=True)
