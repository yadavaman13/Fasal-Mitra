# ML Model Directory

## Plant Disease Recognition Model

### Model Download Instructions

Due to file size limitations, the pre-trained model is not included in the repository. Please download it separately.

#### Steps:

1. **Download the Model**
   - Click [here](https://drive.google.com/file/d/1Ond7UzrNOfdAXWedjlZr2sDXYU6MRBuj/view?usp=sharing) to download the model
   - File name: `plant_disease_recog_model_pwp.keras`
   - Size: ~80MB

2. **Place the Model**
   - Save the downloaded file in this directory (`fasal-mitra/server/app/models/ml/`)
   - The final path should be: `fasal-mitra/server/app/models/ml/plant_disease_recog_model_pwp.keras`

3. **Verify Setup**
   ```bash
   ls fasal-mitra/server/app/models/ml/
   ```
   You should see `plant_disease_recog_model_pwp.keras` in the output.

## Model Details

- **Framework**: TensorFlow/Keras
- **Input Size**: 160x160x3 (RGB images)
- **Classes**: 39 disease classes
- **Crops Supported**: Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, Squash, Strawberry, Tomato

## Supported Disease Classes

The model can detect the following diseases:

### Apple
- Apple Scab
- Black Rot
- Cedar Apple Rust
- Healthy

### Corn
- Cercospora Leaf Spot (Gray Leaf Spot)
- Common Rust
- Northern Leaf Blight
- Healthy

### Grape
- Black Rot
- Esca (Black Measles)
- Leaf Blight (Isariopsis Leaf Spot)
- Healthy

### Tomato
- Bacterial Spot
- Early Blight
- Late Blight
- Leaf Mold
- Septoria Leaf Spot
- Spider Mites (Two-spotted Spider Mite)
- Target Spot
- Tomato Yellow Leaf Curl Virus
- Tomato Mosaic Virus
- Healthy

### Potato
- Early Blight
- Late Blight
- Healthy

### Other Crops
- Cherry (Powdery Mildew, Healthy)
- Peach (Bacterial Spot, Healthy)
- Pepper Bell (Bacterial Spot, Healthy)
- Orange (Huanglongbing/Citrus Greening)
- Strawberry (Leaf Scorch, Healthy)
- Squash (Powdery Mildew)
- Blueberry (Healthy)
- Raspberry (Healthy)
- Soybean (Healthy)

## Usage

The model is automatically loaded by the `MLDiseaseDetectionService` when the server starts.

```python
from app.services.ml_disease_service import get_ml_disease_service

service = get_ml_disease_service()
result = await service.detect_disease(image_bytes, crop_type="Tomato")
```
