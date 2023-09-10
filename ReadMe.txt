Installing the Required Packages:

- The required packages can be insalled with the command: 
-"pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html"
- NOTE: It is VITAL that the "-f https://download.pytorch.org/whl/torch_stable.html" is included in the command.
- NOTE: Some messages regarding conflicting versions allenNLP and Spacy may be displayed. These can be ignored.


Descriptions of Included Folders/Files:
- "Transcripts" : A folder that contains 12 weeks of lecture transcripts, each in a different folder corresponding the week.
- "Sample Questions" : A folder that contains the 12 weeks of questions related to transcripts. Along with a merged and cleaned version of the all the questions a single .txt file
- "semanticQG.py" : A Python script that contains the semantic QG system.
- "templateQG.py" : A Python script that containn the tempalte QG system.
- "requirements.txt" : A text file containing the names and versions of the required libraries.
- "demoContent.txt" : A text file containing an example of a lecture transcript that can be used for testing/demo.
- "structured-prediction-srl-bert.2020.12.15.tar.gz" : The model from AllenNLP that performs the SRL.
- "allQuestions.txt" : A file containing 594 questions that have been cleaned and extracted from the dataset.
- "validQuestions.txt" A file containing the 81 questions from which valid templates were extracted.
- NOTE: The "validQuestions.txt" file can be used to quickly run the program for testing/demo.
- NOTE: However due to the clustering the output will be different to that evalauted in the report.


Required Format of the Input Files:

- The input file containing the content, from which questions are generated, can be any passage of text.
- The text can be of any resonable length (longer text = longer to generate)
- It can contain multiple paragraphs.
- The input file containing the sample questions from which templates are extracted should contain each questions on a new line.
- Examples of the structure of both these files can be seen with "demoContent.txt" and "allQuestions.txt" respectively


How to Run Semantic QG System:

- The code for the semantic QG system is found within "semanticQG.py"
- The program can be executed by running "python3 semanticQG.py"
- Once executed the program will begin by loading in the SRL model (this can take a few seconds).
- NOTE: If running on Windows, an error will be displayed in the console. This can be ignored.
- Once the model is loaded you will be prompted to enter the name of a text file from which you want questions to be generated.
- You should enter the file name EXCLUDING the ".txt" extension (i.e.: demoContent NOT demoContent.txt).
- If the file CANNOT be found, an error message be presented.
- If the file CAN be found, the system will begin to generate questions.
- Upon completion, some statistics regarding the amount generated questions will be displayed in the terminal.
- The generated questions will be output to a file with the same name as the input file with the suffix "SemanticQuestions"
- i.e.: If the input file was "demoContent.txt" the output file will be "demoContentSemanticQuestions.txt"
- This output file will contain the sentence followed by the question/s generated from it by the system.
- To terminate the program you can simply type "stop"


How to Run the Template QG System:

- The code for the Template QG system is found within "templateQG.py"
- The program can be executed by running "python3 templateQG.py"
- Once executed the program will begin by loading in the SRL model (this can take a few seconds)
- NOTE: If running on Windows, an error will be displayed in the console. This can be ignored.
- Once the model is loaded the program will request the name of the file containg the sample questions.
- These sample questions are the questions used to extract templates (The format of the file is explained above).
- You should enter the name of the file containing the questions EXCLUDING the ".txt" extension (i.e.: allQuestions NOT allQuestions.txt)
- If the file CANNOT be found, an error message be presented.
- If the file CAN be found, the system will beging to cluster and extract templates from the questions.
- This can take some time depending on the amount of questions.
- Once completed, the system will display the number of templates extracted.
- Two files will also be created: one with the suffix "Clustered" and another with the suffix "TemplatesClustered"
- e.g.: If the input file was called "allQuestions.txt": 
- "allQuestionsClustered.txt" : Would contain all the questions listed in their respective clusters.
- "allQuestionsTemplatesClustered.txt" : Would contain the extracted templates in their respective clusters.
- NOTE: The templates in this file will only be the valid templates that have met the extraction criteria.
- After template extaction you will be prompted to enter the name of a text file from which you want questions to be generated.
- You should enter the file name EXCLUDING the ".txt" extension (i.e.: demoContent NOT demoContent.txt).
- If the file CANNOT be found, an error message be presented.
- If the file CAN be found, the system will begin to generate questions.
- Upon completion, some statistics regarding the generated questions will be displayed in the terminal.
- The generated questions will be output to a file with the same name as the input file with the suffix "TemplateQuestions"
- i.e.: If the input file was "demoContent.txt" the output file will be "demoContentTemplateQuestions.txt"
- This output file will contain the sentence followed by the question/s generated from it by the system, as well as the template used.
- To terminate the program you can simply type the "stop"











