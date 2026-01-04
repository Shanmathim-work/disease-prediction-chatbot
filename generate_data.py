# generate_data.py
import random
import pandas as pd

disease_templates = {
    "Common Cold": [
        ["sneezing", "runny nose", "sore throat"],
        ["cough", "mild fever", "congestion"]
    ],
    "Influenza": [
        ["high fever", "body ache", "chills", "fatigue"],
        ["fever", "cough", "headache", "sore throat"]
    ],
    "Gastritis": [
        ["stomach pain", "nausea", "vomiting", "bloating"],
        ["upper abdominal pain", "indigestion", "loss of appetite"]
    ],
    "Migraine": [
        ["severe headache", "nausea", "light sensitivity", "aura"],
        ["throbbing headache", "vomiting", "sensitivity to sound"]
    ],
    "Allergy": [
        ["itching", "rash", "sneezing", "watery eyes"],
        ["skin rash", "hives", "itchy eyes"]
    ],
    "Urinary Tract Infection": [
        ["burning urination", "frequent urination", "lower abdominal pain"],
        ["urine smell", "blood in urine", "pain while urinating"]
    ],
    "Pneumonia": [
        ["high fever", "productive cough", "chest pain", "shortness of breath"],
        ["fever", "cough with phlegm", "difficulty breathing"]
    ],
    "Heart Attack": [
        ["sudden chest pain", "shortness of breath", "sweating", "nausea"],
        ["pressure in chest", "pain radiating to arm", "cold sweat"]
    ],
    "Diabetes": [
        ["increased thirst", "frequent urination", "fatigue", "blurred vision"],
        ["slow wound healing", "weight loss", "excessive hunger"]
    ],
    "Hypertension": [
        ["headache", "dizziness", "nosebleed", "blurred vision"],
        ["chest discomfort", "shortness of breath", "fatigue"]
    ],
    "Bronchitis": [
        ["persistent cough", "mucus", "wheezing", "shortness of breath"],
        ["cough with phlegm", "chest discomfort", "tiredness"]
    ],
    "Stomach Ulcer": [
        ["burning stomach pain", "heartburn", "nausea", "vomiting blood"],
        ["abdominal pain after meals", "bloating", "loss of appetite"]
    ]
}

def mk_sentence(symptoms):
    # join with commas and occasionally add a sentence wrapper
    s = ", ".join(symptoms)
    templates = [
        s,
        "I have " + s,
        "Symptoms: " + s,
        "I'm feeling " + s[0] + " and " + (", ".join(symptoms[1:]) if len(symptoms) >1 else "")
    ]
    return random.choice(templates)

rows = []
random.seed(42)
for disease, lists in disease_templates.items():
    # generate 50 examples per disease (mixing, small paraphrases)
    for _ in range(50):
        symptom_list = random.choice(lists)
        # optionally drop/add one symptom to create variation
        if random.random() < 0.2:
            # drop one
            if len(symptom_list) > 1:
                symptom_list = symptom_list[:-1]
        if random.random() < 0.15:
            # add filler symptom
            symptom_list = symptom_list + [random.choice(["fatigue","mild fever","headache","loss of appetite"])]
        sentence = mk_sentence(symptom_list)
        rows.append({"symptoms": sentence, "disease": disease})

df = pd.DataFrame(rows)
print("Generated rows:", len(df))
df.to_csv("data/disease_symptoms.csv", index=False)
print("Saved to data/disease_symptoms.csv")