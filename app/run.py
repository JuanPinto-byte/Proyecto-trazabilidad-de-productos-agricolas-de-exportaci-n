from flask import Flask, render_template, request, redirect, url_for
from flask import session
from config import config
from extensions import db
from routes.auth import auth_bp

app=Flask(__name__)
app.config.from_object(config["development"])
db.init_app(app)
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route("/")
def index():
    return redirect(url_for("auth.login"))

app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html")

if __name__=="__main__":
    app.config.from_object(config["development"])
    app.run(debug=True)

print(app.url_map)