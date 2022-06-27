from flask import Flask, render_template, request
import requests
import smtplib

blog_endpoint = "https://api.npoint.io/05bd5c3eb3e254d1a9d9"
response = requests.get(blog_endpoint)
DATA = response.json()

MY_EMAIL = "your@email.com"
PASSWORD = "your password"

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", data=DATA)


@app.route("/<int:id>")
def show_detail(id):
    display_detail = None
    for item in DATA:
        if item['id'] == id:
            display_detail = item
    return render_template("post.html", item=display_detail)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return receive_data()
    return render_template("contact.html")


def receive_data():
    data = request.form
    print('\n', data['name'], '\n', data['email'], '\n', data['phone'], '\n', data['message'])
    send_message(data['name'], data['email'], data['phone'], data['message'])
    return render_template("contact.html", data=data)


def send_message(name, email, phone, msg):
    email_content = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {msg}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=email,
                            to_addrs=MY_EMAIL,
                            msg=email_content
                            )


if __name__ == "__main__":
    app.run(debug=True)
