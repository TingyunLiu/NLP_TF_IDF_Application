import math
import os, os.path
import sys
import Queue





class TF_IDF:
	
	directory = ""
	total_text_count = 0
	my_e = 0
	popular = ["in", "on", "under", "behind", "at", "of", "after", "between", "off", "to", "with", "around",
			   "as", "by", "over", "below", "about", "without", "above", "before", "into", "onto", "like",
			   "unlike", "for", "beneath", "from", "among", "along", "within", "during", "beside", "up", "down",
			   "upon",

			   "i", "me", "my", "mine", "myself", "you", "your", "yours", "yourself", "he", "him", "his",
			   "himself", "she", "her", "hers", "herself" , "it", "its", "itself", "we", "us", "our", "ours",
			   "ourselves", "they", "them", "their", "theirs", "themselves",

			   "can", "could", "should", "may", "might", "must", "will", "would", "do", "does", "did", "done",
			   "is", "was", "are", "were", "be", "go", "went", "goes", "going", "not", "have", "has", "had", "a",
			   "an"
			  ]

	def __init__(self, dir_path):
		self.directory = dir_path
		self.total_text_count = len([text for text in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory,text))])
		self.my_e = sum(1/float(math.factorial(i)) for i in range(100))
		print '************************ Initialization ************************'


	def __del__(self):
		print '*************************** Finished ***************************'
		print

	def counting_total_word_in_text(self, text):
		count = 0
		with open(os.path.join(self.directory, text), 'r') as file:
			for line in file:
				for word in line.split():
					count += 1
		return count


	def counting_word_in_text(self, target_word, text):
		count = 0
		with open(os.path.join(self.directory, text), 'r') as file:
			for line in file:
				for word in line.split():
					if word.lower() == target_word.lower():
						count += 1
		return count


	def is_word_in_text(self, target_word, text):
		with open(os.path.join(self.directory, text), 'r') as file:
			for line in file:
				for word in line.split():
					if word.lower() == target_word.lower():
						return True
		return False


	def counting_text_included_in_folder(self, word):
		count = 0
		files = [text for text in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, text))]
		for file in files:
			if self.is_word_in_text(word, file):
				count += 1
		return count


	def contain_special(self, word):
		if ('~' in word) or ('`' in word) or ('!' in word) or ('@' in word) or ('#' in word) or ('$' in word) \
		or ('%' in word) or ('^' in word) or ('&' in word) or ('*' in word) or ('(' in word) or (')' in word) \
		or ('{' in word) or ('}' in word) or ('[' in word) or (']' in word) or ('|' in word) or ('\'' in word) \
		or (':' in word) or (';' in word) or ('"' in word) or (',' in word) or ('<' in word) or ('.' in word) \
		or ('>' in word) or ('?' in word) or ('/' in word) or ('\\' in word):
			return True
		else:
			return False


	def TF(self, word_count, total_word):
		return float(word_count)/total_word


	def IDF(self, text_included, total_text):
		ret = float(total_text)/(1 + text_included);
		return math.log(ret, self.my_e)


	def keyword_pickup(self, text, how_many):

		word_dict = {}
		keyword = Queue.PriorityQueue()
		total_word = self.counting_total_word_in_text(text)


		with open(os.path.join(self.directory, text), 'r') as file:
			for line in file:
				for word in line.split():

					word = word.lower()

					if (word in self.popular) or self.contain_special(word) or (word in word_dict):
						continue

					word_count = self.counting_word_in_text(word, text)
					text_included = self.counting_text_included_in_folder(word)

					weight = self.TF(word_count, total_word) * self.IDF(text_included, self.total_text_count)
					
					word_dict[word] = weight
					keyword.put((weight, word))

		while not keyword.empty():
			print keyword.get()


example = TF_IDF(sys.argv[1])
example.keyword_pickup(sys.argv[2], 0)

