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
    prompt = """In JSON format without markdown syntax, describe the image thoroughly and put it in a field named 
            Description. Then list problems in a list named KeyElements that are strictly tied to the complaint,
            and for each element named Element add the coordinates in a list named Coordinates containing the values
            for the value X, Y (centered very precisely on the defect), Width and Height of the rectange to draw and
            centered in X, Y, along with a field to show the confidence named Confidence as a real number from 0
            to 1 about that being an issue"""

    try:
        response = client.chat.completions.create(
            model=GPT_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a techincal expert and a helpful assistant."},
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
        coordinates = element['Coordinates']
        x, y, w, h = coordinates['X'], coordinates['Y'], coordinates['Width'], coordinates['Height']
        confidence = element['Confidence']

        # Disegna il riquadro attorno all'elemento
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Colore verde per il riquadro

        # Aggiungi l'etichetta dell'elemento sopra il riquadro
        text = f"{label} ({confidence*100:.2f}%)"
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Salva l'immagine annotata
    cv2.imwrite(output_path, image)
    print(f"Image annotated and saved to {output_path}")

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     description = describe_image()
#     print(description)
