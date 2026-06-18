import os
import streamlit as st
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

#api_key = os.getenv("OPENAI_API_KEY")

##if not api_key:
  ##  api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI(
    api_key=api_key
)

SYSTEM_PROMPT = """
You are a compliance summarization assistant.

Summarize the input using only information explicitly stated.

Do not infer, assume, estimate, or add information.

Preserve all numerical values, dates, fees, rates, thresholds, eligibility requirements, and exceptions exactly as written.

If information is missing, conflicting, or ambiguous, explicitly state that in the summary.
"""


def generate_summary(text):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    import pandas as pd

    df = pd.read_csv("data/compliance_cases.csv")

    summaries = []

    for text in df["input_text"]:

        summary = generate_summary(text)

        summaries.append(summary)

    df["llm_summary"] = summaries

    df.to_csv("results/summary_results.csv", index=False)

    print("Done. Results saved to results/summary_results.csv")