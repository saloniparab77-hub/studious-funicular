# 🔍 AI Code Reviewer

> A rule-based static code analysis tool built with Python & Streamlit — no API key required, instant feedback, runs 100% offline.

---

## 📌 About the Project

**AI Code Reviewer** is an intelligent static analysis tool that reviews your code and provides:

- 🔴 **Errors** — critical bugs and dangerous patterns
- 🟡 **Warnings** — bad practices and PEP 8 violations
- 🔵 **Info** — suggestions and improvements
- ✅ **Good Points** — what your code does right
- 📊 **Quality Score** — 0 to 100 with grade (A/B/C/D/F)

Built as part of an **Artificial Intelligence Internship** project — no external AI API needed. All analysis is powered by Python's built-in `ast` module and rule-based logic.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🐍 Python Analysis | Syntax check, PEP 8, naming conventions, docstrings, bare except, magic numbers |
| 🗄️ SQL Analysis | SELECT *, missing WHERE clause, SQL injection risk, keyword casing |
| 📝 Generic Analysis | TODO/FIXME detection, hardcoded credentials, comment density |
| 📊 Scoring System | Quality score out of 100 with letter grade |
| 🎨 Dark UI | Clean dark-themed Streamlit interface |
| ⚡ Instant | No API calls — results in milliseconds |

---

## 🛠️ Tech Stack

- **Frontend & Backend:** Streamlit
- **Analysis Engine:** Python `ast` module + Regex rules
- **Language:** Python 3.8+
- **Deployment:** Streamlit Cloud / Google Colab

---

## 📦 Installation & Setup

### Option 1 — Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-code-reviewer.git
cd ai-code-reviewer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run ai_code_reviewer.py
```

Then open `http://localhost:8501` in your browser.

---

### Option 2 — Run on Google Colab (Mobile Friendly)

```python
!pip install streamlit pyngrok

!wget https://raw.githubusercontent.com/YOUR_USERNAME/ai-code-reviewer/main/ai_code_reviewer.py

!streamlit run ai_code_reviewer.py &

from pyngrok import ngrok
url = ngrok.connect(8501)
print("App URL:", url)
```

---

## 📁 Project Structure

```
ai-code-reviewer/
│
├── ai_code_reviewer.py   # Main Streamlit application
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🖥️ How to Use

1. Open the app in your browser
2. Select your **programming language** (Python / SQL / Generic)
3. **Paste your code** in the text area
4. Click **"🔍 Analyze Code"**
5. View your **score, issues, and suggestions** on the right panel

---

## 📊 Scoring System

| Score | Grade | Meaning |
|---|---|---|
| 90 – 100 | A | Excellent code quality |
| 75 – 89 | B | Good with minor issues |
| 60 – 74 | C | Average, needs improvement |
| 40 – 59 | D | Poor, many issues |
| 0 – 39 | F | Critical problems found |

---

## 🔍 What Gets Checked (Python)

- ✅ Syntax errors via `ast.parse()`
- ✅ PEP 8 line length (>79 characters)
- ✅ Trailing whitespace
- ✅ snake_case function naming
- ✅ Single-letter variable names
- ✅ Bare `except:` clauses
- ✅ Missing docstrings
- ✅ Magic numbers
- ✅ Excessive `print()` usage
- ✅ Hardcoded credentials/passwords
- ✅ TODO / FIXME / HACK comments

---

## 🔍 What Gets Checked (SQL)

- ✅ Lowercase SQL keywords
- ✅ `SELECT *` usage
- ✅ `DELETE`/`UPDATE` without `WHERE`
- ✅ SQL injection risk patterns
- ✅ Missing comments

---

## 📸 Screenshots

> *Add screenshots of your app here after running it*

---

## 👩‍💻 Author

**Saloni**
B.Tech — AI & ML
Chhatrapati Shivaji Maharaj University (CSMU), Panvel, Navi Mumbai

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## ⭐ Show Your Support

If you found this project useful, please give it a ⭐ on GitHub!
