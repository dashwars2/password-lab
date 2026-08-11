# 🔐 Password Lab

An educational Grade 10 computer-science-fair project that demonstrates password security concepts.

## What it demonstrates
- String analysis
- Character-set reasoning
- Search-space mathematics
- A deliberately tiny local guessing simulation
- Why longer, less predictable passwords create a larger search space
- Basic cybersecurity hygiene

## Safety
This project is intentionally **not** a password-cracking tool. It does not connect to accounts, websites, login forms, or networks. The guessing demo is limited to a tiny toy search space. For larger passwords, it displays the mathematical estimate instead of attempting an exhaustive search.

Use only fictional test passwords.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Push `app.py` and `requirements.txt` to GitHub, then deploy the repository through Streamlit Community Cloud.
