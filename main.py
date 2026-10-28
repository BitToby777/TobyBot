from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import tobybot_engine

app = FastAPI()

class Question(BaseModel):
    user_question: str
    ID_number: int

class Topic(BaseModel):
    user_topic: str
    ID_number: int

# The Javascript and image files will be in the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def return_homepage():
    with open("index.html", "r") as homepage_file:
        homepage_html = homepage_file.read()
    return homepage_html
    
@app.get("/about", response_class=HTMLResponse)
async def return_about_page():
    with open("about.html", "r") as aboutpage_file:
        about_page_html = aboutpage_file.read()
    return about_page_html
    
@app.post("/ask_question/")
async def ask_question(user_question: Question):
    answers = tobybot_engine.ask_question(user_question.user_question, user_question.ID_number)
    print(answers)
    return {"answers": answers}
    
@app.post("/choose_topic/")
async def choose_topic(user_topic: Topic):
    response = tobybot_engine.choose_topic(user_topic.user_topic, user_topic.ID_number)
    print(user_topic.user_topic)
    print(user_topic.ID_number)
    return { "response": response }
    
