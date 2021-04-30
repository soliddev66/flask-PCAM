from flask import g, render_template, request, make_response, redirect, url_for, jsonify
from setup import app, _PORT,_HOST, _APP_NAME, _PATIENTS_TABLE,_MEASUREMENTS_TABLE,_PLACEHOLDER
from HIM73050 import flask_db as fdb
from login_auth import login_required
from flask import jsonify
from tkinter import *
from tkinter.ttk import *


@app.teardown_appcontext
def close_connection(exception):
    fdb.close_db()

@app.route('/')
def root():
    return render_template('index.html')

'''
    Steps for porting v2 to v3, update routers and templates.

    1) copy measurements(ptid) router code to a NEW patients() router
    and modify its code so that it manages the patient list (allows listing, selecting patients, adding new patient, etc);
        this is similar to how multiple measurements list was managed for the ONE patient in v2 app
    2) rename the measurements(ptid) router to patient(ptid)
        and modify its code so that it will displays information about ONE patient
        and manages their measurement list;
        this is similar to how information about one measurement was managed in v2 app
        (i.e., list, select, add new measurement)
    3) update the measurement(ptid,mid) router
    and modify its code to allow for foth a patient info object and
    a measurement info object be passed along to the templates

    4) rename and modify the templates to reflect the above changes

there is no need to pass the patient argument to the routers;
there will be a patient ID and a patient_info object
'''

@app.route('/patient_select')
@login_required
def select_patient():
    return render_template('patient_selector.html')

@app.route('/patient_list')
@login_required
def patient_list():
    patient_list = fdb.query_db_get_all('SELECT * FROM '+_PATIENTS_TABLE)
    return render_template('patient_list.html', patients=patient_list)

@app.route('/patients',methods=['GET', 'POST'])
@login_required
def patients():
    '''Works'''
    if request.method == 'GET':
        patient_list = fdb.query_db_get_all('SELECT * FROM '+_PATIENTS_TABLE)
        print(patient_list)
        return jsonify(patient_list)
    elif request.method == 'POST':
        fName = request.form['first_name']
        lName = request.form['last_name']
        eMail = request.form['e_mail']
        _date = request.form['date']
        address = request.form['address']
        healthcardno = request.form['healthcardno']
        p1 = -1
        p2 = -1
        p3 = -1
        p4 = -1
        result=fdb.query_db_change('INSERT INTO '+_PATIENTS_TABLE+'(firstname, lastname, email, date_, address, healthcardno, p1, p2, p3, p4) VALUES ({0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0}, {0})'.format(_PLACEHOLDER),(fName, lName, eMail, _date, address, healthcardno, p1, p2, p3, p4))
        if result==None:
            print("Could not insert new record into",_PATIENTS_TABLE)
        return render_template('p1.html', ptid=result)

@app.route('/summary_notes')
@login_required
def summary_notes():
    patient_list = fdb.query_db_get_all('SELECT * FROM '+_PATIENTS_TABLE)
    dic = {
        "rountineCare": [0, 0, 0, 0],
        "activeMonitoring": [0, 0, 0, 0],
        "planAction": [0, 0, 0, 0],
        "actNow": [0, 0, 0, 0]
    }
    for patient in patient_list:
        if patient['p1'] > -1:
            if patient['p1'] == 0:
                dic["rountineCare"][0] = dic["rountineCare"][0] + 1
            elif patient['p1'] == 1:
                dic["activeMonitoring"][0] = dic["activeMonitoring"][0] + 1
            elif patient['p1'] == 2:
                dic["planAction"][0] = dic["planAction"][0] + 1
            else:
                dic["actNow"][0] = dic["actNow"][0] + 1
        if patient['p2'] > -1:
            if patient['p2'] == 0:
                dic["rountineCare"][1] = dic["rountineCare"][1] + 1
            elif patient['p2'] == 1:
                dic["activeMonitoring"][1] = dic["activeMonitoring"][1] + 1
            elif patient['p2'] == 2:
                dic["planAction"][1] = dic["planAction"][1] + 1
            else:
                dic["actNow"][1] = dic["actNow"][1] + 1
        if patient['p3'] > -1:
            if patient['p3'] == 0:
                dic["rountineCare"][2] = dic["rountineCare"][2] + 1
            elif patient['p3'] == 1:
                dic["activeMonitoring"][2] = dic["activeMonitoring"][2] + 1
            elif patient['p3'] == 2:
                dic["planAction"][2] = dic["planAction"][2] + 1
            else:
                dic["actNow"][2] = dic["actNow"][2] + 1
        if patient['p4'] > -1:
            if patient['p4'] == 0:
                dic["rountineCare"][3] = dic["rountineCare"][3] + 1
            elif patient['p4'] == 1:
                dic["activeMonitoring"][3] = dic["activeMonitoring"][3] + 1
            elif patient['p4'] == 2:
                dic["planAction"][3] = dic["planAction"][3] + 1
            else:
                dic["actNow"][3] = dic["actNow"][3] + 1
    return render_template('summary_notes.html', summary=dic)

@app.route('/patient/<ptid>/'+_APP_NAME, methods=['GET', 'POST'])
@login_required
def patient(ptid):
    '''Works '''
    if request.method == 'GET':
        patient_info = fdb.query_db_get_one('SELECT * FROM '+_PATIENTS_TABLE+' WHERE id={0}'.format(_PLACEHOLDER),(ptid,))
        #retrieve measurements
        query='SELECT * FROM '+_MEASUREMENTS_TABLE+' WHERE patient_id={0}'.format(_PLACEHOLDER) # this IS good enough@
        #no need to join - keeping the patient and measurements dictionary separate, makes it easier/more intuitive to write the template code
        #query='SELECT * FROM '+_MEASUREMENTS_TABLE+' as v JOIN (SELECT * FROM Patients WHERE id={0}) as p ON v.patient_id=p.id'.format(_PLACEHOLDER)
        patient_measurements = fdb.query_db_get_all(query,(ptid,))
        return render_template('patient.html', patient=patient_info, measurements=patient_measurements)

    elif request.method == 'POST':
        systolic = request.form['systolic']
        diastolic = request.form['diastolic']
        pulse = request.form['pulse']
        fdb.query_db_change('INSERT INTO '+_MEASUREMENTS_TABLE+'(systolic, diastolic, pulse, patient_id) VALUES ({0}, {0}, {0}, {0})'.format(_PLACEHOLDER),(systolic, diastolic, pulse,ptid))
        return redirect(url_for('patient',ptid=ptid))

@app.route('/patient/<ptid>/'+_APP_NAME+'/measurement/<mid>')
@login_required
def measurement(ptid,mid):
    patient_info = fdb.query_db_get_one('SELECT * FROM '+_PATIENTS_TABLE+' WHERE id={0}'.format(_PLACEHOLDER),(ptid,))
    pt_msmt=fdb.query_db_get_one('SELECT id, systolic, diastolic, pulse, time_recorded FROM '+_MEASUREMENTS_TABLE+' WHERE id = {0}'.format(_PLACEHOLDER), (mid,))
    return render_template('measurement.html',patient=patient_info, measurement=pt_msmt)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    patient_info = fdb.query_db_get_one('SELECT * FROM ' +_PATIENTS_TABLE +' WHERE id={0}'.format(_PLACEHOLDER), (ptid,))
    if request.method == 'POST' and patient_info.validate_on_submit():
        return redirect((url_for('search_results', query=patient_info.search.data)))
    return render_template('search.html', form=patient_info)

# @app.route('/p1.html/<ptid>')
# @login_required
# def health_and_wellbeing(ptid):
#     return render_template('p1.html', ptid)

@app.route('/p1/<int:ptid>/<int:ptsel>')
@login_required
def p1_update(ptid, ptsel):
    query = 'UPDATE '+_PATIENTS_TABLE+' SET p1=? WHERE id=?'
    args = (ptsel, ptid)
    fdb.query_db_change(query, args)
    return jsonify(ptid)
    # return redirect(url_for('social_environment'))

@app.route('/health_and_wellbeing')
@login_required
def health_and_wellbeing():
    id = request.args.get('id')
    return render_template('p1.html', ptid=id)

@app.route('/p2/<int:ptid>/<int:ptsel>')
@login_required
def p2_update(ptid, ptsel):
    query = 'UPDATE '+_PATIENTS_TABLE+' SET p2=? WHERE id=?'
    args = (ptsel, ptid)
    fdb.query_db_change(query, args)
    return jsonify(ptid)

@app.route('/social_environment')
@login_required
def social_environment():
    id = request.args.get('id')
    return render_template('p2.html', ptid=id)

@app.route('/p3/<int:ptid>/<int:ptsel>')
@login_required
def p3_update(ptid, ptsel):
    query = 'UPDATE '+_PATIENTS_TABLE+' SET p3=? WHERE id=?'
    args = (ptsel, ptid)
    fdb.query_db_change(query, args)
    return jsonify(ptid)

@app.route('/health_lit_comm')
@login_required
def health_lit_comm():
    id = request.args.get('id')
    return render_template('p3.html', ptid=id)

@app.route('/p4/<int:ptid>/<int:ptsel>')
@login_required
def p4_update(ptid, ptsel):
    query = 'UPDATE '+_PATIENTS_TABLE+' SET p4=? WHERE id=?'
    args = (ptsel, ptid)
    fdb.query_db_change(query, args)
    return jsonify(ptid)

@app.route('/service_coordination')
@login_required
def service_coordination():
    id = request.args.get('id')
    return render_template('p4.html', ptid=id)

@app.route('/autocompletebyname', methods=['GET'])
@login_required
def autocompletebyname():
    search = request.args.get('q')
    query = 'SELECT * FROM '+_PATIENTS_TABLE + ' WHERE firstname LIKE ? OR lastname LIKE ?'
    args = ('%' + search + '%', '%' + search + '%')
    patient_list = fdb.query_db_get_all(query, args)
    patients = []
    for patient in patient_list:
        name = patient["firstname"] + " " + patient["lastname"]
        patients.append(name)
    return jsonify(patients)

@app.route('/autocompletebyhealthcard', methods=['GET'])
def autocompletebyhealthcard():
    search = request.args.get('q')
    query = 'SELECT * FROM '+_PATIENTS_TABLE + ' WHERE CAST(healthcardno AS TEXT) LIKE ?'
    args = ('%' + search + '%')
    patient_list = fdb.query_db_get_all(query, (args,))
    patients = []
    for patient in patient_list:
        name = patient["firstname"] + " " + patient["lastname"]
        patients.append(name)
    return jsonify(patients)

if __name__ == '__main__':
    app.run(port=_PORT, host=_HOST)

