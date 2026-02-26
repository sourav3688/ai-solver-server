# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from fastapi.staticfiles import StaticFiles
# import os
# import shutil

# from app.gpt_service import solve_question_from_image

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# # ✅ API ROUTE FIRST
# @app.post("/solve")
# async def solve_question(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     result = solve_question_from_image(file_path)
#     return result


# # ✅ Serve static files correctly
# app.mount("/static", StaticFiles(directory="static"), name="static")


# # ✅ Properly serve index.html
# @app.get("/")
# async def serve_home():
#     return FileResponse("static/index.html")


import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.solver import solve_question_from_image

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html") as f:
        return f.read()


@app.post("/solve")
async def solve(image: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, image.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    result = solve_question_from_image(file_path)

    return result