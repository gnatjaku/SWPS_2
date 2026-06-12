# Colab notebooks: lokalne LLM, RAG, AnythingLLM/LM Studio workflow

Paczka zawiera komplet gotowych notebooków do uruchomienia w Google Colab.

## Pliki

1. `01_lokalny_llm_colab_qwen.ipynb`  
   Lokalny model LLM w Colabie: Qwen 0.5B Instruct, funkcja `ask_llm()`, klasyfikacja intencji.

2. `02_rag_tfidf_chromadb_colab.ipynb`  
   RAG krok po kroku: dokumenty, TF-IDF, embeddingi, ChromaDB, lokalny LLM jako generator odpowiedzi.

3. `03_workflow_router_training_colab.ipynb`  
   Workflow AI: router regułowy, mała sieć neuronowa `MLPClassifier`, opcjonalny router LLM.

4. `04_full_lesson_all_in_one_colab.ipynb`  
   Wersja kompletna w jednym notebooku, najlepsza do pokazania na zajęciach.

## Zalecane ustawienia Colab

Wybierz:

`Runtime → Change runtime type → T4 GPU`

Notebooki działają też na CPU, ale generowanie odpowiedzi przez LLM będzie wolniejsze.

## Uwaga o LM Studio

Colab nie widzi lokalnego `localhost` Twojego laptopa. Jeśli LM Studio działa u Ciebie lokalnie pod `http://localhost:1234/v1`, to Colab nie połączy się z tym adresem bez publicznego tunelu. Dlatego w notebookach pokazano odpowiednik lokalnego modelu uruchamiany bezpośrednio w środowisku Colaba.

## Kolejność na zajęciach

Najprościej:

1. Uruchom `04_full_lesson_all_in_one_colab.ipynb`.
2. Jeśli chcesz rozbić materiał na moduły, użyj notebooków 01, 02 i 03.

## Główna puenta dydaktyczna

RAG nie trenuje modelu. RAG dostarcza kontekst.  
Fine-tuning nie służy zwykle do aktualnej wiedzy.  
Workflow decyduje, kiedy użyć promptu, kiedy RAG-a, kiedy Pythona, a kiedy treningu.
