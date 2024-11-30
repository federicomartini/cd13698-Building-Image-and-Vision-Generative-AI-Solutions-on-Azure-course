# dalle.py
from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, DALLE_VERSION, DALLE_DEPLOYMENT
from utils import create_openai_client, generate_image
import os
import json
import requests

# Function to generate an image representing the customer complaint


def generate_image():
    """
    Generates an image based on a prompt using OpenAI's DALL-E model.

    Returns:
    str: The path to the generated image.
    """
    
    # TODO: Create a prompt to represent the customer complaint.
    with open("./output/transcription.txt", "r") as file:
        transcription_text = file.read()

    prompt = "Realistic photo showing very accurately the defects described in a complain. The complaint is the following: " + transcription_text
    print(prompt)
    
    # TODO: Call the DALL-E model to generate an image based on the prompt.
    dalle = create_openai_client(DALLE_VERSION, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)

    try:
        result = dalle.images.generate(
            model=DALLE_DEPLOYMENT,
            prompt=prompt,
            size="1024x1024",
            style="vivid"
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    json_response = json.loads(result.model_dump_json())
    image_url = json_response["data"][0]["url"]
    
    # TODO: Download the generated image and save it locally.
    output_dir = "output"
    output_file = os.path.join(output_dir, "generated_image.png")
    
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Image saved successfully to {output_file}")
    else:
        print(f"Failed to download image. HTTP Status: {response.status_code}")
        pass
    
    return output_file  # Replace this with your implementation

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     image_path = generate_image()
#     print(f"Generated image saved at: {image_path}")
