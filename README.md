# TruthLens AI

**AI-powered claim verification with evidence-backed verdicts.**

TruthLens AI is a multimodal claim verification platform designed to analyze claims, collect relevant web evidence, identify conflicting information, and generate explainable verdicts with source references.

The goal is to help users evaluate online information using evidence rather than relying on unsupported AI-generated answers.

## Features

- **Claim Management** — Submit claims and review saved investigations.
- **Web Evidence Collection** — Gather relevant sources for claim verification.
- **Evidence Analysis** — Evaluate evidence and identify supporting or conflicting information.
- **Explainable Verdicts** — Present a verdict, confidence score, summary, and evidence assessments.
- **Source References** — Display the sources used during an investigation.
- **Multimodal Verification** — Designed to support claims originating from text and visual content.
- **AI Chatbot** — Ask follow-up questions about a claim and its available evidence.
- **Authentication** — Protected access to user-specific claim data.

*Feature availability may depend on the current implementation and configured services.*

## Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, Vite |
| Backend | Python, FastAPI |
| Database | PostgreSQL, Supabase |
| Data access and migrations | SQLAlchemy, Alembic |
| AI and evidence processing | LLMs, RAG, web evidence retrieval |
| Development | Git, GitHub |

## Project Structure

```text
Truthlens 1.0/
├── client/          # React frontend
├── server/          # FastAPI backend
├── docs/            # Project documentation
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- Node.js and npm
- A configured PostgreSQL database
- Required API credentials for the services you enable

### 1. Configure the backend

From the project root, create a virtual environment if you do not already have one:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
python -m pip install -r server/requirements.txt
```

Ensure your environment variables are configured before running migrations.

### 2. Start the backend

From the project root:

```powershell
python -m uvicorn app.main:app --reload --app-dir server --port 8000
```


### 3. Start the frontend

Open a second terminal at the project root:

```powershell
Set-Location client
npm install
npm run dev
```

Open the local URL printed by Vite in the terminal.

To create a production build:

```powershell
npm run build
```

## Security

- Keep API keys and secrets in local environment variables.
- Never commit `.env` files or credentials.
- Use placeholder values in example environment files.
- Keep privileged API keys on the backend.
- Verify evidence and source references before relying on generated verdicts.

## Project Status

TruthLens AI is under active development. Features and integrations may evolve as evidence collection, analysis, and verification capabilities are improved.

## Responsible AI

TruthLens AI assists with evaluating claims; it does not guarantee that every verdict is correct. Results depend on source quality, evidence coverage, retrieval accuracy, and model limitations. Important claims should be checked against reliable primary sources.

## Future Enhancements

- **Advanced Multimodal Verification** — Analyze text, screenshots, images, and social media content to identify potentially misleading claims.
- **OCR-Based Claim Extraction** — Extract text from uploaded images and documents for verification.
- **Improved Evidence Retrieval** — Enhance web search and RAG pipelines to retrieve relevant, reliable, and diverse sources.
- **Contradiction Detection** — Identify disagreements between sources and explain why the evidence conflicts.
- **Evidence Quality Assessment** — Evaluate source credibility, relevance, recency, and evidence coverage.
- **Citation-Backed AI Responses** — Improve traceability by linking generated explanations to supporting source passages.
- **Evaluation and Benchmarking** — Measure retrieval quality, verdict consistency, and citation accuracy using test datasets.
- **Performance and Scalability** — Improve response times, error handling, and resource efficiency.
- **Deployment and Monitoring** — Strengthen production deployment, logging, and service health monitoring.

*These enhancements are planned and may change as the project evolves.*

## License

No license has been specified yet. All rights reserved unless a license is added to this repository.