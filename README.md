# 🎧 Study Buddy AI

> An AI-powered quiz generator that creates multiple-choice and fill-in-the-blank questions on any topic, using Groq LLM and LangChain.

---

## 📌 What Does This App Do?

You enter a topic (e.g. "Indian History"), pick a difficulty level and question type, and the app generates a quiz by:

1. Sending your topic to a Groq LLM (LLaMA 3.1)
2. Receiving a well-structured question back (parsed via Pydantic)
3. Presenting it to you in a Streamlit UI
4. Evaluating your answers and showing your score
5. Letting you download results as a CSV

---

## 🏗️ Project Structure

```
D:/Buddy/
│
├── application.py              # 🚪 Main entry point — the Streamlit web UI
├── requirements.txt            # 📦 Python dependencies
├── setup.py                    # 📦 Package installation config
├── Dockerfile                  # 🐳 Docker image for deployment
├── .env                        # 🔑 API keys (GROQ_API_KEY lives here — NEVER commit this)
├── .gitignore
│
├── manifests/                  # ☸️ Kubernetes deployment files
│   ├── deployment.yaml         #   Deploys 2 replicas of the app
│   └── service.yaml           #   Exposes app on NodePort 80
│
└── src/                       # 🧠 All business logic lives here
    ├── common/
    │   ├── custom_exception.py  #   Custom error class with full traceback info
    │   └── logger.py           #   Logs events to logs/log_YYYY-MM-DD.log daily
    │
    ├── config/
    │   └── settings.py         #   Central config: API key, model name, temperature, retries
    │
    ├── generator/
    │   └── generator_generatior.py  #   QuestionGenerator — calls LLM, retries on failure
    │
    ├── llm/
    │   └── groq_client.py      #   Thin wrapper around ChatGroq from langchain-groq
    │
    ├── models/
    │   └── Question_schemea.py #   Pydantic schemas: MCQQuestion, FILLBlankquestion
    │
    ├── prompts/
    │   └── template.py         #   LangChain PromptTemplate objects for MCQ & fill-blank
    │
    └── utils/
        └── helpers.py          #   QuizManager — handles quiz state, evaluation, CSV saving
```

---

## ⚙️ How It Works — Step by Step

### 1. User Opens the App
Streamlit renders `application.py`. The user fills in the sidebar:

| Field | Options |
|-------|---------|
| **Question Type** | Multiple Choice, Fill in the Blank |
| **Topic** | Any text, e.g. "Indian History", "Python lists" |
| **Difficulty** | Easy, Medium, Hard |
| **Number of Questions** | 1–10 |

### 2. Quiz Generation (Click "Generate Quiz")

```
application.py
  └── QuizManager.generate_questions()
        └── QuestionGenerator (src/generator/generator_generatior.py)
              └── get_groq_llm() → ChatGroq → Groq API (LLaMA 3.1 8B)
```

Inside `QuestionGenerator`:

```
a) Build a prompt using PromptTemplate from src/prompts/template.py
   - mcq_prompt_template  → asks for JSON with question, options[4], correct_answer
   - fill_blank_prompt_template → asks for JSON with question (has "___"), answer

b) Wrap the LLM response with PydanticOutputParser
   - MCQQuestion  → parsed into a Pydantic model
   - FillBlankQuestion → parsed into a Pydantic model

c) Validate structure:
   - MCQ: must have exactly 4 options, correct_answer must be one of them
   - Fill-blank: question string must contain "___"

d) Retry up to MAX_RETRIES (3) if parsing fails, then raise CustomException
```

### 3. Quiz Attempt (User answers in the UI)

```
QuizManager.attempt_quiz()
  └── For each question:
        ├── If MCQ  → st.radio() button group
        └── If Fill-blank → st.text_input() free text
  └── Answers stored in self.user_answers[]
```

### 4. Submit & Evaluate (Click "Submit Quiz")

```
QuizManager.evaluate_quiz()
  └── For each (question, user_answer):
        ├── MCQ:  is_correct = (user_answer == correct_answer)
        └── Fill-blank: is_correct = (user_answer.strip().lower() == answer.strip().lower())
  └── Results stored in self.results[]
```

Score is shown as a percentage. Each question is marked ✅ or ❌ with correct answer shown for wrong ones.

### 5. Save Results (Click "Save Results")

```
QuizManager.save_to_csv()
  └── Saves to results/quiz_results_YYYYMMDD_HHMMSS.csv
  └── Offers download button in Streamlit
```

---

## 🔌 LLM Prompt Flow

### MCQ Prompt (sent to Groq)
```
Generate a {difficulty} multiple-choice question about {topic}.

Return ONLY a JSON object with these exact fields:
- 'question': A clear, specific question
- 'options': An array of exactly 4 possible answers
- 'correct_answer': One of the options that is the correct answer

Example format:
{{
    "question": "What is the capital of France?",
    "options": ["London", "Berlin", "Paris", "Madrid"],
    "correct_answer": "Paris"
}}

Your response:
```

### Fill-in-Blank Prompt (sent to Groq)
```
Generate a {difficulty} fill-in-the-blank question about {topic}.

Return ONLY a JSON object with these exact fields:
- 'question': A sentence with '_____' marking where the blank should be
- 'answer': The correct word or phrase that belongs in the blank

Example format:
{{
    "question": "The capital of France is _____.",
    "answer": "Paris"
}}

Your response:
```

---

## 🔑 Configuration (src/config/settings.py)

| Setting | Value | Meaning |
|---------|-------|---------|
| `GROQ_API_KEY` | from `.env` | API key for Groq Cloud |
| `MODEL_NAME` | `llama-3.1-8b-instant` | Groq model used |
| `TEMPERATURE` | `0.9` | Higher = more creative/random outputs |
| `MAX_RETRIES` | `3` | How many times to retry failed LLM calls |

---

## 🐳 Deployment

### Local (manual)
```bash
cd D:/Buddy
pip install -r requirements.txt
cp .env.example .env   # add your GROQ_API_KEY
streamlit run application.py
```

### Docker
```bash
docker build -t studybuddy .
docker run -p 8501:8501 --env-file .env studybuddy
```

### Kubernetes
```bash
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
```

> **Note:** The Kubernetes deployment expects a Secret named `groq-api-secret` containing the key `GROQ_API_KEY`.

---

## 📁 Key Files at a Glance

| File | Purpose |
|------|---------|
| `application.py` | Streamlit UI — sidebar controls, question display, score display |
| `src/utils/helpers.py` | `QuizManager` — quiz state, evaluation, CSV save |
| `src/generator/generator_generatior.py` | `QuestionGenerator` — LLM call + retry logic |
| `src/llm/groq_client.py` | Creates the ChatGroq client |
| `src/prompts/template.py` | LangChain prompt templates |
| `src/models/Question_schemea.py` | Pydantic models for parsed LLM output |
| `src/common/custom_exception.py` | Custom exceptions with file/line info |
| `src/common/logger.py` | Daily log files in `logs/` directory |
| `src/config/settings.py` | All configuration constants |

---

## ⚠️ Common Issues for New Contributors

1. **`.env` missing** — App will crash if `GROQ_API_KEY` is not set. Copy `.env.example` and fill in your key.
2. **Model parsing** — The LLM must return valid JSON. Prompts include explicit format instructions to reduce failures.
3. **Retries** — If the LLM returns malformed JSON 3 times in a row, `CustomException` is raised.
4. **Fill-blank validation** — The question must contain `"___"`. If the LLM misses it, the question is rejected.

---

## 🛠️ Extending the App

### Add a new question type
1. Add a new Pydantic model in `src/models/Question_schemea.py`
2. Add a new prompt template in `src/prompts/template.py`
3. Add a `generate_<type>` method in `src/generator/generator_generatior.py`
4. Handle the new type in `QuizManager.generate_questions()` and `attempt_quiz()`

### Change the LLM provider
Only `src/llm/groq_client.py` and `src/config/settings.py` need updating.

### Add logging middleware
`src/common/logger.py` uses Python's standard `logging` module. Swap `basicConfig` for a rotating file handler if you need log rotation at size.