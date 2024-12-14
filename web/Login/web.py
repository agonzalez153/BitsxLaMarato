from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from supabase import create_client, Client

# Create a client
SUPABASE_URL = "https://supdrzpdynaekvysaeio.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN1cGRyenBkeW5hZWt2eXNhZWlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQxODQzNjAsImV4cCI6MjA0OTc2MDM2MH0.PpDKwNEUt2l5h2rISdhjgjShzKijozx_dmnKoLFFSMM"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN1cGRyenBkeW5hZWt2eXNhZWlvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNDE4NDM2MCwiZXhwIjoyMDQ5NzYwMzYwfQ.dXYfGmjRFFUL0bUOytGUur8eGS5VxbndLlnmqhThHN4'  # Replace with your secret key
app.config['DEBUG'] = True
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, email):
        self.id = email


@login_manager.user_loader
def load_user(email):
    return User(email)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            user = User(email)
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Email o contraseña incorrectos, por favor, revíselos.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.user:
            flash('¡Tu cuenta ha sido logeada correctamente!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error de registro, por favor, comprueba todos los datos.', 'danger')
    return render_template('register.html')


@app.route('/profile')
@login_required
def profile():
    return 'Logged in as: ' + current_user.id


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(port=5000)