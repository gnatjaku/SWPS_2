# Obrona pracy dyplomowej: RAGDoctor

## Tytuł

**RAGDoctor: lokalny system RAG do odpowiadania na pytania na podstawie dokumentów medycznych**

## Cel wystąpienia

W 10 minut pokazać, że RAGDoctor jest działającym prototypem systemu RAG, który wykorzystuje lokalne modele AI do odpowiadania na pytania na podstawie przygotowanych dokumentów medycznych. Najważniejszy nacisk: RAG jako praktyczne zastosowanie lokalnych modeli AI oraz problemy jakości odpowiedzi, czyli retrieval, re-ranking, cutoff kontekstu i ograniczenia sprzętowe.

Projekt należy przedstawiać jako edukacyjny prototyp RAG, a nie jako narzędzie diagnostyczne.

## Plan czasu

| Czas | Temat | Cel |
|---:|---|---|
| 0:00-0:45 | Wprowadzenie | Co to jest RAGDoctor i czego nie robi |
| 0:45-1:45 | Problem | Dlaczego zwykły LLM nie wystarcza przy dokumentach medycznych |
| 1:45-3:00 | Architektura | Pipeline od dokumentu do odpowiedzi |
| 3:00-4:30 | Lokalne modele AI | LM Studio, Gemma 4 12B, bge-m3, prywatność lokalnego backendu |
| 4:30-6:00 | Retrieval i jakość | Cosine similarity, re-ranking, cutoff kontekstu |
| 6:00-7:30 | Demo | Pytanie w Web GUI, odpowiedź, cytowane chunki |
| 7:30-8:45 | Problemy techniczne | VRAM, PyTorch, fallback po OOM |
| 8:45-9:30 | Ograniczenia | Brak diagnostyki, zależność od dokumentów, jakość danych |
| 9:30-10:00 | Podsumowanie | Co zostało zbudowane i czego projekt uczy |

## Slajdy

1. Tytuł i cel pracy
2. Problem: odpowiedzi LLM bez kontroli nad źródłem
3. Czym jest RAGDoctor
4. Pipeline RAG
5. Architektura systemu
6. Lokalne modele AI: LM Studio, Gemma 4 12B, bge-m3
7. Retrieval, re-ranking i cutoff kontekstu
8. Demo aplikacji
9. Problemy praktyczne: VRAM i fallback CPU
10. Ograniczenia i podsumowanie

## Scenariusz mówiony

### 0:00-0:45: Wprowadzenie

Dzień dobry. Tematem mojej pracy jest **RAGDoctor: lokalny system RAG do odpowiadania na pytania na podstawie dokumentów medycznych**.

Projekt jest edukacyjnym prototypem pokazującym, jak można połączyć lokalne modele AI z mechanizmem RAG, czyli Retrieval-Augmented Generation.  Jego zadaniem jest odpowiadanie na pytania wyłącznie na podstawie wcześniej przygotowanych dokumentów.

Najważniejsza idea pracy jest taka: zamiast traktować model językowy jako niekontrolowane źródło wiedzy, dostarczam mu wybrany kontekst z dokumentów, a następnie wymuszam odpowiedź opartą na tym kontekście.



### 0:45-1:45: Problem

Problem, który rozwiązuje projekt, wynika z ograniczeń zwykłych modeli językowych. Model LLM może odpowiedzieć płynnie, ale nie zawsze wiadomo, na jakiej podstawie odpowiada. W kontekście dokumentów medycznych jest to szczególnie ważne, bo odpowiedź powinna wynikać z konkretnego tekstu, a nie z ogólnej wiedzy modelu albo halucynacji.

Drugim problemem jest lokalność działania. Chciałem sprawdzić, czy da się zbudować praktyczny system pytaniowy nad dokumentami bez wysyłania zapytań do zewnętrznego API modelu. Dlatego projekt wykorzystuje lokalny backend AI: LM Studio do generowania odpowiedzi oraz Ollamę do embeddingów.

RAGDoctor jest więc przykładem zastosowania AI lokalnie: model generuje odpowiedź, ale wiedza pochodzi z dokumentów, które zostały wcześniej zaindeksowane.

### 1:45-3:00: Pipeline RAG

Pipeline systemu składa się z kilku etapów.

Najpierw dokument medyczny jest dzielony na mniejsze fragmenty, czyli chunki. Chunking jest potrzebny, bo całe dokumenty są zbyt długie i zbyt nieprecyzyjne do bezpośredniego wyszukiwania.

Następnie każdy chunk otrzymuje embedding, czyli reprezentację wektorową tekstu. Te embeddingi razem z tekstem i metadanymi źródła są zapisywane w MongoDB.

Gdy użytkownik zada pytanie, system tworzy embedding pytania, porównuje go z embeddingami chunków, wybiera kandydatów i poprawia ranking dodatkowymi regułami leksykalnymi. Dopiero wybrane fragmenty trafiają do modelu LLM jako kontekst odpowiedzi.

Na końcu model generuje odpowiedź, a interfejs pokazuje także cytowane chunki, czyli fragmenty, które zostały użyte jako podstawa odpowiedzi.

### 3:00-4:30: Architektura i lokalne modele AI

Architektura projektu składa się z kilku elementów.

Backend jest napisany w FastAPI. Odpowiada za endpointy ingestu dokumentów, zadawania pytań i eksportu odpowiedzi do PDF. MongoDB pełni rolę magazynu chunków, embeddingów i metadanych źródeł. Web GUI działa jako prosty interfejs demonstracyjny do zadawania pytań i podglądu wykorzystanych fragmentów.

W aktualnej konfiguracji generowanie odpowiedzi odbywa się lokalnie przez LM Studio. Model używany w projekcie to `google/gemma-4-12B`, czyli Gemma 4 12B, traktowana tutaj jako aktualna generacja modelu Gemma od Google do lokalnego generowania odpowiedzi.

Praktyczna konfiguracja zakłada okno kontekstu około 30 tysięcy tokenów. To nie jest ograniczenie narzucone przez kod aplikacji, tylko decyzja uruchomieniowa dobrana do dostępnej pamięci karty graficznej.

Embeddingi są generowane lokalnie przez Ollamę z modelem `bge-m3`. Ten model został wybrany jako bieżący model embeddingów, ponieważ lepiej pasuje do wielojęzycznych tekstów niż wcześniejsze rozwiązanie. Po zmianie modelu embeddingów trzeba ponownie zaindeksować dokumenty, ponieważ embedding pytania i embeddingi chunków muszą pochodzić z tego samego modelu i mieć ten sam wymiar.

### 4:30-6:00: Retrieval, re-ranking i cutoff kontekstu

Najważniejsza część projektu to jakość retrievalu. Samo cosine similarity nie zawsze wystarcza. W testach wcześniejszy model embeddingów potrafił zwracać bardzo podobne wyniki dla tekstów o grypie i HIV, bo dokumenty zawierały podobne słownictwo medyczne.

Dlatego system stosuje hybrydowy re-ranking. Oprócz podobieństwa wektorowego bierze pod uwagę dopasowanie słów kluczowych z pytania, dopasowanie tytułu i źródła, proste normalizowanie polskich form wyrazów oraz premię za zgodność tematu pytania i intencji.

Druga decyzja jakościowa to cutoff kontekstu. Retrieval może zwrócić kilka najlepszych chunków, ale nie każdy z nich powinien trafić do promptu. Jeśli drugi albo trzeci chunk ma bardzo niski wynik, może wprowadzać szum i pogarszać odpowiedź. Dlatego system domyślnie zawsze zostawia najlepszy chunk, ale kolejne fragmenty muszą przekroczyć minimalny próg jakości. Cytacje w odpowiedzi pokazują tylko te chunki, które rzeczywiście zostały przekazane do modelu.

To jest ważne, bo RAG nie polega tylko na „wrzuceniu dokumentów do modelu”. Kluczowe jest dobranie właściwego kontekstu.

### 6:00-7:30: Demo

W tym miejscu pokazuję krótkie demo aplikacji.

W Web GUI wpisuję pytanie, na przykład: „Podaj wirusy wywołujące grypę sezonową?”. System wysyła pytanie do backendu FastAPI. Backend tworzy embedding pytania, wyszukuje podobne chunki w MongoDB, wykonuje re-ranking, odcina słabe fragmenty kontekstu i przekazuje wybrane chunki do modelu w LM Studio.

W odpowiedzi widzimy tekst wygenerowany przez model oraz listę użytych chunków. To jest istotna różnica względem zwykłego chatu z modelem: użytkownik widzi, że odpowiedź została oparta na konkretnych fragmentach dokumentów.

Jeśli odpowiedź nie wynika z kontekstu, model powinien zakomunikować brak wystarczających informacji, zamiast wymyślać odpowiedź.

### 7:30-8:45: Problemy praktyczne i VRAM

Podczas pracy pojawił się też praktyczny problem sprzętowy. LM Studio z modelem Gemma 4 12B i kontekstem około 30K tokenów potrafi zająć prawie całą pamięć GPU. Jednocześnie backend RAG używa PyTorch do batchowego liczenia cosine similarity między embeddingiem pytania a embeddingami chunków.

Domyślna strategia `RAG_SIMILARITY_DEVICE=auto` próbuje użyć GPU, jeśli CUDA jest dostępna. Ale jeśli LM Studio zajmuje większość VRAM, przeniesienie tensorów embeddingów na kartę graficzną może zakończyć się błędem CUDA OOM.

Dlatego w projekcie zastosowałem defensywną strategię: jeśli podczas similarity na GPU wystąpi OOM, aplikacja czyści cache CUDA i powtarza obliczenie na CPU. Wynik semantycznie pozostaje taki sam, tylko obliczenie może być wolniejsze. W praktyce pozwala to zostawić VRAM dla modelu generującego odpowiedź, a część retrievalu policzyć na CPU.

To pokazuje, że projekt nie jest tylko teoretycznym schematem RAG, ale mierzy się z realnymi ograniczeniami lokalnego uruchamiania modeli AI.

### 8:45-9:30: Ograniczenia

RAGDoctor ma świadome ograniczenia.

Po pierwsze, nie jest narzędziem diagnostycznym. Odpowiada tylko na pytania o treść dokumentów i nie powinien być traktowany jako system medyczny wspierający decyzje kliniczne.

Po drugie, jakość odpowiedzi zależy od jakości dokumentów, jakości chunkingu i jakości retrievalu. Jeśli właściwy fragment nie został zaindeksowany albo nie został dobrze dobrany, model nie ma podstaw do dobrej odpowiedzi.

Po trzecie, lokalne działanie zmniejsza potrzebę wysyłania danych do zewnętrznych usług, ale samo w sobie nie oznacza produkcyjnego bezpieczeństwa. Projekt nie implementuje pełnej kontroli dostępu, audytu ani zgodności z regulacjami dla danych medycznych.

### 9:30-10:00: Podsumowanie

Podsumowując, w pracy zbudowałem kompletny lokalny prototyp RAG: od ingestu dokumentów, przez chunking i embeddingi, po retrieval, re-ranking, generowanie odpowiedzi, cytacje, Web GUI i eksport PDF.

Najważniejsza wartość projektu polega na pokazaniu, jak lokalne modele AI można wykorzystać w praktycznym systemie odpowiadania na pytania, ale także jakie problemy trzeba rozwiązać: dobór modelu embeddingów, jakość retrievalu, odcinanie nieistotnego kontekstu i zarządzanie pamięcią GPU.

RAGDoctor pokazuje więc nie tylko działającą aplikację, ale też proces dochodzenia do lepszej jakości odpowiedzi w systemie RAG.

## Demo: konkretna ścieżka

Co uruchomić: 
1. LLMStudio z modelem Gemma 4 12B (przeładować model koniecznie)
2. Ollama z modelem bge-m3 (jest uruchomiona ollama list)
3. docker ps, żeby pokazać, że MongoDB działa, backend i frontend działają (jeśli jest czas, można pokazać logi backendu, że odbiera zapytania)
4. Baza MongoDB
5. Web GUI localhost:3000
6. Swagger localhost:8000/docs


1. Otwórz Web GUI.
2. Wpisz pytanie: „Angina, wirusowa czy bakteryjna?”.  To pytanie jest celowo nieprecyzyjne, żeby pokazać, że model musi znaleźć odpowiedni kontekst, a nie wymyślić odpowiedź z ogólnej wiedzy. Wysoke scory powinny mieć chunki o anginie, ale nie o grypie czy HIV.
   RNA-Wirusy? (odpowiedż z dwóch różnych źródeł)
   CRISPR-Cas9 (Brak konteksytu, tylko top zostaje, drugi został odcięty)
3. Pokaż, że odpowiedź jest wygenerowana naturalnym językiem.
4. Pokaż listę cytowanych chunków i ich score.
5. Powiedz: „Te fragmenty zostały wybrane przez retrieval i przekazane do modelu jako kontekst”.
6. Jeśli jest czas, pokaż eksport PDF jako funkcję uzupełniającą.

## Krótkie odpowiedzi na możliwe pytania komisji

### Czym RAGDoctor różni się od zwykłego chatbota?

Zwykły chatbot odpowiada głównie na podstawie wiedzy zapisanej w modelu. RAGDoctor najpierw wyszukuje fragmenty dokumentów, a dopiero potem przekazuje je modelowi jako kontekst. Dzięki temu odpowiedź jest związana z konkretnymi źródłami.

### Dlaczego projekt nie jest systemem diagnostycznym?

Bo nie analizuje stanu pacjenta, nie stawia diagnozy i nie rekomenduje leczenia. Odpowiada wyłącznie na pytania o treść wcześniej przygotowanych dokumentów.

### Dlaczego użyto MongoDB?

MongoDB przechowuje chunki, embeddingi i metadane w elastycznej strukturze dokumentowej. W lokalnym trybie similarity jest liczone po stronie aplikacji, więc MongoDB pełni głównie rolę magazynu danych RAG.

### Dlaczego samo cosine similarity nie wystarczyło?

Bo teksty medyczne mogą mieć podobne słownictwo mimo innego tematu. Dlatego system dodaje re-ranking leksykalny, dopasowanie tytułu, normalizację polskich form i cutoff słabego kontekstu.

### Dlaczego `bge-m3`?

Bo jest lokalnym modelem embeddingów lepiej pasującym do wielojęzycznych tekstów niż wcześniejsze rozwiązanie. Po jego wprowadzeniu trzeba ponownie zaindeksować dokumenty, ponieważ embeddingi muszą być spójne wymiarowo i modelowo.

### Po co LM Studio i Gemma 4 12B?

LM Studio pozwala lokalnie uruchomić model zgodny z API OpenAI. Gemma 4 12B daje silniejszy lokalny model generujący odpowiedzi, a praktyczne okno około 30K tokenów dobrze pasuje do dostępnej pamięci GPU.

### Co się dzieje, gdy GPU zabraknie pamięci?

Model w LM Studio może zająć większość VRAM. Jeśli PyTorch dostanie CUDA OOM podczas liczenia similarity, aplikacja czyści cache i powtarza obliczenie na CPU. System działa dalej, tylko potencjalnie wolniej.

### Jakie są dalsze kierunki rozwoju?

Najważniejsze kierunki to testy jakości retrievalu na zestawie pytań kontrolnych, porównanie modeli embeddingów, lepszy interfejs ingestu dokumentów, pełniejsze użycie vector search oraz mechanizmy bezpieczeństwa wymagane w środowisku produkcyjnym.


## Bezpieczne sformułowania

- „System odpowiada na podstawie wcześniej przygotowanego kontekstu”.
- „Projekt jest edukacyjnym prototypem RAG”.
- „Model generuje odpowiedź, ale materiał źródłowy pochodzi z zaindeksowanych dokumentów”.
- „Cytowane chunki pokazują, jakie fragmenty zostały użyte jako kontekst”.
- „Jakość odpowiedzi zależy od jakości dokumentów i retrievalu”.
