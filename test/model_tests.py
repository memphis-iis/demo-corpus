import unittest

from democorpus.model import CorpusDoc, _words, compare_docs

class CorpusDocTest(unittest.TestCase):
    def setUp(self):
        self.doc1 = CorpusDoc(
            document_id="d1",
            title="Sentence D1",
            contents="The lazy brown dog just won't hunt;he's a pacifist."
        )

        self.d1_words = ["the", "lazy", "brown", "dog", "just", "won't", "hunt", "he's", "a", "pacifist"]

        self.doc2 = CorpusDoc(
            document_id="d2",
            title="Sentence D2",
            contents="All lazy brown dogs are my friend"
        )

        self.d2_words = ["all", "lazy", "brown", "dogs", "are", "my", "friend"]

    def tearDown(self):
        pass

    def testNoErrors(self):
        self.assertTrue(len(list(self.doc1.errors())) < 1)
        self.assertTrue(len(list(self.doc2.errors())) < 1)

        print(self.doc1.get_item())
        print(self.doc2.get_item())
        print(compare_docs(self.doc1, self.doc2))

    def testPersist(self):
        item = self.doc1.get_item()
        self.assertEqual("d1", item["document_id"])
        self.assertEqual("Sentence D1", item["title"])
        self.assertEqual("The lazy brown dog just won't hunt;he's a pacifist.", item["contents"])

    def testWords(self):
        self.assertEqual(self.d1_words, list(_words(self.doc1.contents)))
        self.assertEqual(self.d2_words, list(_words(self.doc2.contents)))

    def testCompare(self):
        result = compare_docs(self.doc1, self.doc2)

        self.assertEqual(len(self.d1_words), result["doc1_word_count"])

        self.assertEqual(len(self.d2_words), result["doc2_word_count"])

        self.assertTrue(len(self.d1_words) + len(self.d2_words) > result["total_words"])

        self.assertTrue(len(self.d1_words) > result["doc1_unique_words"])
        self.assertTrue(result["doc1_unique_words"] > 0)

        self.assertTrue(len(self.d2_words) > result["doc2_unique_words"])
        self.assertTrue(result["doc2_unique_words"] > 0)

        self.assertTrue(len(self.d1_words) + len(self.d2_words) > result["in_common_words"])
        self.assertTrue(result["in_common_words"] > 0)
        self.assertTrue(result["in_common_words"] < result["total_words"])

        self.assertTrue(result["simple_similarity"] > 0.0)
        self.assertTrue(result["simple_similarity"] < 1.0)

    def testCompareBlank(self):
        result = compare_docs(
            CorpusDoc(document_id="e1", contents=""),
            CorpusDoc(document_id="e2", contents=",.;; ^%")
        )

        self.assertEqual(0, result["doc1_word_count"])
        self.assertEqual(0, result["doc2_word_count"])
        self.assertEqual(0, result["total_words"])
        self.assertEqual(0, result["doc1_unique_words"])
        self.assertEqual(0, result["doc2_unique_words"])
        self.assertEqual(0, result["in_common_words"])
        self.assertTrue(abs(result["simple_similarity"]) < 0.000001)

    def testCompareSelf(self):
        s = CorpusDoc(document_id="s1", contents="identity is redundant")
        result = compare_docs(s, s)

        self.assertEqual(3, result["doc1_word_count"])
        self.assertEqual(3, result["doc2_word_count"])
        self.assertEqual(3, result["total_words"])
        self.assertEqual(0, result["doc1_unique_words"])
        self.assertEqual(0, result["doc2_unique_words"])
        self.assertEqual(3, result["in_common_words"])
        self.assertTrue(abs(1.0 - result["simple_similarity"]) < 0.000001)
