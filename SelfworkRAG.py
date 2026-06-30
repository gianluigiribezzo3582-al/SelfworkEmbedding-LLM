import os

from dotenv import load_dotenv
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise RuntimeError("Controlla di aver inserito la tua OPENAI_API_KEY nel file .env")

# --- Lettura e parsing dei CV ---
documents_dir = "resumes"
documents = []
metadatas = []
ids = []

id = 0
for filename in os.listdir(documents_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(documents_dir, filename), "r", encoding="utf-8") as file:
            chunks = file.read().replace("\n", ".").split("### ")
            for chunk in chunks:
                if not chunk.isspace() and not chunk == "":
                    documents.append(chunk)
                    metadatas.append({"source": filename, "info": chunks[1]})
                    ids.append(str(id))
                    id += 1

# --- Embedding + ChromaDB ---
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_key,
    model_name="text-embedding-3-small",
)

chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(
    name="CVs",
    embedding_function=openai_ef,
)

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
)

# --- Vector similarity search ---
user_question = input("Che tipo di profilo stai cercando? ")

results = collection.query(
    query_texts=[user_question],
    n_results=1,
)

# --- Costruzione del prompt con il contesto recuperato ---
context = (
    f"CONTESTO: nome file {results['metadatas'][0][0]['source']} "
    f"ecco il paragrafo piu' significativo: {results['documents'][0][0]} "
    f"ricorda sempre di menzionare il nome del candidato all'inizio e i dati personali alla fine per il contatto, "
    f"ti lascio tutto qui: {results['metadatas'][0][0]['info']}"
)

prompt = f"""Dato il seguente contesto {context} rispondi alla domanda dell'utente {user_question}
spiegando che nel file individuato c'e' il profilo piu' adatto.
Argomenta la scelta utilizzando il contenuto del testo individuato nel contesto
"""

# --- Generazione della risposta con il modello di linguaggio ---
client = OpenAI(api_key=openai_key)

completion = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {
            "role": "developer",
            "content": "Sei un assistente HR, specializzato nella ricerca di profili professionali",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ],
)

print(completion.choices[0].message.content)
