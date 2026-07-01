import os

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, session

from config import SECRET_KEY
from modules.db import get_connection

app = Flask(__name__)

# ======================================================
# CONFIG
# ======================================================

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = SECRET_KEY


# ======================================================
# MAIN LOGIN
# ======================================================

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_connection()

        cur = conn.cursor()

        query = """

        SELECT * FROM users

        WHERE
        username=%s
        AND password=%s

        """

        cur.execute(query, (

            username,
            password

        ))

        user = cur.fetchone()

        conn.close()

        if user:

            session['user'] = username

            session['role'] = user[3]

            return redirect('/dashboard')

        else:

            return "Invalid Username or Password"

    return render_template("login.html")


# ======================================================
# ADMIN LOGIN
# ======================================================

@app.route('/admin-login',
           methods=['GET', 'POST'])

def admin_login():

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        conn = get_connection()

        cur = conn.cursor()

        query = """

        SELECT * FROM users

        WHERE
        username=%s
        AND password=%s
        AND role='admin'

        """

        cur.execute(query, (

            username,
            password

        ))

        admin = cur.fetchone()

        conn.close()

        if admin:

            session['admin'] = username

            return redirect('/dashboard')

        else:

            return "Invalid Admin Credentials"

    return render_template("admin_login.html")


# ======================================================
# POLICE LOGIN
# ======================================================

@app.route('/police-login',
           methods=['GET', 'POST'])

def police_login():

    conn = get_connection()

    cur = conn.cursor()

    # GET ALL POLICE USERS

    cur.execute("""

        SELECT username, password

        FROM users

        WHERE role='police'

    """)

    police_users = cur.fetchall()

    # LOGIN CHECK

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        query = """

        SELECT * FROM users

        WHERE
        username=%s
        AND password=%s
        AND role='police'

        """

        cur.execute(query, (

            username,
            password

        ))

        user = cur.fetchone()

        if user:

            session['user'] = username

            session['role'] = 'police'

            conn.close()

            return redirect('/dashboard')

        else:

            conn.close()

            return "Invalid Police Username or Password"

    conn.close()

    return render_template(

        "police_login.html",

        police_users=police_users

    )
# ======================================================
# DASHBOARD
# ======================================================

@app.route('/dashboard')
def dashboard():

    guest_mode = False

    if 'user' not in session:

        guest_mode = True

    conn = get_connection()

    cur = conn.cursor()

    # TOTAL VIOLATIONS

    cur.execute("SELECT COUNT(*) FROM violations")

    total_violations = cur.fetchone()[0]

    # TOTAL ACCIDENTS

    cur.execute("SELECT COUNT(*) FROM accidents")

    total_accidents = cur.fetchone()[0]

    # TOTAL FINES

    cur.execute(

        "SELECT COALESCE(SUM(fine),0) FROM violations"

    )

    total_fines = cur.fetchone()[0]

    # HOTSPOTS

    cur.execute("""

        SELECT COUNT(*)

        FROM (

            SELECT location

            FROM accidents

            GROUP BY location

            HAVING COUNT(*) >= 2

        ) AS hotspots

    """)

    hotspot_count = cur.fetchone()[0]

    # VIOLATION CHART

    cur.execute("""

        SELECT
            violation_type,
            COUNT(*)

        FROM violations

        GROUP BY violation_type

    """)

    violation_chart = cur.fetchall()

    # ACCIDENT CHART

    cur.execute("""

        SELECT
            severity,
            COUNT(*)

        FROM accidents

        GROUP BY severity

    """)

    severity_chart = cur.fetchall()

    violation_labels = [
        row[0] for row in violation_chart
    ]

    violation_values = [
        row[1] for row in violation_chart
    ]

    severity_labels = [
        row[0] for row in severity_chart
    ]

    severity_values = [
        row[1] for row in severity_chart
    ]

    conn.close()

    return render_template(

        "dashboard.html",

        total_violations=total_violations,

        total_accidents=total_accidents,

        total_fines=total_fines,

        hotspot_count=hotspot_count,

        violation_labels=violation_labels,

        violation_values=violation_values,

        severity_labels=severity_labels,

        severity_values=severity_values,
        guest_mode=guest_mode

    )


# ======================================================
# ADD VIOLATION
# ======================================================

@app.route('/add-violation',
           methods=['GET', 'POST'])

def add_violation():

    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':

        vehicle_no = request.form['vehicle_no']

        driver_name = request.form['driver_name']

        violation_type = request.form['violation_type']

        fine = request.form['fine']

        location = request.form['location']

        conn = get_connection()

        cur = conn.cursor()

        query = """

        INSERT INTO violations
        (
            vehicle_no,
            driver_name,
            violation_type,
            fine,
            location
        )

        VALUES(%s,%s,%s,%s,%s)

        """

        cur.execute(query, (

            vehicle_no,
            driver_name,
            violation_type,
            fine,
            location

        ))

        conn.commit()

        conn.close()

        return redirect('/view-violations')

    return render_template("add_violation.html")


# ======================================================
# VIEW VIOLATIONS
# ======================================================

@app.route('/view-violations')
def view_violations():

    if 'user' not in session:
        return redirect('/')

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT * FROM violations

        ORDER BY id DESC

    """)

    violations = cur.fetchall()

    conn.close()

    return render_template(

        "view_violations.html",

        violations=violations

    )


# ======================================================
# EDIT VIOLATION
# ======================================================

@app.route('/edit-violation/<int:id>',
           methods=['GET', 'POST'])

def edit_violation(id):

    if 'user' not in session:
        return redirect('/')

    # ADMIN ONLY

    if session.get('role') != 'admin' \
       and not session.get('admin'):

        return "Access Denied"

    conn = get_connection()

    cur = conn.cursor()

    if request.method == 'POST':

        vehicle_no = request.form['vehicle_no']

        driver_name = request.form['driver_name']

        violation_type = request.form['violation_type']

        fine = request.form['fine']

        location = request.form['location']

        query = """

        UPDATE violations

        SET
            vehicle_no=%s,
            driver_name=%s,
            violation_type=%s,
            fine=%s,
            location=%s

        WHERE id=%s

        """

        cur.execute(query, (

            vehicle_no,
            driver_name,
            violation_type,
            fine,
            location,
            id

        ))

        conn.commit()

        conn.close()

        return redirect('/view-violations')

    cur.execute(

        "SELECT * FROM violations WHERE id=%s",

        (id,)

    )

    violation = cur.fetchone()

    conn.close()

    return render_template(

        "edit_violation.html",

        violation=violation

    )


# ======================================================
# DELETE VIOLATION
# ======================================================

@app.route('/delete-violation/<int:id>')
def delete_violation(id):

    if 'user' not in session:
        return redirect('/')

    # ADMIN ONLY

    if session.get('role') != 'admin' \
       and not session.get('admin'):

        return "Access Denied"

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        "DELETE FROM violations WHERE id=%s",

        (id,)

    )

    conn.commit()

    conn.close()

    return redirect('/view-violations')


# ======================================================
# ADD ACCIDENT
# ======================================================

@app.route('/add-accident',
           methods=['GET', 'POST'])

def add_accident():

    if 'user' not in session:
        return redirect('/')

    if request.method == 'POST':

        location = request.form['location']

        latitude = request.form['latitude']

        longitude = request.form['longitude']

        severity = request.form['severity']

        casualties = request.form['casualties']

        reason = request.form['reason']

        evidence = request.files['evidence']

        filename = ""

        if evidence and evidence.filename != "":

            filename = secure_filename(
                evidence.filename
            )

            evidence.save(

                os.path.join(

                    app.config['UPLOAD_FOLDER'],

                    filename

                )

            )

        conn = get_connection()

        cur = conn.cursor()

        query = """

        INSERT INTO accidents
        (
            location,
            latitude,
            longitude,
            severity,
            casualties,
            reason,
            evidence
        )

        VALUES(%s,%s,%s,%s,%s,%s,%s)

        """

        cur.execute(query, (

            location,
            latitude,
            longitude,
            severity,
            casualties,
            reason,
            filename

        ))

        conn.commit()

        conn.close()

        return redirect('/view-accidents')

    return render_template("add_accident.html")


# ======================================================
# VIEW ACCIDENTS
# ======================================================

@app.route('/view-accidents')
def view_accidents():

    if 'user' not in session:
        return redirect('/')

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

        SELECT * FROM accidents

        ORDER BY id DESC

    """)

    accidents = cur.fetchall()

    conn.close()

    return render_template(

        "view_accidents.html",

        accidents=accidents

    )


# ======================================================
# EDIT ACCIDENT
# ======================================================

@app.route('/edit-accident/<int:id>',
           methods=['GET', 'POST'])

def edit_accident(id):

    if 'user' not in session:
        return redirect('/')

    # ADMIN ONLY

    if session.get('role') != 'admin' \
       and not session.get('admin'):

        return "Access Denied"

    conn = get_connection()

    cur = conn.cursor()

    if request.method == 'POST':

        location = request.form['location']

        severity = request.form['severity']

        casualties = request.form['casualties']

        reason = request.form['reason']

        query = """

        UPDATE accidents

        SET
            location=%s,
            severity=%s,
            casualties=%s,
            reason=%s

        WHERE id=%s

        """

        cur.execute(query, (

            location,
            severity,
            casualties,
            reason,
            id

        ))

        conn.commit()

        conn.close()

        return redirect('/view-accidents')

    cur.execute(

        "SELECT * FROM accidents WHERE id=%s",

        (id,)

    )

    accident = cur.fetchone()

    conn.close()

    return render_template(

        "edit_accident.html",

        accident=accident

    )


# ======================================================
# DELETE ACCIDENT
# ======================================================

@app.route('/delete-accident/<int:id>')
def delete_accident(id):

    if 'user' not in session:
        return redirect('/')

    # ADMIN ONLY

    if session.get('role') != 'admin' \
       and not session.get('admin'):

        return "Access Denied"

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        "DELETE FROM accidents WHERE id=%s",

        (id,)

    )

    conn.commit()

    conn.close()

    return redirect('/view-accidents')


# ======================================================
# HOTSPOTS
# ======================================================

@app.route('/hotspots')
def hotspots():

    if 'user' not in session:
        return redirect('/')

    conn = get_connection()

    cur = conn.cursor()

    query = """

    SELECT
        location,

        MAX(latitude) as latitude,

        MAX(longitude) as longitude,

        COUNT(*) as total_accidents

    FROM accidents

    WHERE
        latitude IS NOT NULL
        AND longitude IS NOT NULL

    GROUP BY location

    HAVING COUNT(*) >= 1

    ORDER BY total_accidents DESC

    """

    cur.execute(query)

    hotspot_data = cur.fetchall()

    conn.close()

    return render_template(

        "hotspots.html",

        hotspots=hotspot_data

    )


# ======================================================
# REPORTS
# ======================================================

@app.route('/reports')
def reports():

    if 'user' not in session:
        return redirect('/')

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM violations")
    total_violations = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM accidents")
    total_accidents = cur.fetchone()[0]

    cur.execute(
        "SELECT COALESCE(SUM(fine),0) FROM violations"
    )

    total_fines = cur.fetchone()[0]

    cur.execute("""

        SELECT COUNT(*)

        FROM (

            SELECT location

            FROM accidents

            GROUP BY location

            HAVING COUNT(*) >= 2

        ) AS hotspots

    """)

    hotspot_count = cur.fetchone()[0]

    conn.close()

    return render_template(

        "reports.html",

        total_violations=total_violations,

        total_accidents=total_accidents,

        total_fines=total_fines,

        hotspot_count=hotspot_count

    )


# ======================================================
# PROFILE
# ======================================================

@app.route('/profile')
def profile():

    if 'user' not in session:
        return redirect('/')

    return render_template("profile.html")


# ======================================================
# SETTINGS
# ======================================================

@app.route('/settings')
def settings():

    if 'user' not in session:
        return redirect('/')

    return render_template("settings.html")


# ======================================================
# ADMIN LOGOUT
# ======================================================

@app.route('/admin-logout')
def admin_logout():

    session.pop('admin', None)

    return redirect('/dashboard')
# ADD POLICE

@app.route('/add-police',
           methods=['GET', 'POST'])

def add_police():

    # ADMIN ONLY

    if not session.get('admin'):

        return "Access Denied"

    if request.method == 'POST':

        username = request.form['username']

        password = request.form['password']

        conn = get_connection()

        cur = conn.cursor()

        query = """

        INSERT INTO users
        (username, password, role)

        VALUES(%s,%s,%s)

        """

        cur.execute(query, (

            username,
            password,
            'police'

        ))

        conn.commit()

        conn.close()

        return redirect('/dashboard')

    return render_template("add_police.html")


# ======================================================
# MAIN LOGOUT
# ======================================================

@app.route('/logout')
def logout():

    session.pop('user', None)

    session.pop('role', None)

    session.pop('admin', None)

    return redirect('/dashboard')


# ======================================================
# RUN APP
# ======================================================

if __name__ == '__main__':

    app.run(debug=True)