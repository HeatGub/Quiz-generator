import openai
import re
from app.secret_file import OPENAI_API_KEY #(api_key.py file in this folder)
openai.api_key = OPENAI_API_KEY

def callGPT (topic, n_q, n_a, temperature):
	def generate_prompt():
		return """Here is an exact example of a quiz consisting of 1 question (Q1) about animals. Question has 3 answers (A1, A2, A3):
		Q1: Which of these animals is a marsupial?
		A1. Lion
		A2. Grizzly Bear
		A3. Kangaroo
		Correct = A3. Kangaroo

		Create similarly constructed quiz. Quiz should consist of {} questions. 
		All of the questions should be about {}. Each question should have {} short answers.
		The whole quiz should always start with "Q1:".
		In terms like (Q1:, A2., Correct = A3.) Only numbers should change. 
		Now create the quiz.""".format(n_q, topic, n_a)

	# def generate_prompt():
	# 		return """Whats up"""

	def error_dict(APImessage):
		return dict(
		questions='',
		answers='',
		corrects='',
		finishReason ='API ERROR',
		questionsAmount=0,
		answersMode=0,
		answersSublistsEqual=False,
		correctsValidRange=False,
		responseText=str(APImessage),
		visible=False,
		allOk=False)
	
	try: #to establish connection
		response = openai.Completion.create(engine = "text-davinci-003", prompt=generate_prompt(), max_tokens=3500, temperature=temperature) #459 tokenów w prompcie, 4097 max
		# print(response)
		# response = openai.Completion.create(engine = "text-curie-001", prompt=generate_prompt(), max_tokens=1500, temperature=temperature) #less tokens, different amount of questions and answers, nonsense. Only davinci model undertands the input
		#25 questions with 3 answers = 1500 overall tokens
	except openai.error.APIError as e:
		msg = f"OpenAI API returned an API Error: {e}"
		error_dict(msg)  #pass error message to dictionary
	except openai.error.APIConnectionError as e:
		msg = f"Failed to connect to OpenAI API: {e}"
		error_dict(msg)
	except openai.error.RateLimitError as e:
		msg = f"OpenAI API request exceeded rate limit: {e}"
		error_dict(msg)
	else: #When no API connection exception occurs, try further
		try:  #in case GPT throws something which couldn't be cut by regexps
			finishReason = response.choices[0].finish_reason
			gptPrompt = response.choices[0].text
			# print(gptPrompt)
			#remove empty lines and html patterns to properly regex and display later
			gptPrompt = re.sub('<', '< ', gptPrompt) #html elements disruption prevention
			gptPrompt = re.sub('\n\n', '\n', gptPrompt)
			gptPrompt = re.sub('\n\n\n', '\n', gptPrompt)
			gptPrompt = re.sub('^ *\n*', '', gptPrompt) #for empty lines at the beginning
			gptPrompt = re.sub('^[\.] *\n', '', gptPrompt) #for some reason he used to generate the dot and other rubbish at the beginning
			gptPrompt = re.sub('\t', '', gptPrompt)
			gptPrompt = re.sub('\t\t', '', gptPrompt)
			# print(gptPrompt)
			# print(repr(gptPrompt)) #RAW FORM STRING

			split1 = re.split('\n* *[qQ]\d* *[:/.;-] *', gptPrompt) #split with question regexp. split1 are whole questions with ans and corr and empties ''.
			split1= list(filter(None, split1)) #remove empties ''
			# print(split1)
			# print(len(split1))

			questionsAll = []
			answersAll = []
			answersSublistsLens = []
			corrects = []

			for i in range (len(split1)):
				split2 = re.split('\n', split1[i]) #split by \new line
				split2= list(filter(None, split2)) #remove Nones
				questionsAll.append(split2[0])

				answers = split2[1:-1] # table of answers for one question
				answersList = []
				for i in range(len(answers)):
					current = answers[i]
					current = re.sub('^ *[Aa]\d* *[:/.;-] *', '', current) #regexp for answers pattern. ^ means beginning of whole string
					answersList.append(current)
				answersAll.append(answersList)
				answersSublistsLens.append(len(answersList))
				
				correct = re.split('^ *[Cc]orrect = [Aa](\d*) *[:/.;-] *.*', split2[-1]) #(\d) "get" the digit from a string.  Anything 0-inf times regexp = .*
				correct = list(filter(None, correct)) 
				corrects.append(correct)
				
			corrects = [item for sublist in corrects for item in sublist] #list of lists into list of strs (flattened list)
			correctsAll = [int(i) for i in corrects] 
		
		except: # when error in cutting the response occurs save the whole response text
			return dict(
				questions='',
				answers='',
				corrects='',
				finishReason =finishReason,
				questionsAmount=0,
				answersMode=0,
				answersSublistsEqual=False,
				correctsValidRange=False,
				responseText=response,
				visible=False,
				allOk=False)
		
		else: #when no except(ions) occurs, prepare the whole response dictionary
			questionsAmount = len(questionsAll)
			answersMode = max(set(answersSublistsLens), key=answersSublistsLens.count) #most frequent amount of answers on the list
			if answersSublistsLens == 1: #for questionsAmount = 1
				answersSublistsEqual = True
			else:
				answersSublistsEqual = all(index == answersSublistsLens[0] for index in answersSublistsLens) #all returns True when all is true
			correctsValidRange = all(correctsAll[i] <= answersSublistsLens[i] for i in range(len(correctsAll)))

			#Flags of validation
			if questionsAmount>=1 and answersMode>=2 and correctsValidRange==True and answersSublistsEqual==True and questionsAmount==int(n_q) and answersMode==int(n_a):
				visible = True
				allOk = True
			elif questionsAmount >=1 and answersMode>=2 and correctsValidRange==True:
				visible = True
				allOk = False
			else:
				visible = False
				allOk = False

			return dict(
				questions=questionsAll,
				answers=answersAll,
				corrects=correctsAll,
				finishReason = finishReason,
				questionsAmount=questionsAmount,
				answersMode=answersMode,
				answersSublistsEqual=answersSublistsEqual,
				correctsValidRange=correctsValidRange,
				responseText='',
				visible=visible,
				allOk=allOk)

	# callGPT ('something', 2, 2, 1)