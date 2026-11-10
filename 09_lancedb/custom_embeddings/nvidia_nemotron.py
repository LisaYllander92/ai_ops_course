import os
from dotenv import load_dotenv                     
from openai import OpenAI                           # OpenAI-klienten (används mot NVIDIAs API)
from lancedb.embeddings import TextEmbeddingFunction, get_registry  # LanceDB:s ramverk för embeddings
import numpy as np

load_dotenv()  # Laddar NVIDIA_API från .env

# Skapar en klient som pratar med NVIDIAs OpenAI-kompatibla endpoint
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",  # NVIDIAs API istället för OpenAI
    api_key=os.getenv("NVIDIA_API"),                 # API-nyckel från miljövariabel
    max_retries=3,                                   # Försöker igen upp till 3 gånger vid fel
    timeout=60,                                      # Avbryter efter 60 sekunder
)


# Registrerar klassen i LanceDB under namnet "nvidia-nemotron"
# så den kan användas via get_registry().get("nvidia-nemotron")
@get_registry().register("nvidia-nemotron")
class NvidiaNemotronEmbedding(TextEmbeddingFunction):
    model: str = "nvidia/nemotron-3.5-embed-8b"  # Vilken embedding-modell som används
    dimensions: int = 4096                       # Antal dimensioner i vektorn

    def ndims(self) -> int:
        # LanceDB frågar efter vektorstorleken för att skapa rätt tabellschema
        return self.dimensions

    def _embed_one(self, text: str, input_type: str) -> np.ndarray:
        # Hjälpfunktion: skapar en embedding för en enda text
        response = client.embeddings.create(
            model=self.model,
            input=[text],
            extra_body={"input_type": input_type},  # "passage" (dokument) eller "query" (sökfråga)
        )
        # Gör om svaret till en numpy-array (float32 sparar minne)
        vector = np.asarray(response.data[0].embedding, dtype=np.float32)
        return vector

    def generate_embeddings(self, texts, *args, **kwargs):
        # Rensar indata och skapar embeddings för dokument/text som ska lagras
        texts = self.sanitize_input(texts)
        return [self._embed_one(text, input_type="passage") for text in texts]

    def compute_source_embeddings(self, texts, *args, **kwargs):
        # Anropas av LanceDB när data läggs in i tabellen
        return self.generate_embeddings(texts)

    def compute_query_embeddings(self, query, *args, **kwargs):
        # Anropas av LanceDB vid sökning – använder input_type "query"
        texts = self.sanitize_input(query)
        return [self._embed_one(text, input_type="query") for text in texts]