
import math

def clean_text(txt):
    """Cleans a string of text removing punctuation
    """
    txt = txt.lower()
    txt = txt.replace('.','')
    txt = txt.replace(',','')
    txt = txt.replace('!','')
    txt = txt.replace('?','')
    txt = txt.replace('-','')
    
    return txt

def stem(word):
    """Computes word Stems, and returns a dictionary
    """
    two_suff = ['ed','ty','or','fy', 'er'] #Suffix of len 2
    three_suff = ['ful','ant','ion','ily']
    four_suff = ['ship','ward','ular','ment', 'less']
    if word[-3:] == 'ing':
        if len(word) > 6  and word[-4] == word[-5] :
            word = word[:-4]
        else:
            word = word[:-3]
    elif word[-2:] == 'er' or word[-2:] == 'ly' or word[-2:] in two_suff:
        word = word[:-2]
    elif len(word) > 2 and word[-1] == 's':
        word = stem(word[:-1])
    elif word[-4:] == 'able'or word[-4:] in four_suff:
        word = word[:-4]
    elif word[-3:] == 'ous' or word[-3:] in three_suff:
        word = word[:-3]
        
    return word



def len_sen(s):
    """Computes a dictionary of sentence lenghts
    """
    words = s.replace('.', '##')
    words = words.replace('!', '##')
    words = words.replace('?', '##')
    words = words.split('##')
    len_dic = {}
    #print(words)
    result = []
    for i in range(len(words)):
        wordz = words[i].split()
        result += [len(wordz)]
    #print(result)
    for next_sen in result:
        if next_sen not in len_dic:
            len_dic[next_sen] = 1
        else:
            len_dic[next_sen] += 1
    return len_dic

def compare_dictionaries(d1, d2):
    """Compares two dictionaries
    """
    score = 0
    total = 0
    for key in d1:
        total += d1[key]

    for key in d1:
        if key in d2:
            score += math.log(d1[key]/total)
        else:
            score += math.log(0.5/total)
    return score



def punc_dic(s):
    """Returns a list of the punctuation used in the text sample,
       with duplicates
    """
    result = ''
    for i in range(len(s)):
        if s[i] in '.!?:;':
            result += s[i] + ' '
    words = result.split()
    dic = {}
    
    for next_word in words: #makes the self.punc dictionary
        if next_word not in dic:
            dic[next_word] = 1
        else:
            dic[next_word] += 1
    return dic
    

    
class TextModel:

    def __init__(self, model_name):
        """Constructer 
        """
        self.name = model_name # name of the text model
        self.words = {} # dictionary of no.of times word appears
        self.word_lengths = {} # dictionary of lenghts
        self.stems = {} #a dictionary number of times each word stem appears
        self.sentence_lengths = {} #no. of times each sentence legth appears
        self.punc = {} #no. of times punctuation used

    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths))
        s += '\n'
        s += '  number of word stems: ' + str(len(self.stems))
        s += '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths))
        s += '\n'
        s += '  number of punctuation types: ' + str(len(self.punc))
        return s

    def add_string(self, s):
        """Adds a string to the Text Model
        """
        words = s.lower()
        words = words.split()
        
        for next_word in words: #makes the self.stems dictionary
            word_stem = stem(next_word)
            if word_stem not in self.stems:
                self.stems[word_stem] = 1
            else:
                self.stems[word_stem] += 1

        self.sentence_lengths = len_sen(s) # makes senLen dic



        self.punc = punc_dic(s) #outsorce the problem to punc_dic
        words = clean_text(s)
        words = words.split()
        #print(words)
        current_word = words[0]
        
        for next_word in words:
            len_word = len(next_word)
            if len_word not in self.word_lengths:
                self.word_lengths[len_word] = 1
            else:
                self.word_lengths[len_word] += 1
            if next_word not in self.words:
                self.words[next_word] = 1
            else:
                self.words[next_word] += 1
                
    def add_file(self, filename):
        """Adds a file to the text Model
        """
        file = open(filename, 'r', encoding='utf8', errors='ignore')
        text = file.read()
        file.close()
        text = clean_text(text)
        
        self.add_string(text)
        
            
    def save_model(self):
        """Save model to directory
        """
        filename_words =  self.name + '_' + 'words'
        dictionary = self.words
        file = open(filename_words, 'w')
        file.write(str(dictionary))
        file.close

        filename_words =  self.name + '_' + 'stems'
        dictionary = self.stems
        file = open(filename_words, 'w')
        file.write(str(dictionary))
        file.close

        filename_words =  self.name + '_' + 'sentence_lengths'
        dictionary = self.sentence_lengths
        file = open(filename_words, 'w')
        file.write(str(dictionary))
        file.close

        filename_word_lens = self.name + '_' + 'word_lengths'
        dictionary = self.word_lengths
        file = open(filename_word_lens, 'w')
        file.write(str(dictionary))
        file.close

        filename_word_lens = self.name + '_' + 'punctuation'
        dictionary = self.punc
        file = open(filename_word_lens, 'w')
        file.write(str(dictionary))
        file.close
        
        

    def read_model(self):
        """Read file from directory
        """
        filename_words =  self.name + '_' + 'words'
        file = open(filename_words, 'r')    # Open for reading.
        d_str = file.read()           # Read in a string that represents a dict.
        file.close()
        self.words = dict(eval(d_str))
        
        filename_words =  self.name + '_' + 'stems'
        file = open(filename_words, 'r')    # Open for reading.
        d_str = file.read()           # Read in a string that represents a dict.
        file.close()
        self.words = dict(eval(d_str))

        filename_words =  self.name + '_' + 'sentence_lengths'
        file = open(filename_words, 'r')    # Open for reading.
        d_str = file.read()           # Read in a string that represents a dict.
        file.close()
        self.words = dict(eval(d_str))

        filename_words =  self.name + '_' + 'punctuation'
        file = open(filename_words, 'r')    # Open for reading.
        d_str = file.read()           # Read in a string that represents a dict.
        file.close()
        self.words = dict(eval(d_str))

        filename_word_lens =  self.name + '_' + 'word_lengths'
        file = open(filename_word_lens, 'r')    # Open for reading.
        d_str = file.read()           # Read in a string that represents a dict.
        file.close()
        self.word_lengths = dict(eval(d_str))

    def similarity_scores(self, other):
        list_scores = []
        sim_words = compare_dictionaries(self.words, other.words)
        list_scores += [sim_words]
        
        sim_word_lengths = compare_dictionaries(self.word_lengths, other.word_lengths)
        list_scores += [sim_word_lengths]
        
        sim_stems = compare_dictionaries(self.stems, other.stems)
        list_scores += [sim_stems]
        
        sim_sentence_lengths = compare_dictionaries(self.sentence_lengths, other.sentence_lengths)
        list_scores += [sim_sentence_lengths]

        sim_punc = compare_dictionaries(self.punc, other.punc)
        list_scores += [sim_punc]

        return list_scores

        
    def classify(self, source1, source2):
        """that compares the called TextModel object (self) to two
           other “source” TextModel objects (source1 and source2) 
           and determines which
           of these other TextModels is the more likely source
           of the called TextModel.
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        scores1 = [ '%.2f' % elem for elem in scores1 ]
        scores1 = [elem[1:] for elem in scores1]
        for i in range(len(scores1)):
            scores1[i] = float(scores1[i])
        scores2 = [ '%.2f' % elem for elem in scores2 ]
        scores2 = [elem[1:] for elem in scores2]
        for i in range(len(scores2)):
            scores2[i] = float(scores2[i])
        for i in range(len(scores1)):
            scores1[i] = -scores1[i]
            scores2[i] = -scores2[i]
        
    
        print('Scores for',source1.name, scores1)
        print('Scores for',source2.name, scores2)
        sum_score1 = 0
        sum_score2 = 0
        for i in range(len(scores1)):
            sum_score1 += scores1[i]
            sum_score2 += scores2[i]
        sum_score1 = sum_score1/5
        sum_score2 = sum_score2/5

        if sum_score1 >= sum_score2:
            print(self.name,'is more likley to have come from', source1.name)
        else:
            print(self.name,'is more likley to have come from', source2.name)
   # print("\n")
    

# at the bottom of the file, *outside* of the TextModel class.
def run_tests():
    """ runs tests on a series of files to determine wether they are similar """
    source1 = TextModel('Washington Post')
    source1.add_file('WSJ_source_text.txt')

    source2 = TextModel('Shakespeare_Romeo')
    source2.add_file('shakespeare_source_text.txt')

    new1 = TextModel('Personal Writing Sample')
    new1.add_file('wr_100_source_text.txt')
    new1.classify(source1, source2)
    print("\n")
    
#three other new models below.

    source3 = TextModel('friends_transcript')
    source3.add_file('friends_source_text.txt')

    source4 = TextModel('New York Times')
    source4.add_file('NYT11.txt')
    source4.classify(source3, source1)
    print("\n")
    #NYT is compared to Friends_transcript and Washington Post

    source5 = TextModel('Class_notes')
    source5.add_file('Class_notes.txt')
    source5.classify(source3, source1)
    #Class_notes is compared to friends_transcipt and Washington Post
    
