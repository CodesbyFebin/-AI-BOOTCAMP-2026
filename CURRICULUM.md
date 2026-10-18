# AI-BOOTCAMP 2026 — Curriculum & Study Plan

**Codes by Febin** · [codesbyfebin.github.io](https://codesbyfebin.github.io/) · India
*Curated reference companion to the [resource catalog](README.md). Program overview sourced from `docs/AI-Bootcamp-Curriculum-Overview.docx` (draft, 18 Oct 2026); track structure from the published site outline.*

> Make AI useful. Make it yours.
> A practical learning path through Generative AI, LLM applications, RAG, AI agents, and AI-assisted software development — from first principles to full-stack AI prototypes.

---

## The program at a glance

| | |
|---|---|
| **Path** | Generative AI → LLM Applications → AI Agents → AI-Assisted Building |
| **Tracks** | 01 Foundations · 02 MLOps · 03 LLM Engineering · 04 RAG & Context · 05 Agents & Workflows · 06 AI-Assisted Building |
| **Audience** | Beginners, developers extending into LLM apps, professionals planning AI adoption — **no prerequisites listed**; programming experience helps in the engineering sections |
| **Outcomes** | Plan an AI pilot · build an LLM app, a RAG prototype and a tool-using agent · connect frontend + API + model provider + data store · apply evaluation, testing, observability and responsible-AI practices · use coding assistants with human review |

### The four program parts → six delivery tracks

| Program part (overview doc) | Delivery tracks (site outline) |
|---|---|
| **Part 1 — AI foundations & opportunity**: generative AI concepts, capabilities & limits, use-case selection, adoption strategy, responsible AI | **Track 01** AI/ML Foundations |
| **Part 2 — LLM applications & agent engineering**: Python/JS, terminal, Jupyter, GitHub, virtual envs; model APIs & credentials; LangChain/LCEL, LangGraph, CrewAI, LlamaIndex, LangSmith; app vs agent architecture | **Track 02** MLOps · **Track 03** LLM Engineering · **Track 05** Agents |
| **Part 3 — RAG, multimodal & full-stack**: ingestion → chunking → retrieval → generation; Postgres/Pinecone/Chroma/FAISS; Next.js, Tailwind, FastAPI, Flask, Streamlit; evaluation, testing, observability, LLMOps | **Track 04** RAG & Context · **Track 02** MLOps |
| **Part 4 — AI-assisted development & SaaS**: Cursor AI, Claude Code and comparable assistants; prompting, context management, review workflows; v0, Replit, Firebase/Supabase; to-do app → chatbot → social/voice/image app → basic SaaS | **Track 06** AI-Assisted Building |

---

## Track-by-track study plan (with catalog resources)

### Track 01 — AI / ML Foundations
*Build core code and concepts, from Python to your first machine learning model.*

**Suggested order**
1. Environment & day-one setup — [lewagon/setup](https://github.com/lewagon/setup), [hasankanaan26/prep-kit](https://github.com/hasankanaan26/prep-kit)
2. Python for data — [alfredodeza/python-bootcamp-duke](https://github.com/alfredodeza/python-bootcamp-duke), [qasimriaz002/AI-BootCamp-2026-GIKI](https://github.com/qasimriaz002/AI-BootCamp-2026-GIKI), [ahmadsanafarooq/Python-AI-Bootcamp](https://github.com/ahmadsanafarooq/Python-AI-Bootcamp)
3. ML concepts & first models — [1337-Artificial-Intelligence/Entry-Level-ML-Engineer-Bootcamp](https://github.com/1337-Artificial-Intelligence/Entry-Level-ML-Engineer-Bootcamp), [wikistat/MLTraining](https://github.com/wikistat/MLTraining), [Sayed-Husain/AI-and-Deep-Learning-Bootcamp](https://github.com/Sayed-Husain/AI-and-Deep-Learning-Bootcamp)
4. See a network learn in the browser — [JumpX-Labs/ai-bootcamp-demo01-fruit-nn](https://github.com/JumpX-Labs/ai-bootcamp-demo01-fruit-nn)

Full list: [`resources/01-foundations.md`](resources/01-foundations.md) · Prerequisite drills: [swirl-ai/ai-engineering-bootcamp-prerequisites](https://github.com/swirl-ai/ai-engineering-bootcamp-prerequisites)

### Track 02 — Production ML Systems (MLOps)
*Move from exploratory notebooks to repeatable data, training and serving pipelines.*

1. Data engineering & pipelines — [owshq-academy/ai-data-engineer-bootcamp](https://github.com/owshq-academy/ai-data-engineer-bootcamp), [odsc2015/Data-Wrangling-With-SQL](https://github.com/odsc2015/Data-Wrangling-With-SQL), [keeyong/airflow-bootcamp](https://github.com/keeyong/airflow-bootcamp)
2. Compute & profiling — [openhackathons-org/gpubootcamp](https://github.com/openhackathons-org/gpubootcamp), [openhackathons-org/Profiling-AI-Software-Bootcamp](https://github.com/openhackathons-org/Profiling-AI-Software-Bootcamp)
3. Serving & infrastructure — [VectorInstitute/ai-deployment](https://github.com/VectorInstitute/ai-deployment), [shamarta/ai-infrastructure-bootcamp](https://github.com/shamarta/ai-infrastructure-bootcamp), [becloudready/ai-cloud-engineer-bootcamp](https://github.com/becloudready/ai-cloud-engineer-bootcamp) *(archived)*

Full list: [`resources/02-mlops.md`](resources/02-mlops.md)

### Track 03 — LLM Engineering
*Build capable applications with model APIs, local models, tools and evaluation.*

1. APIs, keys, first calls — [hasankanaan26/prep-kit](https://github.com/hasankanaan26/prep-kit), [madhusudhankonda/ai-apps-bootcamp](https://github.com/madhusudhankonda/ai-apps-bootcamp)
2. Fine-tuning & LLM practice (series) — [ShawhinT/AI-Builders-Bootcamp-1](https://github.com/ShawhinT/AI-Builders-Bootcamp-1) through [#6](https://github.com/ShawhinT/AI-Builders-Bootcamp-6)
3. Evaluation & LLMOps — [productfoundry101/ai-evals-bootcamp](https://github.com/productfoundry101/ai-evals-bootcamp)
4. LLM-powered services — [johndimitry/dio-budget-ai-api](https://github.com/johndimitry/dio-budget-ai-api) (Whisper + GPT-4o tool calls), [labeveryday/language-learning-assistant](https://github.com/labeveryday/language-learning-assistant)

Full list: [`resources/03-llm.md`](resources/03-llm.md)

### Track 04 — RAG & Context
*Connect LLMs to relevant documents and improve the context they receive.*

1. End-to-end RAG chatbot — [gokerguner/gaih-genai-bootcamp](https://github.com/gokerguner/gaih-genai-bootcamp), [aabdulhanan-spec/RAG_CHATBOT_AI-BOOTCAMP](https://github.com/aabdulhanan-spec/RAG_CHATBOT_AI-BOOTCAMP)
2. Enterprise knowledge mining — [sithukyaw007/LearnAI-KnowledgeMiningBootcamp](https://github.com/sithukyaw007/LearnAI-KnowledgeMiningBootcamp), [pyladiesams/global-ai-bootcamp-mar2025](https://github.com/pyladiesams/global-ai-bootcamp-mar2025)
3. From RAG to agents — [alexeygrigorev/ai-bootcamp-codespace](https://github.com/alexeygrigorev/ai-bootcamp-codespace)

Full list: [`resources/04-rag.md`](resources/04-rag.md)

### Track 05 — Agents & Workflows
*Design stateful workflows and agents that use tools to complete multi-step tasks.*

1. Reference implementations — [VectorInstitute/agent-bootcamp](https://github.com/VectorInstitute/agent-bootcamp), [VectorInstitute/eval-agents](https://github.com/VectorInstitute/eval-agents)
2. LangChain / LangGraph / CrewAI — [Md-Emon-Hasan/Complete-Agentic-AI-Bootcamp-With-LangGraph-and-Langchain](https://github.com/Md-Emon-Hasan/Complete-Agentic-AI-Bootcamp-With-LangGraph-and-Langchain), [pragatidev/AIAgentsBootcamp](https://github.com/pragatidev/AIAgentsBootcamp), [vchandu111/5-day-crewAI-bootcamp](https://github.com/vchandu111/5-day-crewAI-bootcamp)
3. Orchestration & MCP — [tobiaszwingmann/n8n-ai-bootcamp](https://github.com/tobiaszwingmann/n8n-ai-bootcamp), [Ratnesh-181998/Build-Agentic-AI-and-Gen-AI-Agents-with-MCP](https://github.com/Ratnesh-181998/Build-Agentic-AI-and-Gen-AI-Agents-with-MCP)
4. Enterprise agent engineering — [Acronus2008/ai-agent-engineering-bootcamp](https://github.com/Acronus2008/ai-agent-engineering-bootcamp), [ThinkInAIXYZ/agent-zero-to-one](https://github.com/ThinkInAIXYZ/agent-zero-to-one)

Full list: [`resources/05-agents.md`](resources/05-agents.md)

### Track 06 — AI-Assisted Building
*Use coding assistants to build full-stack applications and explore SaaS ideas — human-led development.*

1. Vibe coding & AI-native workflows — [fufankeji/VibeCodingCourse_v1](https://github.com/fufankeji/VibeCodingCourse_v1), [AICode-Nexus/ai-native-frontend-bootcamp](https://github.com/AICode-Nexus/ai-native-frontend-bootcamp)
2. Copilot / Claude Code in practice — [ManuOSMx/gh-copilot-bootcamp-python-ai-demo-2025](https://github.com/ManuOSMx/gh-copilot-bootcamp-python-ai-demo-2025), [marketcalls/trading-terminal](https://github.com/marketcalls/trading-terminal)
3. Full-stack & backend with AI — [ozdemirr1/ai-backend-bootcamp](https://github.com/ozdemirr1/ai-backend-bootcamp), [aiQuest-Intelligence/aiQuest-Django-BootCamp-2024](https://github.com/aiQuest-Intelligence/aiQuest-Django-BootCamp-2024), [ibrahimgokyar/n11bootcamp](https://github.com/ibrahimgokyar/n11bootcamp)
4. Dev environments & portfolio — [xinyeah/GenAI-Development-Environments-Boot-Camp](https://github.com/xinyeah/GenAI-Development-Environments-Boot-Camp), [ThomasJButler/AgenticAICoursePortfolio](https://github.com/ThomasJButler/AgenticAICoursePortfolio), [kristineservia/practice](https://github.com/kristineservia/practice)

Full list: [`resources/06-building.md`](resources/06-building.md)

---

## Supporting buckets

| Bucket | Why it matters | File |
|---|---|---|
| **00 · Full-Path Bootcamps** | Complete multi-track programs (e.g. [curiousily/AI-Bootcamp](https://github.com/curiousily/AI-Bootcamp), [harsh-aranga/ai-engineering-bootcamp](https://github.com/harsh-aranga/ai-engineering-bootcamp), [grey8-io/learn-ai-with-grey8](https://github.com/grey8-io/learn-ai-with-grey8)) — ideal if you want one repo to follow end-to-end | [`resources/00-full-path.md`](resources/00-full-path.md) |
| **07 · Cloud & Platform Labs** | Vendor-run labs: [GoogleCloudPlatform/asl-ml-immersion](https://github.com/GoogleCloudPlatform/asl-ml-immersion), [aws-samples/aws-ai-bootcamp-labs](https://github.com/aws-samples/aws-ai-bootcamp-labs), [microsoft/aifundamentalbootcamp](https://github.com/microsoft/aifundamentalbootcamp), NVIDIA NIM, Databricks, Azure | [`resources/07-cloud.md`](resources/07-cloud.md) |
| **08 · Domain & Specialty Projects** | Applied inspiration: computer vision, security/red-teaming, robotics, science, finance, analytics | [`resources/08-domain.md`](resources/08-domain.md) |
| **09 · Cohort Notes & Community Archives** | Student notes, event archives and learning journals — useful as study companions and examples of learner output | [`resources/09-cohort.md`](resources/09-cohort.md) |

---

## The practice loop (how every track is exercised)

```
A · USER PROBLEM          Define a useful outcome
        ↓
B · MODEL + CONTEXT       Choose tools and information
        ↓
C · APPLICATION           Build a coherent experience
        ↓
D · EVALUATE + IMPROVE    Test, observe, iterate   ↺ responsible by design
```

**Toolkit named in the outline** — Foundations: Python, NumPy, Pandas, scikit-learn, PyTorch · Models & APIs: OpenAI, Anthropic, Google, Ollama, Hugging Face · Orchestration: LangChain/LCEL, LangGraph, CrewAI, LlamaIndex, LangSmith · Data & MLOps: Postgres + pgvector, Pandera, DVC, MLflow, Docker · App & Cloud: Next.js, FastAPI, Streamlit, AWS S3/ECR/ECS · AI-assisted dev: Cursor AI, Claude Code, Replit, GitHub, MCP, DSPy.

---

*Draft status: the program overview is a curriculum draft prepared 18 Oct 2026 and is not an official verification document. Linked repositories belong to their authors; see [License & attribution](README.md#️-license--attribution).*
