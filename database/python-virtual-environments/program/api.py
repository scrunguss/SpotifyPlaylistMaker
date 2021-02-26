from fastapi import FastAPI
from starlette.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

import server_interface

db : server_interface.DatabaseConnector #defines the type of this variable
db = server_interface.DatabaseConnector() #Inits connection with server

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

@app.get("/getUserByID", tags=["getUserByID"])
async def getUserByID(id : str):
    return db.getUser(id=id)

@app.get("/getUserByUsername", tags=["getUserByUsername"])
async def getUserByUsername(username : str):
    return db.getUser(username=username)

#Structure of post requests are defined as classes as such:
class addUserRequest(BaseModel):
    username: str
    spotifyID: str
    spotifyAuth: str
@app.post("/addUser",tags=["addUser"])
async def addUser(req : addUserRequest):
    return db.addUser(req.username, req.spotifyID, req.spotifyAuth)

class addPlaylistRequest(BaseModel):
    link: str
    id: int

@app.post("/addUserPlaylist", tags=["addUserPlaylist"])
async def addUserPlaylist(req : addPlaylistRequest):
    return db.addPlaylist(req.link, userID=req.id)

@app.post("/addGroupPlaylist", tags=["addGroupPlaylist"])
async def addGroupPlaylist(req : addPlaylistRequest):
    return db.addPlaylist(req.link, groupID=req.id)

@app.get("/getUserPlaylists", tags=["getUserPlaylists"])
async def getUserPlaylists(id : int):
    return db.getPlaylists(userID=id)

@app.get("/getGroupPlaylists", tags=["getGroupPlaylists"])
async def getGroupPlaylists(id : int):
    return db.getPlaylists(groupID=id)
    

    





