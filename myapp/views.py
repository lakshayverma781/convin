# views.py

from django.shortcuts import redirect
from django.views.generic import View
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

# Replace these values with your own OAuth2 client ID and client secret
CLIENT_ID = '357480382078-tf59f2lv6ho8bls3kccm7s3ei3o9ac9b.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect/'


class GoogleCalendarInitView(View):
    def get(self, request, *args, **kwargs):
        flow = Flow.from_client_config(
            client_config={'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET},
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri=REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        request.session['google_auth_state'] = state
        return redirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request, *args, **kwargs):
        if 'code' in request.GET:
            flow = Flow.from_client_config(
                client_config={'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET},
                scopes=['https://www.googleapis.com/auth/calendar'],
                redirect_uri=REDIRECT_URI,
                state=request.session['google_auth_state']
            )
            flow.fetch_token(code=request.GET['code'])
            credentials = flow.credentials
            request.session['google_credentials'] = credentials.to_json()
            return redirect('/rest/v1/calendar/events/')
        else:
            return redirect('/rest/v1/calendar/init/')
