# ShopAssist AI QA Automation

An AI-focused QA automation project designed to validate the functionality, reliability, policy compliance, and response quality of an e-commerce customer support chatbot.

The project combines traditional automated regression testing with LLM evaluation techniques to assess both deterministic policy requirements and AI-generated responses.

## Tech Stack

- **Python** — Test automation and API integration
- **pytest** — Test execution and data-driven testing
- **DeepEval** — LLM response evaluation
- **Google Gemini** — LLM-as-a-judge evaluation
- **Dify** — RAG-based chatbot development
- **REST APIs** — Chatbot integration and testing
- **GitHub Actions** — Continuous integration

## Project Overview

ShopAssist is a fictional e-commerce customer support chatbot built using Dify.

It uses Retrieval-Augmented Generation (RAG) to retrieve information from a custom knowledge base containing store policies.

The chatbot answers customer questions about:

- Returns and refunds
- Shipping and delivery
- Order cancellations
- Payment security
- Product warranties

The QA automation framework validates the chatbot's responses against predefined business requirements and evaluates whether its answers are relevant, factually grounded, and compliant with store policies.

## Test Coverage

### Automated Regression Testing

The project includes six pytest regression tests covering five policy scenarios.

| Test ID | Scenario |
|---|---|
| TC_001 | Return eligibility based on delivery date |
| TC_002 | Delayed shipping and delivery |
| TC_003 | Cancellation of shipped orders |
| TC_004 | Protection of sensitive payment information |
| TC_005 | Product warranty eligibility |

An additional cancellation test verifies that the chatbot explains why shipped orders cannot be cancelled and mentions the return option.

**Latest cached-response regression results: 6 passed.**

Regression tests use stored chatbot responses by default for fast, repeatable execution. Live chatbot testing is available separately.

### AI Response Evaluation

The project uses DeepEval to evaluate chatbot responses using three metrics:

**1. Policy Correctness (G-Eval)**

Evaluates whether responses follow the expected ShopAssist policies, including eligibility conditions, restrictions, and factual accuracy.

**2. Faithfulness**

Evaluates whether chatbot responses are supported by the retrieved knowledge-base context, helping identify unsupported or hallucinated information.

**3. Answer Relevancy**

Evaluates whether responses directly address the customer's question without unnecessary or irrelevant information.

Each metric is applied to five test scenarios, resulting in **15 AI evaluation checks**.

The configured evaluation threshold is 0.8.

AI evaluations depend on Gemini API availability and usage limits. Some evaluation runs have been interrupted by API rate limits rather than failing their quality thresholds.

## Key QA Finding

### Return Policy Answer Relevancy

During testing, the return eligibility scenario produced a response that was factually grounded but did not meet the answer relevancy threshold.

**Issue:** The retrieved knowledge context contained repetitive policy information, affecting the chatbot's response quality.

**Investigation:** Faithfulness and answer relevancy results were compared to identify the difference between factual grounding and relevance.

**Resolution:** The knowledge-base content was refined, the chatbot response was refreshed, and the affected evaluation was rerun successfully.

This demonstrated how LLM evaluation metrics can reveal response-quality issues that traditional functional assertions may not detect.

## Project Structure

```text
shopassist-ai-qa/
├── .github/
│   └── workflows/
│       └── qa-tests.yml
├── tests/
│   ├── api/
│   │   ├── test_cancellation.py
│   │   └── test_policy_dataset.py
│   └── evaluations/
│       ├── test_ai_evaluation.py
│       ├── test_faithfulness.py
│       └── test_relevancy.py
├── test_data/
├── conftest.py
├── dify_client.py
├── test_cases.json
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/shopassist-ai-qa.git
cd shopassist-ai-qa
```

Replace `YOUR_USERNAME` with the repository owner's GitHub username.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and configure the required credentials:

```dotenv
DIFY_API_BASE_URL=https://api.dify.ai/v1
DIFY_API_KEY=your_dify_api_key
GOOGLE_API_KEY=your_google_api_key
```

Never commit real API keys to version control.

The default cached-response regression tests do not require live API credentials when the corresponding test fixtures are available.

## Running Tests

### Cached-Response Regression Tests

```bash
python -m pytest tests/api/ -v
```

Runs six regression tests against stored chatbot responses.

### Live Chatbot Regression Tests

```bash
python -m pytest tests/api/ -v --live
```

Fetches fresh responses from Dify before validating them.

### AI Evaluation Tests

```bash
python -m pytest tests/evaluations/ -v
```

Runs DeepEval evaluations using the configured Gemini model.

To evaluate fresh chatbot responses:

```bash
python -m pytest tests/evaluations/ -v --live
```

**Note:** AI evaluation requires valid Gemini credentials and may encounter rate limits. Live tests also depend on Dify availability.

## CI/CD — GitHub Actions

GitHub Actions is configured to execute the regression test suite automatically when changes are pushed or pull requests are opened.

The workflow:

1. Checks out the repository.
2. Configures Python 3.12.
3. Installs the project dependencies.
4. Executes the six pytest regression tests.
5. Reports the results in GitHub Actions.

The workflow also supports manual execution.

Gemini-based AI evaluations are excluded from automatic CI runs to avoid unnecessary API usage and rate-limit failures.

## Limitations and Future Improvements

- Cached-response tests validate stored outputs rather than the current availability of the live chatbot.
- Live tests require a configured Dify application and API credentials.
- AI evaluations require external model access and may be affected by API quotas.
- Some regression assertions use exact text matching and may require refinement to handle semantically equivalent responses.
- Future improvements could include additional adversarial testing, expanded policy scenarios, and evaluation reporting.

## Skills Demonstrated

- Python test automation
- Data-driven testing with pytest
- REST API testing
- AI/LLM quality assurance
- RAG chatbot evaluation
- LLM-as-a-judge testing
- Faithfulness and hallucination assessment
- Test result investigation
- Regression testing
- CI/CD with GitHub Actions

---

**Project type:** Personal QA automation portfolio project

**Focus:** AI testing, API automation, and LLM response quality assurance
