import numpy as np
import matplotlib.pyplot as plt
import nltk
from string import punctuation
import copy

sent_per_block = 100

fDir = "/Users/nbilenko/NYB/berkeley/classes/cs294_dataviz/a3/data/murakami/"

files = ["pinball1973.txt", "hardboiled.txt", "norwegianwood.txt", "dancedancedance.txt", "windupbird.txt", "kafkaontheshore.txt", "afterdark.txt", "1q84.txt"]

motifs = [["cat", " cats", "tomcat", "tomcats"],
		["well", "wells"], # find well, check whether the or a before it
		["train", "trains", "station", "stations"],
		["spaghetti", "noodles", "pasta", "ramen"],
		["jazz", "saxophone"],
		["classical", "symphony", "opera"],
		["war", "wars"],
		["ear", "ears", "earlobe", "earlobes"],
		["coffee"],
		["vanish", "vanishing", "vanishes", "vanished", "disappear", "disappearing", "disappears", "disappeared"]]

motifnames = ["cats", "wells", "train stations", "noodles", "jazz", "classical", "war", "ears", "coffee", "vanishing"]
booknames = ["Pinball, 1973", "Hard-boiled Wonderland and the End of the World", "Norwegian Wood", "Dance, Dance, Dance", "The Wind-up Bird Chronicle", "Kafka on the Shore", "After Dark", "1Q84"]

books = []
for f in files:
	books.append(tokens_to_text(tokenize(fDir+f, type = "sent"), skip_punct = True))

csvfile = open("/Users/nbilenko/Sites/murakami.csv", "wb")
bookwriter = csv.writer(csvfile, delimiter=',')
bookwriter.writerow(["book", "motif", "block", "number", "sentence"])

for bi, book in enumerate(books):
	book_name = booknames[bi]
	for mi, motif in enumerate(motifs):
		motif_name = motifnames[mi]
		num_blocks = len(book)/sent_per_block+1
		for block in range(num_blocks):
			sentence_block = book[sent_per_block*block:sent_per_block*(block+1)]
			motif_number = 0
			motif_sentence = ""
			for si, sentence in enumerate(sentence_block):
				orig_sent = copy.deepcopy(sentence).decode("utf-8")
				orig_sent = orig_sent.replace("\n", " ")
				sentence = sentence.lower()
				for p in punctuation:
					sentence = sentence.replace(p, "")
				words = sentence.split()
				for mword in motif:
					if mword in words:
						if mword == "well":
							wid = words.index(mword)
							if words[wid-1] == "a" or words[wid-1] == "the":
								motif_number+=1
								if motif_sentence == "":
									motif_sentence = orig_sent
						else:
							motif_number+=1
							if motif_sentence == "":
								motif_sentence = orig_sent
			bookwriter.writerow([book_name, motif_name, block, motif_number, motif_sentence.encode("utf-8")])
csvfile.close()

def tokenize(fname, type = "wordpunct", encoding = "utf8"):
	f = open(fname)
	raw_text = f.read()
	text = raw_text.decode(encoding)
	if type == "wordpunct":
		tokens = nltk.wordpunct_tokenize(text)
	elif type == "word":
		tokens = nltk.word_tokenize(text)
	elif type == "sent":
		tokens = nltk.sent_tokenize(text)
	else:
		print "Wrong tokenization type specified"
	return tokens

def tokens_to_text(tokens, skip_punct = False, lower = False):
	if skip_punct:
		ttext = [str(token.encode("utf8")) for token in tokens if token not in punctuation]
	else:
		ttext = [str(token.encode("utf8")) for token in tokens]
	if lower:
		ttext = [t.lower() for t in ttext]
	return nltk.Text(ttext)