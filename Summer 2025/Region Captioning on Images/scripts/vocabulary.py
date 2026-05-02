import nltk
import pickle
import pandas as pd
from collections import Counter
from tqdm import tqdm

class Vocabulary:
    def __init__(self):
        self.word2idx = {}
        self.idx2word = {}
        self.idx = 0
        self.add_word('<pad>')
        self.add_word('<start>')
        self.add_word('<end>')
        self.add_word('<unk>')

    def add_word(self, word):
        if word not in self.word2idx:
            self.word2idx[word] = self.idx
            self.idx2word[self.idx] = word
            self.idx += 1
    
    def __call__(self, word):
        if word not in self.word2idx:
            return self.word2idx['<unk>']
        return self.word2idx[word]

    def __len__(self):
        return len(self.word2idx)

def build_vocab(captions_file, threshold):
    df = pd.read_csv(captions_file)
    counter = Counter()
    
    print("Tokenizing captions...")
    for i, row in tqdm(df.iterrows(), total=len(df)):
        try:
            caption = str(row['caption'])
            tokens = nltk.tokenize.word_tokenize(caption.lower())
            counter.update(tokens)
        except Exception as e:
            print(f"Skipping caption: {row.get('caption')}. Error: {e}")

    words = [word for word, cnt in counter.items() if cnt >= threshold]

    vocab = Vocabulary()
    print(f"Building vocabulary... (Threshold: {threshold})")
    for word in tqdm(words):
        vocab.add_word(word)
        
    return vocab

if __name__ == '__main__':

    captions_file = 'Project/data/captions.txt'
    vocab_path = 'Project/data/vocab.pkl'
    threshold = 5

    print(f"Building vocab from: {captions_file}")
    vocab = build_vocab(captions_file, threshold=threshold)
    
    with open(vocab_path, 'wb') as f:
        pickle.dump(vocab, f)
        
    print(f"Total vocabulary size: {len(vocab)}")
    print(f"Vocabulary saved to: {vocab_path}")
