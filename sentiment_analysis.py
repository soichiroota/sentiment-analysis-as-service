from polyglot.text import Text
from polyglot.downloader import downloader
from mlask import MLAsk
import oseti


class SentimentAnalyzer:
    def __init__(self, library=None, lang='en', mecab_arg=''):
        if library == 'mlask':
            self.analyzer = MLAskSentimentAnalyzer(mecab_arg)
        elif library == 'oseti':
            self.analyzer = OsetiSentimentAnalyzer()
        else:
            self.analyzer = PolyglotSentimentAnalyzer(lang=lang)

    def analyze(self, blob):
        return self.analyzer.analyze(blob)


class MLAskSentimentAnalyzer:
    def __init__(self, mecab_arg=''):
        self.analyzer = MLAsk(mecab_arg)

    def analyze(self, blob):
        result = self.analyzer.analyze(blob)
        emotion = dict(
            result['emotion']
        ) if result.get('emotion') else None
        representative = list(
            result['representative']
        ) if result.get('representative') else None
        return dict(
            text=result.get('text'),
            emotion=emotion,
            orientation=result.get('orientation'),
            activation=result.get('activation'),
            emoticon=result.get('emoticon'),
            intension=result.get('intension'),
            intensifier=result.get('intensifier'),
            representative=representative
        )


class OsetiSentimentAnalyzer:
    def __init__(self):
        self.analyzer = oseti.Analyzer()

    def analyze(self, blob):
        return self.analyzer.analyze_detail(blob)


class PolyglotSentimentAnalyzer:
    def __init__(self, lang='en'):
        self.lang = lang

    def analyze(self, blob):
        while not downloader.is_installed("sentiment2." + self.lang):
            pass
        text = Text(blob, hint_language_code=self.lang)
        return [
            self._parse_sentence(
                sentence
            ) for sentence in text.sentences
        ]

    def _parse_sentence(self, sentence):
        polarity = self._get_polarity(sentence)
        entities = self._get_entities(sentence)
        return {
            'raw': sentence.raw,
            'start': sentence.start,
            'end': sentence.end,
            'tokens': sentence.tokens,
            'words': sentence.words,
            'polarity': polarity,
            'entities': entities,
            'language': sentence.language.code
        }

    def _get_polarity(self, sentence):
        try:
            polarity = sentence.polarity
        except ZeroDivisionError:
            polarity = 0.5
        return polarity

    def _get_entities(self, sentence):
        if 'ner2' in downloader.supported_tasks(lang=self.lang):
            entities = [
                self._parse_entity(
                    entity
                ) for entity in sentence.entities
            ]
        else:
            entities = None
        return entities

    def _parse_entity(self, entity):
        try:
            return dict(
                entity=entity,
                positive_sentiment=entity.positive_sentiment,
                negative_sentiment=entity.negative_sentiment
            )
        except IndexError:
            return dict(
                entity=entity,
                positive_sentiment=0,
                negative_sentiment=0
            )


