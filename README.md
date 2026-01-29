# Boxing Champs

Boxing Champs is a narrative-driven, text-based role-playing game inspired by web browser titles like Torn and boxing games like Punch Club. Set in a fictional place named Glovegate City, the game invites players to carve out their legacy in a world where ambition, discipline, and consistency define success. With dedication, effort and skill training the game will advance you from an unknown fighter to a top contender in a vibrant boxing metropolis.

This is the final project developed for the course "CS50W: Web Programming with Python and JavaScript" from Harvard Online Courses. It is the result of months of curiosity, experimentation, and problem-solving that grew beyond its initial idea. I wanted to see how far I could push Django, a framework usually used for content-driven websites, into behaving like a living, responsive game. The result is this browser-based boxing RPG that merges backend logic with dynamic front-end interactivity. It’s a project I’m genuinely proud of because it challenged me to connect everything I had learned about databases, server communication, and user experience into one cohesive system that works in real time.

What makes this project stand out from other CS50W projects is how deeply it integrates backend structure, frontend dynamics, and game logic. Many projects in the course focus on straightforward applications (a search app, an e-commerce app, a wiki, etc), and although this project certainly uses those principles, it layers on top a continuous feedback loop between user actions, server validation, and instant visual response. Almost every button click represents a game mechanic (an event that modifies the database, recalculates stats and updates the interface live) and its complexity isn’t just in the number of lines of code, but in how every part depends on and communicates with the others. The result isn’t just a collection of features but a working system with interconnected rules, consequences, and timing.

This is my first work as a designer and a full-stack developer. I had to plan how data flows, how feedback feels, how pacing affects engagement...etc. It wasn’t just about making Django work, it was about stretching what a Django app can be. I built something interactive, persistent, and dynamic in an environment that isn’t usually used for games, and I did it (or at least tried to) according to web development best practices. That combination of creativity and structure is what makes this project special to me. It’s not only a technical achievement but also a personal milestone in learning to think beyond the typical boundaries of a web application.


## Distinctiveness and Complexity

This project is focused to be a single page interactive game with the fewer HTML templates as possible. It is designed to ease the addition of new content (if desired) by populating the HTMLs using the database instead of modifying the HTML code itself. As an example, at the "City" section (where the player can explore and perform certain actions), every place (and actions to perform) can be added or removed directly from the database without the need of different HTML pages for each place. A single HTML template can be used for the entirety of the City locations with data stored in a few database models (class __Place__ , __AreaAction__ and __CityEvent__), making it easier for modifying the template and adding/removing content to it.

This project was made in Django with 5 models (6 including a modification to __AbstractUser__) and Javascript for many of the player's interactions. This means a progressive UI where the game interface updates in real time as the player performs actions, without needing to reload the entire page. When the player trains, buys an energy drink, or challenge a rival, the updated values for energy, money, and stats and rank are instantly updated and shown on the screen. Using JavaScript and asynchronous requests to the Django backend, the sending and receiving data behind the scenes result in a smoother, more responsive experience that keeps the player immersed and feeling like a live game rather than a page-based website.

This project utilize a probabilistic combat to determines the outcome of fights using a mix of player and rival stats, plus an element of randomness. The backend compares attributes like strength, speed, and stamina to calculate a baseline chance of winning, ensuring that stronger players have a real advantage. However, a random roll is also factored in, so there’s always some uncertainty. This means even underdogs have a very small chance to win by pure luck, and powerful players can still lose if luck turns against them. This balance of skill and chance keeps combat exciting, fair, and replayable.

This project uses the player’s local machine date and time to manage recovery periods, ensuring that energy replenishment continues accurately even when the server is offline. When a player begins resting/recovering, the system records the start time and calculates the duration needed before full recovery (depending if it's a KO or just a rest). This method relies on the client’s local clock instead of constant server-side tracking, so the countdown remains valid as time naturally passes on the player’s device. This approach allows recovery timers to progress smoothly across sessions, giving players a consistent experience whether or not the server is actively running.

This project is mobile responsive as well.


## What’s contained in each file/folder.

The main folder "bcmain" cointains all the .py files modified with code and also subsequent folders "static" and "templates". The folder "static" contains another "bcmain" folder with the images used in the HTML templates, the fonts and the styles (in a .css file). The Javascript file "actions.js" in the "static" folder will process interactively the actions performed by the player and some other functions.

### Static

The file **Boxinglogo.png** is the icon that will show up top-left in the layout for all pages.
The file **challenges.png** is the image shown in the Challenge section where you will fight your rivals for ranking.
The files **Dream1.jpg** up to **Dream8.jpg** are images that will show in a carousel when you are resting or recovering energy.
The files **Champion.jpg**, **Fightlose.png** and **FightWin.png** will show in the modal popup after a fight respetively with a summary and the result as text.
The files **FightersDistrict.png**, **GlovegateCity.png**, **ShadowAlley.png**, **TitanArena.png**, **VictoryPlaza.png** are images that will show respectively while exploring the city in the City.html template.
The files **Gym.png** and **Gym2.png** are the images that will show when training at the Gym.
The files **Home1.png** and **Home2-Player.png** are the images that will show when the player clicks the Home button or when logs in the game.
The file **index1.jpg** is the image shown as presentation when accesing the page without logging in.
The files **KO1.jpg** up to **KO5.jpg** are images that will show in a carousel if the player gets Knocked Out in a fight.
The file **styless.css** contains the personalyzed styles for fonts (which are the files **Moderustic-Bold.ttf**, **Moderustic-Medium.ttf** and **Moderustic-Regular.ttf**). In the styles.css file it is defined the align and color for navigation links and text.

The file **actions.js** connects buttons to backend code, updates player stats and UI dynamically, simulates fights with probability logic and manages game alerts, progress, and energy. It contains all client-side interactivity and gameplay logic. Using JavaScript and the fetch() API it connects the user interface (HTML buttons, alerts, and bars) with the backend (Django views). Every user action like training, recovering energy, joining a gym, or fighting rivals is handled here.

It also handles the alert system, showing short messages to the player in red, yellow, or green boxes, depending on the result of an action. For example, when training or joining a gym, green messages mean success performing the action, red means failure, and yellow means warnings or reminders. These alerts also have close buttons to hide them after popping out.

The actions.js file handles the energy recovery system as well, letting the player refill their energy. When the player clicks the recovery button, a request is sent to the server, and once confirmed, the page refreshes with the player’s energy bar full again and a timer (which is the time it needs to be able to perform actions again).

The functions related to city and places (also coded in the javascript file) handles everything that happens when the player clicks on a location in the city, such as joining or quitting a gym, buying drinks at the bar, or hearing gossip. It sends a request to the server, checks what message it gets back, and updates the game’s display by showing alerts, updating money or energy, or displaying text.

The file also contains a gym section that handles how players train their stats like strength, speed, or stamina. There's a check/validation for ensuring that players have enough energy and users have entered valid training values. If everything is okay, it sends this data to the server, updates the player’s stats on the screen dinamically, adjusts the energy bar, and shows a success message describing how was the training session.

The fight and challenge section of the code handles how battles against NPC (Non Player Characters) or rivals happen. When the player clicks a challenge button and confirm, it retrieves the rival’s data from the server and calculates the player’s chance of winning based on the difference in stats. To determine if win or lose, the game runs a random roll to decide the outcome. Winning updates the player’s money and unlocks the next rival to challenge in the ranking, while losing triggers a “KO” recovery period.

### Templates

The **city.html** template represents the central navigation hub of the game, where players explore Glovegate City. It extends the base layout and loads the places provided by the backend into two columns of clickable links, dividing them dynamically depending on how many zones are available. Each location (gym, bar, arena, etc.) directs the player to a specific subpage or activity, letting them interact with different aspects of the game world without the need of refreshing the page. Functionally, this template acts as a gateway or hub, connecting all major in-game areas and showing how exploration and progression are tied to the player’s interaction with distinct environments.

The **gym.html** template is one of the most interactive sections of the game. It presents the Gym interface where players can train their stats using available energy, view their current gym membership, and track stat improvements after each training. The left side of the page focuses on information like the gym’s description, the player’s current gym level, and some motivational text about reputation and discipline. The right side is interactive, allowing players to allocate portions of their energy to specific attributes like strength, stamina, speed, and defense. This template also includes several alert boxes for success, failure, and warnings, which are dynamically controlled by JavaScript to reflect the results of training in real time. It also uses conditional rendering based on the player’s gym level to disable or enable certain stats, visually guiding the player through progression.

The **challenges.html** template is the core of the combat system, displaying the full roster of rival fighters the player can challenge in the arena. It shows a dynamic table where each rival’s name, nickname, rank, and reputation are listed, and the player’s progression determines which rivals are locked, available, or already defeated. When the player clicks a “Challenge” button, a modal (pop-up window) appears, confirming the fight details such as difficulty, prize, and win chance. All of that is calculated using Python functions in the backend and JavaScript logic. Additional modals display narrative-rich fight outcomes for winning, losing, and ultimately becoming the world champion, each with corresponding images and text to heighten the immersion. This template bridges storytelling, UI design, and probability-driven gameplay, transforming simple data from Django into an engaging battle experience.

The **layout.html** template serves as the foundational base template for the entire application, providing consistent navigation, styling, and structural elements across all pages. It has a navigation bar that conditionally renders different interfaces based on authentication status. For unauthenticated users, it shows a simplified header with login/register options. For authenticated users, it displays a navigation system for the game with tabs (Home, City, Gym, Challenges), a dynamic energy progress bar with conditional recovery functionality, real-time currency display (Jabucks), and user profile dropdown menu for logging out. The whole layout incorporates Bootstrap complements and this template speciffically set the modals for the recovery confirmation workflow and uses Django template logic to disable the recover button when energy is above 50%. This template establishes the core visual identity of the game through consistent branding and menus, responsive design patterns, and modular script organization that all the child templates can extend.

The **login.html** template provides the user authentication interface with a clean, focused form design to create a dedicated login. The template implements Django's form handling and includes conditional error message displays using Django's messaging framework. The minimalist design centers the login form with input fields for username and password, while providing an intuitive redirect to the registration page for new users. 

The **place.html** template creates a dynamic, interactive location interface that serves as the foundation for all explorable game zones. It displays zone-specific imagery and descriptions while implementing the area/action navigation system. The template uses Bootstrap collapse components to create an expandable interface where clicking an "Area" button reveals related "Actions" in the adjacent column. It includes multiple dynamic content sections that update via JavaScript based on user interactions without the need of reloading the page. The template also features alert systems for success/failure feedback and maintains contextual navigation with a "Back to city" button. This design creates a reusable template pattern that can adapt to various in-game locations while providing consistent interaction mechanics.

The **recovering.html** template implements the game's recovery system with a time-based interface. It features a prominent countdown timer with visual spinner elements and dynamically renders different narrative experiences based on recovery mode ('full' energy recovery vs 'KO' knockout recovery). The template uses Bootstrap carousels to display thematic image sequences (dreams or hospital scenes) accompanied by descriptive text that enhances the narrative immersion. The included JavaScript provides critical functionality: disabling navigation during recovery, implementing a real-time countdown with smooth animation, and automatic page refresh upon completion. This template transforms a passive waiting period into an engaging narrative experience that maintains player immersion during downtime.

The **register.html** template handles the user registration interface with a balanced two-column form layout. It organizes input fields logically with essential credentials (username, passwords) in the left column and optional personal information (email, names) in the right column. The template implements Django's form validation system with conditional error message display and includes helpful UI text about data privacy. The design maintains visual consistency with the login page while accommodating more input fields through the split-column approach, creating an efficient registration process that collects necessary information without overwhelming new users.

The **welcome.html** template serves as the game's landing and marketing page for unauthenticated users. It uses a two-column card layout to present the information: the left side provides detailed background about Boxing Champions and the text-based RPG genre, while the right side explains gameplay mechanics and features a prominent "Join Now" button. The template combines engaging imagery with descriptive text that sells the game experience, emphasizing the progression and the strategic depth of the boxing role play. 

The **home.html** template functions as the player dashboard and progression guide for authenticated users. It's the main/home page after logging in. It employs a two-column layout where the left side provides structured gameplay guidance through a numbered step-by-step system (training, reputation building, maintaining success), while the right side displays the player's current character statistics and progression status. The template dynamically shows/hides rank information based on the player's standing and presents all stats in an organized format. This design creates a central hub that both educates new players about game mechanics and provides veteran players with quick access to their current progression state, serving as both tutorial interface and character status dashboard.

### urls.py

This file contains the path for all templates, connecting the URLs to their respective views.py functions.

### models.py

This file defines the Django data models for the game, extending the default Django user model (via AbstractUser) and defining game entities: Player, NonPlayer (rivals), Place, AreaAction, and CityEvent. The models use common field types (CharField, DecimalField, PositiveIntegerField, BooleanField, JSONField, ForeignKey) to store game state and content.

Stats are DecimalField with max_digits=8 and decimal_places=1. This allows high values (up to 9,999,999.9) although the game logic may expect smaller numbers. Decimals are chosen to allow more accurate stat values because the training multiplier may return decimals.

formatted_jabucks() and formatted_stats() are used to present numbers nicely in templates (with commas).

Player.user, AreaAction.place, and CityEvent.area use ForeignKey relationships to connect models, creating clear one-to-many relationships.

AreaAction.actions stores an array of action names in JSON so the frontend can iterate over the list to create buttons dynamically.

sleep_time and awake_time store the current time when the player go to rest and calculate the time it will be awake. During this time, the game will show a screen with a timer where no actions can be performed until the awake time arrives.

Some numeric/game fields allow null and blank (e.g., jabucks, rank_hof) to allow empty values when a player or object is first created but it will be populated in the future.

### views.py

This file defines how the web app responds and fetches data from the database models, processes it, and sends it back to the browser as HTML pages or JSON responses (which the JavaScript in actions.js uses to update the screen dynamically). It also ensures that only logged-in users can access game pages and redirects recovering players to the recovery screen.

The **index()** function checks whether a user is logged in and either redirects them to the home page or shows the welcome screen. 

The **login_view()** function handles user login, verifying the username and password entered in the login form, and showing an error message if the credentials are incorrect. 

The **logout_view()** function logs the user out and takes them back to the welcome page. 

The **register()** function manages new player sign-ups. It ensures both passwords match, creates a new User and a linked Player profile, and automatically logs the user in. If the username already exists or if the password fields don’t match, it shows an error message instead of proceeding.

The **home()** function loads the player’s profile, stats, and rank on the home screen, unless the player is currently recovering, in which case it redirects to the recovery page. 

The **city()** function shows the city map with all available places that players can visit, using data from the Place model. 

The **places()** function loads a specific area in the city, such as the Gym or Bar, along with the actions available in that area. 

The **gym()** function manages the Gym page. When accessed though GET, it displays the page with the player’s current data; when accessed through a POST request, it processes the training inputs sent from the frontend, updates the player’s stats according to their gym level, reduces their energy based on the training effort, and sends the updated values back as a JSON response for the interface to update in real time.

The **recovering()** function handles both “full sleep” and “KO recovery” modes. When accessed through a GET request, it shows a recovery page with a countdown timer and a randomized set of themed images. When accessed through a POST request, it sets how long the recovery will take—eight hours for full recovery or two hours for KO—and updates the player’s energy and recovery status in the database. 

The city and area actions are processed through the **placeaction()** function, which handles most of the player’s interactions when exploring different places. Depending on the button clicked, this function can perform actions such as joining or quitting a gym, buying energy drinks, listening to gossip stories, or starting challenges. When the player tries to join a gym, it checks if they have enough jabucks (in-game currency) and updates their gym membership accordingly. When drinking at the bar, it checks if they have money and if they haven’t already refilled energy that day. The gossip feature selects a random story from the **CityEvent** model. If the clicked button is not an action, the function simply sends back text that describes the area. Each outcome sends a short JSON response back to the frontend, which then displays messages or updates the player’s energy and money.

The challenge and fighting system is managed by the **challenges()** function. When accessed through a GET request, it displays a list of all available NPC rivals ranked by difficulty. It determines which rivals are still locked based on the player’s current rank so players can’t skip ahead too far. When a POST request is made, the function handles two steps of the fight process. The first step is confirmation, where it calculates the difference between the player’s and rival’s stats and sends that data to the frontend to show the win rate and prize amount. The second step happens after the fight ends. If the player wins, the function updates their rank, gives them prize money, and changes their reputation title depending on their new rank, from “Amateur Prospect” to “Hall of Fame Legend”.

Several other helper functions support these main processes. The **check_funds()** function verifies that a player has enough money to perform a specific action, while **check_refill()** ensures a player can only buy one energy drink per day. The **recovery_carousel()** function handles the random selection of images used during recovery screen. Finally, the **check_recovery()** function ensures that if a player is still resting or recovering. If the player’s recovery time hasn’t finished, they are kept on the recovery screen and cannot train, fight, or perform other actions.


## How to run your application

In the console go to the game main directory where the manage.py file is and type: 
__python manage.py runserver__


## Any other additional information the staff should know about your project.

It is recommended to create an admin or superuser account to manage/test the database.


## Requirements

Python (version 3.12) and Django (version 5.1.7)
