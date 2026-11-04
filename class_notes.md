## Förra veckan - structured output
- testa bygga en ai-agent med två olika nvidia modeller
- testa prompta på olika sätt 
- hämta text/data från STI och strukturera den m.h.a agenten
- spara ner resultat i .csv

![Workflow build nvidia agent](images/agent_build_workflow.png)


## Arketektur 
![Architecture](images/back_to_frontend.png)


# Lektion 04/05 - Pydantic FastAPI Chatbot

*Kopiera fil till annan mapp:* 
```bash
cd <work_folder>
cp ../<folder_name>/<file_name>
```

### Skapa agenten med vald modell och testa agenten direkt i teminalen 
1. Skapa agenten och lägg till instructions
2. testa agenten direkt i terminalen
*i scriptet*
```python
movie = movie_agent.run_sync("meddelande till agenten")
```
*i terminalen*
```bash
uv run agent.py
```

- skapa BaseModel för putput formart och vad du vill ha med


- för att testa endpointen @app.get("/...")
```bash
uv runn uvicorn api:app --reload
```



 
