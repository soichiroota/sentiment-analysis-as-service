import os

from polyglot.downloader import downloader


env = os.environ
LANG = env['LANG']


def download(lang='en'):
    downloader.download("embeddings2." + lang)
    supported_tasks = downloader.supported_tasks(lang=lang)
    if "sentiment2" in supported_tasks:
        downloader.download("sentiment2." + lang)
    if "ner2" in supported_tasks:
        downloader.download("ner2." + lang)
    return


if __name__ == '__main__':
    download(lang=LANG)