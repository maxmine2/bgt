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
@app.route('/bugs')
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

@app.errorhandler(400)
@app.route('/err400')
def e400(e):
    return render_template('400.html'), 400
@app.errorhandler(401)
@app.route('/err401')
def e401(e):
    return render_template('401.html'), 401
@app.route('/err402')
def e402(e):
    return render_template('402.html'), 402
@app.errorhandler(403)
@app.route('/err403')
def e403(e):
    return render_template('403.html'), 403
@app.errorhandler(404)
@app.route('/err404')
def e404(e):
    return render_template('404.html'), 404
@app.errorhandler(405)
@app.route('/err405')
def e405(e):
    return render_template('405.html'), 405
@app.errorhandler(406)
@app.route('/err406')
def e406(e):
    return render_template('406.html'), 406
@app.route('/err407')
def e407(e):
    return render_template('407.html'), 407
@app.errorhandler(408)
@app.route('/err408')
def e408(e):
    return render_template('408.html'), 408
@app.errorhandler(409)
@app.route('/err409')
def e409(e):
    return render_template('409.html'), 409
@app.errorhandler(410)
@app.route('/err410')
def e410(e):
    return render_template('410.html'), 410
@app.errorhandler(411)
@app.route('/err411')
def e411(e):
    return render_template('411.html'), 411
@app.errorhandler(412)
@app.route('/err412')
def e412(e):
    return render_template('412.html'), 412
@app.errorhandler(413)
@app.route('/err413')
def e413(e):
    return render_template('413.html'), 413
@app.errorhandler(414)
@app.route('/err414')
def e414(e):
    return render_template('414.html'), 414
@app.errorhandler(415)
@app.route('/err415')
def e415(e):
    return render_template('415.html'), 415
@app.errorhandler(416)
@app.route('/err416')
def e416(e):
    return render_template('416.html'), 416
@app.errorhandler(417)
@app.route('/err417')
def e417(e):
    return render_template('417.html'), 417
@app.errorhandler(418)
@app.route('/err418')
@app.route('/errTeapod')
@app.route('/teapod')
@app.route('/iamteapod')
def e418(e):
    return render_template('418.html'), 418
      
if __name__ == "__main__":
    app.run(port=8080)