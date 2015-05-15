#!/usr/bin/env python

import os
import random
import logging
import uuid
import json

import flask
from flask import Flask, render_template, request, abort, url_for, jsonify

from democorpus.model import CorpusDoc, ensure_tables, compare_docs

logger = logging.getLogger(__name__)

# Note that application as the main WSGI app is required for Python apps
# on Elastic Beanstalk
application = Flask(__name__)
application.secret_key = application.config.get('FLASK_SECRET', "My Default Secret")


def doc_for_persist(doc, include_doc_contents=True):
    """Given a CorpusDoc instance, return a JSON-persistable data structure. NOTE
    that this should only be called by a request-processing function since we
    include the URL
    """
    item = doc.get_item()
    item['URL'] = url_for('get_corpus_doc', docid = doc.document_id)
    item['contents-len'] = len(item['contents'])

    if not include_doc_contents:
        del item['contents']

    return item


@application.before_first_request
def before_first():
    ensure_tables()


@application.route('/')
def main_page():
    return jsonify(
        sevice_name="Corpus ReST Service",
        list_documents=url_for('corpus_list')
    )


@application.route('/demo')
def demo_page():
    return render_template("demo.html")


@application.route('/corpus')
def corpus_list():
    return jsonify(
        documents=[doc_for_persist(doc, False) for doc in CorpusDoc.find_all()]
    )


@application.route('/corpus/<docid>')
def get_corpus_doc(docid):
    doc = CorpusDoc.find(docid)
    if not doc:
        abort(404)
    return jsonify(**doc_for_persist(doc))


@application.route('/corpus', methods=['POST'])
@application.route('/corpus/<docid>', methods=['POST'])
def save_corpus_doc(docid=None):
    try:
        # Note that we are requiring that Content-Type is application/json and
        # intentionally accessing the content property in a way that would raise
        # an exception if it is missing
        submitted = request.get_json()
        if not submitted:
            raise ValueError("No JSON received")

        contents = submitted['contents']
        if not contents:
            raise ValueError("Missing contents")

        title = submitted.get('title', '')
    except:
        logger.exception("Invalid or missing contents payload POST")
        abort(400)

    if not docid:
        docid = str(uuid.uuid4())
        logger.debug("Request for inserted doc - created doc ID %s" % docid)

    doc = CorpusDoc(document_id=docid, title=title, contents=contents)
    doc.save()

    return jsonify(**doc_for_persist(doc, False))


@application.route('/compare/<docid1>/<docid2>')
def corpus_doc_compare(docid1, docid2):
    doc1 = CorpusDoc.find(docid1)
    if not doc1:
        abort(404)

    doc2 = CorpusDoc.find(docid2)
    if not doc2:
        abort(404)

    result = compare_docs(doc1, doc2)
    result['doc1'] = doc_for_persist(doc1, False)
    result['doc2'] = doc_for_persist(doc2, False)

    return jsonify(**result)


# Final app settings depending on whether or not we are set for debug mode
if os.environ.get('DEBUG', None):
    # Debug mode - running on a workstation
    application.debug = True
    logging.basicConfig(level=logging.DEBUG)
else:
    # We are running on AWS Elastic Beanstalk (or something like it)
    application.debug = False
    logging.basicConfig(level=logging.INFO)


# Our entry point - called when our application is started "locally". NOTE that
# this WILL NOT be run by Elastic Beanstalk
def main():
    application.run()
if __name__ == '__main__':
    main()
