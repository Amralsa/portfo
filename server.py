from flask import Flask, render_template, url_for, request, redirect
import csv
app = Flask(__name__)
print(__name__)


@app.route('/')
def my_home():
    return render_template("index.html")
# @app.route('/index.html')
# def my_home1():
#     return render_template("index.html")
#
# @app.route('/about.html')
# def about():
#     return render_template('about.html')
#
# # @app.route('/favicon.ico')
# # def blog():
# #     return
# @app.route('/contact.html')
# def work():
#     return render_template("contact.html")
# @app.route('/thankyou.html')
# def ty():
#     return render_template("thankyou.html")
# @app.route('/works.html')
# def works():
#     return render_template("works.html")
@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)
def write_to_csv(data):
    with open('database.csv', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data ["message"]
        csv_writer = csv.writer(database, delimiter=",", quotechar= '"' ,quoting = csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])

@app.route('/submit_form', methods= ['POST', "GET"])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('./ty.html')
        except:
            return "did not save to database"
    else:
        return "Something Went Wrong..."



