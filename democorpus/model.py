import logging

from .data import DefinedTable


logger = logging.getLogger(__name__)


def ensure_tables():
    """When called, ensure that all the tables that we need are created in the
    database. The real work is supplied by the DefinedTable base class
    """
    for tab in [CorpusDoc]:
        logger.debug("Creating table %s", tab.get_table_name())
        tab.ensure_table()


class CorpusDoc(DefinedTable):
    """Single document in our corpus
    """

    @classmethod
    def get_table_name(self):
        return "CorpusDoc"

    @classmethod
    def get_key_name(self):
        return "document_id"

    def __init__(self, document_id=None, title=None, contents=None):
        self.document_id = document_id
        self.title = title
        self.contents = contents


class InvalidCompareParams(Exception):
    """Exception raise when an invalid comparison is requested
    """
    def __init__(self, errors):
        self.errors = list(errors)
        Exception.__init__("The object was not ready to be saved")


def _words(contents):
    def filt(c):
        if c.isalnum() or c == "'":
            return c
        else:
            return ' '

    for word in ''.join(filt(c) for c in str(contents)).split():
        yield word.lower()

def compare_docs(doc1, doc2):
    """Given two instances of CorpusDoc, return a comparison
    """
    if not doc1 or not isinstance(doc1, CorpusDoc):
        raise InvalidCompareParams("Invalid document object given for comparison")

    if not doc2 or not isinstance(doc2, CorpusDoc):
        raise InvalidCompareParams("Invalid document object given for comparison")

    words1 = set(_words(doc1.contents))
    words2 = set(_words(doc2.contents))

    tot_words = len(words1 | words2)
    if tot_words:
        similar = float(len(words1 & words2)) / float(tot_words)
    else:
        similar = 0.0

    return {
        'doc1_word_count':   len(words1),
        'doc2_word_count':   len(words2),
        'total_words':       tot_words,
        'doc1_unique_words': len(words1 - words2),
        'doc2_unique_words': len(words2 - words1),
        'in_common_words':   len(words1 & words2),
        'simple_similarity': similar
    }
