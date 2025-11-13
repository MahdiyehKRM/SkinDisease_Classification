import uvicorn # type: ignore
from fastapi import FastAPI, File, UploadFile # type: ignore
import numpy as np # type: ignore
from io import BytesIO
from PIL import Image # type: ignore
import tensorflow as tf # type: ignore
app = FastAPI()

MODEL=tf.keras.models.load_model("my_model_cnn_v1.keras")
CLASS_NAMES=['1.Eczema','2.Melanoma','4.Basel Cell Carcinoma(BCC)','5.Melanocytic Nevi(NV)','7.Psoriasis pictures Lichen Planus and related diseases']


@app.get("/")
async def root():
    return {"message": "welcome to my website"}


@app.get("/ping")
async def ping():
    return "hello"

def read_file_as_image(data) -> np.ndarray:
    image=np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
    file: UploadFile=  File(...)

):
    
    image=read_file_as_image(await file.read())
    img_batch=np.expand_dims(image,0)

    predictions=MODEL.predict(img_batch)
    predicted_class=CLASS_NAMES[np.argmax(predictions[0])]
    confidence=np.max(predictions[0])

    return {
        'class':predicted_class, 
        'confidence':float(confidence)
    }

    pass


if __name__=="__main__":
    uvicorn.run(app, host='localhost' ,port=8000)