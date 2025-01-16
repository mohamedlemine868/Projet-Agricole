from flask import Flask, render_template, request
from transformers import pipeline
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
from collections import Counter

matplotlib.use('Agg')

app = Flask(__name__)

# Load the sentiment analysis model
sentiment_model = pipeline("sentiment-analysis", model="./models/bert-sentiment")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    comment_list = []
    if 'comments' in request.form and request.form['comments'].strip():
        comments = request.form['comments']
        comment_list = comments.split('\n')
    elif 'fileInput' in request.files and request.files['fileInput'].filename != '':
        csv_file = request.files['fileInput']
        try:
            df = pd.read_csv(csv_file)
            if 'comments' in df.columns:
                comment_list = df['comments'].dropna().tolist()
            else:
                return "Erreur: La colonne 'comments' est introuvable dans le fichier CSV."
        except Exception as e:
            return f"Erreur de fichier: {str(e)}"
    else:
        return "Aucune donnée reçue. Veuillez soumettre du texte ou un fichier CSV."

    sentiments = [sentiment_model(comment) for comment in comment_list]

    results_df = pd.DataFrame({
        'texte': comment_list,
        'étiquette': [sent[0]['label'] for sent in sentiments],
        'score': [sent[0]['score'] for sent in sentiments]
    })

    def map_label(label):
        if label in ["5 stars", "4 stars"]:
            return "Positif"
        elif label in ["1 star", "2 stars"]:
            return "Négatif"
        elif label == "3 stars":
            return "Mixte"
        else:
            return "Neutre"

    results_df['catégorie'] = results_df['étiquette'].apply(map_label)

    sentiment_counts = results_df['catégorie'].value_counts(normalize=True) * 100
    sentiment_counts = sentiment_counts.reindex(["Positif", "Négatif", "Mixte", "Neutre"], fill_value=0)

    product_quality = int(sentiment_counts["Positif"] / 20) + 1
    satisfaction_level = round(sentiment_counts["Positif"], 2)
    emerging_trends = ", ".join(results_df['texte'].sample(min(5, len(results_df))).tolist())

    most_common_sentiment = sentiment_counts.idxmax()
    if most_common_sentiment == "Négatif":
        advice = "Votre produit reçoit beaucoup de commentaires négatifs. Améliorez la qualité ou le support client pour satisfaire vos utilisateurs."
        icon = "fa-exclamation-triangle"
    elif most_common_sentiment == "Positif":
        advice = "Votre produit est bien reçu par vos utilisateurs. Continuez à fournir un excellent service."
        icon = "fa-thumbs-up"
    elif most_common_sentiment == "Mixte":
        advice = "Les avis sont partagés. Identifiez les problèmes spécifiques et travaillez à les résoudre."
        icon = "fa-info-circle"
    else:
        advice = "Les commentaires semblent neutres. Encouragez vos utilisateurs à fournir des retours plus détaillés."
        icon = "fa-question-circle"

    negative_comments = results_df[results_df['catégorie'] == "Négatif"]['texte'].tolist()
    all_words = " ".join(negative_comments).lower().split()
    frequent_words = Counter(all_words).most_common(5)
    frequent_words_str = ", ".join([f"'{word}'" for word, _ in frequent_words])

    plt.figure(figsize=(8, 6))
    sentiment_counts.plot(kind='bar', color=['green', 'red', 'orange', 'blue'], edgecolor='black')
    plt.title("Répartition des Sentiments")
    plt.xlabel("Catégorie de Sentiment")
    plt.ylabel("Pourcentage (%)")
    plt.xticks(rotation=0)
    plt.ylim(0, 100)
    chart_path = os.path.join('static', 'sentiment_chart.png')
    plt.savefig(chart_path)
    plt.close()

    return render_template(
        'results.html',
        table=results_df[['texte', 'catégorie', 'score']].to_html(classes='table', index=False),
        chart_path=chart_path,
        advice=advice,
        icon=icon,
        frequent_words=frequent_words_str,
        product_quality=product_quality,
        satisfaction_level=satisfaction_level,
        emerging_trends=emerging_trends
    )

if __name__ == '__main__':
    app.run(debug=True)
