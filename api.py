from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import JSONResponse
from gtts import gTTS
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydub import AudioSegment
from pydub.playback import play
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class F(BaseModel):
    file_name:str

@app.get("/pdf-files")
async def get_pdf_files():
    output_folder = "/home/aryan/deep-spark-mentor-ai/backend/output/Chapter_29__Electric_Field_and_Potential"
    try:
        pdf_files = [
            file for file in os.listdir(output_folder) if file.endswith(".txt")
        ]
        
        pdf_files.sort()
        print(f"PDF files found: {pdf_files}")
        return JSONResponse(content={"pdf_files": pdf_files})
    except FileNotFoundError:
        return JSONResponse(content={"error": "Output folder not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@app.post("/start-teaching")
async def start_teaching(f: F):
    output_folder = "/home/aryan/deep-spark-mentor-ai/backend/output/Chapter_29__Electric_Field_and_Potential"
    try:
        file_path = os.path.join(output_folder, f.file_name)
        if not os.path.exists(file_path):
            return JSONResponse(content={"error": "File not found"}, status_code=404)

        with open(file_path, "r", encoding="utf-8") as file:
            text_content = file.read()
        # Remove asterisks (*) from the text content
        text_content = text_content.replace("*", "")
        # Replace backticks (`) with spaces and slashes (/) with "divide by"
        text_content = text_content.replace("`", " ").replace("/", " divide by ")
        # Convert text to speech
        tts = gTTS(text_content, lang="en", slow=False)  # Adjust 'slow' for speed control
        # tts.save("temp.mp3")

        # Optional: Adjust pitch or other properties using pydub
        # audio = AudioSegment.from_file("temp.mp3")
        # audio.export("part.mp3", format="mp3")
        audio_path = "part.mp3"
        tts.save(audio_path)

        return FileResponse(audio_path, media_type="audio/mpeg", filename="part.mp3")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
