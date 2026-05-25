import streamlit as st
import re
import ast
import keyword

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🔍",
    layout="wide",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #0d0d0d;
    color: #e8e8e8;
}

.main { background-color: #0d0d0d; }

h1 { 
    font-family: 'JetBrains Mono', monospace !important;
    color: #00ff88 !important;
    font-size: 2rem !important;
}

h2, h3 { color: #00ff88 !important; }

.stTextArea textarea {
    background-color: #1a1a1a !important;
    color: #e8e8e8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #00ff88, #00cc6a) !important;
    color: #0d0d0d !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0,255,136,0.3) !important;
}

.stSelectbox > div > div {
    background-color: #1a1a1a !important;
    color: #e8e8e8 !important;
    border: 1px solid #333 !important;
}

.score-box {
    background: linear-gradient(135deg, #1a1a1a, #222);
    border: 2px solid #00ff88;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
}

.score-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 3.5rem;
    font-weight: 700;
    color: #00ff88;
}

.score-label {
    font-size: 0.85rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.issue-card {
    background: #1a1a1a;
    border-left: 4px solid;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
    font-size: 14px;
}

.issue-error   { border-color: #ff4444; }
.issue-warning { border-color: #ffaa00; }
.issue-info    { border-color: #4488ff; }
.issue-good    { border-color: #00ff88; }

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    margin-right: 6px;
    text-transform: uppercase;
}
.badge-error   { background: #ff4444; color: #fff; }
.badge-warning { background: #ffaa00; color: #000; }
.badge-info    { background: #4488ff; color: #fff; }
.badge-good    { background: #00ff88; color: #000; }

.stat-row {
    display: flex;
    gap: 10px;
    margin-bottom: 16px;
}
.stat-pill {
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    color: #aaa;
    font-family: 'JetBrains Mono', monospace;
}

.section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #555;
    margin: 20px 0 10px 0;
    border-bottom: 1px solid #222;
    padding-bottom: 6px;
}

.stMarkdown hr { border-color: #222; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  RULE-BASED ANALYSIS ENGINE
# ─────────────────────────────────────────────

def analyze_python(code: str):
    issues = []
    good   = []
    lines  = code.splitlines()

    # ── Syntax check ──────────────────────────
    try:
        tree = ast.parse(code)
        good.append("✅ No syntax errors — code parses successfully.")
    except SyntaxError as e:
        issues.append({
            "type": "error",
            "line": e.lineno,
            "msg": f"Syntax error: {e.msg}",
            "fix": "Check brackets, colons, indentation near the indicated line."
        })
        return issues, good   # can't do deeper analysis

    # ── Line-level checks ─────────────────────
    long_lines, no_spaces_ops, trailing_ws = [], [], []

    for i, line in enumerate(lines, 1):
        stripped = line.rstrip()

        if len(line) > 79:
            long_lines.append(i)

        if re.search(r'[a-zA-Z0-9_]=\w', line) and "==" not in line and "!=" not in line:
            no_spaces_ops.append(i)

        if line != stripped:
            trailing_ws.append(i)

    if long_lines:
        issues.append({
            "type": "warning",
            "line": long_lines,
            "msg": f"Lines exceed 79 characters (PEP 8): {long_lines}",
            "fix": "Break long lines using parentheses or backslash continuation."
        })
    else:
        good.append("✅ All lines within 79-character PEP 8 limit.")

    if trailing_ws:
        issues.append({
            "type": "info",
            "line": trailing_ws,
            "msg": f"Trailing whitespace on lines: {trailing_ws}",
            "fix": "Enable 'trim trailing whitespace' in your editor."
        })

    # ── Variable naming ───────────────────────
    bad_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and len(node.id) == 1 and node.id not in ('i','j','k','x','y','z','n','_'):
            bad_names.append(node.id)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name != node.name.lower():
                issues.append({
                    "type": "warning",
                    "line": node.lineno,
                    "msg": f"Function '{node.name}' should use snake_case (PEP 8).",
                    "fix": f"Rename to '{re.sub(r'(?<!^)(?=[A-Z])','_',node.name).lower()}'."
                })

    if bad_names:
        issues.append({
            "type": "warning",
            "line": None,
            "msg": f"Single-letter variable names (unclear): {list(set(bad_names))}",
            "fix": "Use descriptive names like 'count', 'index', 'value'."
        })
    else:
        good.append("✅ Variable names are descriptive.")

    # ── Bare except ───────────────────────────
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append({
                "type": "error",
                "line": node.lineno,
                "msg": "Bare 'except:' catches ALL exceptions including KeyboardInterrupt.",
                "fix": "Use 'except Exception as e:' or specify the exact exception type."
            })

    # ── Print vs logging ──────────────────────
    print_count = sum(1 for node in ast.walk(tree)
                      if isinstance(node, ast.Call) and
                         isinstance(node.func, ast.Name) and
                         node.func.id == 'print')
    if print_count > 3:
        issues.append({
            "type": "info",
            "line": None,
            "msg": f"Found {print_count} print() statements — consider using logging module.",
            "fix": "Replace with: import logging; logging.info('message')"
        })

    # ── Docstrings ────────────────────────────
    missing_docs = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not (node.body and isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant)):
                missing_docs.append(f"'{node.name}' (line {node.lineno})")
    if missing_docs:
        issues.append({
            "type": "info",
            "line": None,
            "msg": f"Missing docstrings: {', '.join(missing_docs[:5])}",
            "fix": 'Add triple-quoted docstrings: """Brief description."""'
        })
    else:
        good.append("✅ All functions/classes have docstrings.")

    # ── Magic numbers ─────────────────────────
    magic = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if node.value not in (0, 1, -1, 2, True, False):
                magic.append(node.value)
    if len(set(magic)) > 2:
        issues.append({
            "type": "info",
            "line": None,
            "msg": f"Magic numbers detected: {list(set(magic))[:5]}",
            "fix": "Define as named constants: MAX_RETRIES = 3"
        })

    # ── Imports ───────────────────────────────
    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    if imports:
        good.append(f"✅ {len(imports)} import(s) found — dependency management present.")

    # ── Functions defined ─────────────────────
    funcs = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if funcs:
        good.append(f"✅ {len(funcs)} function(s) defined — code is modular.")

    # ── Classes ───────────────────────────────
    classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    if classes:
        good.append(f"✅ {len(classes)} class(es) defined — OOP structure present.")

    return issues, good


def analyze_sql(code: str):
    issues, good = [], []
    upper = code.upper()

    keywords_lower = re.findall(r'\b(select|from|where|join|insert|update|delete|group|order|having)\b', code)
    if keywords_lower:
        issues.append({
            "type": "warning", "line": None,
            "msg": f"SQL keywords in lowercase: {list(set(keywords_lower))}",
            "fix": "Use uppercase for SQL keywords: SELECT, FROM, WHERE..."
        })
    else:
        good.append("✅ SQL keywords are properly uppercased.")

    if re.search(r'SELECT\s+\*', upper):
        issues.append({
            "type": "warning", "line": None,
            "msg": "Using SELECT * fetches all columns — inefficient.",
            "fix": "Specify only needed columns: SELECT id, name, email"
        })

    if re.search(r'WHERE', upper) is None and re.search(r'DELETE|UPDATE', upper):
        issues.append({
            "type": "error", "line": None,
            "msg": "DELETE/UPDATE without WHERE clause — will affect ALL rows!",
            "fix": "Always add WHERE clause: WHERE id = ?"
        })

    if re.search(r"'\s*\+|'\s*\|\|", code):
        issues.append({
            "type": "error", "line": None,
            "msg": "Possible SQL injection: string concatenation in query.",
            "fix": "Use parameterized queries / prepared statements."
        })

    if re.search(r'--', code) or re.search(r'/\*', code):
        good.append("✅ Comments present — query is documented.")

    return issues, good


def analyze_generic(code: str):
    issues, good = [], []
    lines = code.splitlines()
    total = len(lines)

    if total < 5:
        issues.append({"type":"info","line":None,"msg":"Very short code snippet — limited analysis possible.","fix":"Submit more complete code for deeper review."})

    # TODO comments
    todos = [(i+1, l.strip()) for i, l in enumerate(lines) if 'TODO' in l.upper() or 'FIXME' in l.upper() or 'HACK' in l.upper()]
    if todos:
        issues.append({"type":"warning","line":[t[0] for t in todos],"msg":f"{len(todos)} TODO/FIXME/HACK comment(s) found — unfinished work.","fix":"Resolve or create tickets for these items before submission."})

    # Hardcoded credentials
    cred_pattern = re.compile(r'(password|passwd|secret|api_key|token)\s*=\s*["\'][^"\']+["\']', re.IGNORECASE)
    creds = cred_pattern.findall(code)
    if creds:
        issues.append({"type":"error","line":None,"msg":"Possible hardcoded credentials/secrets detected!","fix":"Use environment variables: os.environ.get('API_KEY')"})

    # Long functions (heuristic)
    if total > 50:
        good.append("✅ Substantial codebase — enough code to review meaningfully.")

    # Comment ratio
    comment_lines = [l for l in lines if l.strip().startswith('#') or l.strip().startswith('//')]
    ratio = len(comment_lines) / max(total, 1)
    if ratio < 0.05:
        issues.append({"type":"info","line":None,"msg":"Low comment density (<5%) — code may be hard to understand.","fix":"Add inline comments explaining non-obvious logic."})
    else:
        good.append(f"✅ Good comment density ({ratio*100:.0f}% of lines commented).")

    return issues, good


def compute_score(issues):
    deductions = {"error": 15, "warning": 7, "info": 3}
    score = 100
    for iss in issues:
        score -= deductions.get(iss["type"], 0)
    return max(0, min(100, score))


def grade(score):
    if score >= 90: return "A", "#00ff88"
    if score >= 75: return "B", "#88ff00"
    if score >= 60: return "C", "#ffcc00"
    if score >= 40: return "D", "#ff8800"
    return "F", "#ff4444"


# ─────────────────────────────────────────────
#  UI
# ─────────────────────────────────────────────

st.markdown("# 🔍 AI Code Reviewer")
st.markdown("<p style='color:#888; font-family:JetBrains Mono; font-size:13px;'>Rule-based static analysis · No API required · Instant feedback</p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    lang = st.selectbox("Language", ["Python", "SQL", "Generic (any language)"])
    code_input = st.text_area(
        "Paste your code here",
        height=380,
        placeholder="# Paste your code here...\ndef hello():\n    print('Hello World')",
    )
    run = st.button("🔍 Analyze Code")

with col2:
    if run and code_input.strip():
        code = code_input.strip()
        lines = code.splitlines()

        # Run analysis
        if lang == "Python":
            issues, good = analyze_python(code)
        elif lang == "SQL":
            issues, good = analyze_sql(code)
        else:
            issues, good = [], []

        gen_issues, gen_good = analyze_generic(code)
        issues += gen_issues
        good   += gen_good

        score = compute_score(issues)
        letter, color = grade(score)

        # Score box
        errors   = sum(1 for i in issues if i["type"] == "error")
        warnings = sum(1 for i in issues if i["type"] == "warning")
        infos    = sum(1 for i in issues if i["type"] == "info")

        st.markdown(f"""
        <div class='score-box'>
            <div class='score-number' style='color:{color}'>{score}</div>
            <div style='font-size:1.5rem; color:{color}; font-weight:700;'>{letter}</div>
            <div class='score-label'>Code Quality Score</div>
        </div>
        <div class='stat-row'>
            <span class='stat-pill'>📄 {len(lines)} lines</span>
            <span class='stat-pill'>🔴 {errors} errors</span>
            <span class='stat-pill'>🟡 {warnings} warnings</span>
            <span class='stat-pill'>🔵 {infos} notes</span>
        </div>
        """, unsafe_allow_html=True)

        # Issues
        if issues:
            st.markdown("<div class='section-title'>Issues Found</div>", unsafe_allow_html=True)
            for iss in issues:
                badge_class = f"badge-{iss['type']}"
                label = iss["type"].upper()
                line_info = f" · Line {iss['line']}" if iss.get("line") and not isinstance(iss["line"], list) else ""
                st.markdown(f"""
                <div class='issue-card issue-{iss["type"]}'>
                    <span class='badge {badge_class}'>{label}</span>{line_info}<br>
                    <span style='color:#ddd'>{iss['msg']}</span><br>
                    <span style='color:#666; font-size:12px; font-family:JetBrains Mono'>💡 {iss['fix']}</span>
                </div>
                """, unsafe_allow_html=True)

        # Good things
        if good:
            st.markdown("<div class='section-title'>What's Good</div>", unsafe_allow_html=True)
            for g in good:
                st.markdown(f"""
                <div class='issue-card issue-good'>
                    <span style='color:#ddd; font-size:13px'>{g}</span>
                </div>
                """, unsafe_allow_html=True)

        if not issues and not good:
            st.info("No significant issues found for this snippet.")

    elif run and not code_input.strip():
        st.warning("Please paste some code first!")
    else:
        st.markdown("""
        <div style='color:#444; font-family:JetBrains Mono; font-size:13px; padding-top:40px; text-align:center;'>
            ← Paste code & click<br><strong style='color:#00ff88'>Analyze Code</strong><br>to see results here
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='color:#333; font-size:11px; font-family:JetBrains Mono; text-align:center;'>AI Code Reviewer · Rule-Based Static Analysis · Built with Streamlit</p>", unsafe_allow_html=True)
