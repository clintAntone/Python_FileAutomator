#This is a file automation tool using Python

#If you don't have the below modules you can first install them using the below codes.
#pip3 install pytest-shutil
#pip3 install python-time
#pip3 install watchdog

from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import logging

#First we need to define the below variables
#These folders must exist
source_dir = "/Users/COLLABERA/Downloads"
dest_dir_sfx = "/Users/COLLABERA/Downloads/Downloaded Sound"
dest_dir_music = "/Users/COLLABERA/Downloads/Downloaded Music"
dest_dir_video = "/Users/COLLABERA/Downloads/Downloaded Video"
dest_dir_image = "/Users/COLLABERA/Downloads/Downloaded Image"
dest_dir_installer = "/Users/COLLABERA/Downloads/Applications"
dest_dir_documents = "/Users/COLLABERA/Downloads/Downloaded Documents"
dest_dir_bash = "/Users/COLLABERA/Downloads/Bash"

#Next we will define the supported extension types of the files in the source directory
#Feel free to add additional extension names you wanted to be included
audio_extensions = [".m4a",".mp3",".wav",".wma",".aac"]
installer_extensions = [".exe",".msi",".apk"]
image_extensions = [".jpg",".jpeg",".jpe",".png",".gif",".webp",".psd",".svg",".eps",".ico"]
video_extensions = [".webm",".mpg",".mp2",".mpeg",".mpe",".ogg",".mp4",".mp4v",".m4v",".avi",".wmv",".mov",".flv"]
document_extensions = [".doc",".docx",".pub",".odt",".pdf",".xls",".xlsx",".ppt",".pptx",".txt",".csv",".json",".zip",".json"]
script_extensions = [".sh",".py"]


#Now we will create a function to check if the file that we wanted to move is unique
def make_unique(dest, name):
  filename, extension = splitext(name)
  counter = 1
  #If the file exists, we will be adding number to the end of the filename
  while exists(f"{dest}/{name}"):
    name = f"{filename}({str(counter)}){extension}"
    counter += 1
  
  return name

#This function will be the one responsible for moving the file to the selected directory
def move_file(dest, entry, name):
  if exists(f"{dest}/{name}"):
    unique_name = make_unique(dest, name)
    oldName = join(dest, name)
    newName = join(dest, unique_name)
    rename(oldName, newName)
  move(entry, dest)

#Now, we will be creating an event handler to move the files to the new folders that we specified
#If there will be changes in the source directory, this handler will be executed
class MoverHandler(FileSystemEventHandler):

  def on_modified(self, event):
    #This will loop into the source directory and insert all filenames to the variable entries
    with scandir(source_dir) as entries:
      for entry in entries:
        name = entry.name
        self.check_audio_files(entry, name)
        self.check_video_files(entry, name)
        self.check_image_files(entry, name)
        self.check_document_files(entry, name)
        self.check_installer_files(entry, name)
        self.check_script_files(entry, name)

  #This will loop to every extensions that you have provided
  #check if the name in the parameters contains the extension in the loop
  def check_audio_files(self, entry, name):
    for audio_extension in audio_extensions:
      if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
        if entry.stat().st_size < 10_000_000 or "SFX" in name:
          dest = dest_dir_sfx
        else:
          dest = dest_dir_music
        move_file(dest, entry, name)
        logging.info(f"Moved audio file: {name}")

  def check_video_files(self, entry, name):
    for video_extension in video_extensions:
      if name.endswith(video_extension) or name.endswith(video_extension.upper()):
        move_file(dest_dir_video, entry, name)
        logging.info(f"Moved video file: {name}")

  def check_image_files(self, entry, name):
    for image_extension in image_extensions:
      if name.endswith(image_extension) or name.endswith(image_extension.upper()):
        move_file(dest_dir_image, entry, name)
        logging.info(f"Moved image file: {name}")

  def check_document_files(self, entry, name):
    for document_extension in document_extensions:
      if name.endswith(document_extension) or name.endswith(document_extension.upper()):
        move_file(dest_dir_documents, entry, name)
        logging.info(f"Moved document file: {name}")

  def check_installer_files(self, entry, name):
    for installer_extension in installer_extensions:
      if name.endswith(installer_extension) or name.endswith(installer_extension.upper()):
        move_file(dest_dir_installer, entry, name)
        logging.info(f"Moved installer file: {name}")

  def check_script_files(self, entry, name):
    for script_extension in script_extensions:
      if name.endswith(script_extension) or name.endswith(script_extension.upper()):
        move_file(dest_dir_bash, entry, name)
        logging.info(f"Moved script file: {name}")

#Now we will create the main
#In this main method, we have defined the path on where our automator will look into
#what will be the event handler to use/perform
#we also provided the logging format
if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')
  path = source_dir
  event_handler = MoverHandler()
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:
    while True:
      sleep(10)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()


##Currently, our Python program is running in the background
##I will not interrupt anymore, as I want my files to be organized :)
##That's all, and have a great day.