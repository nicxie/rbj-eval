from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from functools import wraps
from datetime import datetime
from collections import Counter

app = Flask(__name__)

app.secret_key = '123'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'userlogin'


mysql = MySQL(app)

#login/logout routes
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'logged_in' not in session or not session['logged_in']:
                flash('Please log in first.')
                return redirect(url_for('login'))

            user_role = session.get('role')
            if user_role not in allowed_roles:
                flash('Access denied. You do not have permission to view this page.')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Please log in first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/dashboard")
def dashboard(): 
    if 'logged_in' in session and session['logged_in']: 
#ADMIN
        if session['role'] == 'ADMIN':
            return render_template("dashboard.html")
#ACCOUNTING       
        elif session['role'] == 'ACCOUNTING SUPERVISOR':
            return render_template("employeedash.html")
        elif session['role'] == 'BOOKKEEPER':
            return render_template("employeedash.html")
        elif session['role'] == 'ACCOUNTS PAYABLE SPECIALIST':
            return render_template("employeedash.html")
        elif session['role'] == 'AUDIT SPECIALIST':
            return render_template("employeedash.html")
        elif session['role'] == 'BILLING SPECIALIST CDO':
            return render_template("employeedash.html")
        elif session['role'] == 'BILLING SPECIALIST DVO':
            return render_template("employeedash.html")
 #VP AND BRANCH AD
        elif session['role'] == 'VP-FINANCE':
                    return render_template("employeedash.html")
        elif session['role'] == 'BRANCH ADMINISTRATIVE SUPERVISOR':
                    return render_template("employeedash.html")
        
#CREDIT AND COLLECTION        
        elif session['role'] == 'CREDIT AND COLLECTION SUPERVISOR':
            return render_template("employeedash.html")
        elif session['role'] == 'CREDIT AND COLLECTION SPECIALIST':
            return render_template("employeedash.html")
        elif session['role'] == 'FIELD AUDITOR':
            return render_template("employeedash.html")
        elif session['role'] == 'FIELD COLLECTOR':
            return render_template("employeedash.html")
 #LOGISTICS       
        elif session['role'] == 'WAREHOUSE SUPERVISOR':
            return render_template("employeedash.html")
        elif session['role'] == 'LOGISTICS SPECIALIST':
            return render_template("employeedash.html")
        elif session['role'] == 'LOGISTICS CREW':
            return render_template("employeedash.html")
        elif session['role'] == 'PENDING ORDER SPECIALIST':
            return render_template("employeedash.html")
        elif session['role'] == 'COMPANY DRIVER':
            return render_template("employeedash.html")
              
#HR & OPERATIONS       
        elif session['role'] == 'HR MANAGER':
            return render_template("employeedash.html")
        elif session['role'] == 'IT ADMINISTRATOR':
            return render_template("employeedash.html")
        elif session['role'] == 'HR ASSISTANT':
            return render_template("employeedash.html")
        elif session['role'] == 'LIASON OFFICER':
            return render_template("employeedash.html")
        elif session['role'] == 'REPAIR AND VEHICLE MAINTENANCE SPECIALIST':
            return render_template("employeedash.html")
        elif session['role'] == 'UTILITY PERSONNEL':
            return render_template("employeedash.html")
        
        
 #PROCUREMENT       
        elif session['role'] == 'PROCUREMENT SPECIALIST':       
            return render_template("employeedash.html")
        elif session['role'] == 'PROCUREMENT SUPERVISOR':
            return render_template("employeedash.html")
#SALES
        elif session['role'] == 'FIELD SALES SUPERVISOR T1CDO':       
            return render_template("employeedash.html")
        elif session['role'] == 'FIELD SALES SUPERVISOR T2DVO':
            return render_template("employeedash.html")
        elif session['role'] == 'APPLICATIONS AND MARKETING HEAD':
            return render_template("employeedash.html")
        elif session['role'] == 'SALES COORDINATOR':       
            return render_template("employeedash.html")
        elif session['role'] == 'IMAGING SPECIALIST':       
            return render_template("employeedash.html")
        elif session['role'] == 'SALES OPERATION SPECIALIST ':
            return render_template("employeedash.html")
        elif session['role'] == 'IT SPECIALIST SALES ':       
            return render_template("employeedash.html")     
        elif session['role'] == 'PSSR ASOK':
            return render_template("employeedash.html")
        elif session['role'] == 'PROFESSIONAL SALES AND SERVICE REPRESENTATIVE':
            return render_template("employeedash.html")
        elif session['role'] == 'IMAGING HEAD':
            return render_template("employeedash.html")      
        
#TECHNICAL      
        elif session['role'] == 'AFTER SALES SUPPORT SUPERVISOR':
            return render_template("employeedash.html")  
        elif session['role'] == 'SERVICE TECHNICIAN':
           return render_template("employeedash.html")          
    else:   
        flash("Invalid user role.")
        return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def login():
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and user[2] == password:
            session['logged_in'] = True
            session['username'] = user[0]
            session['role'] = user[3]  # Store the user's role from the database
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid credentials. Please try again."
            return render_template("login.html", error=error)
        
    return render_template("login.html", error=None)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        role = request.form.get("role")  # Get the selected role from the form

        # Insert the new user into the database with the selected role
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password, role, fullname) VALUES (%s, %s, %s, %s)", (username, password, role, fullname))
        mysql.connection.commit()
        cursor.close()

        flash("User registration successful!")

        # Redirect to the "View Users" page after successful registration
        return redirect(url_for("view_users"))

    return render_template("register.html")


@app.route("/view_users")
def view_users():
    try:
        # Fetch all user data from the database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
        users_data = cursor.fetchall()
        cursor.close()

        return render_template("view_users.html", users=users_data)
    except Exception as e:
        return f"An error occurred: {str(e)}"

# ... Your existing code ...

@app.route("/delete_user/<int:user_id>", methods=["GET", "POST"])
@login_required
@role_required(allowed_roles=["ADMIN"])  # Only allow ADMIN to delete users
def delete_user(user_id):
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()
        flash("User deleted successfully.")
        return redirect(url_for("view_users"))

    return redirect(url_for("view_users"))

# ... Your existing code ...


    

@app.route("/logout")
def logout():
    session.pop('logged_in', None)  # Remove the 'logged_in' session variable
    session.pop('username', None)    # Optionally, remove the 'username' session variable
    return redirect(url_for("login"))




if __name__ == "__main__":
    app.run(debug=True)

            