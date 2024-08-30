from dotenv import load_dotenv
import os
from nylas import Client
from flask import Flask, request, redirect, url_for, session, jsonify, render_template
from flask_session.__init__ import Session
from nylas.models.auth import URLForAuthenticationConfig
from nylas.models.auth import CodeExchangeRequest
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

nylas = Client(
    api_key = os.environ.get("NYLAS_API_KEY"),
    api_uri = os.environ.get("NYLAS_API_URI"),
)

@app.route("/nylas/auth", methods=["GET"])
def login():
  if session.get("grant_id") is None:
    config = URLForAuthenticationConfig({"client_id": os.environ.get("NYLAS_CLIENT_ID"), 
        "redirect_uri" : "http://127.0.0.1:5000/oauth/exchange"})

    url = nylas.auth.url_for_oauth2(config)

    return redirect(url)
  else:
    return redirect(url_for("recent_emails"))  
  
@app.route("/oauth/exchange", methods=["GET"])
def authorized():
  if session.get("grant_id") is None:
    code = request.args.get("code")

    exchangeRequest = CodeExchangeRequest({"redirect_uri": "http://127.0.0.1:5000/oauth/exchange",
        "code": code, "client_id": os.environ.get("NYLAS_CLIENT_ID")})

    exchange = nylas.auth.exchange_code_for_token(exchangeRequest)
    session["grant_id"] = exchange.grant_id

    return redirect(url_for("recent_emails"))   

@app.route("/nylas/recent-emails", methods=["GET"])
def recent_emails():
    if session.get("grant_id") is None:
        return redirect(url_for("login"))
    
    query_params = {"limit": 5}

    try:
        messages, _, _ = nylas.messages.list(session["grant_id"], query_params)
        emails = [message.to_dict() for message in messages]

        # Pass the emails list to the template
        return render_template('emails.html', emails=emails)
    except Exception as e:
        return f'Error fetching emails: {e}', 500

@app.route("/nylas/send-email", methods=["GET","POST"])
def send_email():
  if request.method == "POST":
     try:
      subject = request.form.get("subject")
      body = request.form.get("body")
      recipient_name = request.form.get("recipient_name")
      recipient_email = request.form.get("recipient_email")
      email_body = {"subject" : subject,
          "body":body,
          "reply_to":[{"name": "Name", "email": os.environ.get("EMAIL")}],
          "to":[{"name": recipient_name, "email": recipient_email}]}
      message = nylas.messages.send(session["grant_id"], request_body = email_body).data
      # return jsonify(message)
      # Return the form with a success message
      return render_template('send_email.html', success=True)
     except Exception as e:
            return f'Error: {e}', 500
  else:
    return render_template('send_email.html')   

# Custom filter to convert Unix timestamp to a readable date format
@app.template_filter('format_datetime')
def format_datetime(value, format='%B %d, %Y %I:%M %p'):
    return datetime.fromtimestamp(value).strftime(format)



if __name__ == "__main__":
  app.run(debug=True)   