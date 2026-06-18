import re
import pandas as pd


df = pd.read_csv("results/summary_results.csv")


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

    # Numbers matter most in compliance
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


fact_recalls = []
hallucinations = []
completeness_scores = []


for _, row in df.iterrows():

    summary = row["llm_summary"]

    facts = [
        fact.strip()
        for fact in str(row["critical_facts"]).split(";")
    ]

    matched = 0

    for fact in facts:

        if fact_present(fact, summary):
            matched += 1

    recall = matched / len(facts)

    fact_recalls.append(recall)

    if recall >= 0.8:
        completeness = 2
    elif recall >= 0.5:
        completeness = 1
    else:
        completeness = 0

    completeness_scores.append(completeness)

    ##hallucinations.append(1 if recall < 0.5 else 0)
    hallucinations.append(1 if recall < 0.4 else 0)

df["fact_recall"] = fact_recalls
df["completeness_score"] = completeness_scores
df["hallucination_flag"] = hallucinations

df.to_csv("results/evaluated_results.csv", index=False)

print("\n===== RESULTS =====")

print(
    f"Hallucination Rate: "
    f"{df['hallucination_flag'].mean():.2%}"
)

print(
    f"Average Fact Recall: "
    f"{df['fact_recall'].mean():.2%}"
)

print(
    f"Average Completeness: "
    f"{df['completeness_score'].mean():.2f}"
)

print("\n===== RESULTS BY STRESS TYPE =====")

print(
    df.groupby("stress_type")[
        [
            "hallucination_flag",
            "fact_recall",
            "completeness_score"
        ]
    ].mean().round(2)
)