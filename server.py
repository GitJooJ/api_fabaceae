# Built-ins
from pathlib import Path

# Locals
from cerebrum import Identifier

# 3rd party
from fastapi import FastAPI, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware


ROOT_PATH = Path(__file__).resolve().parent
CACHE_PATH = Path( ROOT_PATH, 'cache' )

identifier = Identifier()
app = FastAPI()

# Middlewares

origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Routes

@app.post("/files/")
async def upload_file( file: UploadFile ):
    filepath = Path( CACHE_PATH, file.filename )
    content = await file.read()

    with open(filepath, 'wb') as new_file:
        new_file.write(content)

    return { "filename": file.filename }


@app.post("/ai")
async def identify_image( filename: str = Body(..., embed=True) ):
    try: filepath = Path(CACHE_PATH, filename)
    except: raise ValueError("File not found")

    if not ( filepath.is_file() ):
        raise TypeError("Not a file")

    plant_name, accuracy = identifier.identify_plant( filepath )
    return {
        "plant": plant_name,
        "accuracy": accuracy
    }
