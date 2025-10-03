from google.cloud import storage
import cairosvg
from PIL import Image

def get_storage_client():
    # Create a storage client
    return storage.Client()  

def upload_to_gcs(local_file: str, bucket_name: str, blob_name: str) -> str:
    # Upload file to GCS  
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_file)
    return f"gs://{bucket_name}/{blob_name}"

def convert_svg_to_png(svg_path: str, output_path: str) -> str:
    # Convert SVG file to PNG
    cairosvg.svg2png(url=svg_path, write_to=output_path)
    return output_path

def convert_svg_to_jpeg(svg_path: str, output_path: str) -> str:
    # Convert SVG file to JPEG
    temp_png = "temp.png"
    cairosvg.svg2png(url=svg_path, write_to=temp_png)
    img = Image.open(temp_png).convert("RGB")
    img.save(output_path, "JPEG")
    return output_path

def convert_png_to_jpeg(png_path: str, output_path: str) -> str:
    """
    Convert a PNG file to JPEG format.
    Ensures conversion to RGB before saving to avoid transparency issues.
    """
    img = Image.open(png_path).convert("RGB")
    img.save(output_path, "JPEG")
    return output_path
