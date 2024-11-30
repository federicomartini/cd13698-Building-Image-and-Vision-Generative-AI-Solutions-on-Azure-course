# vision.py

from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, GPT_VERSION, GPT_DEPLOYMENT
from utils import create_openai_client
import openai
import os
import base64
from mimetypes import guess_type
import cv2
import json

# Function to describe the generated image and annotate issues


def describe_image():
    """
    Describes an image and identifies key visual elements related to the customer complaint.

    Returns:
    str: A description of the image, including the annotated details.
    """
    # TODO: Load the generated image.
    image_path = "./output/generated_image.png"
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'

    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(
            image_file.read()).decode('utf-8')

    data_url = f"data:{mime_type};base64,{base64_encoded_data}"

    # TODO: Call the model to describe the image and identify key elements.
    client = create_openai_client(GPT_VERSION, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)
    prompt = """Take a step-by-step approach: 1) Evaluate the image to understand the objects you see
                2) In JSON format without markdown syntax, creat a JSON Object
                containing the following fields: "Description"
                where you have to describe the image in detail; "KeyElements", an array of all product defects you see.
                The objects contained in the "KeyElements" array have the
                following attributes: "Element": the defect description, "Confidence": a real number from 0 to 1 about the
                confidence you have for it to be a defect, "X": the X location of the center of the area containing
                the defect in the image, "Y": "X": the Y location of the center of the area containing the defect
                in the image, "Width": the width of the rectangle as a boundary box for the defect which is centered in (X,Y), "Height": The height
                of the rectangle to draw as a boundary box for which is centered in (X,Y)"""

    try:
        response = client.chat.completions.create(
            model=GPT_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a techincal expert."},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]
                }
            ],
            max_tokens=1024
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    # TODO: Extract the description and return it.
    description = response.choices[0].message.content

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, "image_description.txt")
    with open(file_path, "w") as file:
        file.write(description)
        
    #annotate_image(image_path, "output/image_description.txt", "output/annotated_image.png")

    return description  # Replace this with your implementation

def annotate_image(image_path, json_path, output_path):
    # Carica l'immagine
    image = cv2.imread(image_path)

    # Carica il file JSON che contiene i difetti (o gli elementi da annotare)
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Itera sugli "elementi" nel file JSON (KeyElements)
    for element in data['KeyElements']:
        label = element['Element']
        x = element['X']
        y = element['Y']
        width = element['Width']
        height = element['Height']
        confidence = element['Confidence']

        # Calcola le coordinate x1, y1 (top-left) e x2, y2 (bottom-right) del rettangolo
        x1 = int(x - width / 2)
        y1 = int(y - height / 2)
        x2 = int(x + width / 2)
        y2 = int(y + height / 2)

        # Disegna il riquadro attorno all'elemento usando le coordinate calcolate
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Colore verde per il riquadro

        # Aggiungi l'etichetta dell'elemento sopra il riquadro
        text = f"{label} ({confidence*100:.2f}%)"
        cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Salva l'immagine annotata
    cv2.imwrite(output_path, image)
    print(f"Image annotated and saved to {output_path}")

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     description = describe_image()
#     print(description)
