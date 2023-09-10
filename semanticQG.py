from allennlp.predictors.predictor import Predictor
import spacy
import contractions
import os

# Method that performs the input, segmenatation into sentences, and matching of the sentences against the pre-defined
# rules to generate questions and output them to a file: 
def generateQuestions(predictor, nlp, transcriptFileName):
    sentences = [] # Stores all the sentences in the transcript
    transcript = open(transcriptFileName + ".txt") # Reads in the transcript
    output = open(transcriptFileName + 'SemanticQuestions.txt','w') # File to which output questions (and the sentences used) are written
    text = transcript.read() # Read all the text into one string
    text = contractions.fix(text) # Remove contractions (these can mess up the SRL)
    doc = nlp(text) # Used to split the text into sentences

    # Intilialise some variables for coverage statistics
    totalSentences = 0
    numSentences = 0
    numQuestions = 0
    
    # Loop through the sentences filtering out blank lines and start/end labels
    for sent in doc.sents:
        totalSentences += 1
        sent = str(sent).replace("\n"," ")
        sent = str(sent).replace("[MUSIC]","")
        sent = str(sent).replace("[SOUND]","")
        sentences.append(sent) 

    # Loop through the sentences and run the SRL Model on them
    for sent in sentences:
        questions = []  # Stores the generated questions for this sentence 
        result = predictor.predict(sent) # Run the SRL Model
        tagDict = {} # Will store the SRL tags and phrases
        
        # Loop through the output and reformat it to better meet the programs needs
        # Format of TagDict = {verb1: [{SRL Tag: phrase}, {SRL Tag: phrase},...], verb2: [{SRL Tag: phrase}, {SRL Tag: phrase},...],...}
        for verbs in result['verbs']:
            verb = verbs['verb']
            description = verbs['description'] 
            tagDict[verb] = []
            for i in description:
                if i == '[':
                    tag = description[description.find('[')+1:description.find(':')]
                    word = description[description.find(':')+1:description.find(']')]
                    description = description[description.find(']')+1::]
                    arr = tagDict[verb]
                    arr.append({tag:word})
                    tagDict[verb] = arr

       
        # Loop through each list of the tagDict (each list corresponds to a different verb)
        # For each list extract the keys (SRL Tag) and values (Phrases) into parallel lists    
        for list in tagDict.values():
            keys = []
            values = []
            # Append each of these phrases and keys into a parallel list
            for dict in list:
                for key in dict.keys():
                    keys.append(key)
                    values.append(dict[key])
            
            # Check if the keys in the sentences match any of the QG rules
            #################### WHY RULES #########################      
            if (('V' in keys) and ('ARG0' in keys) and ('ARGM-PRP' in keys) and ('ARG1' in keys) and ('ARGM-MOD' in keys)):
                verb = values[keys.index('V')]
                arg0 = values[keys.index('ARG0')]
                arg1 = values[keys.index('ARG1')]
                argMOD = values[keys.index('ARGM-MOD')]
                argPRP = values[keys.index('ARGM-PRP')]
                question = "Why" + argMOD + arg0 + verb + arg1 + '?' # PRP (Purpose) is the answer
                questions.append("Question: " + question + '\n')   
            
            if (('V' in keys) and ('ARG0' in keys) and ('ARGM-CAU' in keys) and ('ARG1' in keys) and ('ARGM-MOD' in keys)):
                verb = values[keys.index('V')]
                arg0 = values[keys.index('ARG0')]
                arg1 = values[keys.index('ARG1')]
                argMOD = values[keys.index('ARGM-MOD')]
                argCAU = values[keys.index('ARGM-CAU')]
                question = "Why" + argMOD + arg0 + verb + arg1 + '?' # CAU (CAU) is the answer
                questions.append("Question: " + question + '\n')
            
            #################### WHAT RULES #########################
            if (('V' in keys) and ('ARG0' in keys) and ('ARGM-MOD' in keys) and ('ARGM-PRP' in keys) and ('ARG1' in keys)):
                verb = values[keys.index('V')]
                arg0 = values[keys.index('ARG0')]
                arg1 = values[keys.index('ARG1')]
                argPRP = values[keys.index('ARGM-PRP')]
                argMOD = values[keys.index('ARGM-MOD')]
                question = "What" + argMOD + arg0 + verb + argPRP + '?' # arg1 is the answer
                questions.append("Question: " + question + '\n')
                
            if (('V' in keys) and ('ARG0' in keys) and ('ARGM-MOD' in keys) and ('ARGM-CAU' in keys) and ('ARG1' in keys)):
                verb = values[keys.index('V')]
                arg0 = values[keys.index('ARG0')]
                arg1 = values[keys.index('ARG1')]
                argCAU = values[keys.index('ARGM-CAU')]
                argMOD = values[keys.index('ARGM-MOD')]
                question = "What" + argMOD + arg0 + verb + argCAU + '?' # arg1 is the answer
                questions.append("Question: " + question + '\n')
                
            if (('V' in keys) and ('ARG0' in keys) and ('ARGM-EXT' in keys) and ('ARG1' in keys) and ('ARGM-MOD' in keys)):
                verb = values[keys.index('V')]
                arg0 = values[keys.index('ARG0')]
                arg1 = values[keys.index('ARG1')]
                argEXT = values[keys.index('ARGM-EXT')]
                argMOD = values[keys.index('ARGM-MOD')]
                question = "To what extent" + argMOD  + arg0 + verb + arg1 + '?' # argEXT (Extent) is the answer
                questions.append("Question: " + question + '\n')
                
                
            #################### HOW RULES #########################
            if (('V' in keys) and ('ARG0' in keys) and ('ARGM-MNR' in keys) and ('ARG1' in keys) and ('ARGM-MOD' in keys)):
                verb = values[keys.index('V')]
                arg0 = values[keys.index('ARG0')]
                arg1 = values[keys.index('ARG1')]
                argMNR = values[keys.index('ARGM-MNR')]
                argMOD = values[keys.index('ARGM-MOD')]
                question = "How" + argMOD + arg0 + verb + arg1 +'?' # MNR (Manner) is the answer
                questions.append("Question: " + question + '\n')
                
            if (('V' in keys) and ('ARG0' in keys) and ('ARGM-ADV' in keys) and ('ARG1' in keys) and ('ARGM-MOD' in keys)):
                verb = values[keys.index('V')]
                arg0 = values[keys.index('ARG0')]
                arg1 = values[keys.index('ARG1')]
                argADV = values[keys.index('ARGM-ADV')]
                argMOD = values[keys.index('ARGM-MOD')]
                question = "How" + argMOD + arg0 + verb + arg1 +'?' # ADV (Adverb) is the answer
                questions.append("Question: " + question + '\n')
                
                
            #################### WHEN RULES #########################
            if (('V' in keys) and ('ARG0' in keys) and ('ARGM-TMP' in keys) and ('ARG1' in keys) and ('ARGM-MOD' in keys)):
                argTMP = values[keys.index('ARGM-TMP')].strip()
                
                # Extra logic to prevent the generation of "when" questions if the argTMP phrase is a certain value
                if argTMP.lower() != "then" and argTMP.lower() != "now" and argTMP.lower() != "before" and argTMP.lower() != "after" and argTMP.lower() != "again" and argTMP.lower() != "eventually":  
                    verb = values[keys.index('V')]
                    arg0 = values[keys.index('ARG0')]
                    arg1 = values[keys.index('ARG1')]
                    argMOD = values[keys.index('ARGM-MOD')]
                    question = "When" + argMOD + arg0 + verb + arg1 +'?' # TMP (Temporal) is the answer
                    questions.append("Question: " + question + '\n')
                 
        # If there are questions, write them to the output file as well as the sentence from which they were derived    
        if len(questions) != 0:
            numSentences += 1
            output.write("--------------------------" + '\n')
            sent = sent.strip()
            output.write("Sentence: "+ sent + '\n')
            for question in questions:
                numQuestions +=1
                output.write(question)
                
    # Display stats about the generated questions
    print("Total Sentences:", totalSentences)
    print("Generated" , numQuestions, "questions from", numSentences, "of the sentences.")
    
    # Close the input and output file
    transcript.close()
    output.close()

if __name__ == "__main__":
    # Initialise the SRL predictor and SpaCy models
    predictor = Predictor.from_path("structured-prediction-srl-bert.2020.12.15.tar.gz")
    nlp = spacy.load("en_core_web_sm")
    userInput = ""
    
    # Input Loop: Ask user for file name to generate questions from
    # contains basic check to see if file exists
    while True:
        userInput = input('Enter Content File Name (type "stop" to close the program): ')
        if userInput.upper() == "STOP":
            break
        if os.path.isfile(userInput + ".txt"):
            print("Generating Questions...")
            generateQuestions(predictor, nlp, userInput)
            print("Questions Saved to: " + userInput + "SemanticQuestions.txt")
        else:
            print("File Not Found.\nPlease enter the name of a valid .txt file (excluding the .txt extension).")
            continue
    

    
    


    
    


    
        
        

    



