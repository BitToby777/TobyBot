import requests
from bs4 import BeautifulSoup
import re

#Welcome to the engine of tobybot! This is where the real magic happens, like Disney or Universal. This program contains all of the functions that TobyBot refers to when deciding on which facts should be told by TobyBot himself!
full_time_fact_list = list()

#This function is used when we remove each of the word endings to see if two words match after each combination of words is tested and removed
def remove_suffix(input_string: str, suffix: str) -> str:
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string
    
#You may ask to yourself... how do we get the super awesome external files like the wondersome words_to_remove, the whimsical word_endings, and the terrific thesaurus? We read these files inside with this function shown below.
def add_external_file(file):
    with open(file, "r") as file_name:
        total_words_to_add = file_name.read()
    list_taken_from_other_file = total_words_to_add.split('\n')
    list_taken_from_other_file.pop()
    return list_taken_from_other_file
    
#Questions and Facts might have weird symbols inside of them, no good! We need to exterminate all of them!!! But when we print out the fact, it regrows its symbols back!
def remove_punctuation(change_word):
    change_word = change_word.replace('"', '')
    change_word = change_word.replace("'", '')
    change_word = change_word.replace(',', '')
    change_word = change_word.replace('.', '')
    change_word = change_word.replace('?', '')
    change_word = change_word.replace('(', '')
    change_word = change_word.replace(')', '')
    change_word = change_word.replace('!', '')
    return change_word

def choose_topic(topic: str, ID_number: int) -> bool:

    # download web page
    url = 'https://en.wikipedia.org/wiki/' + topic
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' }
    response = requests.get(url, headers=headers)
    
    # If we cant load this topic in Wikipedia, return false to tell the caller there was a problem
    if (not response.ok):
        return False
        
    # transform web page html into text
    parsed_web_page = BeautifulSoup(response.text, 'html.parser')
    web_page_text = parsed_web_page.get_text(separator='')

    # Use this for testing specific cases
    # web_page_text = 'Joe said: "I loved it so much." Joe B. Johnson likes to play tennis. I am a good boy. The exact amount was not disclosed, but was reportedly equal to or more than $50 million (c. $96.46 million in 2024), approximately the same amount as the launch budget of the Nintendo Entertainment System in 1985. References.'
    # web_page_text = "Both manga magazines are published by Shogakukan, a long-time business partner of Nintendo, and have featured manga based on Nintendo properties (e.g. Super Mario-kun, Kirby of the Stars, Donkey Kong). References."
    # web_page_text = "In June 1316 at Vincennes, Val-de-Marne, and following a particularly exhausting game, Louis drank a large quantity of cooled wine and subsequently died of either pneumonia or pleurisy, although there was also suspicion of poisoning. References."

    #web_page_text = 'By the 1960s, Budge and others had added Pancho Gonzales and Lew Hoad to the list of contenders. Budge reportedly believed that Gonzales was the greatest player ever.[127] Gonzales said about Hoad, "When Lews game was at its peak nobody could touch him. ... I think his game was the best game ever. Better than mine. He was capable of making more shots than anybody. His two volleys were great. His overhead was enormous. He had the most natural tennis mind with the most natural tennis physique."[128] Before and during the Open Era, Rod Laver remains the only male player in history to have won the calendar year Grand Slam twice in 1962 and 1969 [129] and also the calendar year Professional Grand Slam in 1967.[130] References.'
    
    #web_page_text = "Evan is a really super awesome player. He is so good that he could be the God of life. Joe likes to teach the kids to play football. Susan likes to teach the kids to sew. They love to learn how to make quilts. References."

    # Remove all footnotes (format: [1] [2] etc.)
    web_page_text = re.sub(r'\[.*?\]', '', web_page_text)

    # Replace weird space with normal space
    web_page_text = web_page_text.replace(' ', ' ')

    # If there are instances of a space then a letter/number then a period
    # then strip off the period so that it won't be used for splitting the sentence.
    # Before: Susan B. Anthony was an American social reformer.
    # After:  Susan B Anthony was an American social reformer.
    web_page_text = re.sub(r' (\w)\.', r' \1', web_page_text)

    # If there instances of an open parenthesis then a letter/number then a period
    # then strip off the period so that it won't be used for splitting the sentence.
    # Before: He made $50 million (c. $60 million in 2025), a big paycheck.
    # After:  He made $50 million (c $60 million in 2025), a big paycheck.
    web_page_text = re.sub(r'\(([a-zA-Z])\.', r'(\1', web_page_text)

    # change any instances of a period followed by a line break
    # to a standard sentence ending (a period followed by space)
    web_page_text = web_page_text.replace('.\n', '. ')

    # Replace "Mr. " with "Mr " so we don't split a sentence in the middle of someone's name.
    web_page_text = web_page_text.replace('Mr. ', 'Mr ')

    # Replace "Co. " with "Co " so we don't split a sentence after the abreviation Co. (company)
    web_page_text = web_page_text.replace('Co. ', 'Co ')

    # Replace "No. " with "No " so we don't split a sentence after the abreviation No. (number)
    web_page_text = web_page_text.replace('No. ', 'No ')

    # Replace "St. " with "St " so we don't split a sentence after the abreviation St. (Saint)
    web_page_text = web_page_text.replace('St. ', 'St ')

    # Replace "eg." with "e.g " so we don't split a sentence after this latin abreviation
    # Note that earlier code would have already replaced e.g. with eg.
    web_page_text = web_page_text.replace('eg.', 'e.g')

    #Fix darn period and quote wikipedia errors
    web_page_text = web_page_text.replace('."', '".')

    # Need to add a period after sentences that end in question mark and quote
    # so we can split them properly.
    web_page_text = web_page_text.replace('?"', '?".')

    # Replace fancy dash with normal dash
    web_page_text = web_page_text.replace('–', '-')

    # Replace accented e with normal e
    web_page_text = web_page_text.replace('é', 'e')

    # Replace dumb stinky double space with single space
    web_page_text = web_page_text.replace('  ', ' ')

    # Remove characters in other languages
    web_page_text = web_page_text.encode("ascii", errors="ignore").decode()

    #These are words that do not really tell what the sentences are mentioning, so we can combine them with the previous sentences.
    combine_check_list = ["It", "For example", "Otherwise", "Their", "He", "She", "They", "One of them", "Therefore", "These", "This", "Its", "That", "Such"]
    #This code makes sure that the sentences with those words don't get seperated from the sentences that they go with. This awkward period will get changed before it is written into the new file
    for phrase in combine_check_list:
        web_page_text = web_page_text.replace('. ' + phrase + ' ', '.' + phrase + ' ')

    output_filename = topic + '-text.txt'
    with open(output_filename, 'w') as file:
        file.write(web_page_text)
    print('Wrote file ' + output_filename)


    # Split on a period followed by a space and then NOT followed by a lower case character or an open parenthesis.
    all_facts = re.split(r'(\.)\s(?=[^a-z\(])', web_page_text)

    #Here is where the code determines which lines to keep and which lines to TOSS IN DA TRASH!!!

    #This is the list of all lines that contain either Footnotes or References
    end_list_numbers = list()

    #This is the list of all lines that contain (disambiguation) at the start, making it so that we can determine which lines are unnecessary
    start_list = list()

    #This is the list of all lines that contain Footnotes
    footnotes_list = list()

    #This is the list of all lines that contain References
    references_list = list()

    #This is the list of all lines that are NOT going to be printed due to failing our good fact checker
    ignore_list = list()

    #This is the list of all of the facts that successfully pass the good fact checker and will be transcribed onto the new file
    new_fact_list = list()

    #This is the list that catches all of the different facts that the wikipedia article has caught
    all_testing_facts = list()

    #I added this list because some facts contained lines with banned words but still got accepted due to starting line issues
    dont_save_list = list()

    #The number sentence we are checking
    fact_num = 0
    fact_num_remove_periods = 0
    after_remove_periods_fact_list = list()
    
    for fact in all_facts:
    
        if (fact != '.'):
        
            after_remove_periods_fact_list.append(fact)
    
    all_facts = after_remove_periods_fact_list
    
    for fact in all_facts:
        #The variable that will get checked False if it fails one of our good fact tests
        will_word_be_added = True
        
        #Removes the spaces in front of the fact
        fact.lstrip()
        
        if ("(disambiguation)" in fact):
            start_list.append(fact_num)
            will_word_be_added = False
        if ("Footnotes" in fact):
            footnotes_list.append(fact_num)
            end_list_numbers.append(fact_num)
            will_word_be_added = False
        if ("References" in fact):
            references_list.append(fact_num)
            end_list_numbers.append(fact_num)
            will_word_be_added = False
        if ("\n" in fact):
            line_split = fact.split("\n")
            fact = line_split[-1]
            #The function of the lines up top is to change the fact to only the last line; this allows us to remove the single lines that usuaully appear on top of the actual fact
            
        fact_word_count = fact.split(" ")
        
        #This variable determines if a sentence begins with "For the"
        useless_sentence_sniper = False
        
        if (fact_word_count[0] == 'For'):
            if (fact_word_count[1] == 'the'):
                useless_sentence_sniper = True
                
        for word in fact_word_count:
        
            #This if statement checks if the sentence also has the word "see". This takes out fake facts like, "For the (blah blah), see (blah blah)"
            if (word == 'see'):
                if (useless_sentence_sniper == True):
                    will_word_be_added = False
               
            #These statements removes all of the sentences that contain quotes inside of letters, like (b"m)   
            if ('"' in word):
                if (word[0] == '"'):
                    pass
                elif (word[-1] == '"'):
                    pass
                elif (word[-1] == ','):
                    pass
                
                else:
                    will_word_be_added = False
                    
        #Woah, all sentences with these words inside gotta go! Into the loo!
        if ("^" in fact) or ("This article needs additional citations for verification" in fact) or ("Not to be confused with" in fact) or ("Please help improve this article" in fact) or ("This article is about" in fact) or ("see glossary" in fact) or ("does not cite any sources" in fact) or ("Please help improve this secion" in fact) or ("This section is missing information" in fact) or ("Please expand the section" in fact) or ("This section needs additional citations" in fact) or ("See the above article" in fact) or ("I " in fact) or ("For individual terms, see Glossary" in fact) or ("improve this section" in fact) or ("For more details" in fact) or ("See also" in fact) or ("This article is missing" in fact) or ("Please expand the article" in fact):
            will_word_be_added = False       
            dont_save_list.append(fact_num) 
            
        #If a fact contains less than 6 words, then it most likely isn't very useful and will be taken out back
        if (len(fact_word_count) < 6):
            will_word_be_added = False
            
        #This function simply adds all of the facts into a list of its own, to be used for re-writing in the next part
        all_testing_facts.append(fact)            
        
        #If the fact fails, then it will be added to the ignore_list, meaning that it won't be copied into the new file
        if (will_word_be_added == False):
            ignore_list.append(fact_num)
            
        #TIME FOR THE NEXT FACT! YAY!!!
        fact_num = fact_num + 1
        
        
        
        
        
    #The next section will use the data gathered to finally write out the good facts to the text file!

    #This variable counts all of the facts are being tested in this function, to see if they are in the ignore list
    fact_num = 0

    #This variable is determined by if there are an odd amount of quotes in this section. If so, then we got to EXTERMINATE IT!!! And also the facts after that until we reach another odd quotation mark fact
    is_a_quote_in_this_section = False

    #This allows us to determine what fact number we should ignore up until that point. This is because (disambiguation) is ALWAYS before the first real fact
    if (len(start_list) > 0):
        start_number = start_list[0]
    else:
        #If there is no (disambiguation) in the text
        start_number = -1

    #This bulky chunk code tells us where we should stop spitting the facts into the new file. This is determined by the last usage of Footnotes or References, picking the earlier of the two if both are used.
    if (len(footnotes_list) > 0):
        footnotes_number = footnotes_list[-1]
    else:
        footnotes_number = 999999999
    if (len(references_list) > 0):
        references_number = references_list[-1]
    else:
        references_number = 99999999

    #This variable determines where the last odd number of quotation marks are. It automatically goes back to 0 if it has been 10 times since the last one. OR ELSE THE WHOLE THING COULD GO BOOM BOOOM!
    quote_number = 0

    #This number gets the smaller of the footnotes/references values
    end_number = min(footnotes_number, references_number)





    #This function will either ignore the fact or write it into the new file! It's complex! Just like love... :)
    for fact in all_testing_facts:

        #This variable says if the fact is banned or not
        banned = False
        
        if (start_number < fact_num < end_number):
            for banned_facts in ignore_list:
                if (fact_num == banned_facts):
                    #Bans a fact if the index number matches with one of the banned list index numbers. But it can be saved! This will save facts that have footnotes or references in them before those parts got chopped off like butter
                    banned = True 
                    for numbers in end_list_numbers:
                        if (fact_num == numbers):
                            if (fact_num != end_list_numbers[-1]):
                                if (fact_num not in dont_save_list):
                                
                                    #Horray! The fact is miraculously saved!!! But it can still fail the final part...
                                    banned = False
                        
        else:
        
            banned = True
            
        if (banned == False):
        
            #This function replaces all of the periods without spaces that were put in there to avoid facts that start with words in the combine_check_list 
            fact = fact.replace('.', '. ')
            
            #This function counts all of the quotation marks. If the number is odd, then it must BE GONE!!!! This is because the quote won't be complete in that sentence, a red flag even redder than laying on the beach on a hot summer day.
            number_of_quotation_marks = fact.count('"')
            
            #These if loops check if there is an odd number of quotation marks, with "is_a_quote_in_this_section" changing based on that
            if (number_of_quotation_marks % 2 != 0):
                quote_number = fact_num
                
                if (is_a_quote_in_this_section == False):
                    is_a_quote_in_this_section = True
                    
                else:
                    
                    #This allows us to reset back to normal adding when the next quotation mark is found again
                    quote_number = 0
                    is_a_quote_in_this_section = True
                    
            if (quote_number != 0):
            
                if (fact_num - quote_number > 9):
                   
                   #HORRAY! SOME FACTS ARE GONNA GET SAVED FROM THE GRAVE! This is because it has been 10 facts since the last odd quotation mark sentence was found, avoiding any potential mistake quotation marks in the wikipedia file. This function shall bring them back to life, bringing them upwards the mucky waters from ignore_fact land.           
                   times_fact_saved = 1
                   while True:
                       new_fact_list.append(all_testing_facts[quote_number + times_fact_saved])
                       times_fact_saved = times_fact_saved + 1
                       if (times_fact_saved == 11):
                           break

                   quote_number = 0
                   
            elif (is_a_quote_in_this_section == True):
                is_a_quote_in_this_section = False
            else:        
                #FINALLY! If the fact passes all of those grueling trials, it can be added to the new file. It has gone through war and back.
                quote_number = 0
                new_fact_list.append(fact)
                
        #Now we shall check the new fact and do the whole second-half process again!
        fact_num = fact_num + 1
            





    #print_current_line = False

    #Finally... this function adds the good boy facts into the new file and you can un-comment some lines if you want the program to print all of the facts one by one! :)

    output_filename = topic + '-fact-list.txt'
    with open(output_filename, 'w') as file:
        for item in new_fact_list:
            file.write("(START_FACT)" + item)
            #print(item)
            #input('')

    print('Wrote file ' + output_filename)
    
    full_time_fact_list.append(ID_number)
    
# This particular part morphs all of the facts obtained from the file into a fact_list full of all the facts that any user has any said in a current session! This way, we can refere back to full_time_fact_list to avoid having TobyBot answer a question about the wrong topic entirely! Silly Bot!!!
    
    for fact in new_fact_list:
        full_time_fact_list.append(fact)
    
    return True

#This function is the biggest, the meatiest, the girthiest, not even a contest! This function also calls the other functions up top as well for scoring purposes. This function shall return the score that a question and a fact have with each other. The fact that has the closest match is what TobyBot will bless your ears with. If it's a tie, he says both! The more the merrier.    
def get_match_score(question: str, fact: str) -> float:

    #These three lines allow us to obtain the info from whichever file is passed into the function a mile above.
    banned_word_list = add_external_file("words_to_remove.txt")
    word_endings_list = add_external_file("word_endings.txt")
    lines_of_synonyms = add_external_file("thesaurus.txt")
    banned_question_endings_list = add_external_file("words_to_remove_from_end_of_question.txt")
       
    #These lines split up the questions and facts into words of their own, useful for counting the amount of words in each fact/question.   
    question_word_list = question.split()
    fact_word_list = fact.split()
    
    #But... do we really want very basic and boring words??? NO!!! We want to remove them, using these complex equations to remove the useless words.
    question_word_list = [item for item in question_word_list if item not in banned_word_list]
    fact_word_list = [item for item in fact_word_list if item not in banned_word_list]
    
    for question_ending in banned_question_endings_list: 
        if (question_ending == question_word_list[-1]):
            question_word_list.remove(question_word_list[-1])
            
    #How long are these goofy sentences anyways? These tell us! We use this to determine how many words of the question match with each fact that TobyBot has in his jiggly belly!
    question_word_list_count = len(question_word_list)
    fact_word_list_count = len(fact_word_list)

    #The score will be out of whichever word count is smaller
    minimum_word_list_count = min(question_word_list_count, fact_word_list_count)

    #These variables tell us how far we've gone in word score testing and how many of those words find a match made in heaven
    current_question_word_position = 0
    matches = 0
    
    for word in question_word_list:
        current_question_word_position = current_question_word_position + 1
        found_a_word = False
    
# HERE IS WHERE THE ACTUAL SKY OF FOR LOOPS COMES IN TO STAY!!!!!!!!!!!!!

        for checking_for_match in fact_word_list:
        
# These next lines are after we have just two words to compare! 

            for question_ending in word_endings_list:
            
                for fact_ending in word_endings_list:
                    
# Both the current fact and question word now goes through the stripping process! This strips off the punctuation and word attachments faster than a chmimpanzee devours a banana more amazing than your grandmother's cooking as good as a 5-star meal.

                    word = remove_punctuation(word)
                    checking_for_match = remove_punctuation(checking_for_match)
                    
                    checking_for_similarity_question = remove_suffix(word, question_ending)
                    checking_for_similarity_fact = remove_suffix(checking_for_match, fact_ending)     
                    
                    for synonym_check_line in lines_of_synonyms:
                    
                        #This allows the thesaurus to compare similar words throught the use of commas seperating the word brothers
                        synonym_check_list = synonym_check_line.split(',')
                        
                        for synonym_question in synonym_check_list:
                        
                            for synonym_fact in synonym_check_list:
                            
                                #This if statement if two words are both found on the same line in the thesaurus after all of the censorship process has taken place!
                                if ((checking_for_similarity_question == synonym_question) and (checking_for_similarity_fact.lower() == synonym_fact)):
                                
                                    if (found_a_word == False):
                                    
                                        #HORRAY! WE FOUND A THESAURUS MATCH! Now time to send them on a Honeymoon to Grammar Police land!
                                        matches = matches + 1
                                        found_a_word = True

                    #HORRAY! WE FOUND A NORMAL MATCH! Now time to send them on a Honeymoon to found_a_word land!
                    if (checking_for_similarity_question == checking_for_similarity_fact.lower()):

                        #If the word was alreay found to be similar from another suffix removing combination, we simply let it goooo let it goooo can't hold it back anymoreeeeee
                        if (found_a_word == False):
                            matches = matches + 1
                            found_a_word = True

        #If we checked all words, we are now finished! But not complete. We still gotta check the score between the two different sentences!
        if (current_question_word_position == question_word_list_count):
            score = matches / minimum_word_list_count
            return score
            
            
            
            
            
#Last but not least... the function that TobyBot goes to when you... the viewer... asks a beautiful(or ugly) question! You either get one answer, tons of answers, or no answer at all. Only time can tell.
     
def ask_question(question: str, ID_number: int) -> list:
    
    #No blank questions
    if (len(question) == 0):
        return ['No blank questions. You think you are Taylor Swift with that blank space, baby!']

    #Questions must end with a question mark
    if (question[-1] != '?'):
        return ['You gotta ask a question next time you unimaginative sheep!']
    
    #Questions must be at least 3 words
    if (len(question.split()) < 3):
        return ["Questions need to be at least 3 words long, you non-yappacholic!"]
        
    real_word_checker = question.split()
    
    #Questions must have at least 2 real words
    
    #Take the words in the question and remove the words from the words_to_remove file.
    #Then if there are less than 2 words, tell the user about the problem.
    
    banned_word_list = add_external_file("words_to_remove.txt")
    banned_words_in_question_list = add_external_file("words_not_allowed_in_questions.txt")
    
    useful_words_list = [item for item in real_word_checker if remove_punctuation(item.lower()) not in banned_word_list]
    
    if (len(useful_words_list) < 2):
        return ["Your words are not useful enough! Just like you. (emotional damage)"]
    
    for real_word in real_word_checker:
        for banned_question_word in banned_words_in_question_list:
            if (remove_punctuation(real_word.lower()) == banned_question_word):
                return ['You cannot use "' + banned_question_word + '" in your question!!! It is way too vague, just like your brain!']
    
    
    

    #This list records all of the fact scores that have a score higher than 0.5, which will be used to determine the best fact(s) at the end!
    score_record_list = list()
    
    #This lists all of the facts that have a score higher than 0.5, one/many of these shall be the words that escape out of TobyBot's blabber!
    fact_record_list = list()
    
    #This variable is determined on the score of the fact, completing tossing it in the ocean if it is low!
    found_fact = False
    
    #These format the question and answers so that it can be compared and told to the world
    question = question.replace('?', '')
    question = question.lower()
    answers = list()
    
    reverse_index = -1
    toby_bot_magic_list = []
    
    while True:
        if (full_time_fact_list[reverse_index] == ID_number):
            break
        reverse_index = reverse_index - 1
        # This code goes backwards in indexes to find the last time that the human ID_number can be found in the full_time_fact_list, hence the topic that the human is currently on
        
    for fact in full_time_fact_list[reverse_index + 1:]:
        # This for loop goes through every single fact after the most recent ID_number and adds it to the final list that TobyBot has for the answers. The loop doesn't break until the facts for that one specific topic are over, which can be told by the next ID_number which has integer values
    
        if isinstance(fact, str):
            toby_bot_magic_list.append(fact)
            # Yay! TobyBot can now give this fact as an answer!
            
        elif isinstance(fact, int):
            #Nooooo, no more facts about that topic found!
            break
        
   
    
    #This for loop goes through each fact to see if it gets said or not
    for fact in toby_bot_magic_list:
    
        #The Big Brother Function has come to tell the world the greatest secrets of the Earth
        score = get_match_score(question, fact)
        
        if (score > 0.5):
        
            #HORRAY! THE FUNCTION PASSED! Now what? Both of the record lists obtain another fact/score and the variable is checked true, meaning that there has been at least one fact that passed the test! If none passed. ... we don't talk about that...
            found_fact = True
            score_record_list.append(score)
            fact_record_list.append(fact)     
            
    
    
#HERE IS WHERE THE FINAL PART OF THE CRAZY LABYRINTH REACHES THE END! We either say nothing, or well... not nothing.
    if (found_fact == True):
    
        #Here is where we finally find the best score and turn the number into the fact! And that's just facts, bro.
        print_to_player_value = max(score_record_list)
        fact_checking = 0
        
        #For every fact that has a score that is equivalent to the record score, it wins!!! TobyBot tells you these facts and your day has just gotten 0.000001% better!!!
        for score in score_record_list:
        
            if (score == print_to_player_value):
                answers.append(fact_record_list[fact_checking] + ".")
                
            fact_checking = fact_checking + 1
            
    if (found_fact == False):
    
        #You have failed... no fact is similar enough to your wacky question, so no insane fact shall be brought down onto your plate. Instead you are hungry, feeling thirst towards the cool cucumber-ness of TobyBot's impressment.
        answers.append('My database does not have your answer yet... Sorry!!!')
        
    return answers


