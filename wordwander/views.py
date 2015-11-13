##### -*- coding: utf-8 -*-

import codecs
import operator

from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import os
import re
import sys
from django.db import connection, transaction
from wordwander.models import Word
import pdb

def home(request):
    textblock=request.GET.get('textblock','')
    #print >>sys.stderr, textblock
    print >>sys.stderr, "start home"    
    prefix = request.GET.get('prefix','')
    root = request.GET.get('root','')
    suffix = request.GET.get('suffix','')
    top10k = request.GET.get('top10k',0)
    #pdb.set_trace()

    concordance = ''
    words = []
    if len(textblock) > 0:
        concordance = make_concordance(textblock)
        
    (query, cnt_query) = make_query(prefix, root, suffix, top10k)

    
    print >>sys.stderr, "query:%r" % query
    if len(query)>0:
        words = Word.objects.raw(query)       
        print >>sys.stderr, 'query run!'
    else:
        print >>sys.stderr, 'query not run'
        
    #pdb.set_trace()   
    return render_to_response('home.html', {'prefix':prefix, 'root':root, 'suffix':suffix, 'query':query, 'cnt_query':cnt_query, 'words':words, 'concordance':concordance })

def add_words(line, words):
    """ add the words in line to the dict words """ 
    for word in line.split():
        #pdb.set_trace()
        if word in words.keys():
            words[word] = words[word]+1
        else:
            words[word] = 1



def clean_text(line):
    #pdb.set_trace()   
    if re.search('[a-zA-Z]', line):
        line = line
    else:
        line = ''
    #pdb.set_trace()
    line=re.sub("\W"," ",line)
    line=re.sub("[\.\"\-!\'\\\)\(,\-)?]", "",line)
    #line=re.sub('\.','',line)
    #line=re.sub('"','',line)
    #line=re.sub("!",'',line)
    #line=re.sub("'",'',line)
    #line=re.sub('\(','',line)
    #line=re.sub('\)','',line)
    #line=re.sub(',','',line)
    #line=re.sub('\?','',line)
    #line=re.sub('-','',line)
    line=re.sub('”','',line)
    line=re.sub('“','',line)
    line=re.sub('„','',line)
    line=re.sub('…','',line)
    line= line.lower()

    return line    
    
def make_concordance(textblock):
    words = {}
    textblock = clean_text(textblock)
    add_words(textblock, words)
    return words

def make_query(prefix,root,suffix,top10k=0):

    top10k_clause = ''
    if (top10k > 0) :
        top10k_clause = " and top>0"
    # now make the query...
        
    clause = ''
        
    if len(prefix)>0:
        clause = prefix
    else:
        clause="%%"
            
    if len(root)>0:
        clause = clause + root
    else:
        clause=clause+"%%"
            
    if len(suffix)>0:
        clause = clause + suffix
    else:            
        clause=clause+"%%"
        

    if len(prefix+root+suffix) > 0:
        clause = 'and word like "'+clause+'"'
        query = """select id, word, top from wordwander_word where 1=1 %s %s """ % (clause,top10k_clause)       
        cnt_query = """select count(*) from word where 1=1 %s %s """ % (clause,top10k_clause)       
    else:
        clause = ''
        query = ''
        cnt_query = ''
        
    
    #query = "select word, substr(word,0, instr(word,'" + root + "')) as prefix," +
    #    "substr(word," + root.length + "+ instr(word, '" + root + "' ) ) as suffix,  " +
    #    "instr(word, '" + root + "') as root_pos, " +
    #    "length(substr(word,0, instr(word,'" + root + "'))) as l, " +
    #    "top " +
    #    "from words where " + glob_clause + top10k_clause;
    
    return (query, cnt_query)

        
