from flask import Flask, redirect, render_template, session, url_for, request
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from urllib.parse import urlencode
from pathlib import Path
import os

# ✅ Load .env from same folder as app.py
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

# ✅ Debug: confirm correct CLIENT ID
print("🔍 Using CLIENT ID:", os.getenv("AUTH0_CLIENT_ID"))

# ✅ Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
app.config['SESSION_COOKIE_SECURE'] = False

# ✅ Register Auth0 using OpenID config
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# ✅ Home route
@app.route('/')
def home():
    user_info = session.get('user')
    return render_template('index.html', user=user_info)

# ✅ Login route
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=os.getenv("AUTH0_CALLBACK_URL"))

# ✅ Callback route (after login)
@app.route('/callback')
def callback():
    token = auth0.authorize_access_token()
    userinfo = token['userinfo']  # ✅ No nonce error
    session['user'] = {
        'name': userinfo['name'],
        'email': userinfo['email'],
        'picture': userinfo['picture']
    }
    return redirect('/')

# ✅ Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        f'https://{os.getenv("AUTH0_DOMAIN")}/v2/logout?' +
        urlencode({
            'returnTo': url_for('home', _external=True),
            'client_id': os.getenv("AUTH0_CLIENT_ID")
        })
    )

# ✅ Protected route
@app.route('/protected')
def protected():
    if 'user' not in session:
        return redirect('/login')
    return render_template('protected.html', user=session['user'])

# ✅ Run app
if __name__ == '__main__':
    app.run()
