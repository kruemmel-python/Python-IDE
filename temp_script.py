
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# Quiz mit gemischten Antwortmöglichkeiten

def stelle_frage(frage, antworten, korrekte_antwort):
    print(frage)
    for antwort in antworten:
        print(antwort)
    eingabe = input("Deine Antwort: ")
    if eingabe.lower() == korrekte_antwort.lower():
        print("Richtig! 🎉")
        return True
    else:
        print("Falsch. 😢 Die richtige Antwort war " + korrekte_antwort + ".")
        return False

# Hauptprogramm
fragen = [
    ("Frage 1: Was ist die Hauptstadt von Deutschland?", ["A) Berlin", "B) München", "C) Köln", "D) Frankfurt"], "A"),
    ("Frage 2: Wie viele Bundesländer hat Deutschland?", ["1) 14", "2) 15", "3) 16", "4) 17"], "3"),
    ("Frage 3: Wer hat die Relativitätstheorie entwickelt?", ["A) Isaac Newton", "B) Albert Einstein", "C) Nikola Tesla", "D) Stephen Hawking"], "B"),
    ("Frage 4: Welcher Fluss fließt durch Berlin?", ["1) Rhein", "2) Donau", "3) Elbe", "4) Spree"], "4")
]

punkte = 0
for frage, antworten, korrekte_antwort in fragen:
    if stelle_frage(frage, antworten, korrekte_antwort):
        punkte += 1

print(f"Du hast {punkte} von {len(fragen)} Fragen richtig beantwortet!")