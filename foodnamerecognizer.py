#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 02:32:43 2020

@author: rayansami
"""
import nltk
import re
import pprint
from nltk import Tree
import pdb


patterns="""
    NP: {<JJ>*<NN*>+}
    {<JJ>*<NN*><CC>*<NN*>+}
    {<NP><CC><NP>}
    {<RB><JJ>*<NN*>+}
    """

NPChunker = nltk.RegexpParser(patterns)

def prepare_text(input):
    sentences = nltk.sent_tokenize(input)
    sentences = [nltk.word_tokenize(sent) for sent in sentences] 
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    sentences = [NPChunker.parse(sent) for sent in sentences]
    return sentences


def parsed_text_to_NP(sentences):
    nps = []
    for sent in sentences:
        tree = NPChunker.parse(sent)
        print(tree)
        for subtree in tree.subtrees():
            if subtree.label() == 'NP':
                t = subtree
                t = ' '.join(word for word, tag in t.leaves())
                nps.append(t)
    return nps


def sent_parse(input):
    sentences = prepare_text(input)
    nps = parsed_text_to_NP(sentences)
    return nps