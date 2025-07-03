import random
import numpy as np
from simiir.user.query_generators.base import BaseQueryGenerator

class AdvancedQuestionQueryGenerator(BaseQueryGenerator):
    """
    Query-Generator basierend auf Wahrscheinlichkeiten und POS-Mustern,
    der Fragen mit variablem Satzbau generiert.
    """

    def __init__(self, stopword_file=None, background_file=[]):
        super().__init__(stopword_file, background_file=background_file)

        self.w_words = {
            "how": 0.455,
            "what": 0.269,
            "why": 0.095,
            "is": 0.035,
            "does": 0.034,
            "do": 0.033,
            "can": 0.031,
            "are": 0.025,
            "when": 0.021,
            "who": 0.011,
        }

        self.pos_patterns = {
            "SPACE DET NOUN VERB NOUN PART VERB ADP NOUN": 0.1836,
            "PRON AUX NOUN": 0.1561,
            "AUX PART VERB ADP PROPN CCONJ NOUN PUNCT": 0.1347,
            "SCONJ AUX DET NOUN ADP DET NOUN VERB DET ADJ NOUN CCONJ NOUN PUNCT NOUN ADP PROPN NOUN": 0.1263,
            "PRON AUX ADJ NOUN CCONJ PUNCT PROPN CCONJ PROPN PUNCT": 0.0858,
            "PRON AUX ADJ NOUN": 0.0787,
            "PRON AUX NOUN CCONJ PUNCT PROPN CCONJ PROPN PUNCT": 0.0620,
            "PRON AUX NOUN PUNCT CCONJ PUNCT PROPN CCONJ NUM PUNCT": 0.0596,
            "SCONJ PART VERB NOUN NOUN": 0.0572,
            "SCONJ PART VERB ADJ NOUN NOUN": 0.0560,
        }

         # Realistische Dummy-Wörter pro POS-Tag
        self.dummy_words = {
            "ADJ": ['academic', 'financial', 'social', 'teenage', 'short', 'genital', 'senior', 'high', 'personal', 'cultural'],
            "NOUN": ['students', 'school', 'media', 'effects', 'regulations', 'corporation', 'literacy', 'experience', 'impact', 'grade'],
            "PROPN": ['yearpublished<=2025', 'philippines', 'high', 'school', 'senior', 'yearpublished>=2018', 'egypt', 'social', 'thailand', 'yearpublished>=2020'],
            "VERB": ['learning', 'discussing', 'assessing', 'understanding', 'lived', 'encounter', 'related', 'love', 'ai', 'calling'],
            "NUM": ['yearpublished<=2024', '11', '2024', '2020', '2018', '2015', '5', '9'],
            "SPACE": [' '],
            "DET": ['the'],
            "PRON": ['oneself'],
            "AUX": ['is'],
            "CCONJ": ['and'],
            "ADP": ['in'],
            "PUNCT": ['.'],
            "PART": ['to'],
            "SCONJ": ['how', 'because', 'although']
        }


    def weighted_choice(self, choices):
        items = list(choices.items())
        elements, weights = zip(*items)
        return random.choices(elements, weights=weights, k=1)[0]

    def generate_query_list(self, user_context):
        topic = user_context.topic.title.strip().rstrip("?")
        queries = []

        # Anzahl Queries, z.B. 5
        for _ in range(5):
            # 29% Wahrscheinlichkeit für Fragezeichen
            question_mark = "?" if random.random() < 0.29 else ""

            # 70% Wahrscheinlichkeit mit W-Fragewort zu starten
            if random.random() < 0.7:
                w_word = self.weighted_choice(self.w_words)
                query_words = [w_word]
            else:
                query_words = []

            # Wortlänge mit Mittelwert 11.3, SD = 4 (mindestens 3 Wörter)
            length = max(3, int(np.random.normal(11.3, 4)))

            # POS-Muster auswählen (gewichtet)
            pattern = self.weighted_choice(self.pos_patterns)
            pos_tags = pattern.split()

            # Muster an Länge anpassen
            if len(pos_tags) > length:
                pos_tags = pos_tags[:length]
            elif len(pos_tags) < length:
                pos_tags += ["NOUN"] * (length - len(pos_tags))

            # Wörter aus dummy map holen, topic als Noun ersetzen
            words = []
            for tag in pos_tags:
                if tag == "NOUN":
                    words.append(topic)
                else:
                    words.append(self.dummy_words.get(tag, "word"))

            # Duplikat vermeiden, falls w_word schon als erstes steht
            if query_words and words and words[0] == query_words[0]:
                words = words[1:]

            query = " ".join(query_words + words).strip() + question_mark
            queries.append((query, 1))

        return queries
