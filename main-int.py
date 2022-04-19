import markovify  # библиотека для обработки цепей Маркова
import nltk  # библиотека для обработки естественного языка
import re  # библиотека для разделения строки по шаблону

# графические библиотеки
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter.filedialog as fd

filetypes = [("Текстовый файл", "*.txt")]  # типы используемых файлов


# основа интерфейса
class TextGenerator(ttk.Frame):
    def __init__(self):
        super().__init__()

        self.style = ttk.Style()

        self.initUI()

    def initUI(self):
        # настройки
        self.master.title("Генератор текста")
        self.style.theme_use("default")

        newfont1 = tkFont.Font(family="Comic Sans MS", size=16, weight="bold", slant="italic")

        frame = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        frame.pack(fill=tk.BOTH, expand=True)

        self.pack(fill=tk.BOTH, expand=True)

        # основные компоненты графического интерфейса
        background = tk.Label(
            foreground="gray30",
            background="LightCyan2",
            width=50,
            height=20
        )
        text1 = tk.Label(
            text="Выберите текстовый файл: ",
            background="LightCyan2"
        )
        text2 = tk.Label(
            text="Введите кол-во предложений: ",
            background="LightCyan2"
        )
        entry1 = tk.Entry(
            width=40,
            foreground="black"
        )
        entry2 = tk.Entry(
            width=40,
            foreground="black"
        )
        button1 = tk.Button(
            text="Вывести текст",
            width=15,
            command=lambda: new_window()
        )
        button2 = tk.Button(
            text="···",
            width=5,
            height=1,
            command=lambda: set_txt()
        )

        background.pack(fill=tk.BOTH, expand=True)
        text1.place(x=20, y=10)
        text1.configure(font=newfont1)
        text2.place(x=20, y=70)
        text2.configure(font=newfont1)
        entry1.place(x=25, y=45)
        entry2.place(x=25, y=105)
        button1.place(x=25, y=140)
        button2.place(x=280, y=42)

        # удобный ввод текстового файла
        def set_txt():
            filename = fd.askopenfilename(title="Открыть файл", initialdir="/", filetypes=filetypes)
            entry1.delete(0, tk.END)
            entry1.insert(0, filename)

        # вывод текста в новом окне
        def new_window():
            window = tk.Toplevel()
            window.title("Текст")
            window.geometry("800x300")
            text = tk.Text(
                window,
                foreground="black"
            )
            text.pack(fill=tk.BOTH, expand=True)
            txt = str(entry1.get())
            with open(txt, 'r', encoding='utf-8') as f:  # открытие файла
                corpus = f.read()

            # составление модели
            text_model = markovify.Text(corpus, state_size=3)
            model_json = text_model.to_json()
            reconstituted_model = markovify.Text.from_json(model_json)

            # вывод
            s = int(entry2.get())
            for i in range(s):
                sentence = str(reconstituted_model.make_short_sentence(3000)) + "\n"
                text.insert(0.0, sentence)


class POSifiedText(markovify.Text):  # составление предложения
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


# основное окно
def main():
    root = tk.Tk()
    root.geometry("375x185")
    root.resizable(width=False, height=False)
    app = TextGenerator()
    root.mainloop()


# запуск программы
if __name__ == '__main__':
    main()
