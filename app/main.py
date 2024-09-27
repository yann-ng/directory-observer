
import shutil
from pathlib import Path
import time

# watchdog imports
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

class Handler(PatternMatchingEventHandler):
    """ Manages whole work """
    def __init__(self, destination):
        """
        Args:
            destination(str): The directory where to copy files
        """
        self.destination = destination
        patterns = ["*.png", "*.jpg", "*.txt"] # extensions to observer
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        PatternMatchingEventHandler.__init__(self, 
                                                patterns=patterns, 
                                                ignore_patterns=ignore_patterns, 
                                                ignore_directories=ignore_directories, 
                                                case_sensitive=case_sensitive)
        self.t = time.strftime("%H:%M:%S", time.localtime())

    def on_created(self, event):
        """ What happen when a file is created """
        print("\n======File Created!(",self.t,")\nFile name:", event.src_path)
        shutil.copy2(event.src_path, self.destination)
        print("File Added to Target!")

    def on_modified(self, event):
        """ What happen when a file is modified """
        print("\n======File Modified!(",self.t,")\nFile name:", event.src_path)
        shutil.copy2(event.src_path, self.destination)
        print("File Copied to ./images!")

    def on_deleted(self, event):
        """ What happen when a file is deleted """
        pass

    def on_moved(self, event):
        """ What happen when a file is moved """
        pass

class Watch:
    """ Class responsible for launching Observation """
    def __init__(self, source, destination):
        """ 
        Args: 
            source(str): The directory to scan/observe
            destination(str): The directory where the file should be copy    
        """
        self.destination = destination
        self.source = source
        self.observer = Observer()

    def run(self):
        """ Responsible for launching the observation """
        event_handler = Handler(self.destination)
        self.observer.schedule(event_handler, self.source, recursive=False)
        self.observer.start()
        print("Observing...")
        try: 
            while True:
                time.sleep(3) 
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observation stopped!")
        self.observer.join()

if __name__ == "__main__":
    # TODO: Clear screen after valid directory.
    # TODO: Documentation -have to complete
    
    import sys
    try:
        source = sys.argv[1] # use the first argument as source directory
        # if an argument after source, store as destination
        # else current directory as destination
        destination = sys.argv[2] if len(sys.argv) > 2 else "."
        # Raise an error and close program if source and destination directory are the same
        if source == destination:
            raise SystemExit("[Error] Source and destination directories can't be the same.") 
    except IndexError:
        # Raise an error if atleast source directory is not specified
        raise SystemExit("Usage: %s <Directory_string>" %(sys.argv[0]))

    # Check if the source directory input is a directory 
    source_path = Path(source)
    if not (source_path.is_dir() or source == "."):
        print("The source directory seems not to exist")
        while True:
            source = input("Input a valid directory: ").strip()
            if source_path.is_dir() or source == ".": break
                
    # main job
    watch = Watch(source=source, destination=destination)
    watch.run()
