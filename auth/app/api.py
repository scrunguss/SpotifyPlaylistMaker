from fastapi import FastAPI
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
import spotipy
from spotipy import oauth2
from fastapi.responses import RedirectResponse
import uuid

STATE_LENGTH=16

clientID = 'cfbac69fc1fb41f28dd001bf8f2114b9'
clientSecret = '3ec8cd1f469647afa658904334e760ce'
redirectURI = 'http://localhost:8000/'
scopes = 'user-read-private user-read-email user-library-modify user-library-read'
state = str(uuid.uuid4()).replace("-","")[0:STATE_LENGTH]

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

print("STATE : ",state)
sp_oauth = oauth2.SpotifyOAuth( clientID, clientSecret,redirectURI,scope=scopes,cache_path='.spotipyoauthcache',state=state)

@app.get("/",tags=["root"])
async def root(request : Request):
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = str(request.query_params)
        print("url is :",url)
        code = parse(url)
        print("CODE IS ",code)
        if code and code != '/':
            print("Found Spotify auth code in URL! Trying to get access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token found! Getting user info...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return results

    else:
        return "No Access Token."

@app.get("/login",tags=['login'])
async def login():
    return RedirectResponse(sp_oauth.get_authorize_url())


def parse(url):
    urlstate = url[url.rfind('=')+1:]
    print("STATE FOUND : ",urlstate)
    if state==urlstate:
        print("VALID RESPONSE")
    else:
        print("CSRF ATTACK DETECTED!")

    code = url[url.find('=')+1:url.rfind('&')]
    print("CODE FOUND :",code)
    return code