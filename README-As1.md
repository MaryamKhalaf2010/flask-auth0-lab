# Flask Auth0 Logging & Monitoring Lab

## Author
**Maryam Khalaf**

##  YouTube Demo
[Watch Demo](https://www.youtube.com/watch?v=YOUR_DEMO_LINK_HERE)

---

##  Project Overview
This project demonstrates how to:
- Secure a Flask app with Auth0
- Deploy it to Azure App Service
- Monitor access to protected routes using Azure Monitor Logs
- Set up alerts when unauthorized or excessive access occurs

---

##  Setup Steps

### 1. Auth0 Configuration
- Sign up at [Auth0.com](https://auth0.com) and create a new tenant and app.
- In the Auth0 app settings:
  - **Allowed Callback URLs**: `https://flask-auth0-maryam123-f4gqc5engagcfkc5.canadacentral-01.azurewebsites.net/callback`
  - **Allowed Logout URLs**: `https://flask-auth0-maryam123-f4gqc5engagcfkc5.canadacentral-01.azurewebsites.net`
- Enable the **Username-Password-Authentication** connection
- Copy your `Client ID`, `Client Secret`, and `Domain`

---

### 2. Azure Deployment
- Create the following Azure resources:
  - Resource Group
  - App Service Plan
  - Azure App Service for Flask
  - Log Analytics Workspace
- Enable **AppServiceConsoleLogs** and link App Service to Log Analytics

---

### 3. `.env` File
Create a `.env` file in the root directory:

```env
AUTH0_CLIENT_ID=your_auth0_client_id
AUTH0_CLIENT_SECRET=your_auth0_client_secret
AUTH0_DOMAIN=your_auth0_domain
AUTH0_CALLBACK_URL=https://flask-auth0-maryam123-f4gqc5engagcfkc5.canadacentral-01.azurewebsites.net/callback
AUTH0_AUDIENCE=https://your-auth0-domain/userinfo
SECRET_KEY=your_flask_secret_key
```

---

##  Logging & Detection Logic

### Logging (in `app.py`)
```python
@app.route('/protected')
def protected():
    if 'user' not in session:
        # Log unauthorized access attempt
        app.logger.warning(f"UNAUTHORIZED_ACCESS: ip={request.remote_addr}, timestamp={datetime.utcnow().isoformat()}")
        return redirect('/login')

    # Log valid access
    user_id = session['user'].get('sub', 'unknown')
    app.logger.info(f"PROTECTED_ACCESS: user_id={user_id}, timestamp={datetime.utcnow().isoformat()}")
    return render_template('protected.html', user=session['user'])
```

Logs are sent to Azure Log Analytics using `AppServiceConsoleLogs`.

---

##  Log Monitoring (KQL)

### KQL Query to Track Accesses
```kql
AppServiceConsoleLogs
| where TimeGenerated > ago(24h)
| where ResultDescription has "PROTECTED_ACCESS"
| parse ResultDescription with * "user_id=" user_id ", timestamp=" timestamp
| summarize AccessCount = count(), LastAccess = max(TimeGenerated) by user_id
| where AccessCount >= 1
| project user_id, LastAccess, AccessCount


```

### Result
Shows users who accessed `/protected` more than 10 times in the last 15 minutes.

---

##  Azure Alert Setup

### Alert Rule
- **Signal type**: *Custom log search*
- **Condition**: Use the KQL above
- **Threshold**: > 10 access events per user in 15 mins
- **Action Group**: Email notification to `khal0233@algonquinlive.com`
- **Severity**: 3 (Low)

---

##  HTTP Test File

`test-app.http` (for [REST Client Extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)):

```http
### 1. Access login page (simulate valid login redirect)
GET https://flask-auth0-maryam123-f4gqc5engagcfkc5.canadacentral-01.azurewebsites.net/login
Accept: text/html

###

### 2. Access protected route after login (use real session cookie)
GET https://flask-auth0-maryam123-f4gqc5engagcfkc5.canadacentral-01.azurewebsites.net/protected
Cookie: session=YOUR_REAL_SESSION_COOKIE
Accept: text/html

###

### 3. Access protected route without logging in (unauthorized)
GET https://flask-auth0-maryam123-f4gqc5engagcfkc5.canadacentral-01.azurewebsites.net/protected
Accept: text/html
```

---

##  Final Output

-  Logging user actions and unauthorized attempts
-  Analyzing logs with KQL
-  Triggering alerts when thresholds are exceeded
-  Alerts sent to instructor via email

---

> Built with  by **Maryam Khalaf**
