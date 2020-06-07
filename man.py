from flask import Flask, render_template, request
import pstg
import json

man_settings = json.load(open("man_set.json", "r"))

app = Flask(__name__, template_folder="templates", static_folder="templates/css")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

BUG_STATUS = {
    0:"Opened",
    1:"Working on",
    2:"In next release",
    3:"Closed",
    4:"Canceled"
}

@app.route('/')
def index():
    return render_template("index.html", project_name=man_settings["project_name"])

@app.route('/bug')
def all_bug():
    bugs = []
    for every_bug in pstg.get_all_bugs():
        bugs.append((every_bug[0], every_bug[2]))
    return render_template("all_bugs.html", bugs=bugs)

@app.route('/bug/create', methods=['post', 'get'])
def bug_create_page():
    msg = ''
    bug_id_new = 0
    if request.method == "POST":
        bug_id_new = pstg.create_new_bug({"t": request.form.get('title'), "m": request.form.get('mail'), "d": request.form.get('description'), "p": request.form.get('pass'),})
        msg = f'Bug succesfully created. '
    return render_template("bc.html", message=msg, link= f"/bug/{bug_id_new}")

@app.route('/bug/<int:bug_id>')
def bug_id_page(bug_id):
    bug = pstg.get_bug_by_id(bug_id)
    if bug == []:
        return render_template("bug_id.html", bug_id=bug_id, bug_title="Bug not found")
    return render_template("bug_id.html", bug_id=bug_id, bug_title=bug[0][2], mail=bug[0][4], bug_description=bug[0][3], bug_status_pbl=BUG_STATUS[bug[0][1]])

@app.route('/bug/<int:bug_id>/close', methods=['post', 'get'])
def bug_remove(bug_id):
    msg = ''
    bug = pstg.get_bug_by_id(bug_id)
    if bug == []:
        return render_template("close.html", bug_id="Bug not found.")
    if request.method == 'POST':
        if not request.form.get('i_know'):
            return render_template("close.html", bug_id=bug_id, message="You have to accept rule via checkbox")
        if bug[0][5] == request.form.get('psswd') or request.form.get('root_passwd') == man_settings["root_pswrd"]:
            pstg.delete_bug(bug_id)
            return render_template("close_c.html")
        return render_template("close.html", bug_id=bug_id, message="Password is uncorrect")
    return render_template("close.html", message=msg, bug_id=bug_id)

@app.route('/bug/<int:bug_id>/status/change', methods=["post", "get"])
def bug_status_change_page(bug_id):
    msg = ''
    link = f"/bug/{bug_id}"
    bug=pstg.get_bug_by_id(bug_id)
    if bug == []:
        return render_template("status.html", message="Bug is not found")
    if request.method == "POST":
        new_status= request.form.get('status')
        pstg.change_status(bug_id, new_status)
        msg = "Done."
    a = bug[0][1]
    if a == 0:
        return render_template("status.html", bug_id=bug[0][0], o0_disbl="disabled", message=msg, link=link)
    if a == 1:
        return render_template("status.html", bug_id=bug[0][0], o1_disbl="disabled", message=msg, link=link)
    if a == 2:
        return render_template("status.html", bug_id=bug[0][0], o2_disbl="disabled", message=msg, link=link)
    if a == 3:
        return render_template("status.html", bug_id=bug[0][0], o3_disbl="disabled", message=msg, link=link)
    if a == 4:
        return render_template("status.html", bug_id=bug[0][0], o4_disbl="disabled", message=msg, link=link)

@app.route('/bug/<int:bug_id>/cancel', methods=['GET', 'POST'])
def bug_cancel(bug_id):
    msg = ''
    bug=pstg.get_bug_by_id(bug_id)
    print(bug)
    if bug == []:
        return render_template("cancel.html", message="Bug not found", bug_id=bug_id)
    if request.method == "POST":
        if bug == []:
            return render_template("cancel.html", message="Bug not found", bug_id=bug_id)
        if request.form.get("psswrd") == bug[0][5]:
            pstg.cancel_bug(bug_id)
            return render_template("cancel.html", message="Bug succesfully cancelled", bug_id=bug_id)
        elif request.form.get("psswrd") != bug[0][5]:
            return render_template("cancel.html", message="Password is uncorrect", bug_id=bug_id)
    return render_template("cancel.html", bug_id=bug_id)
        
if __name__ == "__main__":
    app.run(port=8080)