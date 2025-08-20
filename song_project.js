// DOM Elements - Labels, inputs, and wrappers for the user interface
const labels = document.getElementsByTagName("label");
//all inputs
const inputs = document.getElementsByTagName("input");
//all wrapper
const buttonWrapper = document.getElementsByClassName("button");
//form, body, headline and others HTML holder elements
const musicWebsite = document.getElementById("musicWebsite");
const form = document.getElementById("formLinkPython");
const body = document.getElementById("mainBody");
const headLine = document.getElementById("headLine");
const pet = document.getElementById("thePet");

//music container
const musicContainer = document.getElementById("musicContainer");
//input and wrapper field for username and password
const lableInputUserName = document.getElementsByClassName("userNames")[0];
const labelInputPassWord = document.getElementsByClassName("passWords")[0];
const inputUserNameWrapper = document.getElementsByClassName("input")[0];
const inputPassWordWrapper = document.getElementsByClassName("input")[1];
const inputUserName = document.getElementById("inputUserName");
const inputPassWord = document.getElementById("inputPassWord");

//Buttons

//Sign up buttoms and its wrapper
const signUpButtonWrapper = document.getElementById("signUpButtons");
const signUpButton = document.getElementById("signUpButton");
//submit button and its wrapper
const submitButton = document.getElementById("submitButton");
const submitButtonWrapper = document.getElementById("submitButtons");

//chess Game properties
const chessGameWeb = document.getElementById("chessGameWebsite");
const addCard = document.getElementById("addCard");
const allUsersCards = document.getElementById("getAllUsersCards");
const removeCard = document.getElementById("removeCard");
const battleCards = document.getElementById("battleCards");

//ai Website properties
const aiWeb = document.getElementById("aiWebsite");
const recommendMusic = document.getElementById("recommendMusic");
const pickMusic = document.getElementById("pickMusic");
const chatBox = document.getElementById("chatMessages")

//add/delete music Website properties
const musicAddDeleteWeb = document.getElementById("musicAddDeleteWebsite");
const musicInput = document.getElementById("musicInput");
const addButton = document.getElementById("addButton");
const deleteButton = document.getElementById("deleteButton");

//Recording and sending audio Website properties
const recordingWeb = document.getElementById("recordingWebsite");
const recordAudio = document.getElementById("recordAudio");

//Casino website properties
const casinoWeb = document.getElementById("casinoWebsite");
const lowerOrHigher = document.getElementById("lowerOrHigherWrapper");

//Shop website properties
const shopWeb = document.getElementById("shopWebsite");
const buyBanishCard = document.getElementById("buyBanishCard");

//Image extractor website properties
const imageExtractorWeb = document.getElementById("imageExtractorWebsite");
const imageExtractWrapper = document.getElementById("imageExtractWrapper");

//adding event listener to the form for first run
form.addEventListener("submit", submitLogin);

//when loading the page, get how many users are there.
window.addEventListener("load", loadingPageBasedOnUserCount);

//Pet summoning for the users
pet.addEventListener("click", levelUp);
body.removeChild(pet);

// Global variables to store application state
var aiWebButtonWrapper = "";
var musicList = []; // Stores the user's music collection
var numberOfUsers = 0; // Tracks total number of registered users
var username = ""; // Current user's username
var password = ""; // Current user's password
var music = ""; // Temporary storage for music input
const APIURL = `http://localhost:8000`; // Base URL for the API
var STATEBATTLECARD = ""; // Current application state
var cardId1 = ""; // First card ID for battle system
var username2 = ""; // Second username for battle system
var cardId2 = ""; // Second card ID for battle system
var recordingBox = []; // Stores recorded audio chunks
var recordingWebButtonWrapper = ""; // Wrapper for the recording web button
let recorder; // Recorder instance for audio recording
let audioContext; // Audio context for handling audio streams
let stream; // Media stream for audio input
var recordData = ""; //String data get from recording audio by the Pet or anywhere else except Recording Page

const handlePetRecordingRouteFunc = createDynamicFunction(
  submitRecordingWeb,
  "pet"
);
const handlePetStopRecordingRouteFunc = createDynamicFunction(
  submitStopRecording,
  "pet"
);
const handleRecordingPageRecordingRouteFunc = createDynamicFunction(
  submitRecordingWeb,
  "recordingPage"
);
const handleRecordingPageStopRecordingRouteFunc = createDynamicFunction(
  submitStopRecording,
  "recordingPage"
);

//All the existing functions that are used in the HTML file

// Function to handle initial page load and user count check
function loadingPageBasedOnUserCount() {
  console.log("Loading page based on user count...");

  //run numberOfUsers route
  fetch("http://localhost:8000/numberOfUsers")
    .then((response) => response.json())
    .then((data) => {
      numberOfUsers = data.userCount || 0; // Get the user count from the response, default to 0 if not present
      //unable to assign null to userCount therefore assign 0 to it
      if (data.userCount == null || data.userCount == 0) {
        console.log("User count data received:");
        data.userCount = 0;
        headLine.innerHTML =
          "Welcome to my~~~~ Worldddddd! Are you ready to dip into the world of music?Click on me to hop on!";
        headLine.addEventListener("click", function () {
          openLoginPage();
          musicWebsite.removeChild(headLine);
        });
      } else if (data.userCount > 0) {
        //if already got data, move to the login part.
        musicWebsite.removeChild(headLine);
        openLoginPage();
      }
    })
    //in case there is an error
    .catch((error) => console.error("Fetch error:", error));
}

// Function to handle user login form submission
function submitLogin(event) {
  // Get the input value and modify it
  let userNameInput = inputUserName.value;
  let passWordInput = inputPassWord.value;
  username = userNameInput;
  password = passWordInput;

  event.preventDefault(); // Stop normal form submission

  //Function to handle the login form submission
  //making the url
  let url = `http://localhost:8000/checkingUser/?username=${encodeURIComponent(
    userNameInput
  )}&password=${encodeURIComponent(passWordInput)}`;
  fetch(url, {
    method: "GET",
  })
    //Handle the response
    .then(async (response) => {
      
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      return response.json();
    })
    .then((data) => {
      if(data.message == "Login successful"){
      form.removeEventListener("submit", submitLogin);
      console.log("Login successful:", data);
      //open the welcome page
      openWelcomePage();
      submitButton.removeEventListener("click", submitLogin);
      signUpButtonWrapper.removeEventListener("click", openSignUpPage);
      submitButton.type = "button";

      //Pet created
      body.appendChild(pet);}
      else{
        console.error("Error:", data.message);
        resetFormValue()
      }
    });
}

// Function to handle new user registration
function submitSignup(event) {
  event.preventDefault(); // Stop normal form submission

  // Get the input value and modify it
  let userNameInput = inputUserName.value;
  let passWordInput = inputPassWord.value;
  username = userNameInput;
  password = passWordInput;

  // Create the URL with values from the input fields
  let url = `http://localhost:8000/addUser/?username=${encodeURIComponent(
    userNameInput
  )}&password=${encodeURIComponent(passWordInput)}`;

  // send a POST request to the Python backend
  fetch(url, {
    method: "POST",
  })
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      tempVar = safeBase64Decode(response.headers.get("header"));
      console.log(tempVar)
      return response.blob();
    })

    .then((audioBlob) => {
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();

      form.removeEventListener("submit", submitSignup);
      openWelcomePage();
      submitButton.removeEventListener("click", submitSignup);
      signUpButtonWrapper.removeEventListener("click", openLoginPage);
      submitButton.type = "button";

      //Pet created
      body.appendChild(pet);
    });
}

// Function to display the login page interface
function openLoginPage() {
  resetFormValue();

  console.log("Open login page");

  musicWebsite.appendChild(form);

  //Form label setup
  if (form.contains(document.getElementsByClassName("userNames")[0])) {
    document.getElementsByClassName("userNames")[0].innerHTML =
      "May I have your account name please?";
    document.getElementsByClassName("passWords")[0].innerHTML =
      "Tell me a secret. *Your password*";
  }

  //Form setup
  form.appendChild(signUpButtonWrapper);
  if (musicWebsite.contains(musicContainer))
    musicWebsite.removeChild(musicContainer);
  if (!form.contains(inputPassWordWrapper))
    form.appendChild(inputPassWordWrapper);

  //Handling submit button
  submitButton.innerHTML = "Songs comin for ya!";
  signUpButtonWrapper.removeEventListener("click", openLoginPage);
  signUpButtonWrapper.addEventListener("click", openSignUpPage);
  submitButton.addEventListener("click", submitLogin);
  submitButton.removeEventListener("click", submitSignup);
}

// Function to display the signup page interface
function openSignUpPage() {
  resetFormValue();

  //Form label setup
  document.getElementsByClassName("userNames")[0].innerHTML =
    "Time to sign up your username!";
  document.getElementsByClassName("passWords")[0].innerHTML =
    "And your password?";

  //submit button setup
  submitButton.removeEventListener("click", submitLogin);
  submitButton.addEventListener("click", submitSignup);
  signUpButton.innerHTML = "Thinking again?";
  signUpButtonWrapper.removeEventListener("click", openSignUpPage);
  signUpButtonWrapper.addEventListener("click", openLoginPage);
}

// Function to display the welcome page after successful login/signup
async function openWelcomePage() {
  resetFormValue();
  getAllUserMusic();
  await musicWebsite.prepend(musicContainer);

  backGroundManagement("music");

  //tke time till we need it again so but here to avoid error when we need to open Welcome page again
  if (form.contains(labelInputPassWord)) form.removeChild(labelInputPassWord);
  if (form.contains(inputPassWordWrapper))
    form.removeChild(inputPassWordWrapper);
  if (!form.contains(signUpButtonWrapper))
    form.appendChild(signUpButtonWrapper);

  //Form the label setup

  document.getElementsByClassName("userNames")[0].innerHTML =
    "Welcome " + username + "!";
  if (form.contains(inputUserNameWrapper))
    form.removeChild(inputUserNameWrapper);

  submitButton.innerHTML = "You want to add more music?";
  submitButton.addEventListener("click", openAddMusicPage);

  signUpButton.innerHTML = "Wanna have some games?";
  signUpButton.addEventListener("click", openChessGamePage);

  //AiWEB Related Setup Button
  if (!musicWebsite.contains(document.getElementById("aiWebButton"))) {
    aiWebButtonWrapper = await document.createElement("div");
    aiWebButton = document.createElement("button");
    aiWebButton.type = "button";
    aiWebButton.id = "aiWebButton";
    aiWebButton.innerHTML = "Wanna have some AI helps?";
    aiWebButtonWrapper.className = "button";
    aiWebButtonWrapper.id = "aiWebButtonWrapper";
    aiWebButtonWrapper.appendChild(aiWebButton);
    form.appendChild(aiWebButtonWrapper);
    aiWebButton.addEventListener("click", openAiPage);
    aiWebButtonWrapper = document.getElementById("aiWebButtonWrapper");
  }

  //Recording Related Setup Button
  if (!musicWebsite.contains(document.getElementById("recordingWebButton"))) {
    recordingWebButtonWrapper = document.createElement("div");
    const recordingWebButton = document.createElement("button");
    recordingWebButton.type = "button";
    recordingWebButton.id = "recordingWebButton";
    recordingWebButton.innerHTML = "Wanna record your own music?";
    recordingWebButtonWrapper.className = "button";
    recordingWebButtonWrapper.id = "recordingWebButtonWrapper";
    recordingWebButtonWrapper.appendChild(recordingWebButton);
    form.appendChild(recordingWebButtonWrapper);
    recordingWebButton.addEventListener("click", openRecordingPage);
    recordingWebButtonWrapper = document.getElementById(
      "recordingWebButtonWrapper"
    );
  }

  //Casino Related Setup Button
  if (!musicWebsite.contains(document.getElementById("casinoWebButton"))) {
    const casinoWebButtonWrapper = document.createElement("div");
    const casinoWebButton = document.createElement("button");
    casinoWebButton.type = "button";
    casinoWebButton.id = "casinoWebButton";
    casinoWebButton.innerHTML = "A bit gambling stream coming??";
    casinoWebButtonWrapper.className = "button";
    casinoWebButtonWrapper.id = "casinoWebButtonWrapper";
    casinoWebButtonWrapper.appendChild(casinoWebButton);
    casinoWebButtonWrapper.addEventListener("click", openCasinoPage);
    form.appendChild(casinoWebButtonWrapper);
  }

  //Shop Related Setup Button
  if (!musicWebsite.contains(document.getElementById("shopWebButton"))) {
    const shopWebButtonWrapper = document.createElement("div");
    const shopWebButton = document.createElement("button");
    shopWebButton.type = "button";
    shopWebButton.id = "shopWebButton";
    shopWebButton.innerHTML = "Odd to buy some cash?";
    shopWebButtonWrapper.className = "button";
    shopWebButtonWrapper.id = "shopWebButtonWrapper";
    shopWebButtonWrapper.appendChild(shopWebButton);
    shopWebButtonWrapper.addEventListener("click", openShopPage);
    form.appendChild(shopWebButtonWrapper);
  }

  //Image Extractor Setup Button
  if (!musicWebsite.contains(document.getElementById("imageExtractorWebButton"))) {
    const imageExtractorWebButtonWrapper = document.createElement("div");
    const imageExtractorWebButton = document.createElement("button");
    imageExtractorWebButton.type = "button";
    imageExtractorWebButton.id = "imageExtractorWebButton";
    imageExtractorWebButton.innerHTML = "Wanna extract image from music?";
    imageExtractorWebButtonWrapper.className = "button";
    imageExtractorWebButtonWrapper.id = "imageExtractorWebButtonWrapper";
    imageExtractorWebButtonWrapper.appendChild(imageExtractorWebButton);
    imageExtractorWebButtonWrapper.addEventListener(
      "click",
      openImageExtractorPage
    );
    form.appendChild(imageExtractorWebButtonWrapper);
  }
}

// Function to display the music addition page
function openAddMusicPage() {
  backGroundManagement("musicAddDelete");

  resetFormValue();

  addReturnWelcomePageButton();

  addButton.addEventListener("click", addMusic);
  deleteButton.addEventListener("click", deleteMusic);
}

// Function to add new music to user's collection
async function addMusic() {
  // Get the input value and modify it
  music = musicInput.value;

  //Checking if there is data or not
  if (!music) console.log("Mei you shenme le!");

  // Create the URL with values from the input fields
  let url = `http://localhost:8000/addMusic/?username=${encodeURIComponent(
    username
  )}&userMusic=${encodeURIComponent(music)}`;

  // send a POST request to the Python backend
  await fetch(url, {
    method: "POST",
  })
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      getAllUserMusic();
      console.log(safeBase64Decode(response.headers.get("header")));
      return response.blob();
    })
    .then((audioBlob) => {
      const audioURL = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioURL);
      // Return the promise from getAllUserMusic
      audio.play();
    });
}

// Function to remove music from user's collection
async function deleteMusic() {
  // Get the current music value from the input field
  const music = musicInput.value;

  //Checking if there is data or not
  if (!music) {
    console.log("Mei you shenme le!");
    return; // Exit the function if no music is specified
  }

  //Making an url for fetching
  let url = `http://localhost:8000/deleteMusic/?username=${encodeURIComponent(
    username
  )}&musicId=${encodeURIComponent(music)}`;

  // send a POST request to the Python backend
  await fetch(url, {
    method: "DELETE",
  })
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      getAllUserMusic();
      console.log(
        "Music Deleted: " + safeBase64Decode(response.headers.get("header"))
      );
      return response.blob();
    })
    .then((audioBlob) => {
      const audioURL = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioURL);
      // Return the promise from getAllUserMusic
      audio.play();
    })
    .catch((error) => console.error("Error deleting card: ", error));
}

// Function to reset form input values
function resetFormValue() {
  //Reset data
  for (var i = 0; i < inputs.length; i++) inputs[i].value = "";
}

// Function to fetch and display all user's music
function getAllUserMusic() {
  fetch(
    `http://localhost:8000/getAllUserMusic/?username=${encodeURIComponent(
      username
    )}`
  )
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      return response.json();
    })
    .then((data) => {
      // Assuming the response is a JSON object with a 'music' property
      musicList = data[0].userMusic || []; // Use an empty array if 'music' is not present
      // Clear previous music list
      musicContainer.innerHTML = "Your Music List:";

      // Populate the music list
      musicList.forEach((music) => {
        const musicItem = document.createElement("li");
        musicItem.style.fontSize = "20px";
        musicItem.innerHTML = music.userMusic + " (" + music.musicId + ")";
        musicContainer.appendChild(musicItem);

        // Creating a redirecting Button
        const youtubeRedirectingButton = document.createElement("button");
        youtubeRedirectingButton.innerHTML =
          "Teleporting to " + music.userMusic;
        youtubeRedirectingButton.className = "youtubeRedirectingButton";
        youtubeRedirectingButton.addEventListener("click", function () {
          window.open(
            `https://www.youtube.com/watch?v=${music.musicId}`,
            "_blank"
          );
          gettingMusicShard();
        });
        musicItem.appendChild(document.createElement("br"));
        musicItem.appendChild(youtubeRedirectingButton);
      });
    })
    .catch((error) => console.error("Fetch error:", error));
  console.log("Music List:", musicList);
}

// Function to upgrade + collect musicShard
function gettingMusicShard() {
  fetch(
    `http://localhost:8000/levelUp/?username=${encodeURIComponent(username)}`
  ).then(async (response) => {
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData.detail); // This is what FastAPI sets
      throw new Error(errorData.detail);
    }
  });
}

// Function to open the chess game interface
function openChessGamePage(event) {
  event.preventDefault();

  if (!body.contains(chessGameWeb)) body.appendChild(chessGameWeb);
  if (body.contains(musicWebsite)) body.removeChild(musicWebsite);
  if (body.contains(aiWeb)) body.removeChild(aiWeb);
  if (body.contains(musicAddDeleteWeb)) body.removeChild(musicAddDeleteWeb);
  if (body.contains(recordingWeb)) body.removeChild(recordingWeb);

  addReturnWelcomePageButton();

  resetFormValue();

  addCard.addEventListener("click", openAddCardPage);
  removeCard.addEventListener("click", openRemoveCardPage);
  battleCards.addEventListener("click", openBattleCardPage);

  getAllUsersCards();
}

// Function to fetch all user cards for the game
function getAllUsersCards() {
  fetch(
    `http://localhost:8000/getAllUserCards/?userName=${encodeURIComponent(
      username
    )}`
  )
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      return response.json();
    })
    .then((data) => {
      // Assuming the response is a JSON object with a 'music' property
      const cards = data[0].card || []; // Use an empty array if 'music' is not present
      // Clear previous music list
      allUsersCards.innerHTML = "Your Cards List:";

      // Populate the music list
      cards.forEach((card) => {
        const cardItem = document.createElement("li");
        cardItem.innerHTML =
          "Card Name: " +
          card.cardName +
          "<br>" +
          "Card Id: " +
          card.cardId +
          "<br>" +
          "Power: " +
          card.power;
        allUsersCards.appendChild(cardItem);
      });
    })
    .catch((error) => console.error("Fetch error:", error));
}

// Function to display the card addition interface
function openAddCardPage() {
  resetFormValue();

  if (!addCard.contains(document.getElementById("inputAddCard"))) {
    const inputAddCard = document.createElement("input");
    inputAddCard.id = "inputAddCard";
    document.getElementById("addCard").appendChild(inputAddCard);
    const buttonAddCard = document.createElement("button");
    document.getElementById("addCard").appendChild(buttonAddCard);
    buttonAddCard.style.height = "20px";
    buttonAddCard.style.width = "18px";
    buttonAddCard.id = "buttonAddCard";
    buttonAddCard.innerHTML = "+"; // Add text to the button
    buttonAddCard.addEventListener("click", submitAddCard);
    addCard.removeEventListener("click", openAddCardPage);
  }
}

// Function to display the card removal interface
function openRemoveCardPage() {
  resetFormValue();

  if (!removeCard.contains(document.getElementById("inputRemoveCard"))) {
    const inputRemoveCard = document.createElement("input");
    inputRemoveCard.id = "inputRemoveCard";
    document.getElementById("removeCard").appendChild(inputRemoveCard);
    const buttonRemoveCard = document.createElement("button");
    document.getElementById("removeCard").appendChild(buttonRemoveCard);
    buttonRemoveCard.style.height = "20px";
    buttonRemoveCard.style.width = "18px";
    buttonRemoveCard.id = "buttonRemoveCard";
    buttonRemoveCard.innerHTML = "+"; // Add text to the button
    buttonRemoveCard.addEventListener("click", submitRemoveCard);
    removeCard.removeEventListener("click", openRemoveCardPage);
  }
}

// Function to handle adding new cards
function submitAddCard() {
  const cardId = document.getElementById("inputAddCard").value;

  fetch(
    `http://localhost:8000/addCard/?userName=${encodeURIComponent(
      username
    )}&musicId=${encodeURIComponent(cardId)}&shardRequired=${encodeURIComponent(
      150
    )}`,
    {
      method: "POST",
    }
  )
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      getAllUsersCards();
      console.log(safeBase64Decode(response.headers.get("header")));
      return response.blob();
    })
    .then((audioBlob) => {
      console.log("Blob type:", audioBlob.type);
      console.log("Blob size:", audioBlob.size);
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    })
    .catch((error) => {
      console.error("Error adding card:", error);
    })
    .finally(() => {
      // Clean up elements regardless of success/failure
      const inputElement = document.getElementById("inputAddCard");
      const buttonElement = document.getElementById("buttonAddCard");
      if (inputElement) addCard.removeChild(inputElement);
      if (buttonElement) addCard.removeChild(buttonElement);
      addCard.addEventListener("click", openAddCardPage);
    });
}

// Function to handle removing cards
function submitRemoveCard() {
  const cardId = document.getElementById("inputRemoveCard").value;

  fetch(
    `http://localhost:8000/removeCard/?userName=${encodeURIComponent(
      username
    )}&cardId=${encodeURIComponent(cardId)}`,
    {
      method: "GET",
    }
  )
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      getAllUsersCards();

      console.log(
        "Card removed is " + safeBase64Decode(response.headers.get("header"))
      );
      return response.blob();
    })
    .then((audioBlob) => {
      console.log("Blob type:", audioBlob.type);
      console.log("Blob size:", audioBlob.size);
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();

      console.log("Card removed successfully!");
      getAllUsersCards(); // Refresh the cards list
    })
    .finally(() => {
      // Clean up elements regardless of success/failure
      const inputElement = document.getElementById("inputRemoveCard");
      const buttonElement = document.getElementById("buttonRemoveCard");
      if (inputElement) removeCard.removeChild(inputElement);
      if (buttonElement) removeCard.removeChild(buttonElement);
      removeCard.addEventListener("click", openRemoveCardPage);
    });
}

// Function to handle card battle submissions
function submitBattleButtonCard(value) {
  console.log("Current STATE:", STATEBATTLECARD);
  console.log("Input value:", value);
  if (!value || value.trim() === "") {
    console.error("Please enter a valid value");
    return false;
  }

  switch (STATEBATTLECARD) {
    case "player1 card":
      cardId1 = value;
      break;
    case "player2 name":
      username2 = value;
      break;
    case "player2 card":
      cardId2 = value;
      break;
  }
  return true;
}

// Function to reset the battle state
function resetBattleState() {
  STATEBATTLECARD = "";
  cardId1 = "";
  username2 = "";
  cardId2 = "";
}

// Function to display the card battle interface
function openBattleCardPage() {
  if (!battleCards.contains(document.getElementById("inputBattleCards"))) {
    resetFormValue();

    const inputBattleCards = document.createElement("input");
    inputBattleCards.id = "inputBattleCards";
    document.getElementById("battleCards").appendChild(inputBattleCards);

    const buttonBattleCards = document.createElement("button");
    document.getElementById("battleCards").appendChild(buttonBattleCards);
    buttonBattleCards.style.height = "20px";
    buttonBattleCards.style.width = "18px";
    buttonBattleCards.id = "buttonBattleCards";
    buttonBattleCards.innerHTML = "+"; // Add  to the button

    battleCards.removeEventListener("click", openBattleCardPage);
    buttonBattleCards.addEventListener("click", openBattleCardPage);
  }

  if (STATEBATTLECARD == "") {
    STATEBATTLECARD = "player1 card";
    inputBattleCards.placeholder = "Enter your card ID";
  } else if (STATEBATTLECARD == "player1 card") {
    if (!submitBattleButtonCard(inputBattleCards.value)) return;
    inputBattleCards.value = "";
    STATEBATTLECARD = "player2 name";
    inputBattleCards.placeholder = "Enter opponent's username";
  } else if (STATEBATTLECARD == "player2 name") {
    if (!submitBattleButtonCard(inputBattleCards.value)) return;
    STATEBATTLECARD = "player2 card";
    inputBattleCards.value = "";
    inputBattleCards.placeholder = "Enter opponent's card ID";
  } else if (STATEBATTLECARD == "player2 card") {
    if (!submitBattleButtonCard(inputBattleCards.value)) return;
    inputBattleCards.value = "";
    battleCards.removeChild(inputBattleCards);
    battleCards.removeChild(buttonBattleCards);
    battleCards.addEventListener("click", openBattleCardPage);
    battleCards.removeEventListener("click", openBattleCardPage);

    fetch(
      `http://localhost:8000/battleCard/?userName1=${encodeURIComponent(
        username
      )}&userName2=${encodeURIComponent(
        username2
      )}&cardId1=${encodeURIComponent(cardId1)}&cardId2=${encodeURIComponent(
        cardId2
      )}`
    )
      .then(async (response) => {
        if (!response.ok) {
          const errorData = await response.json();
          console.error("Error:", errorData.detail); // This is what FastAPI sets
          throw new Error(errorData.detail);
        }

        console.log(
          "Battle result: " + safeBase64Decode(response.headers.get("header"))
        );
        const result =
          safeBase64Decode(response.headers.get("header")) || "Unknown result";
        //Display battle result to user
        const resultDiv = document.createElement("div");
        resultDiv.id = "temporaryDiv";
        resultDiv.innerHTML = `Battle Result: ${result}`;
        battleCards.appendChild(resultDiv);
        return response.blob();
      })
      .then((audioBlob) => {
        console.log("Blob type:", audioBlob.type);
        console.log("Blob size:", audioBlob.size);
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();

        getAllUsersCards();
        //Refresh the cards list
        //Clean up after 3 seconds
        setTimeout(() => {
          divToRemove = document.getElementById("temporaryDiv");
          battleCards.removeChild(divToRemove);
        }, 6000);
      })

      .catch((error) => {
        console.error("Error in battle:", error);
        const errorDiv = document.createElement("div");
        errorDiv.innerHTML = `Error: ${error.message}`;
        errorDiv.style.color = "red";
        battleCards.appendChild(errorDiv);
        // Clean up error message after 3 seconds
        setTimeout(() => {
          battleCards.removeChild(errorDiv);
        }, 5000);
      })
      .finally(() => {
        resetBattleState(); // Reset all state variables
      });
  }
}

// Function to add a return button to welcome page
async function addReturnWelcomePageButton() {
  //Normal prop
  if (
    !document
      .getElementsByClassName("backGround")[0]
      .contains(document.getElementById("returnButton"))
  ) {
    if (
      !document
        .getElementsByClassName("backGround")[0]
        .contains(document.getElementById("returnButtonWrapper"))
    ) {
      let returnButtonWrapper = document.createElement("div");
      returnButtonWrapper.className = "input";
      returnButtonWrapper.id = "returnButtonWrapper";
      document
        .getElementsByClassName("backGround")[0]
        .appendChild(returnButtonWrapper);
    }

    let returnButton = document.createElement("button");
    returnButton.id = "returnButton";
    returnButton.innerHTML = "Back to the Welcome town";
    returnButton.addEventListener("click", returnToWelcomePage);
    returnButtonWrapper.appendChild(returnButton);
  }
}

// Function to return to the welcome page
function returnToWelcomePage() {
  if (!body.contains(musicAddDeleteWeb)) {
    for (let i of Array.from(document.getElementsByTagName("input"))) {
      i.remove();
    }

    for (let i of Array.from(document.getElementsByTagName("button"))) {
      i.remove();
    }
    for (let i of Array.from(document.getElementsByTagName("select"))) {
      i.remove();
    }
    document.getElementById("returnButtonWrapper").remove();
  }

  backGroundManagement("welcome");

  openWelcomePage();
}

// Function to open the AI features page
function openAiPage() {
  backGroundManagement("ai");

  addReturnWelcomePageButton();

  recommendMusic.addEventListener("click", openRecommendMusicPage);
  pickMusic.addEventListener("click", openPickMusicPage);
}

// Function to open the music recommendation page
function openRecommendMusicPage() {
  if (!recommendMusic.contains(document.getElementById("inputQuery"))) {
    const inputQuery = document.createElement("input");
    inputQuery.id = "inputQueryRecommend";
    recommendMusic.appendChild(inputQuery);
    const buttonQuery = document.createElement("button");
    recommendMusic.appendChild(buttonQuery);
    buttonQuery.style.height = "20px";
    buttonQuery.style.width = "18px";
    buttonQuery.id = "buttonQueryRecommend";
    buttonQuery.innerHTML = "+"; // Add text to the button
    buttonQuery.addEventListener("click", (query) =>
      submitQueryRecommendMusic(inputQuery.value, query)
    );
    recommendMusic.removeEventListener("click", openRecommendMusicPage);
  }
}

// Function to handle music recommendation queries
function submitQueryRecommendMusic(query) {
  //Write the message to the chat box      
  let messageBox = document.createElement("li")
  messageBox.textContent = query
  chatBox.appendChild(messageBox)
  socket.emit("response", {"message":query})
  fetch(
    `http://localhost:8000/aiSuggestMusic/`,
    {
      method: "POST",
    }
  )
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      const answer = safeBase64Decode(response.headers.get("header"));

      // Remove loading message
      recommendMusic.removeChild(loadingDiv);
      
      // Remove the result after 10 seconds
      setTimeout(() => {
        if (recommendMusic.contains(resultDiv)) {
          recommendMusic.removeChild(resultDiv);
        }
      }, 10000);
      return response.blob();
    })
    .then((audioBlob) => {
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    })
    .catch((error) => {
      // Remove loading message
      recommendMusic.removeChild(loadingDiv);

      // Create error message
      const errorDiv = document.createElement("div");
      errorDiv.innerHTML = `Error: ${error.message}`;
      errorDiv.style.color = "red";
      recommendMusic.appendChild(errorDiv);

      // Remove the error message after 5 seconds
      setTimeout(() => {
        if (recommendMusic.contains(errorDiv)) {
          recommendMusic.removeChild(errorDiv);
        }
      }, 5000);
    });
}

// Function to open the music picker page
function openPickMusicPage() {
  if (!pickMusic.contains(document.getElementById("inputQuery"))) {
    console.log("gay");

    const inputQuery = document.createElement("input");
    inputQuery.id = "inputQueryPick";

    pickMusic.appendChild(inputQuery);
    const buttonQuery = document.createElement("button");
    pickMusic.appendChild(buttonQuery);

    buttonQuery.style.height = "20px";
    buttonQuery.style.width = "18px";
    buttonQuery.id = "buttonQueryPick";
    buttonQuery.innerHTML = "+"; // Add text to the button

    buttonQuery.addEventListener("click", (query) =>
      submitQueryPickMusic(inputQuery.value, query)
    );
    pickMusic.removeEventListener("click", openPickMusicPage);
  }
}

// Function to handle music picker queries
function submitQueryPickMusic(query) {
  // Create loading message
  const loadingDiv = document.createElement("div");
  loadingDiv.innerHTML = "Searching for music picks...";
  loadingDiv.style.color = "blue";
  pickMusic.appendChild(loadingDiv);

  fetch(
    `http://localhost:8000/aiPickMusic/?username=${encodeURIComponent(
      username
    )}&query=${encodeURIComponent(query)}`,
    {
      method: "POST",
    }
  )
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      const answer = safeBase64Decode(response.headers.get("header"));

      // Remove loading message
      pickMusic.removeChild(loadingDiv);

      // Create success message with recommendations
      const resultDiv = document.createElement("div");
      resultDiv.innerHTML = `Recommendations: ${answer}`;
      resultDiv.style.color = "green";
      pickMusic.appendChild(resultDiv);

      // Remove the result after 10 seconds
      setTimeout(() => {
        if (pickMusic.contains(resultDiv)) {
          pickMusic.removeChild(resultDiv);
        }
      }, 10000);
      return response.blob();
    })
    .then((audioBlob) => {
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    })

    .catch((error) => {
      // Remove loading message
      pickMusic.removeChild(loadingDiv);

      // Create error message
      const errorDiv = document.createElement("div");
      errorDiv.innerHTML = `Error: ${error.message}`;
      errorDiv.style.color = "red";
      pickMusic.appendChild(errorDiv);

      // Remove the error message after 5 seconds
      setTimeout(() => {
        if (pickMusic.contains(errorDiv)) {
          pickMusic.removeChild(errorDiv);
        }
      }, 5000);
    });
}

//Function level Up pet when clicked
function levelUp() {
  pet.removeEventListener("click", levelUp);
  pet.addEventListener("click", handlePetRecordingRouteFunc);

  fetch(
    `http://localhost:8000/levelUp/?username=${encodeURIComponent(username)}`,
    {
      method: "POST",
    }
  )
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      console.log(safeBase64Decode(response.headers.get("header")));
      return response.blob();
    })
    .then((audioBlob) => {
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
    })
    .catch((error) => console.log(error));
}

//Extra decode stuff from AI ChatGPT generated
function safeBase64Decode(encoded) {
  const binary = atob(encoded); // base64 → binary string
  const bytes = Uint8Array.from(binary, (c) => c.charCodeAt(0)); // binary → byte array
  return new TextDecoder().decode(bytes); // bytes → Unicode string
}

//Function to open the recording page
function openRecordingPage() {
  backGroundManagement("recording");

  //Add the recording web button
  if (!recordingWeb.contains(document.getElementById("startRecordingWeb"))) {
    startRecordingWeb = document.createElement("button");
    startRecordingWeb.type = "button";
    startRecordingWeb.id = "startRecordingWeb";
    startRecordingWeb.innerHTML = "Start Recording";
    recordingWeb.appendChild(startRecordingWeb);
    startRecordingWeb.addEventListener(
      "click",
      handleRecordingPageRecordingRouteFunc
    );

    //Add the select language option
    const selectLanguage = document.createElement("select");
    selectLanguage.id = "selectLanguage";
    recordingWeb.appendChild(selectLanguage);
    const optionEnglish = document.createElement("option");
    optionEnglish.value = "en";
    optionEnglish.text = "English";
    selectLanguage.appendChild(optionEnglish);
    const optionVietnamese = document.createElement("option");
    optionVietnamese.value = "vi";
    optionVietnamese.text = "Vietnamese";
    selectLanguage.appendChild(optionVietnamese);
    const optionChinese = document.createElement("option");
    optionChinese.value = "zh";
    optionChinese.text = "Chinese";
    selectLanguage.appendChild(optionChinese);
    const optionJapanese = document.createElement("option");
    optionJapanese.value = "ja";
    optionJapanese.text = "Japanese";
    selectLanguage.appendChild(optionJapanese);
  }
  //Return home button
  addReturnWelcomePageButton();
}

async function submitRecordingWeb(routeRecord) {
  console.log(routeRecord);

  //Specify where did the recording button was clicked

  if (routeRecord == "recordingPage") {
    const btn = document.getElementById("startRecordingWeb");
    btn.removeEventListener("click", handleRecordingPageRecordingRouteFunc);
    btn.innerHTML = "Stop Recording";
    btn.addEventListener("click", handleRecordingPageStopRecordingRouteFunc);
  } else if (routeRecord == "pet") {
    pet.addEventListener("click", handlePetStopRecordingRouteFunc);
    pet.removeEventListener("click", handlePetRecordingRouteFunc);
  }

  // Request microphone access
  stream = await navigator.mediaDevices.getUserMedia({ audio: true });

  // Create audio context with 16kHz sample rate
  audioContext = new (window.AudioContext || window.webkitAudioContext)({
    sampleRate: 16000,
  });

  // Connect mic stream
  const input = audioContext.createMediaStreamSource(stream);

  // Initialize Recorder.js
  recorder = new Recorder(input, { numChannels: 1 }); // mono channel
  recorder.record();
}

async function submitStopRecording(routeRecord) {
  if (routeRecord == "recordingPage") {
    const btn = document.getElementById("startRecordingWeb");
    btn.addEventListener("click", handleRecordingPageRecordingRouteFunc);
    btn.innerHTML = "Start Recording";
    btn.removeEventListener("click", handleRecordingPageStopRecordingRouteFunc);
    var language = document.getElementById("selectLanguage").value;
  } else if (routeRecord == "pet") {
    pet.removeEventListener("click", handlePetStopRecordingRouteFunc);
    pet.addEventListener("click", handlePetRecordingRouteFunc);
    var language = en;
  }
  recorder.stop();

  recorder.exportWAV(async (blob) => {
    const formData = new FormData();
    formData.append("audioFile", blob, "recording.wav");

    const response = await fetch(
      `http://localhost:8000/getRecord/?language=${encodeURIComponent(
        language
      )}`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error:", errorData.detail); // This is what FastAPI sets
      throw new Error(errorData.detail);
    }

    let tempVar = safeBase64Decode(response.headers.get("header"));
    console.log(tempVar);

    if (routeRecord == "recordingPage") creatingRecordList(tempVar);
    else if (routeRecord == "pet") {
      for (const i of document.getElementsByTagName("input")) {
        i.value = tempVar;
      }
    }
    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
  });

  stream.getTracks().forEach((track) => track.stop());
}

function creatingRecordList(answer) {
  let tempVar = document.getElementById("recordingList");
  if (!recordingWeb.contains(tempVar)) {
    let tempVarForHeadList = document.createElement("ul");
    tempVarForHeadList.id = "recordingList";
    tempVarForHeadList.innerHTML = "Recording List";
    recordingWeb.insertBefore(tempVarForHeadList, returnButtonWrapper);
    tempVar = tempVarForHeadList;
  }

  let tempVarForList = document.createElement("li");
  tempVarForList.innerHTML = answer;
  tempVar.appendChild(tempVarForList);
}

function createDynamicFunction(functionName, sourceResource) {
  return function wrapperFunction(event) {
    functionName(sourceResource, event);
  };
}

function backGroundManagement(event) {
  if (body.contains(casinoWeb)) body.removeChild(casinoWeb);
  if (body.contains(musicWebsite)) body.removeChild(musicWebsite);
  if (body.contains(recordingWeb)) body.removeChild(recordingWeb);
  if (body.contains(aiWeb)) body.removeChild(aiWeb);
  if (body.contains(musicAddDeleteWeb)) body.removeChild(musicAddDeleteWeb);
  if (body.contains(chessGameWeb)) body.removeChild(chessGameWeb);
  if (body.contains(shopWeb)) body.removeChild(shopWeb);
  if (body.contains(imageExtractorWeb)) body.removeChild(imageExtractorWeb);

  switch (event) {
    case "casino":
      body.appendChild(casinoWeb);
      break;
    case "music":
      body.appendChild(musicWebsite);
      break;
    case "recording":
      body.appendChild(recordingWeb);
      break;
    case "ai":
      body.appendChild(aiWeb);
      break;
    case "musicAddDelete":
      body.appendChild(musicAddDeleteWeb);
      break;
    case "chessGame":
      body.appendChild(chessGameWeb);
      break;
    case "shop":
      body.appendChild(shopWeb);
      break;
    case "imageExtractor":
      body.appendChild(imageExtractorWeb);
      break;
  }
}
function openCasinoPage() {
  backGroundManagement("casino");
  lowerOrHigher.addEventListener("click", openPlayLowerOrHigherPage);
  addReturnWelcomePageButton();
}

function openPlayLowerOrHigherPage() {
  resetFormValue();

  if (!lowerOrHigher.contains(document.getElementById("inputLowerOrHigher"))) {
    // Create input field
    const inputLowerOrHigher = document.createElement("input");
    inputLowerOrHigher.id = "inputLowerOrHigher";
    lowerOrHigher.appendChild(inputLowerOrHigher);
    const buttonLowerOrHigher = document.createElement("button");
    lowerOrHigher.appendChild(buttonLowerOrHigher);
    buttonLowerOrHigher.style.height = "20px";
    buttonLowerOrHigher.style.width = "18px";
    buttonLowerOrHigher.id = "buttonAddCard";
    buttonLowerOrHigher.innerHTML = "+"; // Add text to the button
    buttonLowerOrHigher.addEventListener("click", submitPlayLowerOrHigher);
    addCard.removeEventListener("click", openPlayLowerOrHigherPage);

    // Create select field
    const selectLowerOrHigher = document.createElement("select");
    selectLowerOrHigher.id = "selectLowerOrHigher";
    lowerOrHigher.appendChild(selectLowerOrHigher);
    const optionLower = document.createElement("option");
    optionLower.value = "Lower";
    optionLower.text = "Lower";
    selectLowerOrHigher.appendChild(optionLower);
    const optionHigher = document.createElement("option");
    optionHigher.value = "Higher";
    optionHigher.text = "Higher";
    const optionSame = document.createElement("option");
    optionSame.value = "Same";
    optionSame.text = "Same";
    selectLowerOrHigher.appendChild(optionHigher);
    selectLowerOrHigher.appendChild(optionSame);
  }
}

async function submitPlayLowerOrHigher() {
  let cardId = document.getElementById("inputLowerOrHigher").value;
  let guessing = document.getElementById("selectLowerOrHigher").value;

  let url = `http://localhost:8000/higherOrLower/?userName=${encodeURIComponent(
    username
  )}&cardId=${encodeURIComponent(cardId)}&guess=${encodeURIComponent(
    guessing
  )}`;
  const response = await fetch(url, {
    method: "POST",
  });
  if (!response.ok) {
    const errorData = await response.json();
    console.error("Error:", errorData.detail); // This is what FastAPI sets
    throw new Error(errorData.detail);
  }
  let tempVar = safeBase64Decode(response.headers.get("header"));
  console.log(tempVar);
  const audioBlob = await response.blob();
  const audioUrl = URL.createObjectURL(audioBlob);
  const audio = new Audio(audioUrl);
  audio.play();
}

async function openShopPage() {
  backGroundManagement("shop");

  getBanishedCardStocks();

  addReturnWelcomePageButton();
}

async function getBanishedCardStocks() {
  let url = `http://localhost:8000/getAllBanishedCard/?userName=${encodeURIComponent(
    username
  )}`;
  fetch(url, {
    method: "GET",
  })
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      return response.json();
    })
    .then((data) => {
      // Assuming the response is a JSON object with a 'music' property
      const cards = data[0].bannedCard || []; // Use an empty array if 'music' is not present
      // Clear previous music list
      buyBanishCard.innerHTML = "Your Banished Cards List:";
      // Populate the music list
      cards.forEach((card) => {
        const cardItem = document.createElement("li");
        const buyButton = document.createElement("button");
        buyButton.innerHTML = "Buy back " + card.cardName;
        buyCard = createDynamicFunction(buyBanishedCard, card.cardId);
        buyButton.addEventListener("click", buyCard);

        cardItem.innerHTML =
          "Card Name: " + card.cardName + "  |||  " + "Card Id: " + card.cardId;

        buyBanishCard.appendChild(cardItem);
        buyBanishCard.appendChild(buyButton);
      });
    });
}

function buyBanishedCard(cardId) {
  let url = `http://localhost:8000/buyBanishedCard/?userName=${encodeURIComponent(
    username
  )}&cardId=${encodeURIComponent(cardId)}&shardRequired=${encodeURIComponent(
    300
  )}`;
  fetch(url, {
    method: "GET",
  })
    .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      return response.blob();
    })
    .then((audioBlob) => {
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play();
      getBanishedCardStocks();
    });
}

async function openImageExtractorPage() {
  backGroundManagement("imageExtractor");

  imageExtractWrapper.innerHTML= ""
  let selectTypeOfInput = document.createElement("select");
  imageExtractWrapper.appendChild(selectTypeOfInput);

  const optionCV = document.createElement("option");
  optionCV.value = "CV";
  optionCV.text = "CV reader";
  selectTypeOfInput.appendChild(optionCV);

  let buttonImageExtractor = document.createElement("button");
  imageExtractWrapper.appendChild(buttonImageExtractor);

  buttonImageExtractor.type = "button"
  buttonImageExtractor.style.height = "20px";
  buttonImageExtractor.style.width = "auto";
  buttonImageExtractor.id = "buttonImageExtractor";
  buttonImageExtractor.innerHTML = "Add Image here"; // Add text to the button
  
  selectTypeOfInput.id = "selectTypeOfInput";
  buttonImageExtractor.addEventListener("click", openExtractingPage);
  buttonImageExtractor.removeEventListener("click", openImageExtractorPage);

  addReturnWelcomePageButton();
}

async function openExtractingPage(event) {

  if (!imageExtractorWeb.contains(document.getElementById("inputImageExtractor"))) {
    // Create input field
    const inputImageExtractor = document.createElement("input");
    inputImageExtractor.type = "file";
    inputImageExtractor.id = "inputImageExtractor";
    imageExtractWrapper.prepend(inputImageExtractor);

    let buttonImageExtractor = document.getElementById("buttonImageExtractor")
    let input = document.getElementById("selectTypeOfInput").value;
    if (input == "CV") {
      buttonImageExtractor.removeEventListener("click", openExtractingPage)
      buttonImageExtractor.addEventListener("click",submitCVReader)
    }}
  }

async function submitCVReader(event) {

  event.preventDefault();

  let inputToExtract = document.getElementById("inputImageExtractor");
  let fileToExtract = inputToExtract.files[0];
  if (!fileToExtract) return;

  let reader = new FileReader();
  reader.readAsDataURL(fileToExtract);
  reader.onload = function () {
    let url = `http://localhost:8000/store_image_file/?username=${encodeURIComponent(
    username
  )}`;
  fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      userName: username,
      fileName: fileToExtract.name,
      fileData: reader.result
    })
  })

  .then(async (response) => {
      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData.detail); // This is what FastAPI sets
        throw new Error(errorData.detail);
      }
      return response.json();
    })
    .then((data) => {
      console.log(data.message);
    })
}
}