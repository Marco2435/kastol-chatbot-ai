
import pandas as pd
from sklearn.model_selection import train_test_split
import os

def prepare_dataset(feedback_path='feedback/trainingsdata.csv', reward_path='logs/reward_training_data.csv'):
    dfs = []
    if os.path.exists(feedback_path):
        df1 = pd.read_csv(feedback_path)
        df1 = df1.rename(columns={'vraag': 'question', 'correct_antwoord': 'answer'})
        df1 = df1[['question', 'answer']].dropna()
        dfs.append(df1)
    if os.path.exists(reward_path):
        df2 = pd.read_csv(reward_path)
        df2 = df2.rename(columns={'vraag': 'question', 'correctie': 'answer'})
        df2 = df2[['question', 'answer']].dropna()
        dfs.append(df2)
    if not dfs:
        raise ValueError("Geen trainingsdata gevonden.")
    df = pd.concat(dfs).drop_duplicates()
    df = df[df['answer'].str.len() > 10]
    train, test = train_test_split(df, test_size=0.2, random_state=42)
    train.to_csv("ml_training/train.csv", index=False)
    test.to_csv("ml_training/test.csv", index=False)
    return train, test
