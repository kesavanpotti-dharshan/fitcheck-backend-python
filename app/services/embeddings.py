from dotenv import load_dotenv
import os
from google import genai


load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def embed_text(text: str) -> list[float]:
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    print("Embedded text:" + str(result.embeddings[0].values))
    return result.embeddings[0].values
