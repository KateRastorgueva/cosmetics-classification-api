from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import io
import torch
import torch.nn as nn
from torchvision import transforms, models

app = FastAPI(title="Cosmetics Classification API")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class_names = ['eyeshadow', 'foundation', 'lipstick', 'mascara', 'other']
model = models.resnet18(weights=None)
model.fc = nn.Linear(512, 5)
model.load_state_dict(torch.load("model/cosmetics_model.pt", map_location=device))
model = model.to(device)
model.eval()
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def get_prediction(image_tensor):
    model.eval()
    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        return predicted_class, probabilities.cpu().numpy()[0]
# GET /health — проверка работоспособности сервиса
@app.get("/health")
async def health():
    return {"status": "ok"}

# POST /predict — принимает изображение, возвращает JSON
# Валидация входных данных и обработка ошибок
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(status_code=400, detail="фНеверный формат")
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Файл больше 10 МБ")
    
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        predicted_idx, probabilities = get_prediction(image_tensor)
        
        predicted_class = class_names[predicted_idx]
        probability = float(probabilities[predicted_idx])
        all_classes = {class_names[i]: float(probabilities[i]) for i in range(len(class_names))}
        
        return {
            "class": predicted_class,
            "probability": probability,
            "all_classes": all_classes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка {str(e)}")

# Реализуйте запуск приложения через Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
