from transformers import pipeline
from PIL import Image

# 1. Initialize the Image Classification pipeline
image_classifier = pipeline("image-classification")

# 2. *** ABSOLUTELY ENSURE THIS PATH IS CORRECT ***
# Example: image_file_path = "C:/Users/User/Pictures/my_dog.jpg"
image_file_path = "C:/Users/User/Pictures/tabby_cat.jpg"

# 3. Load the image
# If the path is wrong, this line will cause an error that Python MUST display.
image = Image.open(image_file_path)

# 4. Run the classification
result = image_classifier(image)

# 5. Print the result
print("\n--- Image Classification Test Result ---")
print("Image Path:", image_file_path)
print("Model's Top Prediction:", result[0]['label'])
print("Confidence:", f"{result[0]['score']*100:.2f}%")