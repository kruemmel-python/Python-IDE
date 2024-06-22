def lade_fragen():
    fragen = [
        {
            "frage": "Was ist 2 + 2?",
            "antworten": ["1. 3", "2. 4", "3. 5"],
            "korrekte_antwort": "2"
        },
        {
            "frage": "Was ist die Hauptstadt von Frankreich?",
            "antworten": ["a. Berlin", "b. Madrid", "c. Paris"],
            "korrekte_antwort": "c"
        },
        {
            "frage": "Welche Zahl ist eine Primzahl?",
            "antworten": ["1. 4", "2. 6", "3. 11"],
            "korrekte_antwort": "3"
        },
        {
            "frage": "Welche Farbe hat der Himmel?",
            "antworten": ["a. Grün", "b. Blau", "c. Gelb"],
            "korrekte_antwort": "b"
        }
    ]
    return fragen

def quiz_spielen(fragen):
    punkte = 0
    for i, frage in enumerate(fragen):
        print(f"Frage {i+1}: {frage['frage']}")
        for antwort in frage['antworten']:
            print(antwort)
        
        antwort = input("Ihre Antwort eingeben: ").strip().lower()
        if antwort == frage['korrekte_antwort']:
            print("Richtig!")
            punkte += 1
        else:
            print(f"Falsch! Die richtige Antwort war: {frage['korrekte_antwort']}")
        print()

    print(f"Quiz beendet! Sie haben {punkte} von {len(fragen)} Punkten erreicht.")

if __name__ == "__main__":
    fragen = lade_fragen()
    quiz_spielen(fragen)
