# Flask Auth0 Login App — CST8919 Lab 1

This project is a Flask web application that demonstrates secure user authentication using **Auth0**. It allows users to log in and log out, and access a protected route available only to authenticated users.

## 🔐 Auth0 Integration

- Users are authenticated through Auth0 (OAuth 2.0 / OpenID Connect).
- User info (name, email, picture) is stored in the Flask session after login.
- Auth0 handles login UI, tokens, and session security.

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/MaryamKhalaf2010/flask-auth0-lab.git
cd flask-auth0-lab
```
### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
### 4. Create a .env File

In the root folder, create a file called .env and add the following values:

```bash
AUTH0_CLIENT_ID=your_auth0_client_id
AUTH0_CLIENT_SECRET=your_auth0_client_secret
AUTH0_DOMAIN=your_domain.auth0.com
AUTH0_CALLBACK_URL=http://127.0.0.1:5000/callback
APP_SECRET_KEY=your_random_secret_key
```

### 5. Run the App

```bash
flask run
```

Open your browser at: http://127.0.0.1:5000

## Demo Video
### Watch Demo (YouTube)

https://youtu.be/6s95eMxwMjo

The video includes:

A walkthrough of login/logout

Access to protected route

Explanation of how Auth0 and Flask integration works

## Author
Maryam Khalaf.
For CST8919 - Secure Web Application Development



