Installation and Setup:

- Ensure you are using Python version 3.9

- On Windows and Linux to install the required libraries perform the following steps:
    1) Run the command: "pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html"
    -  NOTE: It is VITAL that the "-f https://download.pytorch.org/whl/torch_stable.html" is included in the command.
    2) After the packages have been installed run the command: "python3 -m spacy download en_core_web_sm"
    - This will download the english package for Spacy.

- On Mac to install the required libraries perform the following steps:
    1) Alter the requirements.txt file by removing the "+cpu" from torch and torchvision.
    2) Run the command: "pip install -r requirements.txt"
    3) After the libraries have been installed run the command: "python3 -m spacy download en_core_web_sm"
    - This will download the english package for Spacy.

- Fixes to some common erors:
    - Pip can not find "torch version 1.7.1" package:
        - Make sure that Python version 3.9 is being used.
        - This can be done using "python3.9 -m pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html"
        - Or using the actual path to the the python 3.9 installation: "/usr/bin/python3.9 -m pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html"

    - Error when building wheel for jsonnet:
        - Install the python dev tools for python3.9 with the command: "sudo apt-get install python3.9-dev"


Descriptions of Included Folders/Files:

- "Transcripts" : A folder that contains 12 weeks of lecture transcripts, each in a different folder corresponding the week.
- "Sample Questions" : A folder that contains the 12 weeks of questions related to transcripts. Along with a merged and cleaned version of the all the questions in seperate .txt files.
- "Evaluation Data": A folder than contains the excel files with the results of the survey and internal evaluation.
- "semanticQG.py" : A Python script that contains the Semantic QG system.
- "templateQG.py" : A Python script that contains the Template QG system.
- "requirements.txt" : A text file containing the names and versions of the required libraries.
- "demoContent.txt" : A text file containing an example of a lecture transcript that can be used for testing/demo.
- "structured-prediction-srl-bert.2020.12.15.tar.gz" : The model from AllenNLP that performs the SRL.
- "allQuestions.txt" : A file containing 594 questions that have been cleaned and extracted from the dataset.
- "validQuestions.txt" A file containing the 81 questions from which valid templates were extracted.
- NOTE: The "validQuestions.txt" file can be used to quickly run the program for testing/demo.
- NOTE: However, due to the clustering the output will be different to that evalauted in the report.


Required Format of the Input Files:

- NOTE: All input files should be placed at the same level as the Python scripts.

- Content File:
    - This is the file that contains the text from which questions will be generated.
    - This can be any passage of text.
    - The text can be of any resonable length (longer text = longer to generate questions)
    - It can contain multiple paragraphs.
    - The format can be seen in "demoContent.txt"

- Sample Questions File:
    - The is the file containing the sample questions from which templates are extracted.
    - The file should contain each question on a new line.
    - The format can be seen in "allQuestions.txt" and "validQuestions.txt"
    

How to Run the Semantic QG System:

- NOTE: If the "structured-prediction-srl-bert.2020.12.15.tar.gz" model is not already downloaded (i.e.: not at same level as the "semanticQG.py" script):
    - Comment out line 166.
    - Uncomment line 167.
    - This will download the model when the program is executed.
    - However, this will require the model to re-downloaded every time the program is run.
    - Thus, the model can be manually be downloaded from: "https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz"
    - After downlading, place the model at the same level as the semanticQG.py script.

- The code for the semantic QG system is found within "semanticQG.py"
- The program can be executed by running "python3 semanticQG.py"
- Once executed the program will begin by loading in the SRL model (this can take a few seconds).
- NOTE: If running on Windows, an error will be displayed in the console. This can be ignored.
- On the first time running the code it may automatically install an NLTK Wordnet package.
- Once the model is loaded you will be prompted to enter the name of a text file from which you want questions to be generated.
- The file should be placed at the same level as the "semanticQG.py" script.
- You should enter the file name EXCLUDING the ".txt" extension (i.e.: demoContent NOT demoContent.txt).
- If the file CANNOT be found, an error message be presented.
- If the file CAN be found, the system will begin to generate questions.
- Upon completion, some statistics regarding the amount generated questions will be displayed in the terminal.
- The generated questions will be output to a file with the same name as the input file with the suffix "SemanticQuestions"
- i.e.: If the input file was "demoContent.txt" the output file will be "demoContentSemanticQuestions.txt"
- This output file will contain the sentence followed by the question/s generated from it by the system.
- To terminate the program you can simply type "stop"


How to Run the Template QG System:

- NOTE: If the "structured-prediction-srl-bert.2020.12.15.tar.gz" model is not already downloaded (i.e.: not at same level as the "semanticQG.py" script):
    - Comment out line 166.
    - Uncomment line 167.
    - This will download the model when the program is executed.
    - However, this will require the model to re-downloaded every time the program is run.
    - Thus, the model can manually be downloaded from: "https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz"
    - After downlading, place the model at the same level as the semanticQG.py script.

- The code for the Template QG system is found within "templateQG.py"
- The program can be executed by running "python3 templateQG.py"
- Once executed the program will begin by loading in the SRL model (this can take a few seconds)
- On the first time running the code it may automatically install an NLTK Wordnet package.
- NOTE: If running on Windows, an error will be displayed in the console. This can be ignored.
- Once the model is loaded the program will request the name of the file containing the sample questions.
- These sample questions are the questions used to extract templates (The format of the file is explained above).
- You should enter the name of the file containing the questions EXCLUDING the ".txt" extension (i.e.: allQuestions NOT allQuestions.txt)
- The file should be placed at the same level as the "templateQG.py" script.
- If the file CANNOT be found, an error message be presented.
- If the file CAN be found, the system will beging to cluster and extract templates from the questions.
- This can take some time depending on the amount of questions.
- Once completed, the system will display the number of templates extracted.
- Two files will also be created: one with the suffix "Clustered" and another with the suffix "TemplatesClustered"
- e.g.: If the input file was called "allQuestions.txt": 
    - "allQuestionsClustered.txt" : Would contain all the sample questions listed in their respective clusters.
    - "allQuestionsTemplatesClustered.txt" : Would contain the extracted templates in their respective clusters.
- NOTE: The templates in this file will only be the valid templates that have met the extraction criteria.
- After template extaction you will be prompted to enter the name of a text file from which you want questions to be generated.
- You should enter the file name EXCLUDING the ".txt" extension (i.e.: demoContent NOT demoContent.txt).
- The file should be placed at the same level as the "templateQG.py" script.
- If the file CANNOT be found, an error message be presented.
- If the file CAN be found, the system will begin to generate questions.
- Upon completion, some statistics regarding the generated questions will be displayed in the terminal.
- The generated questions will be output to a file with the same name as the input file with the suffix "TemplateQuestions"
- i.e.: If the input file was "demoContent.txt" the output file will be "demoContentTemplateQuestions.txt"
- This output file will contain the sentence followed by the question/s generated from it by the system, as well as the template used.
- To terminate the program you can simply type the "stop"











