import sys
import os
# Garante que a raiz do projeto está no sys.path para todos os contextos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from monitoring.events import EventBus

def test_eventbus_emit_and_subscribe():
    bus = EventBus()
    result = []
    def handler(data):
        result.append(data)
    bus.subscribe('teste', handler)
    bus.emit('teste', 42)
    assert result == [42]
