[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fnext.js%2Ftree%2Fcanary%2Fexamples%2Fhello-world&env=CLIENT_ID,API_KEY,API_URI&envDescription=Client%20ID%20and%20API%20Key%20can%20be%20found%20and%20generated%20respectively%20on%20your%20Nylas%20Dashboard.%20For%20API%20URI%20you%20choose%20between%20'https%3A%2F%2Fapi.us.nylas.com'%20or%20'https%3A%2F%2Fapi.eu.nylas.com'%20depending%20on%20the%20region%20of%20your%20application.&envLink=https%3A%2F%2Fdeveloper.nylas.com%2Fdocs%2Fv3%2Fgetting-started%2Fset-up%2F&project-name=my-nylas-email-app&repository-name=my-nylas-email-app) [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/saif2khan/quickstart-email-python) [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://www.heroku.com/deploy?template=https://github.com/heroku/node-js-getting-started)

# How to run

1. Install the dependencies

```bash
pip3 install Flask, dotenv
```

2. Run the project

```bash
python quickstart-email-python.py
```

3. In the Nylas dashboard, create a new application and set the hosted auth callback URL to `http://localhost:5000/oauth/exchange`

4. env variables

```env
NYLAS_CLIENT_ID=""
NYLAS_API_KEY=""
NYLAS_API_URI="https://api.us.nylas.com"
EMAIL="<RECIPIENT_EMAIL_ADDRESS_HERE>"
```

5. Open your browser and go to `http://localhost:5000/nylas/auth` and log in and end user account. Enjoy!
