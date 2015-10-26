
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import os
import re
import sys
from django.db import connection, transaction
from wordwander.models import Word


def home(request):
    prefix = request.GET.get('prefix','')
    root = request.GET.get('root','')
    suffix = request.GET.get('suffix','')
    top10k = request.GET.get('top10k',0)

     
    (query, cnt_query) = make_query(prefix, root, suffix, top10k)
    print >>sys.stderr, "query:%r" % query
    if len(query)>0:
        words = Word.objects.raw(query)
        

        print >>sys.stderr, 'query run!'
        for w in words:
            print >>sys.stderr, "w:%r" % w
        print >>sys.stderr, "done printing results"
    else:
        print >>sys.stderr, 'query not run'
        words = ['1','2','3']
        
    return render_to_response('home.html', {'prefix':prefix, 'root':root, 'suffix':suffix, 'query':query, 'cnt_query':cnt_query, 'words':words })

    
    
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

        
