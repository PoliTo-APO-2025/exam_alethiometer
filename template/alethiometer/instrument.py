from typing import Set, Optional, Callable, Tuple, List


class InstrumentError(Exception):
    pass


class Alethiometer:
    def __init__(self):
        pass

    # R1
    def __len__(self) -> int:
        pass

    def add_symbol(self, name: str, prev_name: Optional[str] = None) -> None:
        pass

    def get_next_symbol(self, name: str, steps: int = 1) -> str:
        pass   

    # R2
    def add_concepts(self, *texts: str) -> int:
        pass

    def chain_concepts(self, text: str, *chained_texts: str) -> None:
        pass

    def get_next_concepts(self, text: str) -> Set[str]:
        pass
    
    def get_previous_concepts(self, text: str) -> Set[str]:
        pass
    
    # R3
    def link_symbol_to_concept(self, symbol_name: str, concept_text: str) -> None:
        pass
    
    def get_concepts_of_symbol(self, symbol_name: str, func: Callable[[str], bool] = None) -> Set[str]:
        pass

    def get_symbols_of_concept(self, text) -> List[Tuple[str, int]]:
        pass
    
    # R4
    def translation(self, symbol_names: List[str]) -> Optional[str]:
        pass
    