// Welcome to TobyBot's Website Goodness! Here he will make choices based off whatever devious actions the human takes. For instance, TobyBot will behave differently if the topic is set versus not set

// This variable is chosen by the player, and determines what Wikipedia file TobyBot downloads and scans into his vast mind
let topic = "(NONE)";

// This variable goes up whenever the human wants to hear TobyBot yap about the same question even more! This way, we pinpoint the exact list number and make TobyBot spit it out HARD
let index = 0;

// This list keeps track of all of the answers that score the highest score when it comes to TobyBot's whimsical word-matching (ties make many answers end up in this list)
let answers = [];

// This tiny but essential function saves all of the buttons that are disabled when TobyBot is thinking or typing. Without any buttons, TobyBot will only be left to himself. This function is called many times, when TobyBot is done with his botty yater.
function enableButtons()  {


    const moreButton = document.getElementById("tellMeMore");
    const resetButton = document.getElementById("resetTopic");
    const sendingButton = document.getElementById("sendButton");

    resetButton.disabled = false;
    sendingButton.disabled = false;
    moreButton.disabled = false;
}

function typeWriter(newText) {
    const moreButton = document.getElementById("tellMeMore");
    const resetButton = document.getElementById("resetTopic");
    const sendingButton = document.getElementById("sendButton");
    
// Here is the only spot where these buttons get disabled! With this function, TobyBot will be able to type out the text that you and him say! While this occurs, you cannot press any buttons.
    
    moreButton.disabled = true;
    resetButton.disabled = true;
    sendingButton.disabled = true;
    
    return new Promise((resolve) => {
        const textareaElement = document.getElementById("myTextarea");
        const typingSpeed = 20; // This number determines how long it takes TobyBot to say each word.
        for (let i = 0; i < newText.length; i++) {
            setTimeout(() => {
                textareaElement.value += newText.charAt(i); // This line adds a single letter to the screen. This process happens sooooo many times, so it'll seem like the sentence is slowly spilling itself out
                
                textareaElement.scrollTop = textareaElement.scrollHeight; // This line gradually scrolls you down as he types, so you can see every word clearly.
                if (i === newText.length - 1) {
                    resolve(); // Done typing
                }
            }, typingSpeed * i);
        }
    });
}

// Such a baby function above! It simply picks an ID_number that is used to confirm what topic has been demanded by each different person using TobyBot at the same time!
function getIdNumber(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

let ID_number_generated = getIdNumber(1, 10000000000); 


// This dope function determines whether TobyBot should continue spitting out facts so hard they break windows, or halt the spitting, after TobyBot has run out of his precious automated Bot Juice 2000
  async function handleTellMeMore() {

    const moreButton = document.getElementById("tellMeMore");
    const resetButton = document.getElementById("resetTopic");
    const sendingButton = document.getElementById("sendButton");
      
      if (index >= answers.length - 1) {
      
      // If we run out, the human gets to refill his juice meter with new questions! Otherwise, we increase the index and continue the CHAIN of answers that TobyBot has in STORE for us!
      
          let addToConversation = '\n' + 'TobyBot: Aahh, fuddles! It looks like I have run out of da juice that makes my fact machine bubble! Geometrically dominate your situation by asking me a brand spanking new question! :D';
          await typeWriter(addToConversation);
          enableButtons();
          moreButton.setAttribute("hidden", "true");
          index = 0;
          return;
          
      }    
      
      index++;
      addToConversation = '\n' + 'TobyBot: ' + answers[index];
      await typeWriter(addToConversation);
      enableButtons();
      
  }

// Humans have low attention spans. Think about this... do you scroll past shorts or reels every few sections just to stimulate your jumpy brain? Well, TobyBot can recreate this feeling by altering his style whenever the human feels bored of the same ol' topic. We need a ton of functions for this since the answer list, place in the list, and extra buttons all need to VANISH
  async function handleResetTopic() {
  
    const moreButton = document.getElementById("tellMeMore");
    const resetButton = document.getElementById("resetTopic");
    const topicHeader = document.getElementById("topicHeader");
    const sendingButton = document.getElementById("sendButton");
    
    // alert(ID_number_generated);
  
    topic = "(NONE)";
    index = 0;
    answers = [];
    
    addToConversation = '\n' + 'TobyBot: I guess that topic does not rub you the right way! Pick a brand new topic - even better than the last one - to make our interaction as fun as bunnies!';
    await typeWriter(addToConversation);
    
    
    topicHeader.textContent = "Current Epic Topic: Nothing yet!";
        
    resetButton.setAttribute("hidden", "true");
    
    moreButton.setAttribute("hidden", "true");
    
    enableButtons();
    
  }


// This listens for any key press inside the input field, which when Enter or Click occur, awesome things can happen!
document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("myInput");

    inputField.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {
        event.preventDefault(); 
        handleSend();
        }
    });
});

// This function gives TobyBot a little break to think about his lack of life choices in between his thinking 
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// When you ask somebody a question, they don't always respond immediately! If you ask somebody what the squire root of a refrigerator that came from Home Deport at 13 AM, they would blow their socks off! TobyBot displays his thinking phrases in a cool red color (oxymoron) and processes the data that he recieves from da Wiki! TobyBot also checks if your questions are stinky or winky!
async function handleSend() {

  const moreButton = document.getElementById("tellMeMore");
  const resetButton = document.getElementById("resetTopic");
  const sendingButton = document.getElementById("sendButton");
  
  // This variable is null when TobyBot is waiting for the user to type, and becomes active when you are waiting for him! An index of 2,000 means 2 seconds btw
    
  let thinkingInterval = null;

  const ThinkingElement = document.getElementById("tobyThinkingStatus");

  try {
  
  // We first begin with the try variable, which is what the code NORMALLY does, but gets halted once TobyBot stops thinking and has an answer for ya. We also need tons of variables for this complex procedure, bruh! (another oxymoron)
  
    const inputElement = document.getElementById("myInput");
    const inputValue = inputElement.value;
    let addToConversation = '\n' + 'You: ' + inputValue;
    await typeWriter(addToConversation);
    inputElement.value = "";
    
  const thinkingPhrases = [
  // Here is the rotation of phrases that TobyBot says to show that his ideas are flowing through him faster than the current before a waterfall of surprise
        "Shaking my magic juices...",
        "Diving into my deepest memories...",
        "Uncovering facts rarer than diamonds...",
        "Crunching numbers down...",
        "Doing a little dance to pass the time...",
        "Replaying all previous scenarios in my head, hand-picking the Tobylicious memory that will MASSIVELY captivate you...",
        "Eating robot smarties...",
        "Mixing a smoothie of knowledge and golden strawberries..."
      ];
      
    let phraseIndex = 0;
    
    ThinkingElement.textContent = thinkingPhrases[phraseIndex];
    
// This chunk of code rotates between the awesome messages, making sure to cycle back once the last message has been displayed on your either tiny and depressing screen(144p), or MASSIVE and shiny screen!(4k)
     thinkingInterval = setInterval(() => {
       phraseIndex = (phraseIndex + 1) % thinkingPhrases.length;
       ThinkingElement.textContent = thinkingPhrases[phraseIndex];
    }, 2000);
    
// apiUrl decides which file to go into, and dataToSend sends the data back into this javascript, what a perfect name! 10/10
    
    let apiUrl = "";
    let dataToSend = {};
    let dataToSendJson = "";
    
    if (topic == "(NONE)")
    {
        apiUrl = "choose_topic";
        // alert(inputValue);
        // alert(ID_number_generated);
        dataToSend = { 
          user_topic: inputValue,
          ID_number: ID_number_generated
        };
        //alert(dataToSend);
        dataToSendJson = JSON.stringify(dataToSend);
    }
    else
    {
    	apiUrl = "ask_question";
    	// alert(inputValue);
    	// alert(ID_number_generated);
    	dataToSend = {
    	  user_question: inputValue,
    	  ID_number: ID_number_generated
        };
        dataToSendJson = JSON.stringify(dataToSend);
    }
    
// This chunk code figures out if the requests done by the website were a success. If not, THEN VERY BAD THINGS WILL HAPPEN!!! (like your ice cream falls flat on the face on a boiling day lifeguarding
    
    // alert(dataToSendJson);
    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: dataToSendJson
    };
    
    const response = await fetch(apiUrl, requestOptions);
    
    if (thinkingInterval) {
      clearInterval(thinkingInterval);
    }
    ThinkingElement.textContent = "";

    // Check if the request was successful (status in the 200-299 range)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const textResponse = await response.text();
    const jsonResponse = JSON.parse(textResponse);
    
// This marks the end of the chunk that doesn't really affect the code, but catches errors meaner than Buck Snuckerson! (a chatter that brags about his wealth and accomplishments, but his actual achivements are very questionable


// If topic is not set yet...
    if (topic == "(NONE)")
    {
        
        const { response: topicFound} = jsonResponse;
// Topic was found! The topic variable shall be set
        
    	if (topicFound == true)
    	{
    	    addToConversation = '\n' + 'TobyBot: Ooh, I love that topic! Ask me anything, and I will use my juices to solve your puzzling questions!';
            await typeWriter(addToConversation);
            enableButtons();
    	    topic = inputValue;
    	    
// This allows our (OMG SO EPIC AMAZING I LOVE IT SO SIGMA YESSSS) topic to be changed in the blink of an I! Also the ResetTopic makes his grand appearance ig
    	    document.getElementById("topicHeader").textContent = "Current Epic Topic: " + topic;
    	    document.getElementById("resetTopic").removeAttribute("hidden");
    	}
        else    	
    	{
// Topic not found, NOOOOOOOOOOOOOOO!!!!!!!!! WAAAAAAAAAAAAAAA!!!!!!!!!!!!!! The human needs to pick something ELSE! 
    	    addToConversation = '\n' + 'TobyBot: UH OH! My database does not have your savvy topic! Ask me about some other topic, silly!';
            await typeWriter(addToConversation); 
            enableButtons();
    	}
    }
    
// If the topic is already set, then these checks make sure that the questions that the human is asking aren't too FREAKY! If they are weird and lacking typical question punctuation, then TobyBot will NOT give the human the amazing gift of the new buttons that someone with common sense will obtain!
    else
    {
    	answers = jsonResponse.answers;
    	index = 0;
    	
    	const AnswerCheck = answers[0];
    	addToConversation = '\n' + 'TobyBot: ' + answers[index];
    	await typeWriter(addToConversation);
        enableButtons();
    	
    	//alert(answers.length);
    	
        if (
        AnswerCheck.includes('My database does not have your answer yet') ||
        AnswerCheck.includes('You think you are Taylor Swift') ||
        // I find this answer check particularly funny because even though this line means somebody left BLANK SPACE, a TobyBot code inspector might blush past this and think that I am dissing on Taylor Swift! Haha me so funny lol
        AnswerCheck.includes('You gotta ask a question next time') ||
        AnswerCheck.includes('Questions need to be at least 3 words long') ||
        AnswerCheck.includes('Your words are not useful enough') ||
        AnswerCheck.includes('It is way too vague, just like your brain')
) {
    	
    	document.getElementById("tellMeMore").setAttribute("hidden", "true"); 
    	}
    	
    	else {
    	    document.getElementById("tellMeMore").removeAttribute("hidden");
    	}
    	
// This commented out function served as testing for when I wanted to see if every answer choice truly popped up! Even TobyBot used to have his not-so-silly quirks!

//        answers.forEach(function(item)
//        {
        //    alert('test');
        //    alert(item);
//        });
        //alert('Finished loop');
    }

  } catch (error) {
// Catch 21! Whoops wrong show. Errors are caught here, which takes us off the normal path.  
  
    console.error('There was a problem with the fetch operation:', error);
    
  } finally {
  
// This code runs after TobyBot has finally made up his beatiful, glorious, smooth mind! I promise I ain't glazing him! Now, we deviate away from the traditional "try" passageway, and transfer over to these lines, which keep TobyBot from being stuck in infinite loops where he says his thinking lines FOREVER AND EVER AND ever and ever and ev...e......r...............

    if (thinkingInterval) {
      clearInterval(thinkingInterval);
    }
    ThinkingElement.textContent = ""; 
  }

}

