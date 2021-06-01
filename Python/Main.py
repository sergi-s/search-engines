from flask import Flask, redirect, url_for, request, render_template
import GenearteFiles
app = Flask(__name__)


@app.route("/")
def Main():
    return render_template("home.html", img=url_for('static', filename='sergi.png'))


@app.route("/search", methods=['POST', "GET"])
def search():
    if request.method == "POST":
        if("search" in request.form.keys()):
            query = request.form['input_query']
            files = GenearteFiles.Files(endLetter='f', rangeUpper=5,
                                        rangeLower=10, useOld=True)
            if(request.form["models"] == "statistical"):
                return GenearteFiles.Search_Statistical(files, query)
            elif(request.form["models"] == "vectorspace"):
                result = GenearteFiles.Search_VectorSpace(files, query)
                # print(files.TermDocFreq)
                for i in files.allFiles:
                    print(i.idfi)
                print(files.TermDocFreq)
                return result

        elif("generate" in request.form.keys()):
            files = GenearteFiles.Files(numFiles=10, endLetter='f', rangeUpper=5,
                                        rangeLower=10, useOld=False)
            return "File Generated"


if __name__ == "__main__":
    app.run(debug=True)
