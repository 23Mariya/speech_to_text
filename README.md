# Speech-to-Text Project

This project is a **Speech-to-Text** application that converts spoken language into written text using a variety of speech recognition models. It allows users to upload audio files or use a microphone to convert speech into text, which can then be processed or saved as a text file.

## Features

- **Speech-to-Text**: Converts speech from audio files or real-time microphone input to text.
- **Support for Multiple Audio Formats**: Supports various audio file formats for conversion.
- **Real-time Processing**: Option to use the microphone for real-time speech conversion.
- **High Accuracy**: Uses advanced speech recognition models like OpenAI Whisper for high accuracy.

## Installation

To run this project locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/23Mariya/speech_to_text.git

2. Navigate to the Project Folder
   cd speech_to_text

3. Create and Activate a Virtual Environment (Optional but Recommended)
   For Windows:
   python -m venv venv
   .\venv\Scripts\activate

   For macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

4. Install Dependencies
   pip install -r requirements.txt

5. Run the Application
   python app.py

Using the Microphone
To convert real-time speech to text, make sure you have a working microphone. Run the application and start speaking.

Using Audio Files
You can upload an audio file for conversion by placing it in the project folder or providing the file path in the input.

Contributing
Feel free to fork this repository, open issues, and submit pull requests. Contributions are welcome!

Acknowledgements
OpenAI Whisper: For providing an advanced speech recognition model used in this project.