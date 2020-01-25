import requests
import hashlib
from flask import Flask, render_template, request, redirect
import csv
app = Flask(__name__)
print(__name__)


def request_api_data(query_char):
    url = 'http://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code} check the API and try again')
    return res
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)
def main(password):
        count = pwned_api_check(password)
        if count:
            return(f'{password} was found {count} times... You should probably change your password')
        else:
            return(f'{password} was NOT found. Carry on!')
    # return 'done!'

@app.route('/')
def my_home():
    return render_template("index.html")

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

@app.route('/Passwords',  methods= ['POST', "GET"])
def passwords():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            password = data["Password"]
            if len(password) > 7:
                return main(password)
            else:
                return "Enter a minimum of 8 characters!"

        except:
            return "Something Went Wrong!"


#game time
import random


def guess_me(guess):
    answer = random.randint(1, 10)
    if int(guess) == answer:
        return "Well done! Take a rest, you deserve it!"
    else:
        return "Uh Oh! Try again, do not let this thing beat you! Hint: the number is from 1-10."


@app.route('/Guess_me',  methods= ['POST', "GET"])
def guess():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            guess = data["guesser"]
            if len(guess) == 1 or 2 :
                return guess_me(guess)
            else:
                return "Please enter one number!"
        except:
            return "something went wrong"


