import os
import json

import responder

from download import download
from sentiment_analysis import SentimentAnalyzer


env = os.environ
DEBUG = env['DEBUG'] in ['1', 'True', 'true']
LIBRARY = env['LIBRARY']
MECAB_ARG = env['MECAB_ARG']
LANG = env['LANG']

api = responder.API(debug=DEBUG)
if LIBRARY == 'polyglot':
    download(lang=LANG)    
analyzer = SentimentAnalyzer(
    library=LIBRARY,
    lang=LANG,
    mecab_arg=MECAB_ARG
)


@api.route("/")
async def analyze(req, resp):
    body = await req.text
    json_body = json.loads(body)
    docs = [analyzer.analyze(
        text
    ) for text in json_body]
    resp.media = dict(data=docs)


if __name__ == "__main__":
    api.run()