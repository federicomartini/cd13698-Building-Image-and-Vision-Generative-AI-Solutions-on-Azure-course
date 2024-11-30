# gpt.py
from config import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, GPT_VERSION, GPT_DEPLOYMENT
from utils import create_openai_client
import os
import openai

# Function to classify the customer complaint based on the image description


def classify_with_gpt():
    """
    Classifies the customer complaint into a category/subcategory based on the image description.

    Returns:
    str: The category and subcategory of the complaint.
    """
    # TODO: Create a prompt that includes the image description and other relevant details.
    with open("./output/transcription.txt", "r") as file:
        image_description = file.read()
    with open("./categories.json", "r") as file:
        categories = file.read()

    prompt = f"You are an expert. I want to know the best category and subcategory in a JSON format for this case: {image_description}. The categories and subcategories to choose from are listed in JSON format as follows: {categories}"
        
    # TODO: Call the GPT model to classify the complaint based on the prompt.
    client = create_openai_client(GPT_VERSION, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)
    response = client.chat.completions.create(
        model=GPT_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a techincal expert and a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ]
            }
        ],
        max_tokens=1024
    )

    # TODO: Extract and return the classification result.

    classification = response.choices[0].message.content

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, "classification.txt")
    with open(file_path, "w") as file:
        file.write(classification)

    return classification  # Replace this with your implementation

# Example Usage (for testing purposes, remove/comment when deploying):
# if __name__ == "__main__":
#     classification = classify_with_gpt()
#     print(classification)
