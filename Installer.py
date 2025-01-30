# Make sure each of the following imports are installed using PIP (PIP install os, PIP install subprocess, etc..)
import os
import subprocess
import speech_recognition as sr
import pyttsx3

class Installers: # This is the class for the module if you plan on importing it into a larger project
    def __init__(self, installer_dir):
        self.installer_dir = installer_dir
        self.installers = [
            'Google Chrome.exe', # Needs to be spelled the same as in the directory and include the '.exe' 
            '', # Add anpther program here, every program will need its own line and a comma after the second apostrophe
        ]

    def install_program(self, installer):
        installer_path = os.path.join(self.installer_dir, installer)
        if os.path.exists(installer_path):
            print(f"Installing {installer}...")
            try:
                subprocess.run(['powershell', '-Command', f'Start-Process "{installer_path}" -Verb RunAs'], check=True)
                print(f"{installer} installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {installer}. Error: {e}")
            except OSError as e:
                print(f"OS error: {e}")
        else:
            print(f"Installer {installer} not found in {self.installer_dir}.")

    def list_installers(self):
        print("Available installers:\n")
        for index, installer in enumerate(self.installers):
            print(f"{index + 1}: {installer}")
            print("=" * 30)  # Separator line

    def speak(self, text): # Change voice output settings here
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()

    def recognize_speech(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for your choice...")
            try:
                audio = recognizer.listen(source, timeout=5)  # Set a timeout for user input
                spoken_text = recognizer.recognize_google(audio)
                print(f"You said: {spoken_text}")
                return spoken_text.lower()
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start.")
                return None
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None

    def install_all(self):
        print("Installing all programs...")
        for installer in self.installers:
            self.install_program(installer)

    def install_selected(self):
        self.list_installers()
        self.speak("Would you like to install a program or install everything?") # What the program says before you choose the program(s)
        selected_input = self.recognize_speech()

        if selected_input:
            if selected_input == "install everything": # If you choose to install everything
                self.install_all()
            elif selected_input.isdigit():
                index = int(selected_input) - 1
                if 0 <= index < len(self.installers):
                    selected_installer = self.installers[index]
                    self.install_program(selected_installer)
                else:
                    print("Invalid number. Please enter a valid number from the list.")
            else:
                installer_names = [installer.lower() for installer in self.installers]
                if selected_input in installer_names:
                    self.install_program(self.installers[installer_names.index(selected_input)])
                else:
                    print("Invalid choice. Please enter a valid installer name or number from the list.")

if __name__ == "__main__":
    installer_dir = r'YOUR DIRECTORY HERE' # Input the directory of your files here
    installer = Installers(installer_dir)
    installer.install_selected()
