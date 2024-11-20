from flask import Flask, render_template

# Create a Flask application
app = Flask(__name__)

# Define a route
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/edit")
def edit_page():
    return render_template("edit.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


