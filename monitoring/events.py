# events.py
"""
Módulo de sistema de eventos para arquitetura orientada a eventos.
Permite registrar handlers e emitir eventos de forma assíncrona ou síncrona.
"""
from collections import defaultdict
from typing import Callable, Dict, List, Any

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable):
        """Registra um handler para um tipo de evento."""
        self._handlers[event_type].append(handler)

    def emit(self, event_type: str, *args, **kwargs):
        """Dispara um evento para todos os handlers registrados."""
        for handler in self._handlers[event_type]:
            handler(*args, **kwargs)

# Instância global do EventBus
bus = EventBus()
