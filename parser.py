from lxml import etree
from io import StringIO, BytesIO
import math 
import numpy

def test():
  print 'hello'
  pass


if __name__ == "__main__":
	#parser = etree.XMLParser(ns_clean=True)
	tree = etree.parse( "queries/query-train.xml")
	#print etree.tostring(tree.getroot(), encoding='utf-8')
	a = tree.findall('topic/concepts')# concepts narrative question


	for item in a:
	  print etree.tostring( item, encoding='utf-8')
	  
	#print etree.dump(a[0])


	###########################################################
	queryChar = []
	tree = etree.parse( "queries/query-train.xml").getroot()
	for i in tree:
	  print i.tag, '====='
	  for j in i:
	    print j.tag
	    print j.text	 	    
	    queryChar.append( j.text.strip() )
	  break	
	#print '[%s]' % ', '.join(map(str, queryChar))
	#print queryChar[:]
	allchars = ''.join(map(str, queryChar))# str
	allchars = allchars.split('').strip() 
	allchars = allchars.replace('\n','')
	print allchars
	allchars_uni = allchars.decode('utf-8')
	print '============================================================'

	# a = tree.findall(".//concepts")
	# print len(a)
	# for i in a:
	#   print i.tag
	###########################################################################################
# parse end
#
############################################################################################
	docNumber_all = 97445.0
	index_voc = 0
	# Get inverted-index as a python dictionary hash
	file_inv = open('wm/inverted-index', 'r')
	Dic = {}
	invertedDic = {}
	lineKey = tuple()
	print 'Dictionary Construction'
	i = 0# for break, delete
	for index, line in enumerate(file_inv):	
	  # if i == 40:
	  #   break
	  # i = i+1
	  ########
	  line_seg = line.strip().split(' ')
	  if len(line_seg) == 3:# term	  	
	    lineKey = (line_seg[0], line_seg[1])
	    Dic[lineKey] = {'df':line_seg[2]}
	    if line_seg[2]=='0':# document
	      Dic[lineKey].update( {'idf': 0} )
	    else:# line_seg[2]!=0
	      Dic[lineKey].update( {'idf':math.log( docNumber_all/float(line_seg[2]) )} )
	    Dic[lineKey].update( {'index': index_voc} )
	    invertedDic.update({index_voc:lineKey})# to retreive the key by index
	    index_voc+=1
	  elif len(line_seg) == 2:  	
	    Dic[lineKey].update( {line_seg[0]:line_seg[1]} )
	  else:
	    print 'Warrning: the length of the line is out of the range!!!'
##########################end dictionary of term freq
# query
# we need dictionary of term freq here!!! 
    file_voc = open('wm/vocab.all','r')
    vocDic = dict()
    query_vector = [0 for x in range(1761424)]# fix...
    query_vector_idf = [0 for x in range(1761424)]# fix...
    for index, line in enumerate(file_voc):# the dict for vocab.all
      char = line.strip().decode('utf8')
      vocDic.update( {char : index} )# index is int

    for char_id in range(len(allchars_uni)-1):
      char_curr = allchars_uni[char_id]
      char_next = allchars_uni[char_id+1]
      id_char_curr = vocDic[char_curr]
      id_char_next = vocDic[char_next]
      key_bigram = (str(id_char_curr),str(id_char_next))
      key_unigram = (str(id_char_curr), '-1')
      if Dic.has_key( key_bigram ):
    	index_query = Dic[key_bigram]['index']
    	query_vector[index_query] += 1 
    	query_vector_idf[index_query] = Dic[key_bigram]['idf']
      else:
      	index_query = Dic[key_unigram]['index']
      	query_vector[index_query] += 1
      	query_vector_idf[index_query] = Dic[key_unigram]['idf']
      	
    denominator_norm = sum([ (x*x) for x, x in zip(query_vector,query_vector) ])# to do: 1,get normalize one, 2,
    # tf-idf
    #query_vector_tfidf = [a*b for a,b in zip(query_vector,query_vector_idf)]

    #a = [i for i,x in enumerate(query_vector) if x == 1] # get the id of values
#############################################################################
	# Generating Big matrix, term frequency
	count=0
	#matrix = [ [0 for x in range(len(Dic))] for y in range(int(docNumber_all))]# initialization, 2D array
	matrix_short = [[0 for x in range(docNumber_all)] for y in range(int(300))]
	for key1 in Dic:# i is key, for uni term or bi term
	  termID = int(key1[0])
	  for key2 in Dic[key1]:# for docID
	    if key2 != 'df' and key2 != 'idf' and key2 != 'index':
	      docID = int(key2)
	      print 'docID is ', docID
          termFre = int(Dic[key1][key2])    	 
          index_word = Dic[key1]['index'] - 300*count
          #print 'index is ', index_word
          matrix_short[index_word][docID] += termFre
 
	      



	#





















