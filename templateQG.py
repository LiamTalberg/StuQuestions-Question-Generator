from allennlp.predictors.predictor import Predictor
import spacy
import contractions
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import os

# Method takes in: 
# the ClusteredQuestions dictonary which contains lists of questions (the value) assosiated with a cluster (the key)
# a fileName (used to create the output files for the templates) 
# and the predictor (the SRL model)
# Using these inputs it returns: 
# the valid templates in a dictionary of the same structure as ClusteredQuestions
# the valid templates a singular list
# writes the outputs to the file: questionsFileNameTemplatesClustered.txt
def extractTemplates(clusteredQuestions, questionsFileName, predictor):

    clusteredTemplates = {} # {Cluster1: [t1,t2,t3,...], Cluster2: [t1,t2,t3,...]...."}
    keyCount = -1 # Used to generate clusterIDs
    templates = [] # Stores the created templates
    
    # Extract each list of clustered sample questions
    for questions in clusteredQuestions.values():
        keyCount +=1
        clusteredTemplates[keyCount] = [] # Create new entry in dictionary
        question = ""
        
        # Read in the questions and run the SRL model on them
        for question in questions:
            question = str(question)
            result = predictor.predict(question)
            tagDict = {} # {verb1: [{SRL Tag: phrase}, {SRL Tag: phrase},...], verb2: [{SRL Tag: phrase}, {SRL Tag: phrase},...],...}
            # Store the SRL labels in Tag Dict
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
            
            
            # Lines 53 - 80: Merges together the different non-overlapping tag groups into a single entry
            # Determine the verb with the most tags and set this as the "base"
            mostTags = []
            maxTags = 0 
            for item in tagDict.values():
                if len(item) > maxTags:
                    maxTags = len(item)
                    mostTags = item
            
            if mostTags != []:
                longestDict = mostTags

               
                # Extract the list from the tagDict
                for list in tagDict.values():
                    # Loop through the dict of Key to Value in the list
                    for dict in list:
                        # For each value in the dict
                        for val1 in dict.values():   
                            found = False
                            # Extract the dict from the list
                            for singleDict in longestDict:
                                # Extract the value from the dict
                                for val2 in singleDict.values():
                                    if val2.__contains__(val1):
                                        found = True
                                        break
                            # If tag/phrase is non-overlapping then add it to the longestDict
                            if found == False:
                                longestDict.append(dict)
                
                                
                template = question
                splitTemplate = template.split()
                count = 0 
                # Loop through the question and replace phrases to create a candiate template
                for item in longestDict:
                    count +=1
                    key = item.keys()
                    value = item.values()
                    key = str(key)
                    value = str(value)
                    key = key[key.find("['")+2:key.find("']"):] # Extract the key/tag
                    value = value[value.find("['")+2:value.find("']"):].strip() # Extract the value/word/phrase
                    
                 
                    # Logic applied to keep certain question words or auxilary verbs
                    # If first word then keep the auxverb/question word
                    # else replace it with the key (srl tag) if it has one
                    if count == 1: 
                        if key == "ARGM-MOD" or value.lower().strip() in ["what", "how", "why", "when", "which", "where"]: # "what" in value.lower() or "how"  in value.lower() or "why"  in value.lower() or "when"  in value.lower() or "where"  in value.lower() or "which"  in value.lower():
                            pass
                        else:
                            continue 
                    else:     
                        template = re.sub(r'\b' + re.escape(value) + r'\b', '<' + key + '>', template)
                        
                # Check to see if the created template is valid
                # Valid if: At least 3 tags, no duplicate tags, at least 50% of the words are tags
                if "<" in template and template not in templates:
                    splitTemplate = template.split()
                    numTags = 0
                    duplicateTag = False
                    seenElements = []
                    
                    # Check for duplicate tags
                    for i in range(len(splitTemplate)):
                        if i == len(splitTemplate)-1:
                            tag = splitTemplate[i][:len(splitTemplate[i])-1:]
                        else:
                            tag = splitTemplate[i]
                            
                        if tag in seenElements:
                            duplicateTag = True
                            break
                        else:
                            seenElements.append(splitTemplate[i])
                        
                        if "<" in splitTemplate[i]:
                            numTags += 1
                    
                    # If pass all the checks then appned the template to the list for this cluster in the dictionary 
                    if numTags >= 3 and numTags / len(splitTemplate) >= 0.5 and duplicateTag == False:
                        templates.append(template)
                        value = clusteredTemplates[keyCount]
                        value.append(template)
                        clusteredTemplates[keyCount] = value
                        
    # Once all templates created then write the templates, and the cluster they are in, to a file
    clusteredTemplatesOutput = open(questionsFileName + "TemplatesClustered.txt","w")  
    keyCount = 0
    for list in clusteredTemplates.values():
        keyCount += 1
        clusteredTemplatesOutput.write("Cluster "+ str(keyCount) + ":\n")
        for template in list:
            clusteredTemplatesOutput.write(template + "\n") 
    
    # Close the file
    clusteredTemplatesOutput.close()  
              
    return templates, clusteredTemplates             
    
# This method reads the file from which content is to be extracted
# It then segments the text into sentences
# For each sentence calls the templateFill() method which attempts to generate question/s
def contentExtract(contentFileName, nlp, predictor, clusteredTemplates, kmeans, vectorizer):
    
    # Variables used for data analysis purposes
    numQuestions = 0
    numSentences = 0
    totalSentences = 0

    sentences = []
    transcript = open(contentFileName + '.txt', "r") # opens the file containing the "content"
    questionOutput = open(contentFileName + "TemplateQuestions.txt", 'w') # Creates the file to which the output questions will be wrriten
    text = transcript.read() # Reads in the contents of the file to a string
    text = contractions.fix(text) # Remove contractions (these can mess up the SRL)
    doc = nlp(text) # Used to split the text into sentences

    # Loop through the sentences filtering out blank lines and start/end labels
    for sent in doc.sents:
        totalSentences+=1
        sent = str(sent).replace("\n"," ")
        sent = str(sent).replace("[MUSIC]","")
        sent = str(sent).replace("[SOUND]","")
        sentences.append(sent) 
    
    # Loop through the sentences and run the SRL Model on them
    for sent in sentences:
        result = predictor.predict(sent)
        tagDict = {} # Will store the SRL tags and phrases: {verb1: [{SRL Tag: phrase}, {SRL Tag: phrase},...], verb2: [{SRL Tag: phrase}, {SRL Tag: phrase},...],...}
        
        # Loop through the output from the SRL and restructure it
        # Storing the output in the tagDict
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
        
        
        # Loop through the tagDict which has the Keys (SRL tag) and the Value (the phrase/words)
        questionsReturned = [] # Used to store the generated questions for this sentence 
        templatesUsedReturned = []  # Used to store the templates used to generate the questions (parallel to above)         
        for list in tagDict.values():
            keys = []
            values = []
            
            # Append each of these words and keys to 2 parallel lists
            for dict in list:
                for key in dict.keys():
                    keys.append(key)
                    values.append(dict[key])
            
            # Call method to generate question from this sentence given the keys and values and the templates
            # Add the returned generated questions and used templates to the lists
            questions, templatesUsed = templateFill(sent, keys, values, clusteredTemplates, kmeans, vectorizer)
            questionsReturned += questions
            templatesUsedReturned += templatesUsed

        # Write the generated questions, templates and the sentence from which they were generated to the output file
        if questionsReturned != []:
            numSentences += 1
            sent = sent.strip()
            questionOutput.write("--------------------------" + '\n')
            questionOutput.write("Sentence: " + sent + "\n")
            for i in range(len(questionsReturned)):
                numQuestions += 1
                questionOutput.write("Template: " + templatesUsedReturned[i])
                questionOutput.write("Question: " + questionsReturned[i])
                

    # Display some statistics
    print("Total Sentences in Transcript: " + str(totalSentences))
    print(str(numQuestions), "Questions Generated from", str(numSentences), "of the Sentences.\n")
    print("Questions Saved to: " + questionsFileName + "TemplateQuestions.txt")
    
    # Close the file
    questionOutput.close()
                
# This method uses the sentence extracted keys and values to attempt fill the extracted templates and return questions                                               
def templateFill(sentence, keys, values, clusteredTemplates, kmeans, vectorizer):    
      
    filledTemplates = [] # Stores the filled templates (i.e: the generated questions)
    templatesUsed = [] # Stores the templates used to generate the questions (parallel list to the one above)
    firstWords = [] # Stores the first word in each template (Used to reduce number of questions generated)
    argMod = False # Stores if a question starting with an Aux-Verb has been generated
    
    # Get the cluster that this sentence best fits into
    # then retrieve the templates for this cluster
    predictedCluster = predictCluster(kmeans, sentence, vectorizer)
    templates = clusteredTemplates[predictedCluster]
    
    # Loop through the templates retrieved
    for template in templates:
        tags = []
        splitWords = template.split(" ")
        
        # Extract the tags
        for word in splitWords:
            if "<" in word:
                tags.append(word[1:word.find(">")])

        # If all the tags in the templates match the keys in the sentence then fill the template
        sameTags = all(item in keys for item in tags)
        if sameTags:
            filledTemplate = template
            for item in keys:
                filledTemplate = filledTemplate.replace("<"+item+">", values[keys.index(item)].strip())    
            
            firstWord = filledTemplate[:filledTemplate.find(" "):]

            # Further check to determine if the filled template meets some requirements:
            # have not already generated a question with that question word
            # and/or that already we havent generated a question with an an Aux-Verb (as these questiosn are all essentially duplicates)
            # If these checks are passed then append the filled the template to the filledTemplates list
            if firstWord not in firstWords and (firstWord.lower() not in ["can", "would", "could", "should", "may", "will"] or argMod == False):
                filledTemplate = filledTemplate.lower()
                filledTemplate = filledTemplate.capitalize()
                filledTemplates.append(filledTemplate + "\n")
                templatesUsed.append(template + "\n")
                firstWords.append(firstWord)
                if firstWord.lower() in ["can", "would", "could", "should", "may", "will"]:
                    argMod = True
    
    # Return the parallel lists of filledTemplates and templatesUsed  
    return(filledTemplates, templatesUsed)       

# This method reads in the input questions and clusters them in 12 clusters
# This output is stored in a dictionary: {cluster1 : [t1,t2,t3,...], cluster2: [t1,t2,t3,...],...}
def clusterQuestions(questionFileName):
    
    # Read in the file and and store each question in a list
    inputFile = open(questionFileName+ ".txt")
    questions = []
    for question in inputFile:
        questions.append(question.strip())
    
    # Set up and vectorize the text/questions
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(questions)
    
    # Perform the k-means clustering into 12 clusters
    kmeans = KMeans(n_init=10, n_clusters=12, random_state=42)
    kmeans.fit(X)

    # Write the questions and their clusters to an output file
    # Populate the clusterDict with the questions
    clusterDict = {} # {cluster1 : [q1,q2,q3..], cluster 2 : [q1,q2,q3...]}
    output = open(questionFileName + "Clustered.txt", 'w')
    for clusterID in range(12):
        clusterQuestions = np.array(questions)[kmeans.labels_ == clusterID]
        clusterDict[clusterID] = [] # Initialise the blank list for the dict entry
        output.write("Cluster:" + str(clusterID + 1) + ":\n")
        # Write each question in this cluster to the file and append to dict list
        for question in clusterQuestions:
            clusterValue = clusterDict[clusterID]
            clusterValue.append(question)
            clusterDict[clusterID] = clusterValue 
            output.write(question + "\n")
    
    # Return the dict of clustered questions as well as the k-means and vectorizer
    return clusterDict, kmeans, vectorizer
 
# Predicts what cluster each sentence should be in (and thus what templates to use)           
def predictCluster(kmeans, sentence, vectorizer):
    
    # Vectorize the sentence and then predict its cluster
    sentenceTfidf = vectorizer.transform([sentence])
    predictedCluster = kmeans.predict(sentenceTfidf)[0]

    # Return the predicted cluster
    return predictedCluster  
            
if __name__ == "__main__":
    
    # Load the SRL predictor and spacy library
    print("Loading SRL and Spacy Models...")
    predictor = Predictor.from_path("structured-prediction-srl-bert.2020.12.15.tar.gz")
    nlp = spacy.load("en_core_web_sm")
      
    userInput = ""
    questionsFileName = ""
    # Input Loop to get file containing sample questiosn to generate templates from
    while True:
        userInput = input('Enter the File Containing the Sample Questions (type "stop" to close the program): ')
        if userInput.upper() == "STOP":
            exit(0)
        if os.path.isfile(userInput + ".txt"):
            questionsFileName = userInput
            break  
        else:
            print("File Not Found.\nPlease enter the name of a valid .txt file (excluding the .txt extension).")
            continue
    
    # Call methods to perform the k-means clustering
    # and to extract the templates from these clustered questions
    templates = [] 
    print('Clustering Questions from File: ' + questionsFileName + ".txt")
    clusteredQuestions, kmeans, vectorizer = clusterQuestions(questionsFileName)
    print("Clustering Completed. Now Extracting Templates...")
    templates, clusteredTemplates = extractTemplates(clusteredQuestions, questionsFileName, predictor)
    print(str(len(templates)), "Valid Template/s Extracted.\n")
    
   
    # Input Loop: Ask user for file name to generate questions from
    # contains basic check to see if file exists
    while True:
        userInput = input('Enter Content File Name (type "stop" to close the program): ')
        if userInput.upper() == "STOP":
            break
        # If it is a valid file, then call the method to extract the content (and from there generate questions)
        if os.path.isfile(userInput + ".txt"):
            print("Generating Questions...")
            contentExtract(userInput, nlp, predictor, clusteredTemplates, kmeans, vectorizer)
        else:
            print("File Not Found.\nPlease enter the name of a valid .txt file (excluding the .txt extension).")
            continue
        
        
    
    
        
  
    
   