from typing import Set, Optional, Callable, Tuple, List


class InstrumentError(Exception):
    pass


class Symbol:
    def __init__(self, name):
        self._name = name
        self._previous = None
        self._next = None
        self._concepts = set()
    
    @property
    def name(self):
        return self._name

    @property
    def next(self):
        return self._next
    
    @next.setter
    def next(self, val):
        self._next = val

    def link_concept(self, concept):
        self._concepts.add(concept)

    @property
    def concepts(self):
        return self._concepts


class Concept:
    def __init__(self, text):
        self._text = text
        self._children = set()
        self._parents = set()
        self._symbols = set()
    
    @property
    def text(self):
        return self._text

    @property
    def children(self):
        return self._children
    
    @property
    def parents(self):
        return self._parents
    
    def add_child(self, concept):
        self._children.add(concept)
    
    def add_parent(self, concept):
        self._parents.add(concept)

    def link_symbol(self, symbol):
        self._symbols.add(symbol)

    @property
    def symbols(self):
        return self._symbols


class Alethiometer:
    def __init__(self):
        self._symbols = {}
        self._concepts = {}

    # R1
    def __len__(self) -> int:
        return len(self._symbols)

    def add_symbol(self, name: str, prev_name: Optional[str] = None) -> None:
        sym = Symbol(name)
        if prev_name is not None:
            if prev_name not in self._symbols:
                raise InstrumentError("Previous not defined")
            prev = self._symbols[prev_name]
            sym.next = prev.next
            prev.next = sym
        else:
            sym.next = sym
        self._symbols[name] = sym

    def get_next_symbol(self, name: str, steps: int = 1) -> str:
        sym = self._symbols[name]
        for _ in range(steps):
            sym = sym.next
        return sym.name    

    # R2
    def add_concepts(self, *texts: str) -> int:
        count = 0
        for text in texts:
            if text not in self._concepts:
                self._concepts[text] = Concept(text)
                count += 1
        return count

    def chain_concepts(self, text: str, *chained_texts: str) -> None:
        base_concept = self._concepts[text]
        for c_text in chained_texts:
            concept = self._concepts[c_text]
            base_concept.add_child(concept)
            concept.add_parent(base_concept)

    def get_next_concepts(self, text: str) -> Set[str]:
        return {c.text for c in self._concepts[text].children}
    
    def get_previous_concepts(self, text: str) -> Set[str]:
        return {c.text for c in self._concepts[text].parents}
    
    # R3
    def link_symbol_to_concept(self, symbol_name: str, concept_text: str) -> None:
        symbol = self._symbols[symbol_name]
        concept = self._concepts[concept_text]
        symbol.link_concept(concept)
        concept.link_symbol(symbol)
    
    def get_concepts_of_symbol(self, symbol_name: str, func: Callable[[str], bool] = None) -> Set[str]:
        concepts = {c.text for c in self._symbols[symbol_name].concepts}
        concepts = {c for c in concepts if func(c)} if func else concepts
        return concepts

    def get_symbols_of_concept(self, text) -> List[Tuple[str, int]]:
        return list(
            sorted(
                map(lambda s: (s.name, len(s.concepts)), self._concepts[text].symbols),
                key=lambda x: x[1],
                reverse=True
            )
        )
    
    # R4
    def translation(self, symbol_names: List[str]) -> Optional[str]:
        symbols = [self._symbols[name] for name in symbol_names]
        sentence = []
        if self._depth_search(symbols, sentence):
            return " ".join(sentence)
        return None
    
    def _depth_search(self, symbols, sentence, chained=None):
        if not symbols:
            return True
        symbol_concepts = symbols[0].concepts
        concepts = symbol_concepts.intersection(chained) if chained is not None else symbol_concepts

        for concept in concepts:
            sentence.append(concept.text)
            if self._depth_search(symbols[1:], sentence, concept.children):
                return True
            sentence.pop()
        return False
    