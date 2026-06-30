# SelfworkRAG

Esempio base di RAG (Retrieval-Augmented Generation): indicizza dei CV in ChromaDB usando gli embedding di OpenAI, recupera il candidato più pertinente rispetto a una domanda e usa un modello GPT per generare una risposta motivata.

Lo script `SelfworkRAG.py` è la versione standalone della logica esplorata in `Esempio-RAG.ipynb`.

## Requisiti

- Python 3.10+
- Una API key OpenAI valida

## Setup

1. Clona il repository e spostati nella cartella del progetto.

2. Crea e attiva un virtual environment:

   ```bash
   python -m venv venvrag
   ```

   Attivazione:
   - Windows (PowerShell): `venvrag\Scripts\Activate.ps1`
   - Windows (cmd): `venvrag\Scripts\activate.bat`
   - Linux/Mac: `source venvrag/bin/activate`

3. Installa le dipendenze:

   ```bash
   pip install -r requirements.txt
   ```

4. Crea un file `.env` nella root del progetto con la tua chiave OpenAI:

   ```
   OPENAI_API_KEY=la-tua-chiave-openai
   ```

   Il file `.env` è escluso da Git (vedi `.gitignore`): non committare mai la tua chiave.

## Struttura del progetto

- `SelfworkRAG.py` — script principale: ingestion dei CV, indicizzazione in ChromaDB, query semantica e generazione della risposta
- `resumes/` — cartella con i CV di esempio in formato `.txt` (sezioni separate da intestazioni `### `)
- `Esempio-RAG.ipynb` — notebook esplorativo da cui deriva lo script
- `requirements.txt` — dipendenze Python del progetto

## Esecuzione

```bash
python SelfworkRAG.py
```

Lo script:
1. legge tutti i `.txt` in `resumes/` e li suddivide in chunk;
2. crea/aggiorna una collection ChromaDB (`CVs`) con embedding `text-embedding-3-small`;
3. esegue una query semantica con una domanda di esempio (modificabile editando `user_question` nello script);
4. costruisce un prompt di contesto con il CV più pertinente trovato;
5. genera e stampa a video la risposta con il modello `gpt-5-nano`.

## Testare con CV propri

Aggiungi nuovi file `.txt` in `resumes/` seguendo lo stesso formato di quelli di esempio: la prima sezione `### ` deve contenere i dati di contatto (nome, ruolo, email, telefono, ecc.), le sezioni successive il contenuto del profilo (esperienza, competenze...).
