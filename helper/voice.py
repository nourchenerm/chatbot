import speech_recognition
from tkinter import *
from tkinter import font
from chatbot import chatbot_logic, load_qa

root = Tk()
root.geometry("500x300")
root.title("Reconnaissance Vocale")

file_path = "intents.json"
qa_data = load_qa(file_path)

def voiceReco():
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)
        try:
            text = recognizer.recognize_google(audio, language='fr-FR')
            print("Texte reconnu :", text)
            response = chatbot_logic(text,qa_data,"fr" )
            print(response)

            textF.delete("1.0", "end")
            textF.insert(END, text)
            textF.tag_add("center", 1.0, "end")
            return text
        except speech_recognition.UnknownValueError:
            print("Impossible de reconnaître l'audio.")
        except speech_recognition.RequestError as e:
            print(f"Erreur lors de la requête : {e}")

ButtonFont = font.Font(size=20)
LabelFont = font.Font(size=15)

Label(root, text="Le texte s'affichera ici", font=LabelFont).pack()

textF = Text(root, height=5, width=52, font=LabelFont)
textF.tag_configure("center", justify='center')
textF.pack()

Button(root, text='Écouter', font=ButtonFont, command=voiceReco).place(x=220, y=200)

root.mainloop()