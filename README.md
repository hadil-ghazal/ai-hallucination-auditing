---
title: AI Hallucination Auditing
sdk: streamlit
sdk_version: "1.45.1"
app_file: app.py
license: mit
colorFrom: blue
colorTo: indigo
pinned: false
short_description: Auditing LLM reliability in compliance workflows.
---

# AI Hallucination Auditing

Evaluating LLM reliability in high-stakes compliance workflows through hallucination auditing and stress testing.

## Problem Statement

Organizations are rapidly adopting large language models for compliance, regulatory, and financial workflows. However, hallucinated information can introduce legal, operational, and reputational risk.

This project investigates when and why LLMs fail when summarizing compliance-related documents.

## Research Question

Under which conditions do large language models hallucinate most frequently when interpreting compliance text?

## Project Overview

This application generates summaries from compliance scenarios and automatically audits the outputs for reliability.

The system evaluates whether critical facts are preserved and flags responses that may require human review.

## Features

* Interactive Streamlit dashboard
* Synthetic compliance benchmark dataset
* Automated LLM summarization
* Hallucination auditing pipeline
* Dynamic user-provided text evaluation
* Risk scoring and recommendations

## Stress Test Categories

* Ambiguous prompts
* Incomplete information
* Conflicting context
* Domain-specific jargon
* Long-context scenarios
* Standard compliance scenarios

## Evaluation Metrics

* Fact Recall
* Hallucination Rate
* Completeness Score
* Risk Level Classification

## Results

The final evaluation dataset contained 120 synthetic compliance scenarios spanning six stress-test categories.

### Overall Performance

| Metric                     | Result |
| -------------------------- | -----: |
| Hallucination Rate         |  22.5% |
| Average Fact Recall        |  59.4% |
| Average Completeness Score |   1.06 |

### Performance by Stress Type

| Stress Type  | Hallucination Rate | Fact Recall |
| ------------ | -----------------: | ----------: |
| Normal       |                35% |         65% |
| Ambiguous    |                 0% |         50% |
| Conflicting  |                35% |         43% |
| Incomplete   |                65% |         39% |
| Jargon       |                 0% |         72% |
| Long Context |                 0% |         87% |

### Key Findings

* Incomplete information produced the highest hallucination risk.
* Conflicting context reduced fact recall substantially.
* Domain-specific jargon had less impact than expected.
* Long-context scenarios performed better than incomplete scenarios.
* Evaluation methodology significantly influenced measured hallucination rates.

These results suggest that missing information is a stronger driver of hallucinations than document length.

## Tech Stack

* Python
* Streamlit
* OpenAI API
* Pandas
* python-dotenv

## Reproducibility

### Prerequisites

* Python 3.10+
* OpenAI API key

### Installation

Clone the repository:

```bash
git clone https://github.com/hadil-ghazal/ai-hallucination-auditing.git

cd ai-hallucination-auditing
```

Create and activate a virtual environment:

```bash
python -m venv .venv

source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

### Generate the Synthetic Dataset

```bash
python src/generate_dataset.py
```

This creates:

```text
data/compliance_cases.csv
```

### Generate LLM Summaries

```bash
python src/generate_summary.py
```

This creates:

```text
results/summary_results.csv
```

### Run Evaluation

```bash
python src/evaluation/evaluate.py
```

This creates:

```text
results/evaluated_results.csv
```

### Launch the Dashboard

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Future Improvements

* Multi-model comparisons
* Retrieval-augmented verification
* Human feedback loops
* Citation-based validation
* Real-time monitoring dashboards
* Regulatory rule engines

## Disclaimer

This project is a research prototype intended for educational purposes only and should not be used as a substitute for formal compliance review

Human review remains essential for highstakes use cases
