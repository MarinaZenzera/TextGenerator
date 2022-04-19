import markovify        # библиотека для обработки цепей Маркова
import nltk             # библиотека для обработки естественного языка
import re               # библиотека для разделения строки по шаблону

class POSifiedText(markovify.Text):         # составление предложения
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


text = str(input("Введите название файла: ")+".txt")    # выбор файла

with open(text, 'r', encoding='utf-8') as f:            # открытие файла
    corpus = f.read()

# составление модели
text_model = markovify.Text(corpus, state_size=3)
model_json = text_model.to_json()
reconstituted_model = markovify.Text.from_json(model_json)

# вывод
s = int(input("Введите число предложений: "))

for i in range(s):
    print(reconstituted_model.make_short_sentence(3000))
