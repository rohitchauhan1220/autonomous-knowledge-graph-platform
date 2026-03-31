from flask import Flask, request, render_template
from graph_builder import process_text

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form["text"]
        process_text(text)
        return "Graph Updated!"
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)