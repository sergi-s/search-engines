from flask import Flask, redirect, url_for, request, render_template
import GenearteFiles
app = Flask(__name__)


@app.route("/")
def Main():
    return render_template("home.html", img=url_for('static', filename='sergi.png'))


@app.route("/search", methods=['POST', "GET"])
def search():
    # ? GET
    if request.method == "GET":
        if(request.args.get("search") == "Search"):
            query = request.args.get("input_query")
            return "null"
        if(request.args.get("generate") == "Generate Files"):
            files = GenearteFiles.Files(numFiles=3, endLetter='f', rangeUpper=5,
                                        rangeLower=10, useOld=False)
            return "Generate Files"
    """------------------------------------------------------------"""
    # ? POST
    if request.method == "POST":
        if("search" in request.form.keys()):
            query = request.form['input_query']
            if(request.form["models"] == "statistical"):
                return GenearteFiles.Search_Statistical(query)
            elif(request.form["models"] == "vectorspace"):
                return GenearteFiles.Search_VectorSpace(query)

        elif("generate" in request.form.keys()):
            files = GenearteFiles.Files(numFiles=3, endLetter='f', rangeUpper=5,
                                        rangeLower=10, useOld=False)
            return "HELLO generate"


if __name__ == "__main__":
    app.run(debug=True)
