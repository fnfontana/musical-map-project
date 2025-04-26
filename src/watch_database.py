import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
from monitoring.events import bus

# Caminho do banco de dados
DB_PATH = os.path.join('data', 'musical_map.db')

class DatabaseChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(DB_PATH):
            print("Alteração detectada no banco de dados.")
            bus.emit('database_modified', path=event.src_path)

# Handler de exemplo: atualizar o mapa ao modificar o banco
def update_map_on_db_change(path):
    print(f"[EVENTO] database_modified - Atualizando o mapa devido à alteração em: {path}")
    subprocess.run(['python', 'src/main.py'])

bus.subscribe('database_modified', update_map_on_db_change)

if __name__ == "__main__":
    event_handler = DatabaseChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(DB_PATH), recursive=False)
    print("Monitorando alterações no banco de dados...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()