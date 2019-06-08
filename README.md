# Symulator Śmieciarki
Projekt na przedmiot **Sztuczna Inteligencja**

## Członkowie projektu
  - Dawid Wietrzych
  - Jacek Krakowski
  - Michał Romaszkin
  - Jakub Kwiatkowski
  - Aleksander Chandrykowski
  
## Opis projektu
### Nazwa kodowa 
***Garbage truck simulator***

### Założenia 
Celem podjętych działań przez naszą grupę było stworzenie dyskretnej mapy, opierającej się na liście dwuwymiarowej jako środowiska do poruszania się inteligentnej śmieciarki. Do zrealizowania ruchu śmieciarki posłużylilśmy się znannymi algorytmami jak _Breadth-first search_ czy _Depth-first search_. Agent (śmieciarka) za pomocą uzyskanych rezultatów ("przejść" ww. algorytmami) przemieszcza się do losowo (za każdym wygenerowaniem mapy) rozmieszczonych domków, w których zalegają śmieci.

## Struktura projektu
Składowe projektu dzielą się na:

### Scripts
Folder zawierający wszystkie pliki źródłowe symulacji. Odpowiedzialne za poprawne działanie samej aplikacji okienkowej, generowania obrazów, czy w końcu logiki związanej z działaniami jakie podejmuję śmierciarka. Należą do nich:

Klasy z konstruktorami poszczególnych obiektów:
- _Bin.py_
- _Collector.py_
- _Dump.py_
- _Grass.py_
- _MapElement.py_
- _Road.py_

A także plik z zawartością logiki do symulacji o nazwie _Simulation.py_

### Images
Tu znajdują się wszystkie potrzebne grafiki, które generowane są na mapie (domki, śmietniki, trawa, droga).

### Data
Nic innego jak potrzebne dane do uczenia maszynowego, jak np. pozycje śmieciarki z wygenerowania klikudziesięciu map.

### Documentation
Plik zawierający dokumentację projektu.
  
  2019&reg; All rights reserved
