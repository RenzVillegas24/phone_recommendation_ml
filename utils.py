def get_word_frequencies(lst, words):
    word_freq = {}
    for i, row in enumerate(lst):
        text = row.lower()  # Convert text to lowercase
        for word in text.split():
            if all(v.lower() in text for v in word):  # Convert word to lowercase
                if word in word_freq.keys():
                    word_freq[word].add(i)
                else:
                    word_freq[word] = set()            
    return word_freq

def get_top_words(lst, top_n=10):
    word_count = {}
    for sentence in lst:
        if sentence is None:
            continue
        words = sentence.lower().replace('/', ' ').strip('_.,!?()[]{}"\'').replace('|', ' ').split()  # Convert text to lowercase
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1
    top_words = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:top_n])
    return top_words




