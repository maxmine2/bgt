from flask import Flask, render_template
import db

app = Flask(__name__, template_folder="templtates")

BUG_STATUS = {
    0:"Opened",
    1:"Working on",
    2:"In next release",
    3:"Closed",
    4:"Canceled"
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/bug')
def bug_main_page():
    return 'You could create a bug here'

@app.route('/bug/<int:bug_id>')
def bug_id_page(bug_id):
    bug = db.get_bug_by_id(bug_id)
    print(bug)
    return render_template("bug_id.html", )

@app.route('/bug/<int:bug_id>/close')
def bug_remove(bug_id):
    return "You could close bug #{} here".format(bug_id)

@app.route('/bug/<int:bug_id>/status')
def bug_status(bug_id):
    return "You could get a status of bug #{} here".format(bug_id)

@app.route('/bug/<int:bug_id>/status/change')
def bug_status_change_page(bug_id):
    return "You could change a status of bug#{} here".format(bug_id)

if __name__ == "__main__":
    app.run()