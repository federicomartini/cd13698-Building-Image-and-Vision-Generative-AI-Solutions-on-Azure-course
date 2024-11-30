# main.py

# Import functions from other modules
from whisper import transcribe_audio
from dalle import generate_image
from vision import describe_image, annotate_image
from gpt import classify_with_gpt

# Main function to orchestrate the workflow


def main():
    """
    Orchestrates the workflow for handling customer complaints.
    
    Steps include:
    1. Transcribe the audio complaint.
    2. Create a prompt from the transcription.
    3. Generate an image representing the issue.
    4. Describe the generated image.
    5. Annotate the reported issue in the image.
    6. Classify the complaint into a category/subcategory pair.
    
    Returns:
    None
    """
    # TODO: Call the function to transcribe the audio complaint.
    # !!!   Not Mandatory for the Project Rubric - The transcription is in
    #       output/transcription.txt

    # TODO: Create a prompt from the transcription.
    with open("./output/transcription.txt", "r") as file:
        prompt = file.read()

    # TODO: Generate an image based on the prompt.
    image_path = generate_image()
    if image_path == None:
        return None

    # TODO: Describe the generated image.
    description = describe_image()

    # TODO: Annotate the reported issue in the image.
    annotate_image(image_path, "output/image_description.txt", "output/annotated_image.png")

    # TODO: Classify the complaint based on the image description.
    classification = classify_with_gpt()

    # TODO: Print or store the results as required.
    print(classification)

    pass  # Replace this with your implementation

# Example Usage (for testing purposes, remove/comment when deploying):
if __name__ == "__main__":
    main()
