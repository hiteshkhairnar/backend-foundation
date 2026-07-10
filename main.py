from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Mission Global Engineer - Backend Started 🚀"}

@app.get("/about")
def about():
    return {
        "name": "Hitesh Khairnar",
        "role": "Backend Developer & AI Engineer",
        "mission": "Mission Global Engineer"
    }