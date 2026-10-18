#!/usr/bin/env python3
"""
AI-BOOTCAMP 2026 — catalog builder (Codes by Febin)
===================================================
Extracts every public GitHub repository collected from the AI-bootcamp search
(170 repos, snapshot 2026-10-18), merges them into one curated catalog and
generates:

    data/repos.json          machine-readable extraction (all fields)
    data/repos.csv           spreadsheet-friendly extraction
    CATALOG.md               single-page index of all repository links
    resources/00..09-*.md    one curated file per curriculum track / bucket

Run from the repository root:   python3 scripts/build_catalog.py
"""

from __future__ import annotations

import csv
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# Category taxonomy — aligned with the AI-BOOTCAMP curriculum (6 tracks)
# plus four supporting buckets for cloud labs, domain projects, full-path
# programs and cohort/community archives.
# --------------------------------------------------------------------------
CATS = {
    "FP": ("00", "full-path", "Full-Path Bootcamps (Start Here)",
           "Complete, multi-track programs that carry you from foundations all the way to shipped AI products."),
    "F":  ("01", "foundations", "Track 01 · AI / ML Foundations",
           "Python, data tooling, classic machine learning and deep-learning fundamentals."),
    "M":  ("02", "mlops", "Track 02 · Production ML & MLOps",
           "Data pipelines, training/serving infrastructure, GPUs & HPC, profiling, deployment."),
    "L":  ("03", "llm", "Track 03 · LLM Engineering",
           "Model APIs, prompting, fine-tuning, evaluation, LLMOps and LLM-powered services."),
    "R":  ("04", "rag", "Track 04 · RAG & Context",
           "Retrieval-augmented generation, vector search, knowledge mining and context engineering."),
    "A":  ("05", "agents", "Track 05 · Agents & Workflows",
           "Tool-using agents, LangGraph / CrewAI / n8n orchestration, MCP and multi-agent systems."),
    "B":  ("06", "building", "Track 06 · AI-Assisted Building",
           "Vibe coding, Copilot / Cursor / Claude Code workflows and full-stack AI product builds."),
    "C":  ("07", "cloud", "Cloud & Platform Labs",
           "AWS, Google Cloud, Azure, NVIDIA, Databricks and other vendor-run bootcamp labs."),
    "D":  ("08", "domain", "Domain & Specialty Projects",
           "Computer vision, security, robotics, science, finance, analytics and other applied domains."),
    "N":  ("09", "cohort", "Cohort Notes & Community Archives",
           "Student notes, cohort forks, event archives and personal learning-journey repos."),
}

# --------------------------------------------------------------------------
# Extraction: (full_name, description, language, stars, updated, topics, cat, archived)
# Snapshot of public GitHub search results for "AI bootcamp", 2026-10-18.
# Stars are approximate at extraction time ("19.7k" -> 19700).
# --------------------------------------------------------------------------
REPOS = [
    ("lewagon/setup", "Setup instructions for Le Wagon's students on their first day of AI Software Development Bootcamp", "Ruby", 19700, "2026-10-17", "ruby, setup", "FP", False),
    ("GoogleCloudPlatform/asl-ml-immersion", "Notebooks, code samples and reference for machine learning and generative AI on Google Cloud for the Advanced Solutions Lab (ASL) bootcamps.", "Jupyter Notebook", 2600, "2026-10-17", "machine-learning, tensorflow, google-cloud-platform, agents, adk", "C", False),
    ("curiousily/AI-Bootcamp", "Self-paced bootcamp on Generative AI. Tutorials on ML fundamentals, Ollama, LLMs, RAGs, LangChain, LangGraph, Fine-tuning, DSPy & AI Agents.", "Jupyter Notebook", 956, "2026-10-12", "machine-learning, artificial-intelligence, llama, ai-agents, rag", "FP", False),
    ("openhackathons-org/gpubootcamp", "GPU bootcamp material for HPC and AI.", "Jupyter Notebook", 549, "2023-11-02", "data-science, machine-learning, deep-learning, hpc, gpu", "M", False),
    ("EcZachly/databricks-ai-bootcamp-capstone", "Capstone project for the Databricks AI bootcamp.", "", 278, "2026-08-05", "", "C", False),
    ("tyrchen/geektime-bootcamp-ai", "AI bootcamp course from Geektime (Chinese).", "Python", 237, "2026-03-26", "", "FP", False),
    ("sunnysavita10/Full-Stack-GenAI-Bootcamp-1.0", "Full-stack Generative AI bootcamp, cohort 1.0.", "Jupyter Notebook", 153, "2026-10-12", "", "FP", False),
    ("apatti/AIEBootcamp", "AI Engineering bootcamp.", "Jupyter Notebook", 130, "2025-03-10", "", "FP", False),
    ("fufankeji/VibeCodingCourse_v1", "Vibe Coding AI Full Stack Development Practical Training 2026 - The First AI Programming Bootcamp.", "TypeScript", 124, "2026-03-12", "", "B", False),
    ("phkhanhtrinh23/translation_layoutrecovery", "Translates a .pdf file while preserving the original layout (2nd-prize bootcamp project).", "Python", 122, "2024-11-15", "firebase, docker-compose, nextjs, machine-translation, postgresql", "D", False),
    ("aws-samples/aws-ai-bootcamp-labs", "Collection of notebooks and code examples for AWS AI Bootcamps.", "Jupyter Notebook", 113, "2018-08-27", "", "C", False),
    ("rameerez/brain-computer-interfacing", "Brain-Computer Interfacing bootcamp course + projects @ Saturdays.AI (BCI + AI).", "Jupyter Notebook", 84, "2020-05-03", "python, machine-learning, course, ai, notebook", "D", False),
    ("harsh-aranga/ai-engineering-bootcamp", "Self-paced bootcamp for engineers building AI into production systems: tokenization, embeddings, prompting and beyond.", "Python", 81, "2026-09-11", "", "FP", False),
    ("ShawhinT/AI-Builders-Bootcamp-1", "Code repository for AI Builders Bootcamp #1 (fine-tuning, RAG, LLMs).", "HTML", 71, "2025-01-23", "ai, fine-tuning, rag, llm", "L", False),
    ("solliancenet/data-ai-technical-bootcamp", "Student materials for the Data & AI Technical Bootcamp.", "", 58, "2022-03-29", "", "C", False),
    ("gtech-mulearn/Pathway-AI-Bootcamp", "Pathway AI bootcamp learning path (muLearn).", "", 58, "2024-05-11", "", "F", False),
    ("SAP-archive/btp-ai-sustainability-bootcamp", "Sample code and exercises of the BTP AI & sustainability bootcamp (SAP).", "Jupyter Notebook", 54, "2026-02-10", "sample, machine-learning, sustainability, computer-vision, deep-learning", "D", True),
    ("1337-Artificial-Intelligence/Entry-Level-ML-Engineer-Bootcamp", "Entry-Level ML Engineer Bootcamp - kickstart your AI journey.", "Jupyter Notebook", 53, "2025-03-25", "", "F", False),
    ("vishalvoid/100xSchool_Bootcamp_1.0", "100xdevs Bootcamp 1.0 @hkirat - all assignments and notes (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 53, "2026-01-26", "devops, web-development, code, notes, aiml", "N", False),
    ("AICode-Nexus/ai-native-frontend-bootcamp", "Frontend development in the LLM era - AI-native tech stack & workflow training (12 lessons, scripts + demos + exercises, Chinese).", "Shell", 51, "2026-05-06", "", "B", False),
    ("Nicolepcx/ORM_AI_Agents_Bootcamp", "AI agents bootcamp notebooks.", "Jupyter Notebook", 50, "2026-09-24", "", "A", False),
    ("alfredodeza/python-bootcamp-duke", "Official syllabus for AIPI 503 - Python Bootcamp for Data and AI (Duke).", "", 50, "2024-07-25", "", "F", False),
    ("GlobalAICommunity/GlobalAIBootcamp2019", "Workshops and presentations for the Global AI Bootcamp 2019.", "", 49, "2019-12-02", "", "N", True),
    ("ShawhinT/AI-Builders-Bootcamp-2", "Code repository for AI Builders Bootcamp #2 (fine-tuning, RAG, LLMs).", "HTML", 48, "2025-03-06", "ai, fine-tuning, rag, llm", "L", False),
    ("VizuaraAILabs/Vizuara-Agents-10Day-Bootcamp", "All code files shared in the Vizuara AI Agents 10-day bootcamp.", "Jupyter Notebook", 47, "2025-07-04", "", "A", False),
    ("anacaroliness9/bootcamp-ai-luis-speech-search", "Classify phone calls and extract information using Azure AI services (Portuguese).", "Jupyter Notebook", 44, "2021-05-07", "", "D", False),
    ("openhackathons-org/agentic-ai-bootcamp", "Agentic AI bootcamp labs (NVIDIA OpenHackathons).", "Jupyter Notebook", 40, "2026-10-02", "", "A", False),
    ("swirl-ai/ai-engineering-bootcamp-prerequisites", "Prerequisites track for the AI engineering bootcamp (Python & tooling).", "Python", 40, "2026-03-12", "", "F", False),
    ("gokerguner/gaih-genai-bootcamp", "Turkish RAG (Retrieval-Augmented Generation) chatbot project from the Generative AI 101 Bootcamp.", "Python", 40, "2025-10-10", "", "R", False),
    ("aiQuest-Intelligence/aiQuest-Django-BootCamp-2024", "Django bootcamp - five 2.5-hour classes over five consecutive days.", "HTML", 37, "2024-05-22", "", "B", False),
    ("pragatidev/AIAgentsBootcamp", "Build and deploy powerful AI agents using LangChain, RAG, LangGraph and GPT - beginner to advanced.", "Python", 36, "2026-10-06", "automation, multi-agent, bootcamp, ai-agents, rag", "A", False),
    ("tobiaszwingmann/n8n-ai-bootcamp", "Official course repo for the O'Reilly live event 'n8n AI Bootcamp: Building AI Workflows and Agents From Scratch'.", "CSS", 36, "2026-10-09", "", "A", False),
    ("ShawhinT/AI-Builders-Bootcamp-3", "Code repository for AI Builders Bootcamp #3 (fine-tuning, RAG, LLMs).", "HTML", 32, "2025-03-07", "ai, fine-tuning, rag, llm", "L", False),
    ("WeiDaiWD/Private-AI-Bootcamp-Materials", "Materials from the Private AI Bootcamp hosted by Microsoft, Redmond WA, Dec 2-4 2019.", "", 32, "2020-08-19", "", "C", False),
    ("openhackathons-org/Profiling-AI-Software-Bootcamp", "Profiling with NVIDIA Nsight Systems - optimizing distributed data-parallel training.", "", 30, "2026-04-23", "", "M", False),
    ("owshq-academy/ai-data-engineer-bootcamp", "AI Data Engineer Bootcamp.", "Python", 29, "2025-09-04", "", "M", False),
    ("becloudready/ai-cloud-engineer-bootcamp", "Free DevOps roadmap - AWS, Kubernetes, Terraform, Docker, CI/CD & SRE with hands-on labs.", "", 29, "2026-06-16", "devops, career, interview-preparation, career-development", "M", True),
    ("multigroupco/AI-Agents-Bootcamp", "AI Agents Bootcamp with Turkiye Veri Toplulugu.", "HTML", 29, "2026-10-11", "", "A", False),
    ("pranavgade20/aisb", "AI Security Bootcamp public repository.", "HTML", 28, "2026-07-02", "", "D", False),
    ("xinyeah/GenAI-Development-Environments-Boot-Camp", "Hands-on resource hub for the Generative AI Development Environments Bootcamp.", "", 27, "2025-10-23", "", "B", False),
    ("VectorInstitute/agent-bootcamp", "Reference implementations for the Agentic AI bootcamp (Vector Institute).", "Python", 26, "2026-10-17", "", "A", False),
    ("ShawhinT/AI-Builders-Bootcamp-4", "Code repository for AI Builders Bootcamp #4 (fine-tuning, RAG, LLMs).", "HTML", 26, "2025-05-30", "ai, fine-tuning, rag, llm", "L", False),
    ("openhackathons-org/End-to-End-Computer-Vision", "AI bootcamp material: an end-to-end workflow for computer vision.", "Jupyter Notebook", 26, "2023-09-12", "opencv, deep-neural-networks, computer-vision, deep-learning, image-processing", "D", True),
    ("ibrahimgokyar/n11bootcamp", "Java Spring Boot, microservices, JWT, RabbitMQ, JPA, Hibernate, Keycloak, Spring AI - enterprise backend bootcamp (Turkish).", "Java", 25, "2026-06-04", "jwt, microservices, spring, keycloak, rabbitmq", "B", False),
    ("DataScienceNigeria/AIBootcamp-2019", "AI bootcamp 2019 materials (Data Science Nigeria).", "HTML", 24, "2019-12-16", "python, machine-learning, r, statistics, ai", "F", False),
    ("Anubhavsingh311/AIML_Learning_Bootcamp", "AI/ML learning bootcamp notebooks.", "Jupyter Notebook", 24, "2026-08-05", "", "F", False),
    ("Skillsoft-Content/AWS-Certified-AI-Practitioner-Bootcamp", "AWS Certified AI Practitioner bootcamp content.", "", 21, "2025-04-02", "", "C", False),
    ("ai-analyst-lab/ai-analyst-plus", "AI Product Analyst Plus - full system + premium skills for bootcamp and consulting.", "Python", 20, "2026-07-15", "", "D", False),
    ("Ramsi-K/free-genai-bootcamp-2025", "GenAI Bootcamp 2025 (Andrew Brown & ExamPro) - documented learning journey through the 6(+3)-week bootcamp.", "Python", 20, "2025-04-13", "generative-ai", "N", False),
    ("codecentric/codecentric.AI-bootcamp", "Course contents for the codecentric.AI bootcamp (German).", "Jupyter Notebook", 19, "2022-09-24", "", "FP", True),
    ("Cinnamon/ai-bootcamp-2024", "Cinnamon AI bootcamp 2024 notebooks.", "Jupyter Notebook", 18, "2024-08-02", "", "FP", False),
    ("GlobalAICommunity/global-ai-bootcamp-2025", "Global AI Bootcamp 2025 session materials.", "JavaScript", 18, "2025-03-07", "", "N", True),
    ("wikistat/MLTraining", "Machine learning training for data science and AI - bootcamp in progress.", "Jupyter Notebook", 18, "2024-10-06", "data-science, machine-learning, statistics, bootcamp, clustering-algorithm", "F", False),
    ("PacktPublishing/AI-and-Quantum-Computing-Mastery---From-Zero-to-Expert-Bootcamp", "AI & Quantum Computing Mastery - From Zero to Expert Bootcamp (Packt).", "Jupyter Notebook", 18, "2025-12-15", "", "D", False),
    ("EdwinTSalcedo/Bootcamp-Computer-Vision-for-the-SDGs", "Course materials for the Bootcamp on Computer Vision for the SDGs (HackCities x Google AI).", "Jupyter Notebook", 18, "2022-07-18", "", "D", False),
    ("ed-donner/sds", "Repo for the SuperDataScience AI Engineering Bootcamp.", "Jupyter Notebook", 16, "2025-10-23", "", "FP", False),
    ("vchandu111/5-day-crewAI-bootcamp", "5-day CrewAI bootcamp.", "", 16, "2026-01-27", "", "A", False),
    ("anilsharmay/AI-Engineering-Bootcamp", "Course work required for AI Engineering Bootcamp certification.", "Jupyter Notebook", 16, "2025-11-09", "", "N", False),
    ("GlobalAICommunity/GlobalAIBootcamp2018", "Workshops, presentations and demos from the Global AI Bootcamp 2018.", "", 16, "2018-12-26", "", "N", True),
    ("RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito", "Code and slides of the AI Engineer bootcamp (Spanish, Codigofacilito).", "Python", 15, "2026-05-25", "", "FP", False),
    ("Wagademy/AI2Web3", "Introductory bootcamp on decentralized AI agents (Web3).", "", 15, "2025-02-10", "", "D", False),
    ("radanliev/Agentic-AI-Security-Demos", "Agentic AI security bootcamp: multi-agent observability, prompt injection, red-teaming, adversarial evaluation.", "Python", 15, "2026-08-24", "observability, multi-agent-systems, autonomous-agents, ai-security, prompt-injection", "D", True),
    ("productfoundry101/ai-evals-bootcamp", "Evaluate AI products for production - 21 hands-on lessons on evals, metrics, fairness, agents, red teaming.", "", 15, "2026-06-08", "bootcamp, red-teaming, rag, prompt-engineering, llmops", "L", False),
    ("ThomasJButler/AgenticAICoursePortfolio", "Portfolio of web apps for the CodeCademy 'Mastering Generative AI & Agents for Developers' bootcamp.", "TypeScript", 15, "2026-06-02", "python, api, ai, backend, rag", "B", False),
    ("alexeygrigorev/ai-bootcamp-codespace", "Code for the AI Bootcamp: from RAG to agents.", "Jupyter Notebook", 14, "2025-11-30", "", "FP", False),
    ("42-AI/Python-Bootcamp-Corrections", "Amended corrections of the Python bootcamp by 42 AI.", "", 14, "2022-03-05", "", "F", False),
    ("microsoft/aifundamentalbootcamp", "Get hands-on with AI apps in the App Innovation Fundamental Bootcamp (Microsoft).", "Jupyter Notebook", 13, "2026-04-22", "", "C", False),
    ("gilberto-BE/aifi-bootcamp", "AIFI bootcamp notebooks.", "Jupyter Notebook", 13, "2022-03-03", "", "F", False),
    ("devidrees/AI-Data-Analytics-Bootcamp-October-Batch", "Data Analytics and Artificial Intelligence Bootcamp BDA62.", "Python", 13, "2026-09-27", "python, machine-learning, data-analytics, powerbi", "D", False),
    ("Moinuddin9777/BwAI_Bootcamp_H2S_2026_Hyd", "Build with AI bootcamp series by Hack2Skill and Google for Developers.", "", 13, "2026-07-18", "", "N", False),
    ("odsc2015/Data-Wrangling-With-SQL", "Data wrangling with SQL - part of the AI+ / ODSC West bootcamp training series.", "", 13, "2025-10-11", "", "M", False),
    ("GDG-on-Campus-Benha/Data-Science-AI-24.25", "Official repository of GDG on Campus Banha BootCamp - Data Science & AI track.", "", 13, "2025-02-02", "", "N", False),
    ("abofficial444/KOWOPE", "Machine-learning project: predict customer loan default risk (bootcamp exercise).", "Jupyter Notebook", 13, "2022-03-15", "", "D", False),
    ("VectorInstitute/eval-agents", "Reference implementations for the Agentic AI evaluation bootcamp (Vector Institute).", "Python", 12, "2026-10-15", "", "A", False),
    ("madhusudhankonda/ai-apps-bootcamp", "Software engineer's bootcamp: developing AI applications.", "Python", 12, "2025-06-03", "", "L", False),
    ("GlobalAICommunity/global-ai-bootcamp-2023", "Global AI Bootcamp 2023 session materials.", "", 12, "2023-03-07", "", "N", True),
    ("vivianaranha/complete-ai-engineer-bootcamp-2026", "Python -> ML -> Deep Learning -> LLMs -> RAG -> Agents -> MCP -> APIs -> Evaluation -> Security -> Deployment -> Enterprise AI.", "Python", 12, "2026-09-09", "", "FP", False),
    ("gulbahar-donmez/Team-116", "AI bootcamp team project.", "CSS", 12, "2025-08-30", "", "N", False),
    ("ManuOSMx/gh-copilot-bootcamp-python-ai-demo-2025", "GitHub Copilot bootcamp demo (Python + AI).", "HTML", 11, "2026-04-29", "", "B", False),
    ("keeyong/airflow-bootcamp", "Apache Airflow bootcamp.", "Python", 11, "2025-05-26", "", "M", False),
    ("marketcalls/trading-terminal", "Trading terminal built using Claude Code as part of AI Bootcamp 2.0.", "TypeScript", 11, "2026-07-11", "react, sqlite, stock-market, fastapi, yfinance", "B", False),
    ("kaankilc/GlobalAIHub_Data_Science_Bootcamp_Project", "Final project of Global AI Hub - Aygaz Data Science Bootcamp.", "Jupyter Notebook", 11, "2023-07-24", "", "N", False),
    ("grey8-io/learn-ai-with-grey8", "Free, self-driving AI bootcamp powered by a local LLM tutor - 15 projects across 12 phases, Python basics to deploying agents.", "Python", 11, "2026-10-14", "python, open-source, education, machine-learning, ai", "FP", False),
    ("AbdulRahmanAzam/AI-Season-Course-Material", "Runnable code from AI Season AI Agents Bootcamp (cohort 01): LLM APIs, RAG, agent harness, LangChain, multimodal agents, A2A.", "Python", 11, "2026-09-26", "python, course, mcp, bootcamp, urdu", "A", False),
    ("sithukyaw007/LearnAI-KnowledgeMiningBootcamp", "Enterprise-scale intelligent search over business documents using Azure Cognitive Search.", "HTML", 10, "2018-11-10", "", "R", False),
    ("Naureenfathima/blockseblock-ai-bootcamp", "AI bootcamp exercises.", "Python", 10, "2026-08-15", "", "N", False),
    ("ShawhinT/AI-Builders-Bootcamp-6", "Code repository for AI Builders Bootcamp #6 (fine-tuning, RAG, LLMs).", "Jupyter Notebook", 10, "2025-09-19", "ai, fine-tuning, rag, llm", "L", False),
    ("iws3/gen-ai-2026-official-Repo", "The Generative AI Bootcamp official repository 2026.", "HTML", 10, "2026-08-18", "", "L", False),
    ("hemansnation/AI-Agents-Accelerator", "AI Agents bootcamp / accelerator.", "Python", 10, "2026-02-12", "", "A", False),
    ("qasimriaz002/AI-BootCamp-2026-GIKI", "Python foundations for GIKI AI Boot Camp 2026: NumPy, Pandas & Matplotlib for AI/ML.", "Python", 10, "2026-07-07", "python, numpy, pandas, matplotlib", "F", False),
    ("openhackathons-org/NIM-Bootcamp", "Hands-on applications using NVIDIA Inference Microservices (NIM).", "Jupyter Notebook", 10, "2026-01-29", "natural-language-processing, rag, nims, genai, llm-inference", "C", True),
    ("Sayed-Husain/AI-and-Deep-Learning-Bootcamp", "AI and Deep Learning bootcamp repository - a journey into cutting-edge AI.", "Jupyter Notebook", 10, "2025-12-25", "machine-learning, deep-learning, tensorflow, numpy, sklearn", "F", False),
    ("ONground-Korea/2023-AIKU_DeepLearning-Bootcamp", "2023-1 Korea University AIKU deep-learning vacation bootcamp: Deep into Deep (Korean).", "Jupyter Notebook", 10, "2023-07-10", "", "F", False),
    ("AhmadSait/IntroAI", "Introduction to AI bootcamp at KAU.", "", 10, "2025-01-08", "", "F", False),
    ("tinkerhub/Practical-AI-Bootcamp", "Practical AI bootcamp notebooks (TinkerHub).", "Jupyter Notebook", 9, "2021-11-25", "", "F", False),
    ("VectorInstitute/ai-deployment", "AI deployment bootcamp reference implementations (Vector Institute).", "Python", 9, "2025-11-27", "ai, deployment", "M", False),
    ("openhackathons-org/AI-Powered-Physics-Bootcamp", "AI-powered physics bootcamp labs.", "Jupyter Notebook", 9, "2026-04-23", "", "D", False),
    ("pyladiesams/global-ai-bootcamp-mar2025", "Azure AI workshops (Pyladies Amsterdam, Global AI Bootcamp Mar 2025).", "", 9, "2025-03-06", "workshop, rag, azure-open-ai, microsoft-copilot, azure-postgresql", "R", False),
    ("ahmadsanafarooq/Python-AI-Bootcamp", "Hands-on projects, assignments, notebooks and materials from the Python & AI Bootcamp at iCode.", "Jupyter Notebook", 9, "2025-09-19", "python, ai, numpy, plotly, pandas", "F", False),
    ("shikharkumar13/AI-Engineering-Bootcamp", "AI engineering bootcamp archive.", "Python", 9, "2026-08-23", "", "N", True),
    ("enesmanan/gaih-genai-egitim", "GAIH - Akbank Generative AI introductory bootcamp webinar materials (Turkish).", "Jupyter Notebook", 9, "2025-10-19", "", "R", False),
    ("ThinkInAIXYZ/agent-zero-to-one", "Hands-on, zero-to-one AI agent bootcamp by ThinkInAI x MemVerge: long-term memory, toolchains, deployment.", "", 9, "2025-11-28", "", "A", False),
    ("HROlive/Tropical-Cyclone-Intensity-Estimation", "Categorizing hurricanes by intensity with a deep CNN trained on GPUs (bootcamp project).", "Jupyter Notebook", 9, "2023-09-11", "python, machine-learning, deep-learning, neural-network, cnn", "D", False),
    ("openbuildxyz/Startnet-AI-Bootcamp", "Starknet AI agent developer bootcamp - blockchain + AI innovation (Chinese).", "", 8, "2025-05-28", "bootcamp, web3, starknet", "D", False),
    ("PacktPublishing/Full-Stack-AI-and-Mastering-AI-Agents-Bootcamp", "Full-Stack AI and Mastering AI Agents bootcamp (Packt).", "Python", 8, "2025-12-15", "", "A", False),
    ("RamsesCamas/Bootcamp_AI_Engineer_Codigofacilito_2nd_Gen", "Code and slides of the AI Engineer bootcamp, 2nd generation (Spanish).", "Python", 8, "2026-10-17", "", "FP", False),
    ("popescuaaa/upb-ai-bootcamp-2024", "Course materials for the AI bootcamp (UPB 2024).", "Jupyter Notebook", 8, "2024-04-11", "", "F", False),
    ("Acronus2008/ai-agent-engineering-bootcamp", "14-day self-paced bootcamp for enterprise AI agent engineering: architecture, security, distribution.", "HTML", 8, "2026-08-15", "", "A", False),
    ("JumpX-Labs/ai-bootcamp-demo01-fruit-nn", "Interactive in-browser neural-network teaching tool (React + TensorFlow.js): 6 fruit classes, 10 features (Chinese).", "TypeScript", 8, "2026-07-24", "", "F", False),
    ("mybozkir/Pokemon_Classification", "Pokemon classification project - Global AI Akbank data-analysis bootcamp (Turkish).", "Jupyter Notebook", 8, "2024-05-18", "", "D", False),
    ("Ratnesh-181998/Build-Agentic-AI-and-Gen-AI-Agents-with-MCP", "Model Context Protocol (MCP) bootcamp: MCP architecture and its role in the agentic AI ecosystem.", "", 8, "2026-10-14", "github, python, docker, mcp, faiss", "A", False),
    ("husnusensoy/tt-ai-bootcamp", "TT AI Bootcamp 2026 notebooks.", "Jupyter Notebook", 7, "2026-07-04", "", "N", False),
    ("labeveryday/language-learning-assistant", "Language-learning assistant built for the Generative AI bootcamp.", "Python", 7, "2025-02-16", "", "L", False),
    ("angwanqi/gcp-ai-bootcamp", "GCP AI bootcamp notebooks.", "Jupyter Notebook", 7, "2025-11-26", "", "C", False),
    ("ShawhinT/AI-Builders-Bootcamp-5", "Code repository for AI Builders Bootcamp #5 (fine-tuning, RAG, LLMs).", "Jupyter Notebook", 7, "2025-07-11", "ai, fine-tuning, rag, llm", "L", False),
    ("Ali-Razmdideh/ai-bootcamp", "Quera AI bootcamp exercises (https://quera.org/bootcamp/ai).", "HTML", 7, "2026-06-12", "", "F", False),
    ("DataScienceNigeria/DSN-AI-Bootcamp-2024-Qualification-Project-Participation-and-Hackathon", "DSN AI Bootcamp 2024 qualification project & hackathon participation.", "", 7, "2024-09-25", "", "N", False),
    ("MajidRaimi/AI-BootCamp", "Artificial Intelligence boot camp from the AI Club at Imam Abdulrahman University.", "Jupyter Notebook", 7, "2023-01-17", "", "F", False),
    ("Wagademy/agent-camp", "Introductory bootcamp for coding with decentralized AI agents.", "", 7, "2025-02-15", "", "A", False),
    ("Md-Emon-Hasan/Complete-Agentic-AI-Bootcamp-With-LangGraph-and-Langchain", "Complete hands-on agentic AI bootcamp: LangGraph, LangChain, multi-agent workflows, RAG pipelines, tools.", "Jupyter Notebook", 7, "2026-05-22", "natural-language-processing, deep-learning, transformers, semantic-search, multi-agent-systems", "A", False),
    ("mukundnaramesh2605/ai-ml-course-bootcamp", "AI/ML course bootcamp notebooks.", "Jupyter Notebook", 0, "2026-10-18", "", "N", False),
    ("0686sushmita/gen_ai", "v18hub GenAI bootcamp notebooks.", "Jupyter Notebook", 0, "2026-10-18", "", "N", False),
    ("milangavric2003/ai-bootcamp-week-7", "AI bootcamp week 7 exercises.", "Python", 0, "2026-10-18", "", "N", False),
    ("backy22/ai-engineering-bootcamp-prerequisites", "Fork of the AI engineering bootcamp prerequisites.", "Python", 0, "2026-10-18", "", "N", False),
    ("kristineservia/practice", "Practice projects from TripleTen's AI-Assisted Software Engineering bootcamp content.", "JavaScript", 0, "2026-10-18", "", "B", False),
    ("Gift-Sato-Kuepouo/Quadruped_-bionic_for_-grade_6-9-_programming", "PuppyPi bionic quadruped K-12 AI & robotics bootcamp (grades 6-9): 12-week curriculum, ROS/SLAM/IoT/ML projects.", "", 0, "2026-10-18", "", "D", False),
    ("tech-tj/ai-bootcamp", "AI bootcamp pages.", "HTML", 0, "2026-10-18", "", "N", False),
    ("johndimitry/dio-budget-ai-api", "Intelligent budgeting API with Spring Boot & Spring AI: Whisper transcription + GPT-4o tool calls (Portuguese).", "Java", 0, "2026-10-18", "", "L", False),
    ("erradihanae8-AI/Geeks_Bootcamp_AI-Full-Stack-Developer-", "Geeks bootcamp AI full-stack developer exercises.", "Python", 0, "2026-10-18", "", "N", False),
    ("mfrdixon/STAC_AI_Bootcamp", "STAC AI workshop: seven financial AI notebooks, evidence graphs, evaluation and governance experiments.", "Jupyter Notebook", 0, "2026-10-18", "", "D", False),
    ("Project-TETI/BOOTCAMP-AI", "Post-disaster damage assessment & triage system (SegFormer + RAG).", "Jupyter Notebook", 0, "2026-10-17", "", "D", False),
    ("GAURAV24-CODE/AI-ML-Engineer-Bootcamp", "AI/ML engineer bootcamp notebooks.", "Jupyter Notebook", 1, "2026-10-17", "", "N", False),
    ("diegofloriano/dio-budgeting-spring-ai", "Spring Boot project with Spring AI and Gradle from Bootcamp DIO (Portuguese).", "Java", 0, "2026-10-17", "", "L", False),
    ("anne9985/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-17", "devops, web-development, code, notes, aiml", "N", False),
    ("Wilson6858/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-17", "devops, web-development, code, notes, aiml", "N", False),
    ("KimberlyRay74864/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-17", "devops, web-development, code, notes, aiml", "N", False),
    ("ShahzadSarwar10/Full-Stack-AI-Bootcamp-B-12", "Full-stack AI bootcamp, batch 12 coursework.", "Python", 0, "2026-10-17", "", "N", False),
    ("douglaspersson53/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-17", "devops, web-development, code, notes, aiml", "N", False),
    ("juliawarren01261/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-17", "devops, web-development, code, notes, aiml", "N", False),
    ("mlbala/fde-bootcamp", "Forward Deployed Engineer bootcamp: Python, API development, cloud deployment, RAG, agentic systems.", "Jupyter Notebook", 0, "2026-10-17", "", "FP", False),
    ("luisnriquet/Bootcamp-ai", "Bootcamp AI exercises.", "Python", 0, "2026-10-17", "", "N", False),
    ("shamarta/ai-infrastructure-bootcamp", "AI Infrastructure bootcamp: building and managing modern AI infrastructure with Linux, Docker and friends.", "Python", 0, "2026-10-17", "", "M", False),
    ("vardhanshree5-cloud/dark-vader", "AI bootcamp project.", "TypeScript", 0, "2026-10-17", "", "N", False),
    ("Lina18558/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-17", "devops, web-development, code, notes, aiml", "N", False),
    ("palashlabre07/google-bootcampAI", "Bootcamp with AI exercises.", "TypeScript", 0, "2026-10-17", "", "N", False),
    ("iamrajendraverma/ai-bootcamp-bhopal", "AI bootcamp Bhopal project.", "TypeScript", 0, "2026-10-17", "", "N", False),
    ("Engstrom59470/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-17", "devops, web-development, code, notes, aiml", "N", False),
    ("abuzaid268/Agentic-AI-Bootcamp-Students", "Agentic AI bootcamp student repository.", "HTML", 0, "2026-10-17", "", "N", False),
    ("yassine-adabache/Geeks.Institute-ai-full-stack-bootcamp", "Geeks Institute AI full-stack bootcamp work.", "", 0, "2026-10-17", "", "N", False),
    ("DennyM55/agentic-ai-bootcamp", "Agentic AI bootcamp exercises.", "Python", 0, "2026-10-17", "", "N", False),
    ("shallysubhash/ai-engineering-buildcamp-codespaces", "Code for AI engineering bootcamp (codespaces).", "Jupyter Notebook", 0, "2026-10-17", "", "N", False),
    ("Raunak1818/ai-llm-engineering-bootcamp", "Learning journey in AI & LLM engineering: Python, Git, Docker, RAG, agents, LangChain, LangGraph, multimodal AI.", "Python", 0, "2026-10-17", "", "N", False),
    ("aabdulhanan-spec/RAG_CHATBOT_AI-BOOTCAMP", "AI-powered Toronto travel chatbot using RAG, LangChain, HF embeddings, Pinecone, OpenAI and Streamlit.", "Python", 0, "2026-10-17", "", "R", False),
    ("Gaurav-devv/AI-Bootcamp-2026", "AI bootcamp 2026 notebooks.", "Jupyter Notebook", 1, "2026-10-17", "", "N", False),
    ("Maheen1824/Python-to-AI-bootcamp", "3-day learning-based bootcamp: Python to AI.", "Python", 0, "2026-10-17", "", "N", False),
    ("atiashafiq1103/AtiaShafiq_python-to-ai-bootcamp", "Code files for the Python-to-AI bootcamp (GDGoC CUI Wah): Python fundamentals, basic data analysis.", "", 0, "2026-10-17", "", "N", False),
    ("moizbintariq/Python-to-ai-Bootcamp", "Python-to-AI bootcamp notebooks.", "Jupyter Notebook", 0, "2026-10-17", "", "N", False),
    ("LaylaAbboud02/ai-ml-bootcamp", "AI/ML bootcamp notebooks.", "Jupyter Notebook", 0, "2026-10-17", "", "N", False),
    ("Chidinmanjoku/DSN--AI--BOOTCAMP--2026--SALES-PROFITABILITY-DASHBOARD", "Data cleaning, dashboard auditing and sales/profitability analysis with Excel & Power BI (DSN AI Bootcamp 2026).", "", 0, "2026-10-17", "", "D", False),
    ("ShaffaqAmjad/Python-to-AI-Bootcamp", "Practice work for the 3-day Python to AI bootcamp.", "Python", 1, "2026-10-17", "", "N", False),
    ("NaomiMabini/AI-REU-Bootcamp-2026", "AI REU bootcamp 2026 notebooks.", "Jupyter Notebook", 0, "2026-10-18", "", "N", False),
    ("nayeonlewis665/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-18", "devops, web-development, code, notes, aiml", "N", False),
    ("hanateixeira1733/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-18", "devops, web-development, code, notes, aiml", "N", False),
    ("Pinare890/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-18", "devops, web-development, code, notes, aiml", "N", False),
    ("Deborahr324/100xSchool_Bootcamp_1.0", "Fork of 100xdevs Bootcamp 1.0 notes & assignments (WebDev + DevOps, AI and ML, Web3, DSA).", "JavaScript", 0, "2026-10-18", "devops, web-development, code, notes, aiml", "N", False),
    ("ozdemirr1/ai-backend-bootcamp", "12-month AI-assisted backend/full-stack developer bootcamp: Python, FastAPI, PostgreSQL, Docker, React, AI integration.", "Python", 0, "2026-10-18", "", "B", False),
    ("mori-kirkland/ai-engineer-bootcamp-prerequisties", "A starting point for AI engineer training.", "", 0, "2026-10-18", "", "N", False),
    ("hasankanaan26/prep-kit", "Prep kit for SE Factory's Applied AI Engineering bootcamp: venv, APIs, keys, first LLM calls, setup check.", "Python", 0, "2026-10-18", "", "F", False),
    ("aykut-gumus/AI-dev-bootcamp", "AI dev bootcamp notebooks.", "Jupyter Notebook", 0, "2026-10-18", "", "N", False),
    ("niat-cloud/AI-bootcamp-Check-In", "AI bootcamp check-in app.", "TypeScript", 0, "2026-10-18", "", "N", False),
]


def fmt_stars(n: int) -> str:
    if n >= 1000:
        v = n / 1000
        return f"{v:.1f}k".replace(".0k", "k")
    return str(n)


def repo_url(name: str) -> str:
    return f"https://github.com/{name}"


def build_records():
    recs = []
    for name, desc, lang, stars, updated, topics, cat, archived in REPOS:
        num, slug, title, blurb = CATS[cat]
        recs.append({
            "full_name": name,
            "url": repo_url(name),
            "description": desc,
            "language": lang or "—",
            "stars": stars,
            "stars_display": fmt_stars(stars),
            "updated": updated,
            "topics": [t.strip() for t in topics.split(",") if t.strip()],
            "category": cat,
            "category_slug": slug,
            "category_title": title,
            "archived": archived,
        })
    return recs


def table(rows, with_cat=False):
    head = "| Repository | ★ | Language | Updated | Description |"
    sep = "|---|---:|---|---|---|"
    lines = [head, sep]
    for r in rows:
        arch = " *(archived)*" if r["archived"] else ""
        desc = r["description"].replace("|", "/")
        lines.append(
            f"| [{r['full_name']}]({r['url']}) | {r['stars_display']} | {r['language']} | {r['updated']} | {desc}{arch} |"
        )
    return "\n".join(lines)


def main():
    recs = build_records()
    os.makedirs(f"{ROOT}/data", exist_ok=True)
    os.makedirs(f"{ROOT}/resources", exist_ok=True)

    # ---------------- data exports ----------------
    with open(f"{ROOT}/data/repos.json", "w", encoding="utf-8") as fh:
        json.dump({
            "project": "AI-BOOTCAMP 2026 · Codes by Febin",
            "source": "Public GitHub search extraction (AI bootcamp repositories)",
            "snapshot_date": "2026-10-18",
            "repo_count": len(recs),
            "categories": {k: {"slug": v[1], "title": v[2], "blurb": v[3]} for k, v in CATS.items()},
            "repos": recs,
        }, fh, indent=2, ensure_ascii=False)

    with open(f"{ROOT}/data/repos.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["full_name", "url", "description", "language", "stars", "updated", "topics", "category_code", "category", "archived"])
        for r in recs:
            w.writerow([r["full_name"], r["url"], r["description"], r["language"],
                        r["stars"], r["updated"], "; ".join(r["topics"]),
                        r["category"], r["category_title"], r["archived"]])

    # ---------------- per-category resource files ----------------
    cat_counts = Counter(r["category"] for r in recs)
    for code, (num, slug, title, blurb) in CATS.items():
        rows = sorted([r for r in recs if r["category"] == code], key=lambda r: -r["stars"])
        md = [f"# {title}", "", blurb, "",
              f"`{len(rows)} repository links` · part of the [AI-BOOTCAMP 2026 catalog](../README.md) · back to [full catalog](../CATALOG.md)", "",
              "Sorted by GitHub stars at extraction time (2026-10-18).", "",
              table(rows), ""]
        with open(f"{ROOT}/resources/{num}-{slug}.md", "w", encoding="utf-8") as fh:
            fh.write("\n".join(md))

    # ---------------- CATALOG.md (everything, one page) ----------------
    lines = ["# Full Catalog — every extracted repository", "",
             f"All **{len(recs)}** repositories extracted from the AI-bootcamp search snapshot (2026-10-18), grouped by curriculum track. Machine-readable copies live in [`data/repos.json`](data/repos.json) and [`data/repos.csv`](data/repos.csv).", ""]
    for code, (num, slug, title, blurb) in CATS.items():
        rows = sorted([r for r in recs if r["category"] == code], key=lambda r: -r["stars"])
        lines += [f"## {title}", "", f"_{blurb}_ [`{len(rows)} repos`](resources/{num}-{slug}.md)", "", table(rows), ""]
    with open(f"{ROOT}/CATALOG.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"OK — {len(recs)} repository links, {len(CATS)} categories")
    for code, (num, slug, title, _) in CATS.items():
        print(f"  {num} {slug:<10} {cat_counts[code]:>3} repos  {title}")


if __name__ == "__main__":
    main()
