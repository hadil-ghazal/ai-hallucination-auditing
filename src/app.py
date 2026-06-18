import re
import pandas as pd
import streamlit as st

from generate_summary import generate_summary

st.set_page_config(
    page_title="AI Hallucination Auditing",
    page_icon="🔎",
    layout="wide"
)


def clean_text(text):

    text = str(text).lower()

    text = text.replace("$", "")
    text = text.replace(",", "")

    text = re.sub(r"[^a-z0-9.% ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def fact_present(fact, summary):

    fact = clean_text(fact)
    summary = clean_text(summary)

    numbers = re.findall(r"\d+(?:\.\d+)?", fact)

    for number in numbers:
        if number not in summary:
            return False

    fact_words = [
        word for word in fact.split()
        if len(word) > 3 and not word.isdigit()
    ]

    if len(fact_words) == 0:
        return True

    matches = sum(
        1 for word in fact_words
        if word in summary
    )

    return matches / len(fact_words) >= 0.7


df = pd.read_csv("results/evaluated_results.csv")

df["display_name"] = (
    "Case "
    + df["id"].astype(str)
    + " • "
    + df["stress_type"]
    .str.replace("_", " ")
    .str.title()
)

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.small-label {
    font-size: 0.85rem;
    color: #6b7280;
}

.metric-card {
    background-color: #f8f9fc;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid #e6e8ef;
}

</style>
""", unsafe_allow_html=True)

st.title("AI Hallucination Auditing")

st.markdown(
    "### Evaluating LLM Reliability in High-Stakes Compliance Workflows"
)

st.warning(
    "Research prototype only. Human review is required before making compliance decisions."
)

left, right = st.columns([1, 2])

with left:

    selected_case = st.selectbox(
        "Select a Benchmark Scenario",
        options=df["display_name"]
    )

    selected_row = df[
        df["display_name"] == selected_case
    ].iloc[0]

with right:

    input_text = st.text_area(
        "Or Paste Your Own Compliance Text",
        value=selected_row["input_text"],
        height=180
    )

if st.button("Run Audit"):

    with st.spinner("Running audit..."):

        summary = generate_summary(input_text)

        facts = [
            fact.strip()
            for fact in str(
                selected_row["critical_facts"]
            ).split(";")
        ]

        matched = 0

        for fact in facts:

            if fact_present(fact, summary):
                matched += 1

        fact_recall = matched / len(facts)

        hallucination_flag = (
            1 if fact_recall < 0.4 else 0
        )

        row = selected_row.copy()

        row["llm_summary"] = summary
        row["fact_recall"] = fact_recall
        row["hallucination_flag"] = hallucination_flag

else:

    row = selected_row

fact_recall_pct = int(row["fact_recall"] * 100)

if fact_recall_pct >= 80:
    risk = "Low"
    risk_color = "green"

elif fact_recall_pct >= 50:
    risk = "Medium"
    risk_color = "orange"

else:
    risk = "High"
    risk_color = "red"

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### Input Text")

    st.info(input_text)

with col2:

    st.markdown("### LLM Summary")

    st.success(row["llm_summary"])

st.markdown("### Audit Results")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Fact Recall",
    f"{fact_recall_pct}%"
)

m2.metric(
    "Hallucination Flag",
    "Yes" if row["hallucination_flag"] else "No"
)

m3.markdown(
    f"""
    <div class="metric-card">
        <div class="small-label">Risk Level</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            color: {risk_color};
        ">
            {risk}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

m4.metric(
    "Stress Category",
    row["stress_type"]
    .replace("_", " ")
    .title()
)

st.markdown("---")

details, recommendations = st.columns(2)

with details:

    st.markdown("### Critical Facts")

    facts = str(row["critical_facts"]).split(";")

    for fact in facts:
        st.write(f"• {fact.strip()}")

with recommendations:

    st.markdown("### Recommended Action")

    if risk == "High":

        st.error("""
Human review required.

Recommended next steps:

- Validate all numerical values manually
- Cross-check source documentation
- Confirm missing disclosures
- Escalate before customer-facing use
        """)

    elif risk == "Medium":

        st.warning("""
Additional verification recommended.

Recommended next steps:

- Review critical figures
- Verify eligibility requirements
- Confirm dates, fees, and thresholds
        """)

    else:

        st.success("""
Automated checks passed.

Recommended next steps:

- Proceed with standard review process
- Spot-check key figures
- Continue monitoring model performance
        """)

with st.expander("View Evaluation Methodology"):

    st.markdown("""
### Metrics

- Fact Recall: Percentage of critical facts captured in the summary
- Hallucination Flag: Triggered when recall falls below threshold
- Risk Level: Derived from fact recall score

### Stress Tests

- Ambiguous prompts
- Incomplete information
- Conflicting context
- Domain-specific jargon
- Long context windows

### Known Limitations

- Automated fact matching may miss valid paraphrases
- Human review remains necessary for high-stakes use cases
""")

st.caption(
    "AI Hallucination Auditing | Duke AIPI Deep Learning NLP 2026"
)