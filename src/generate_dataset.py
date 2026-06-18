# generate_dataset.py

# This script creates a synthetic dataset for testing
# LLM hallucinations in compliance summarization tasks

import pandas as pd
import random

random.seed(42)

stress_types = [
    "normal",
    "ambiguous",
    "incomplete",
    "conflicting",
    "jargon",
    "long_context"
]

templates = {
    "normal": [
        {
            "input": "The account offers a {apy}% APY. Customers must maintain a minimum balance of ${balance} to earn the disclosed APY.",
            "summary": "The account offers a {apy}% APY and requires a minimum balance of ${balance}.",
            "facts": "{apy}% APY; ${balance} minimum balance"
        },
        {
            "input": "Wire transfers submitted before {time} ET are processed the same business day.",
            "summary": "Wire transfers submitted before {time} ET are processed the same business day.",
            "facts": "{time} ET cutoff"
        }
    ],

    "ambiguous": [
        {
            "input": "Customers may qualify for a bonus if certain deposit requirements are met within the promotional period.",
            "summary": "Customers may qualify for a bonus if they meet unspecified deposit requirements during the promotional period.",
            "facts": "bonus eligibility unclear; promotional period"
        },
        {
            "input": "Fees could apply depending on account activity.",
            "summary": "Account fees may apply depending on account activity, but specific conditions are not provided.",
            "facts": "fees may apply; conditions unspecified"
        }
    ],

    "incomplete": [
        {
            "input": "The account earns a promotional APY for a limited time.",
            "summary": "The account offers a promotional APY, but the rate and duration are not specified.",
            "facts": "promotional APY; missing rate; missing duration"
        },
        {
            "input": "A fee may be charged for early withdrawal.",
            "summary": "Early withdrawals may incur a fee, but the amount is not specified.",
            "facts": "early withdrawal fee; fee amount missing"
        }
    ],

    "conflicting": [
        {
            "input": "The account has no monthly maintenance fee. A $15 monthly maintenance fee applies if the balance falls below $500.",
            "summary": "The account may charge a $15 monthly maintenance fee if the balance falls below $500 despite stating there is no monthly fee.",
            "facts": "$15 fee; below $500 balance; conflicting statements"
        },
        {
            "input": "Wire transfers are processed the same day. Requests received after 4:00 PM ET are processed the next business day.",
            "summary": "Wire transfers are generally processed the same day, except requests submitted after 4:00 PM ET are processed the next business day.",
            "facts": "same-day processing; 4:00 PM cutoff"
        }
    ],

    "jargon": [
        {
            "input": "Acct holders must maintain a min DDB of ${balance} to earn the disclosed APY.",
            "summary": "Account holders must maintain a minimum daily balance of ${balance} to earn the APY.",
            "facts": "${balance} minimum daily balance; APY"
        },
        {
            "input": "OD fees apply when the ledger balance falls below zero by more than $50.",
            "summary": "Overdraft fees apply when the account balance is overdrawn by more than $50.",
            "facts": "overdraft fee; more than $50"
        }
    ],

    "long_context": [
        {
            "input": "Customers can access online banking services 24/7. Mobile check deposit is available through the app. The account offers a {apy}% APY. Rates may change after account opening. Customers must maintain a minimum balance of ${balance} to earn the disclosed APY. Paper statements cost $3 per month.",
            "summary": "The account offers a {apy}% APY that may change after account opening and requires a minimum balance of ${balance}. Paper statements cost $3 per month.",
            "facts": "{apy}% APY; rates may change; ${balance} minimum balance; $3 paper statement fee"
        },
        {
            "input": "Customers receive fraud monitoring alerts and free online bill pay. Wire transfers submitted before {time} ET are processed the same day. Dormant accounts may incur a $10 monthly fee after 12 months of inactivity.",
            "summary": "Wire transfers submitted before {time} ET are processed the same day. Dormant accounts incur a $10 monthly fee after 12 months of inactivity.",
            "facts": "{time} ET cutoff; $10 dormant fee; 12 months inactivity"
        }
    ]
}

apys = [1.25, 2.10, 3.50, 4.25, 4.75, 5.10]
balances = [500, 1000, 2500, 5000, 10000, 25000]
times = ["3:00 PM", "4:00 PM", "5:00 PM"]

rows = []

row_id = 1

for stress_type in stress_types:

    for _ in range(20):

        template = random.choice(templates[stress_type])

        apy = random.choice(apys)
        balance = random.choice(balances)
        time = random.choice(times)

        rows.append({
            "id": row_id,
            "stress_type": stress_type,
            "input_text": template["input"].format(
                apy=apy,
                balance=balance,
                time=time
            ),
            "ground_truth_summary": template["summary"].format(
                apy=apy,
                balance=balance,
                time=time
            ),
            "critical_facts": template["facts"].format(
                apy=apy,
                balance=balance,
                time=time
            )
        })

        row_id += 1

df = pd.DataFrame(rows)

df.to_csv("data/compliance_cases.csv", index=False)

print(f"Created {len(df)} exampls")
