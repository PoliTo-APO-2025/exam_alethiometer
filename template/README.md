# Alethiometer
Scrivere un programma python che permetta di simulare l'utilizzo di un aletiometro (descritto in seguito).

I moduli e le classi vanno sviluppati nel package *alethiometer*.
Non spostare o rinominare moduli e classi esistenti e non modificare le signature dei metodi.

In *main.py* viene fornito del semplice codice, da voi modificabile, che testa le funzionalità base.
Esso mostra esempi di uso dei metodi principali dei controlli richiesti.

Tutte le eccezioni, se non altrimenti specificato, sono di tipo *InstrumentError* definito nel modulo *instrument*.


## R1: Simboli (6/19)
La classe *Alethiometer* nel modulo *instrument* rappresenta un aletiometro.
Lo strumento genera una sequenza di simboli che può essere tradotta in una frase, associando ogni simbolo a un concetto.
I simboli dell'aletiometro sono rappresentati su di una circonferenza (come i numeri di un orologio), e sono identificati univocamente dal loro nome.

Il metodo
```python
add_symbol(self, name: str, prev_name: Optional[str] = None) -> None
```
della classe *Alethiometer* permette di aggiunge un nuovo simbolo allo strumento.
Il metodo accetta come parametri, rispettivamente, il nome del simbolo da aggiungere e il nome del simbolo dopo il quale deve essere aggiunto (simbolo precedente).
Il nuovo simbolo andrà a posizionarsi fra il simbolo precedente e quello che prima si trovava dopo di esso.
Si assuma che quando viene inserito il primo simbolo il secondo parametro sia quello di default (```None```).

Se il simbolo precedente non è stato ancora definito, lanciare un'eccezione.

Il metodo
```python
get_next_symbol(self, name: str, steps: int = 1) -> str
```
della classe *Alethiometer* accetta come parametri il nome di un simbolo e un numero di passi.
Il metodo deve restituire il nome del simbolo che si raggiunge partendo dal simbolo indicato e spostandosi sulla circonferenza per il numero di passi specificato.
È possibile che sia necessario **PERCORRERE LA CIRCONFERENZA PIÙ VOLTE** prima di raggiungere il simbolo finale.
Se è presente **UN SOLO SIMBOLO**, ogni spostamento **RIPORTA AL SIMBOLO STESSO**.

Implementare il metodo
```python
__len__(self) -> int
```
della classe *Alethiometer* di modo che la "lunghezza" sia pari al numero di simboli contenuti dall'aletiometro.


## R2: Concetti (5/19)
Ogni concetto è identificato univocamente da un testo di una o più parole.

Il metodo
``` python
add_concepts(self, *texts: str) -> int
```
della classe *Alethiometer* permette di aggiungere uno o più concetti, passando i testi che li identificano come parametri.
Il metodo restituisce il numero di concetti aggiungi, scartando possibili concetti duplicati già aggiunti in precedenza.

Il metodo
```python
chain_concepts(self, text: str, *chained_texts: str) -> None
```
della classe *Alethiometer* permette di concatenare un concetto, il cui testo è passato come primo parametro, a diversi altri concetti (successivi), i cui testi sono passati come parametri successivi.
I collegamenti sono **DIREZIONALI**, dal concetto di partenza a ognuno di quelli successivi.
Se due concetti sono già stati concatenati in una data direzione, non concatenarli nuovamente.

Il metodo
```python
get_next_concepts(self, text: str) -> Set[str]
```
della classe *Alethiometer* accetta il testo di un concetto e restituisce un set contenente i testi dei concetti a esso successivi.


Il metodo
``` python
get_previous_concepts(self, text: str) -> Set[str]
```
della classe *Alethiometer* accetta il testo di un concetto e restituisce un set contenente i testi dei concetti a esso precedenti.


## R3: Associazioni (4/19)
Il metodo
```python
link_symbol_to_concept(self, symbol_name: str, concept_text: str) -> None
```
della classe *Alethiometer* permette di associare un simbolo a un concetto, passando come parametri il nome del simbolo e il testo del concetto.
Un concetto può essere collegato a più simboli, e un simbolo a più concetti.
L'associazione tra simboli e concetti è **INDIRETTA**.
Se l'associazione è già presente, il metodo **NON** deve far nulla.

Il metodo
```python
get_concepts_of_symbol(self, symbol_name: str, func: Callable[[str], bool] = None) -> Set[str]
```
della classe *Alethiometer* accetta come parametri il nome di un simbolo e una funzione.
Il metodo deve restituire un set contenente i testi dei concetti associati al simbolo, filtrandoli tramite la funzione passata come secondo parametro.
La funzione accetta come parametro il testo di un concetto e restituisce un valore booleano che indica se includerlo (true) o no (false).
Se il secondo parametro è **None** restituire i testi di tutti i concetti associati al simbolo.

Il metodo
```python
get_symbols_of_concept(self, text) -> List[Tuple[str, int]]
```
della classe *Alethiometer* accetta come parametro il testo di un concetto.
Esso restituisce una lista contente una tupla per ciascuno dei simboli a esso associati.
Il primo elemento di ogni tupla è il nome del simbolo, mentre il secondo è il numero di concetti associati a esso.
La lista deve essere ordinata in modo decrescente secondo il numero di concetti associati ai simboli (secondo elemento della tupla).

## R4: Traduzione (4/19)
Il metodo
```python
translation(self, symbol_names: List[str]) -> Optional[str]
```
della classe *Alethiometer* accetta come parametro un lista contenente una sequenza di nomi di simboli e restituisce la stringa corrispondente alla traduzione della sequenza.
La traduzione viene effettuata traducendo ogni simbolo della sequenza in un concetto, per poi unirne i testi (separandoli con uno spazio.)
Una traduzione è valida se si verificano le seguenti condizioni
1. un concetto può essere la traduzione di un simbolo della sequenza solo se i due sono associati.
2. considerando due simboli contigui nella sequenza, il concetto in cui viene tradotto il primo simbolo deve avere tra i sui concetti **SUCCESSIVI** il concetto in cui viene tradotto il secondo simbolo.

Se più traduzioni sono possibili, è indifferente quale viene restituita.
Per esempio, se la sequenza è di un solo simbolo, la traduzione è un testo qualsiasi dei concetti associati a esso.
Se nessuna traduzione è possibile per la sequenza fornita, il metodo deve restituire ```None```.
