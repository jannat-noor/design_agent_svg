from google import adk, genai
from google.genai.types import GenerateContentConfig
from google.cloud import storage
from .converters import convert_svg_to_png, convert_svg_to_jpeg, upload_to_gcs
from IPython.display import Image, Markdown, display
import re

# this design_agent takes user input as a TEXT, generates SVG image file, converts svg to png, jpeg, stores all three file in GCS bucket
# uses model gemini-2.5-flash, 
# gemini-2.5-flash-image-preview is not available
# image quality is not that good

# PROJECT_ID = "ai2396-intellimake-env4"
#LOCATION = "global"
#MODEL_ID = "gemini-2.5-flash"

import os
# Add credentials here or in the .env 
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "default-project")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
MODEL_ID = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "gemini-2.5-flash")

# Create Vertex AI client
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

def generate_image_to_svg(prompt: str) -> str:
    # Generate SVG content
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=f"Generate an SVG image based on this prompt: {prompt}. Only return valid SVG code.",
        config=GenerateContentConfig(
            response_modalities=["TEXT"],
            candidate_count=1,
        ),
    )

    svg_code = response.candidates[0].content.parts[0].text

    # Clean SVG
    import re
    match = re.search(r"<svg.*?>.*?</svg>", svg_code, re.DOTALL)
    if not match:
        raise ValueError("Model did not return valid SVG content.")
    clean_svg = match.group(0)

    # Save cleaned SVG
    svg_path = "/tmp/generated.svg"
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(clean_svg)


    # Convert and upload (call converters)
    png_path = convert_svg_to_png(svg_path, "/tmp/generated.png")
    jpeg_path = convert_svg_to_jpeg(svg_path, "/tmp/generated.jpg")

    # Display the generated PNG in IPython/Cloud Shell
    #display(Image(filename=png_path, width=400, height=400))

    # from PIL import Image
    # img = Image.open("/tmp/generated.png")
    # img.show()

    # Upload to GCS
    bucket_name = "noor-design-agent-2626"
    svg_uri = upload_to_gcs(svg_path, bucket_name, "generated/generated.svg")
    png_uri = upload_to_gcs(png_path, bucket_name, "generated/generated.png")
    jpeg_uri = upload_to_gcs(jpeg_path, bucket_name, "generated/generated.jpg")

    return f"SVG: {svg_uri}\nPNG: {png_uri}\nJPEG: {jpeg_uri}"


# Root agent
root_agent = adk.Agent(
    name="design_agent",
    description="Generates SVG images from text using Gemini 2.5 Flash, converts to PNG/JPEG, and saves all to GCS.",
    instruction="Generate images from user text prompts and save them in multiple formats to Google Cloud Storage.",
    model=MODEL_ID,
    tools=[generate_image_to_svg],
)
