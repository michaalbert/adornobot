import argparse
import markovify
import nltk
import re
import spacy
import sys

nlp_en = spacy.load('en_core_web_sm')
nlp_de = spacy.load('de_core_news_sm')

class POSifiedText(markovify.Text):

	def __init__(
		self,
		input_text,
		state_size=2,
		chain=None,
		parsed_sentences=None,
		retain_original=True,
		well_formed=True,
		reject_reg='',
		lang='de',
	):

		self.lang = lang
		super().__init__(
				input_text, 
				state_size,
				chain,
				parsed_sentences,
				retain_original,
				well_formed,
				reject_reg
		)
		

	def word_split(self, sentence):
		if self.lang == 'de':
			return ['::'.join((word.orth_, word.pos_)) for word in nlp_de(sentence)]
		elif self.lang == 'en':
			return ['::'.join((word.orth_, word.pos_)) for word in nlp_en(sentence)]

	def word_join(self, words):
		sentence = ' '.join(word.split('::')[0] for word in words)
		return sentence

def adornobot(n_sentences=1, lang='de', state_size=3, pos=False):
	#print(lang, n_sentences, char_limit, state_size)
	if lang == 'de':
		filename = 'minima_moralia_de.txt'
	elif lang == 'en':
		filename = 'minima_moralia_en.txt'
	else:
		sys.exit(1)
	
	with open(filename, encoding='utf8') as f: 
		text = f.read()

	if pos:
		print("Building text model...")
		text_model = POSifiedText(text, state_size=state_size, lang=lang)
		print("Text model ready, printing sentences:\n")
	else:
		text_model = markovify.Text(text, state_size=state_size)
	for i in range(n_sentences):
		#print(text_model.make_short_sentence(char_limit) + '\n')
		print(text_model.make_sentence() + '\n')
	return

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate Adorno-like sentences based on Minima Moralia using a Markov chain.')
	parser.add_argument('--n_sentences', '-n', default=1, nargs='?', type=int)
	parser.add_argument('--lang', default='de', nargs='?', type=str)
	parser.add_argument('--state_size', default=2, nargs='?', type=int)
	parser.add_argument('--pos', action='store_true', default=False)
	args = parser.parse_args()
	adornobot(args.n_sentences, args.lang, args.state_size, args.pos)
