# LanceDB & Embeddings: En komplett guide och referens

Denna guide sammanfattar hur du arbetar med **LanceDB** och **Embedding-modeller** i Python. Den täcker både det manuella sättet att generera vektorer och det mer avancerade/automatiska sättet genom att skapa en **Custom Embedder** kopplad till LanceDB:s PyArrow-schema.

---

## 1. Installation & Beroenden

För att köra LanceDB tillsammans med inbäddningsmodeller (t.ex. från HuggingFace via `sentence-transformers` eller `fastembed`) behövs följande paket:

```bash
pip install lancedb sentence-transformers pyarrow pydantic
```

* **`lancedb`**: Det vektordatabas-bibliotek som lagrar tabeller och utför vektorsökningar (ANN / KNN).
* **`sentence-transformers`** (eller motsvarande): Genererar vektorrepresentationer (embeddings) av text eller bild.
* **`pyarrow`**: Hanterar underliggande datatyper och scheman för högpresterande lagring i LanceDB.
* **`pydantic`**: Används för att definiera tabellscheman i LanceDB.

---

## 2. Jämförelse av två tillvägagångssätt

| Egenskap | Sätt 1: Manuell Vektorhantering | Sätt 2: Automatic / Custom Embedder |
| :--- | :--- | :--- |
| **Princip** | Du omvandlar text till vektor *innan* du skickar datan till LanceDB, och omvandlar sökfrågan manuellt vid sökning. | Du registrerar en Embedder i LanceDB:s schema. LanceDB vektoriserar texten automatiskt vid `add()` och `search()`. |
| **Kodkomplexitet** | Enkel i starten, men kräver mer kod vid varje infogning och sökning. | Kräver lite mer setup i början, men ger extremt ren och återanvändbar kod därefter. |
| **Användningsfall** | När du vill ha total kontroll över embedding-processen eller arbetar med färdiga vektorer. | Standardiseringen i produktion, RAG-applikationer och när man vill minimera repetitiv kod. |

---

## 3. Sätt 1: Manuell Vektorhantering (Explicit Embeddings)

Här ansvarar applikationen för att driva datan genom embedding-modellen både vid lagring och sökning.

### Steg:
1. Anslut till databasen (`lancedb.connect`).
2. Ladda embedding-modellen (t.ex. `SentenceTransformer`).
3. Vektorisera datan i Python.
4. Skapa tabell och sätt in datan.
5. Vektorisera söksträngen manuellt och sök.

### Kodexempel:
```python
import lancedb
from sentence_transformers import SentenceTransformer

# 1. Anslut till lokal databas
db = lancedb.connect("./lancedb_data")

# 2. Ladda embedding-modell
model = SentenceTransformer("all-MiniLM-L6-v2")

# 3. Preparera data med manuell embedding
raw_documents = [
    {"text": "Python är ett populärt programmeringsspråk."},
    {"text": "LanceDB är en snabb vektordatabas."},
]

data_with_vectors = []
for doc in raw_documents:
    vector = model.encode(doc["text"]).tolist()
    data_with_vectors.append({
        "text": doc["text"],
        "vector": vector
    })

# 4. Skapa tabell
tbl = db.create_table("manual_docs", data=data_with_vectors, mode="overwrite")

# 5. Manuell sökning
query_text = "Vad är LanceDB?"
query_vector = model.encode(query_text).tolist()

results = tbl.search(query_vector).limit(2).to_pandas()
print(results)
```

---

## 4. Sätt 2: Custom / Automatic Embedder i LanceDB Schema

Genom att definiera en **Custom Embedding Function** som ärver från LanceDB:s registrator (`TextEmbeddingFunction`) integreras modellen direkt i tabellens Pydantic-schema.

### Varför göra på detta sätt?
* **Renare kod:** Du behöver bara skicka råtext vid sökning (`tbl.search("min sökfråga")`), LanceDB sköter omvandlingen i bakgrunden.
* **Mindre risk för fel:** Minskar risken att man av misstag använder fel embeddingmodell på en sökfråga jämfört med vad tabellen byggdes med.
* **Abstraktion:** Separerar databaslagring och modell-logik från din övriga applikationskod.

### Steg:
1. Importera `TextEmbeddingFunction` och `LanceModel` från `lancedb.pydantic`.
2. Skapa en custom klass dekorerad med `@register(...)`.
3. Definiera tabellschemat med `LanceModel` och ange vilket fält som är källa (source) respektive destination (vector).
4. Sätt in rådata (utan vektorer) och sök direkt med strängar.

### Kodexempel:
```python
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import TextEmbeddingFunction, register
from sentence_transformers import SentenceTransformer

# 1. Registrera din anpassade Embedder
@register("my-custom-embedder")
class CustomSentenceTransformer(TextEmbeddingFunction):
    name: str = "all-MiniLM-L6-v2"

    def ndims(self) -> int:
        # Returnera storleken på vektorn som modellen genererar (t.ex. 384 för MiniLM)
        return 384

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        # Instansiera eller använd modellen för att generera vektorer
        model = SentenceTransformer(self.name)
        embeddings = model.encode(texts)
        return embeddings.tolist()

# 2. Skapa ett schema kopplat till din embedder
embedder = CustomSentenceTransformer()

class DocumentSchema(LanceModel):
    # 'source=text' talar om att vektorn ska genereras automatiskt från text-fältet
    text: str = embedder.SourceField()
    vector: Vector(embedder.ndims()) = embedder.VectorField()

# 3. Anslut och skapa tabell med schemat
db = lancedb.connect("./lancedb_custom_data")
tbl = db.create_table("auto_docs", schema=DocumentSchema, mode="overwrite")

# 4. Lägg till rådata (LanceDB genererar vektorer automatiskt!)
raw_documents = [
    {"text": "Python är ett populärt programmeringsspråk."},
    {"text": "LanceDB är en snabb vektordatabas."},
]
tbl.add(raw_documents)

# 5. Sök direkt med en sträng (LanceDB vektoriserar automatiskt!)
results = tbl.search("Vad är LanceDB?").limit(2).to_pandas()
print(results[["text", "_distance"]])
```

---

## 5. Viktiga kom-ihåg och Best Practices

1. **Vektordimensioner (`ndims`):** 
   Se till att antalet dimensioner i schemat matchar exakt vad din embedding-modell levererar (exempelvis 384 för `all-MiniLM-L6-v2`, 1536 för OpenAI `text-embedding-3-small`).
2. **Lagring i minne vs på disk:**
   `lancedb.connect("./path")` skapar en diskbaserad databas (LANCE-format). För tester i minnet kan du skriva `lancedb.connect("memory://")` eller ett temporärt dir.
3. **Avståndsmått (Distance Metrics):**
   Standard i LanceDB är L2 (Euclidean distance). Vid sökning representerar `_distance` avståndet mellan frågan och dokumentet – ett lägre värde innebär högre relevans/likhet.