from google.cloud import aiplatform
from dotenv import load_dotenv
import os

load_dotenv()

aiplatform.init(project="root-isotope-465710-h1", location="us-central1")
print("Authenticated and ready to use Vertex AI.")
