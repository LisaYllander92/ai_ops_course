# DevOps, AIOps och AI-applikationer – kort översikt

## 1. Roller och ansvar i DevOps- och AIOps-team

DevOps handlar om hur system byggs och levereras; AIOps om hur de drivs och optimeras i produktion med hjälp av AI (anomalidetektering, incidenthantering, automatisering). Ett typiskt team har DevOps-/plattformsingenjörer (CI/CD, infrastruktur som kod, deployment), SRE (tillförlitlighet, övervakning) och i AIOps-fallet AIOps-/ML-ingenjörer och dataforskare som lägger AI-driven analys ovanpå driftflödena. Samarbete över teamgränser och förtroende för AI-automation är vanliga utmaningar.

**Källor**

- [Role of an AIOps Engineer – Selector](https://www.selector.ai/learning-center/role-of-an-aiops-engineer-key-responsibilities-explained/)
- [What is AIOps? – CIO](https://www.cio.com/article/3529772/what-is-aiops-injecting-intelligence-into-it-operations.html)
- [DevOps Team Roles and Responsibilities – IT Svit](https://itsvit.com/articles/devops-team-roles-and-responsibilities/)

## 2. Containers och Docker för AI-miljöer

Docker paketerar kod, bibliotek och drivrutinsberoenden (t.ex. CUDA, PyTorch) i en image, vilket ger reproducerbara och portabla miljöer och slutar "det fungerar på min maskin". För GPU-arbetslaster används NVIDIA Container Toolkit, och Docker Compose kan reservera GPU:er för tjänster. Samma image kan köras lokalt, på GPU-moln eller i Kubernetes.

**Källor**

- [NVIDIA GPU-stöd i Docker för AI/ML – OneUptime](https://oneuptime.com/blog/post/2026-01-16-docker-nvidia-gpu-ai-ml/view)
- [AI-arbetsflöden med Docker + GPU-moln – Runpod](https://www.runpod.io/articles/guides/ai-workflows-with-docker-gpu-cloud)

## 3. Vektordatabaser

En vektordatabas lagrar embeddings (numeriska representationer av text, bild, ljud) och söker på likhet i stället för exakt matchning, ofta med cosinuslikhet. För snabb sökning används ANN-index som HNSW. De kan kombinera vektorsökning med metadatafilter och är ett nyckelled i semantisk sökning och RAG. Exempel: Qdrant, Pinecone, Milvus, Weaviate, pgvector. Samma embeddingmodell måste användas för lagring och sökning.

**Källor**

- [What is a Vector Database? – NVIDIA](https://www.nvidia.com/en-gb/glossary/vector-database/)
- [What is a vector database? – SAP](https://www.sap.com/resources/what-is-a-vector-database)
- [Vector database – Voxel51](https://voxel51.com/glossary/vector-database)

## 4. Prompt engineering, few-shot och chain-of-thought

Prompt engineering är att formulera indata så att språkmodellen ger önskat resultat utan omträning.

- **Zero-shot:** bara instruktion, inga exempel.
- **Few-shot:** 2–5 exempel i prompten visar format och mönster (in-context learning).
- **Chain-of-thought (CoT):** modellen uppmanas resonera i steg innan svar, vilket hjälper vid komplexa problem. Kombinerat med few-shot visar man exempel på resonemanget.

  **Källor**

- [Few-Shot Prompting Guide – Mem0](https://mem0.ai/blog/few-shot-prompting-guide)
- [Chain of Thought Prompting Guide – PromptHub](https://www.prompthub.us/blog/chain-of-thought-prompting-guide)
- [Few-Shot Chain-of-Thought – Avahi](https://avahi.ai/glossary/few-shot-chain-of-thought/)

## 5. CI/CD med AI-modeller

CI/CD för ML utökar vanlig CI/CD med tester av data och modeller, samt kontinuerlig träning (CT): pipeline-CI bygger och testar kod, pipeline-CD distribuerar pipelines och modeller till produktion. Modeller kan försämras när data ändras, så övervakning kan trigga omträning. Modeller versioneras i ett modellregister.

**Källor**

- [CI/CD for Automated Deployment of ML Models using MLOps – arXiv](https://arxiv.org/pdf/2202.03541)
- [CI/CD for Machine Learning – Iguazio](https://www.iguazio.com/glossary/ci-cd-for-machine-learning/)
- [CI/CD for MLOps – Hopsworks](https://www.hopsworks.ai/dictionary/ci-cd-for-mlops)

## 6. Källkod → Git → Pipeline → AI-applikation (inkl. LLM-integration)

Flödet: kod pushas till Git → pipeline triggas (t.ex. GitHub Actions) → build och tester → Docker-image byggs och pushas till ett register (t.ex. ECR) → deployment till driftmiljö. LLM-integration kräver att API-nycklar hanteras som secrets (aldrig i koden) och att prompts och konfiguration versioneras tillsammans med koden.

**Källor**

- [CI/CD for Machine Learning (pipelinesteg) – Iguazio](https://iguazio.com/?p=5238)
- [ExpenTrack: LLM-app med CI/CD via GitHub Actions – GitHub](https://github.com/SoloCoderHi/ExpenTrack)
- [Continuous Deployment with GitHub Actions – LlamaIndex](https://developers.llamaindex.ai/python/llamaagents/llamactl/cd-with-github-actions/)

## 7. Pipelines lokalt och i molnet för drift av AI-agenter

- **Lokalt:** Docker/Docker Compose på egen maskin eller server, med GPU via NVIDIA Container Toolkit. Ger kontroll över data och kostnad men kräver eget underhåll.
- **Moln:** pipeline (t.ex. GitHub Actions) distribuerar agenten till en hanterad plattform eller container-/Kubernetes-miljö med skalning och övervakning. Agentens specifikation hålls i Git och uppdateras automatiskt vid varje push.
  _Obs: sökningen specifikt för detta ämne avbröts, så beskrivningen bygger delvis på allmän kunskap och de nedan relaterade källorna._

**Källor**

- [Continuous Deployment with GitHub Actions (agentdeployment) – LlamaIndex](https://developers.llamaindex.ai/python/llamaagents/llamactl/cd-with-github-actions/)
- [NVIDIA GPU-stöd i Docker – OneUptime](https://oneuptime.com/blog/post/2026-01-16-docker-nvidia-gpu-ai-ml/view)
- [ExpenTrack – GitHub](https://github.com/SoloCoderHi/ExpenTrack)

## 8. Bygga och integrera RAG (Retrieval Augmented Generation)

RAG kompletterar en LLM med egen data. Flöde: (1) dokument delas upp i bitar och embeddas, (2) lagras i en vektordatabas, (3) användarens fråga embeddas och liknande bitar hämtas (retrieval), (4) bitarna läggs in i prompten och modellen genererar ett svar grundat i dem. Fördelen är aktuell, verifierbar information utan omträning. Retrieval kan förbättras med hybridsökning (BM25 + vektor) och omrankning.

**Källor**

- [How to build a RAG system – Weights & Biases](https://wandb.ai/rag-course/rag-course/reports/How-to-build-a-RAG-system--Vmlldzo5NjY0NDUw)
- [How to Build a RAG System – Mindee](https://www.mindee.com/blog/build-rag-system-guide)
- [A beginner's guide to building a RAG application from scratch – Towards Data Science](https://towardsdatascience.com/a-beginners-guide-to-building-a-retrieval-augmented-generation-rag-application-from-scratch-e52921953a5d/)


# Vad är AI?

En sammanfattning av vad artificiell intelligens (AI) är, baserad på tankekartan och definitionen från ChatGPT 4.5.

## Definition

Artificiell intelligens (AI) syftar på **simulering av mänsklig intelligens** i processer som utförs av datorsystem.

I grund och botten handlar AI om att skapa **maskiner eller mjukvara som kan utföra uppgifter som vanligtvis kräver mänsklig intelligens**.

### Processer som ingår

- **Inlärning** (learning): att förvärva kunskap eller färdigheter genom data, erfarenhet eller instruktion
- **Resonemang** (reasoning): att tillämpa logik för att dra slutsatser eller lösa problem
- **Perception** (perception): att tolka sensoriska intryck, t.ex. syn eller taligenkänning
- **Språkteknologi** (natural language processing): att förstå och generera mänskligt språk
- **Beslutsfattande** (decision-making): att välja handlingar utifrån inlärda eller programmerade kriterier

## System

Ett AI-system:

- uppvisar **intelligent beteende**
- **lär sig från data**
- **analyserar sin omgivning** och vidtar åtgärder

## Nivåer av AI

| Nivå | Beskrivning |
|------|-------------|
| **Narrow AI** (snäv AI) | Löser ett avgränsat problem, t.ex. att köra en bil |
| **AGI** (Artificial General Intelligence) | Kan lösa alla problem som människor kan lösa |
| **ASI** (Artificial Super Intelligence) | Överträffar mänsklig intelligens i alla avseenden |

## Delområden

- **Maskininlärning** (machine learning)
- **Djupinlärning** (deep learning), som i sin tur omfattar:
  - **Generativ AI**
  - **Språkteknologi** (natural language processing)
  - **Datorseende** (computer vision)

## Översikt

```text
                         ┌─ System ──────── intelligent beteende, lär från data,
                         │                  analyserar omgivning och agerar
                         │
Vad är AI? ──────────────┼─ Nivåer ──────── Narrow AI → AGI → ASI
                         │
                         └─ Delområden ──── Maskininlärning
                                            └─ Djupinlärning
                                               ├─ Generativ AI
                                               ├─ Språkteknologi (NLP)
                                               └─ Datorseende
```

