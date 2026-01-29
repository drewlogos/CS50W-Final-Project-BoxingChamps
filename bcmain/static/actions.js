document.addEventListener('DOMContentLoaded', () => {
    // Hide alerts 
    hide_alerts()
    // Show Yellow alert 1 - warning (Gym section only)
    if (document.querySelector('#alertyellow1')) {
        var yellow_alert = document.querySelector('#alertyellow1')
        yellow_alert.style.display = 'block'
        // Set close button for Yellow alert 1 - warning
        var alertbtny1 = document.querySelector('#alertbtny1')
        alertbtny1.addEventListener('click',function() {
            document.querySelector('#alertyellow1').style.display = 'none'
        })};
        // Set close button for Green alert 
    if (document.querySelector('#alertbtng')){
        var alertbtng = document.querySelector('#alertbtng')
        alertbtng.addEventListener('click',function() {
            document.querySelector('#alertgreen').style.display = 'none'
        })};
        // Set close button for Red alert 
    if (document.querySelector('#alertbtnr')){
        var alertbtnr = document.querySelector('#alertbtnr')
        alertbtnr.addEventListener('click',function() {
            document.querySelector('#alertred').style.display = 'none'
        })};
        // Set close button for Yellow alert 2 - warning
    if (document.querySelector('#alertbtny2')){
        var alertbtnr = document.querySelector('#alertbtny2')
        alertbtnr.addEventListener('click',function() {
            document.querySelector('#alertyellow2').style.display = 'none'
        })};   

    // Set function for Recover Energy button (layout)
    var recoverbutton = document.getElementById('recoverbtn2');
    recoverbutton.addEventListener('click', function(){
        energy_recovery();
    });

    // Set function to all action buttons (City/Places section)
    if (document.querySelector('.place_act_btn')) {
        var actionbuttons = document.querySelectorAll('.place_act_btn');
        actionbuttons.forEach((button) => 
        button.addEventListener('click', function() {
            placeaction(this);
        }))};
    
    // Set function for training buttons (Gym section. Similar to placeaction button)
        // to select button: id="gymtrain" name="gymtrain".
    if (document.querySelector('#gymtrain')){
        var trainbutton = document.querySelector('#gymtrain')
        trainbutton.addEventListener('click', function(){
                gymtrain(this);
        })};

    // Set function for all challenge buttons to confirm before entering a fight
    if (document.querySelectorAll('button.challenge')){
        var challengebuttons = document.querySelectorAll('button.challenge')
        challengebuttons.forEach((button) =>
            button.addEventListener('click', function() {
                confirm_challenge(this);
        }))};

    //Set function for redirect when losing a fight (after clicking OK button from pop-up)
    if (document.querySelector('#losebtn')){
        var losebtn = document.querySelector('#losebtn')
        losebtn.addEventListener('click', function(){
            window.location.replace("/home");
        })};

// Set funtion to hide all alerts on page load
function hide_alerts() {
    var alerts = document.querySelectorAll('.alert')
    alerts.forEach((alert) => 
        alert.style.display = 'none');
};

// Set function for Action Buttons and Areas in City/Place section
function placeaction(button){
    // Send data to views corresponding to the action button clicked
    fetch('/paction', {
        method: 'POST',
        body: JSON.stringify({
            id: button.id,
            action: button.name,
            zone: document.querySelector("#zonename").innerText
        })
        })
    // Process response
    .then(response => response.json())
    .then(result => {
        // Actions in Fighter's District 
            // For Gym buttons
                // If Player is in correct gym, redirect to Gym page
        if (result['message'] == "train_success") {
            window.location = "/gym"
        }
                // If Player is not in a gym yet, it should join one
        else if (result['message'] == "train_fail"){
                    // Show red alert message (Fail. Must join a gym first) and hide other alerts
            hide_alerts()
            document.querySelector('#alerttextr').innerText = "You need to join the Gym first if you want to train here."
            document.querySelector('#alertred').style.display = "block"      
        } 
                // When Player joins a Gym.
        else if(result['message'] == "join_success"){           
                    // Show green alert message (Success. Joined) and hide other alerts
            hide_alerts()
            document.querySelector('#alerttextg').innerText = `You have joined the gym "${result['gym']}". You can start training your stats.`
            document.querySelector('#alertgreen').style.display = "block"
                    // Pay Gym Fee. Update jabucks on top layout (change attribute value)
            document.getElementById("jabucks").innerText = result.jabucks_upd
        }
        else if(result['message'] == "join_fail"){           
                    // Show red alert message (Fail. Not joined) and hide other alerts
            hide_alerts()
            document.querySelector('#alerttextr').innerText = "You are already in this Gym."
            document.querySelector('#alertred').style.display = "block"
        }       
        else if(result['message'] == "join_fee"){           
                    // Show red alert message (Fail. Not joined) and hide other alerts
            hide_alerts()
            document.querySelector('#alerttextr').innerText = `You need ꞗ-${result.fee.toLocaleString('en-US')} to join this Gym`
            document.querySelector('#alertred').style.display = "block"
        }       
                //When Player quits a Gym.
        else if(result['message'] == "quit_success"){
                    // Show green alert message (Success. Quitted) and hide other alerts
            hide_alerts()
            document.querySelector('#alerttextg').innerText = `You have quitted the gym "${result['gym']}". You should join one to train your stats.`
            document.querySelector('#alertgreen').style.display = "block"
        }
        else if(result['message'] == "quit_fail"){           
                    // Show red alert message (Fail. Not in gym) and hide other alerts
            hide_alerts()
            document.querySelector('#alerttextr').innerText = "You cannot quit the Gym if you have not joined first."
            document.querySelector('#alertred').style.display = "block"
        }  
        else if(result['message'] == "quit_cannot"){           
                // Show red alert message (Fail. Quitting from other gym) and hide other alerts
            hide_alerts()
            document.querySelector('#alerttextr').innerText = `You cannot quit a Gym that you have not joined. Go to ${result['zone']} and quit "${result['gym']}" Gym, or join this one directly`
            document.querySelector('#alertred').style.display = "block"
        }  
            // Bar buttons
                // Gossip (Show stories/lore of the game)
        else if (result['message'] == "gossip"){
            document.querySelector('.event').style.display = "block"
            document.querySelector('.eventtitle').innerHTML = result['title']
            document.querySelector('.eventtext').innerHTML = result['text']
            window.scrollBy(0, 150);
        }
                // Buy Drinks (Restore some energy)
        else if (result['message'] == "drink"){
            // Update energy bar on top layout (change attribute value and text).
            document.getElementById("ebar").setAttribute("aria-valuenow", result.energy_upd);
            document.getElementById("ebarprogress").setAttribute("style", `width: ${ result.energy_upd }%`);
            if (result.energy_upd >= 100){
                document.getElementById("ebarprogress").innerText = `Full (${result.energy_upd}%)`;
            }
            // Disable Recover button in top layout                   
            document.getElementById("recoverbtn").setAttribute("disabled", "")            
            // Update jabucks on top layout (change attribute value)
            document.getElementById("jabucks").innerText = result.jabucks_upd
            // Show green alert message (Successful recover) and hide other alerts
            hide_alerts()
            document.querySelector('#alerttextg').innerText = "You have bought some cans of energy drinks and guzzle them up one after the other. You feel so energetic like running on liquid lightning (+60 energy)."
            document.querySelector('#alertgreen').style.display = "block"
        }
        else if (result['message'] == "no funds"){
            // Show red alert (No money)
            hide_alerts()
            document.querySelector('#alerttextr').innerText = "You dont have enough jabucks left. You should try winning tournaments to earn some."
            document.querySelector('#alertred').style.display = "block"
        }
        else if (result['message'] == "no refill"){
            // Show red alert (No refills)
            hide_alerts()
            document.querySelector('#alerttextr').innerText = "Drinking too much soda will give you the jitters. You should come back tomorrow."
            document.querySelector('#alertred').style.display = "block"
        }
        else if (result['message'] == "redirect"){
            window.location.replace("/challenges");
        }
            // If no action is detected/clicked then it's an Area button.
        else {
                // Show area intro/text section
            document.querySelector('.intro-area').style.display = 'block'
            document.querySelector('.intro-area-title').innerHTML = button.name
            document.querySelector('.intro-area-text').innerHTML = result.message
            window.scrollBy(0, 150);
        }
    })
};

// Set function for Gym > Training buttons
function gymtrain(button){
    // Get User Energy value from template (top layout)
    var penergy = Number(document.getElementById('ebar').getAttribute("aria-valuenow"));
    // Create a dictionary to store inputs from user
    var training = {
        str: document.getElementById('inputstr').value,
        sta: document.getElementById('inputsta').value,
        defn: document.getElementById('inputdefn').value,
        dex: document.getElementById('inputdex').value,
        spd: document.getElementById('inputspd').value,
        acc: document.getElementById('inputacc').value
    };
    // Validate the training values (for empty/nulls inputs) and convert strings to integers
    for (key in training) {
        if (training[key] == '') {
            training[key] = 0
        }
        else {
            training[key] = Number(training[key]);
        }
    };
    // Validate that energy spent souldn't exceed the player energy
        // If no energy left show red alert message (Failed training) and hide all other alerts
    if (penergy == 0) {
        hide_alerts()
        document.querySelector('#alerttextr').innerText = "You have no energy left to train. You should rest and come back later."
        document.querySelector('#alertred').style.display = "block"
    }
        // If not enough energy show red alert message (Failed training) and hide all other alerts 
    else if ((training.str + training.dex + training.spd + training.sta + training.acc + training.defn) > penergy) {
        hide_alerts()
        document.querySelector('#alerttextr').innerText = "You cannot use more energy than what you have left. You should reconsider the energy distribution or go sleep to recover."
        document.querySelector('#alertred').style.display = "block"
    }
        // If zero distribution/allocation overall, show yellow alert message (Warning) and hide all other alerts.
    else if (training.str + training.dex + training.spd + training.sta + training.acc + training.defn == 0) {
        hide_alerts()
        document.querySelector('#alerttexty2').innerText = `You want to train but you don't know where to start. Allocate your energy in the distribution section before training.`
        document.querySelector('#alertyellow2').style.display = "block"
    }
        // If all is good/valid
    else {
        // Pass data to views.py
        fetch('/gym', {
            method: 'POST',
            body: JSON.stringify({
                id: button.id,       
                action: "update",
                training: {
                    str: training.str,
                    dex: training.dex,
                    spd: training.spd,
                    sta: training.sta,
                    acc: training.acc,
                    defn: training.defn
                }
            })
        })
        // Process response
        .then(response => response.json())
        .then(result => {
            // Update player's stats in template
            document.getElementById('penergy').innerText = result.penergy
            document.getElementById('pstr').innerText = result.pstr
            document.getElementById('pdex').innerText = result.pdex
            document.getElementById('pspd').innerText = result.pspd
            document.getElementById('pacc').innerText = result.pacc
            document.getElementById('psta').innerText = result.psta
            document.getElementById('pdefn').innerText = result.pdefn
            // Update energy bar on top layout (change attribute value)
            document.getElementById("ebar").setAttribute("aria-valuenow", result.penergy);
            document.getElementById("ebarprogress").setAttribute("style", `width: ${ result.penergy }%`);
            // Show green alert message (Successful train) and hide other alerts
            hide_alerts()
            document.querySelector('#alerttextg').innerText = `You have trained ${training.str + training.defn} reps with the dumbells, ${training.spd + training.acc} sparring sessions and jumped the rope ${training.dex + training.sta} sets. 
                You feel your muscles pumping.`
            document.querySelector('#alertgreen').style.display = "block"
            // Remove text in energy bar
            document.getElementById("ebarprogress").innerText = ""
            // Enable Full Recover button (top layout) if energy below 50%
            if (result.penergy < 50 ){
                document.getElementById("recoverbtn").removeAttribute("disabled")
            }
            else if (result.penergy >= 100 ){
                document.getElementById("ebarprogress").innerText = `Full (${result.penergy})%`;
            }
        })
    };
};

// Set full energy recovery function
function energy_recovery(){
    // Trigger full recovering code
    fetch('/recovering/full', {
        method: 'POST',
        body: JSON.stringify({
            id: 'full'
        })
    })
    .then(response => response.json())
    .then(redirect => {
        window.location.href = redirect.redirect;
    })
};

// Set challenge/fight confirmation function
function confirm_challenge(button){
    // To store/calculate the winrate chance for showing in modal popup (in template) and final result
    var winrate = 0
    var prize = "TBD"
    var final_result = "TBD"
    // Confirm the challenge (identify npc to fight)
    fetch('/challenges', {
        method: 'POST',
        body: JSON.stringify({
            id: "confirmation",
            npc_rank: Number(button.name)
        })
        })
    // Process response
    .then(response => response.json())
    .then(result => {
        // Calculate win rate %
        winrate = calculate_winrate(result.stat_diff)
        // Round/Floor winrate and Randomize roll (this is the fight simulation)
        var round_winrate = Math.floor(winrate / 10) * 10
        var roll = Math.floor(Math.random() * 10) + 1
        // Populate modal before fight
        document.getElementById("fightbtn").setAttribute('name', button.name)
        document.getElementById("npcname").innerText = result.npcname
        document.getElementById("npcnickname").innerText = result.npcnickname
        document.getElementById("npcrank").innerText = button.name
        document.getElementById("prize").innerText = result.prize.toLocaleString()
            // For winrate and difficulty
        document.getElementById("winrate").innerText = winrate
        var difficulty = document.getElementById("difficulty")
        var difficultycolor = document.getElementById("difficulty_color")
        var winratecolor = document.getElementById("winrate_color")
        if (winrate < 20){
            difficulty.innerText = "Very Hard"
            difficultycolor.setAttribute('style', "color: #6d0a0a")
            winratecolor.setAttribute('style', "color: #6d0a0a")
        }
        else if ((winrate < 40) && (winrate >= 20)) {
            difficulty.innerText = "Hard"
            difficultycolor.setAttribute('style', "color: #aa1212")
            winratecolor.setAttribute('style', "color: #aa1212")
        }
        else if ((winrate < 60) && (winrate >= 40)) {
            difficulty.innerText = "Balanced"
            difficultycolor.setAttribute('style', "color: #B8860B")
            winratecolor.setAttribute('style', "color: #B8860B")
        }
        else if ((winrate < 80) && (winrate >= 60)) {
            difficulty.innerText = "Easy"
            difficultycolor.setAttribute('style', "color: #009700")
            winratecolor.setAttribute('style', "color: #009700")
        }
        else {
            difficulty.innerText = "Very Easy"
            difficultycolor.setAttribute('style', "color: #006400")
            winratecolor.setAttribute('style', "color: #006400")
            }
    // Prepare "fight" button according to win/lose
        // High winrate == guaranteed win.
        // When rolling the lose chance is if it exceeds the winrate. i.e (60% winrate means the roll has to score 1-6 to win and 7-10 to lose)
            //in some cases it was losing with 90% winrate so I decided to guarantee a win with high chance.
        console.log(roll)
        if (winrate >= 90 || roll <= round_winrate / 10){
            final_result = "Win" // APPLY BENEFITS (+$ prize) and determine if it win the game
            if (button.name == 1) {
                // Adjust fight button in Modal 1 to show Modal 4 (champion) in template
                fightbtn = document.getElementById("fightbtn")
                fightbtn.setAttribute("data-bs-target", "#champion")
                fightbtn.setAttribute("data-bs-toggle", "modal")
                fightbtn.setAttribute("data-bs-dismiss", "modal")
                // Trigger function to disable "challenge button" and change color after a win
                document.getElementById("champion").addEventListener('click', function(){
                    update_challengebtn(button.name, result.prize)
                })
            }
            else {
                // Adjust fight button in Modal 1 to show Modal 2 (win) in template
                fightbtn = document.getElementById("fightbtn")
                fightbtn.setAttribute("data-bs-target", "#challengeWin")
                fightbtn.setAttribute("data-bs-toggle", "modal")
                fightbtn.setAttribute("data-bs-dismiss", "modal")
                // Trigger function to disable "challenge button" and change color after a win
                document.getElementById("challengeWin").addEventListener('click', function(){
                    update_challengebtn(button.name, result.prize)
                })
            }  
        }
        // Similarly to the win, some very hard fights (with very low chances 10%) were resulting in a win. I decided to guarantee a lose with low chance
            // Set it to 30 % for more realism/difficulty
        else if (winrate <= 30 || roll > round_winrate / 10){
            final_result = "Lose" // APPLY PENALTIES (2 hours recovery - KO) 
            // Adjust fight button to show Modal 3 (defeat) and redirect after click ok
            fightbtn = document.getElementById("fightbtn")
            fightbtn.setAttribute("data-bs-target", "#challengeLose")
            fightbtn.setAttribute("data-bs-toggle", "modal")
            fightbtn.setAttribute("data-bs-dismiss", "modal")
            return (final_result)
        }
        //Return variables for update views.py in the next .then
        prize = Number(result.prize)
        rank = Number (button.name)
        return {final_result, prize, rank}
    })
    // Update player data (backend) after clicking the fight confirmation button.
    .then(returned => {
        // Set up the fight button click handler
        fightbtn.addEventListener('click',function() {
            updateplayerbackend(returned);
        })
    })
};   

function updateplayerbackend(returned){
if (returned.final_result == "Win"){
            // Trigger function to update player data in the backend
            challengewin(returned.prize, returned.rank)
        }
        else {
            // Trigger KO recovery code with 2h penalty (using id) and redirect to recovery page
            fetch('/recovering/KO', {
                method: 'POST',
                body: JSON.stringify({
                    id: 'KO'
                })
            })
        }
}

// Set function to disable "challenge button" and change color after a win
function update_challengebtn(rank, prize){
    // Select challenge button, disable and change color
    var challengebtn = document.getElementById("npc"+rank)
    challengebtn.setAttribute("disabled", "")
    challengebtn.classList.remove("btn-outline-secondary")
    challengebtn.classList.add("btn-success")
    challengebtn.innerText = "Completed"
    // Update jabucks in layout (top bar). Add prize to existing funds
    var jabucks = document.getElementById("jabucks").innerText
        // Remove commas and convert to number then sum
    jabucks = jabucks.replace(",", "")
    jabucks = Number(jabucks) + prize
        // Reformat to commas and update template
    document.getElementById("jabucks").innerText = jabucks.toLocaleString('en-US')
    // Unlock next rival and modify challenge button appearance
    var nextrank = rank-1
    nextchallengebtn = document.getElementById("npc"+(nextrank))
    nextchallengebtn.removeAttribute("disabled")
    nextchallengebtn.classList.remove("btn-secondary")
    nextchallengebtn.classList.add("btn-outline-secondary")
    nextchallengebtn.innerText = "Challenge"
};

// Set function to calculate win chance
function calculate_winrate(stat_diff){
    var winrate = 0
    // Calculate winrate %. Process Stats difference (result from fetch)
    for (key in stat_diff) {
        // If difference above 2500, +15% chance increase // between 1000 and 2500, 10% increase // between -200 and 1000, 5% increase// under -200, 0%
        if (stat_diff[key] > 5000) {
            winrate += 30
        }
        else if (stat_diff[key] > 3500) {
            winrate += 25
        }
        else if (stat_diff[key] > 2500) {
            winrate += 15
        }
        else if ((stat_diff[key] > 1000) && (stat_diff[key] <= 2500)){
            winrate += 10
        }
        else if ((stat_diff[key] > -200) && (stat_diff[key] <= 1000)){
            winrate += 5
        }
        else {
            winrate += 0
        }
    }
    if (winrate > 100) {
        winrate = 90
    }
    return winrate;
};

// Set win function
function challengewin(prize, rank){
    // Modify player rank and prize in backend
    fetch('/challenges', {
        method: 'POST',
        body: JSON.stringify({
            id: 'challengewin',
            prize: prize,
            rank: rank 
        })
    })
};

// End of DOM
});