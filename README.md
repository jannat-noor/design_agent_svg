# Design Agent SVG

This project implements a **design agent** using **Google ADK** and **Vertex AI**.  
The agent generates SVG images from text prompts, converts them to PNG and JPEG, and uploads all files to **Google Cloud Storage (GCS)**.

## Features
- Generate images from user text prompts in **SVG** format.
- Convert SVG images to **PNG** and **JPEG**.
- Upload all images to **GCS** and optionally save locally.

## Setup

1. **Clone repository**
```bash
git clone https://github.com/jannat-noor/design_agent_svg.git
cd design_agent_svg
```
2. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Create .env file with your configuration:**
```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
```
4. **(Optional) Activate virtual environment**
```bash
source .venv/bin/activate
```
## Usage

- Run directly with Python
- python agent.py

## Run using Docker
```bash
docker build -t design-agent .
docker run --env-file .env design-agent
```

## Notes

- Model used: gemini-2.5-flash
- Currently generates basic SVG images; quality can be improved by generating PNG directly or using a different model.

## Files
- agent.py — Main agent code
- converters.py — SVG/PDF/PNG conversion and GCS upload
- requirements.txt — Python dependencies
- .env — Environment variables (not included in repo)
- Dockerfile — Container setup



