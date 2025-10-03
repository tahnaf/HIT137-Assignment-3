from transformers import pipeline # pyright: ignore[reportMissingImports]

# 1. Initialize the Text Classification pipeline
classifier = pipeline(
    "zero-shot-classification", 
    model="facebook/bart-large-mnli"
)

# 2. Define test input and custom labels
text_to_analyze = "The parcel arrived soaking wet and the contents were ruined."
custom_labels = ["Shipping Damage", "Order Mistake", "General Inquiry", "Positive Feedback"]

# 3. Run the classification
result = classifier(text_to_analyze, custom_labels)

print("--- Text Classification Test Result ---")
print("Input:", result['sequence'])
print("Top Prediction:", result['labels'][0])
print("Confidence:", f"{result['scores'][0]*100:.2f}%")