# Validierung

Tools zur Validierung einer REDCap Instanz / eines Projektes. 

## Automatisiertes Testen
Als erstes Unterprojekt wird eine Möglichkeit zum automatisierten testen
von REDCap-Projekten/Fragebögen umgesetzt. Dazu wird eine [yaml-Datei](browser_based/test1.yaml)
erstellt, die ein Testszenario (Probeeingaben, erwartete Reaktionen, erwartete Daten) enthält. 

Mit Hilfe von Selenium werden dann über einen Browser die entsprechenden Eingaben automatisch getätigt
und ein Testprotokoll erstellt. 

Ziel ist es, nach Updates oder Änderungen am Projekt-Setup sicherzustellen, dass alle
spezifizierten Funktionalitäten das erwartete Verhalten zeigen. 

Wie immer besteht die Herausforderung darin, die Tests parallel zum Projekt zu entwickeln, und nicht
zu sehr von REDCap-Interna (CSS-Klassen/DOM Identifier) abhängig zu sein, deren Änderung
Einfluss auf das automatisierte testen, nicht jedoch auf die normale Nutzer-Interaktion hätte.

Aktuell wird lediglich eine Basisfunktionalität zum Testen von Surveys umgesetzt, insbesondere
da die Syntax noch nicht final ist. 
