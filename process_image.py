import os
from google.cloud import documentai_v1 as documentai


def process_image_with_document_ai(
    project_id: str, location: str, processor_id: str, file_path: str, key_path: str
):
    # Set up Google Cloud authentication
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

    # Create a Document AI client
    client = documentai.DocumentProcessorServiceClient()

    # Processor name (update with your project and processor details)
    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    # Load the image file
    with open(file_path, "rb") as image_file:
        image_content = image_file.read()

    # Create a raw document request
    raw_document = documentai.RawDocument(
        content=image_content, mime_type="image/jpeg"
    )  # Update MIME type if needed

    # Request to process the document
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    result = client.process_document(request=request)

    # Extract the text from the response
    document = result.document

    extracted_text = document.text
    extracted_text = extracted_text.replace("\n", " ")

    # Extract entities from the document
    entities = [
        {
            "type": entity.type_,
            "value": entity.mention_text,
            "confidence": entity.confidence,
        }
        for entity in document.entities
    ]

    input_variables = {"extracted_data_from_bill": extracted_text, "entities": entities}

    return input_variables
