from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import List

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/src/images", StaticFiles(directory="src/images"), name="images")

templates = Jinja2Templates(directory="templates")



# @app.get("/", response_class=HTMLResponse)
# def read_root():
#     return open("main.html", "r").read()

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )



@app.post("/upload-files")
async def create_upload_files(request: Request, files: List[UploadFile] = File(...)):
    for file in files:
        contents = await file.read()
        #save the file
        with open(f"src/images/{file.filename}", "wb") as f:
            f.write(contents)

    show = [file.filename for file in files]

    #return {"Result": "OK", "filenames": [file.filename for file in files]}
    return templates.TemplateResponse("index.html", {"request": request, "show": show})