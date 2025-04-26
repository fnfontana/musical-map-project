import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
from monitoring.events import bus

INPUT_DIR = os.path.join('input')

class InputChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith('.csv'):
            print(f"Novo arquivo CSV detectado: {event.src_path}")
            bus.emit('input_file_modified', path=event.src_path)
    def on_modified(self, event):
        if event.src_path.endswith('.csv'):
            print(f"Arquivo CSV modificado: {event.src_path}")
            bus.emit('input_file_modified', path=event.src_path)

def repopulate_database_on_input_change(path):
    print(f"[EVENTO] input_file_modified - Repopulando banco devido a alteração em: {path}")
    subprocess.run(['python', 'src/populate_database.py'])

bus.subscribe('input_file_modified', repopulate_database_on_input_change)

if __name__ == "__main__":
    event_handler = InputChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=INPUT_DIR, recursive=False)
    print("Monitorando alterações na pasta de entrada (input/)...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
