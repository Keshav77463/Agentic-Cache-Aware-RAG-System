import pandas as pd
import re
df = pd.read_csv("../data/Reviews.csv")

print(df.shape)
print(df.head())
print(df.describe())
print(df.columns)
print(df.info())

df = df[['Text', 'Summary', 'Score']]
df['Summary'] = df['Summary'].fillna('')
df['Text'] = df['Text'].fillna('')
print(df.head())
print(df['Summary'])
df = df[df['Text'].str.len() > 50]
print(df.info())
df = df.sample(50000, random_state=42)
df['combined'] = df['Summary'] + " " + df['Text']
print(df.head())
print(len(df))
print(df['combined'].iloc[0])
print(df.head())
print(len(df))
print(df['combined'].iloc[0])
df.to_csv("../data/processes.csv", index=False)

df = df[['combined', 'Score']]
df.to_csv("../data/cleaned_reviews.csv", index=False)
df.rename(columns={'combined': 'text'}, inplace=True)
df.to_csv("../data/cleaned_reviews.csv", index=False)
def clean_text(text):
    text = re.sub(r'<.*?>', '', text)        # remove HTML
    text = re.sub(r'\s+', ' ', text).strip() # fix spacing
    return text

df['text'] = df['text'].apply(clean_text)
df.to_csv("../data/cleaned_reviewss.csv", index=False)

