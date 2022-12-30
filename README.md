### Notes
This is still in alpha, so an API key for the Riot API is required for this to work.

### Usage
There must be a folder titles `readme-lol-items` in the repository that you wish to use this action in. Additionally, a file titled `config.json` with the following contents must exist:

```json
{
    "Summoner Name": "R1tzcrackers",
    "Matches": 10,
    "Target File": "README.md",
    "Toggle Credit": 1,
    "Skin Substitutions": {
        "Yasuo": "Nightbringer Yasuo",
        "Yone": "Dawnbringer Yone",
        "Akali": "K/DA Akali",
        "Taliyah": "Pool Party Taliyah",
        "Katarina": "Battle Queen Katarina"
    },
    "Extra Info": {
        "Seconds of CC": 1,
        "Display Rank": 1,
        "Main Lane": 1,
        "Ability Count": 1,
        "Solokills": 1,
        "Takedowns": 1,
        "Mastery": 1,
        "K/D/A": 1,
        "Pentakills": 1,
        "Quadrakills": 1,
        "Triplekills": 1,
        "Doublekills": 1
    }
} 
```
The "Skin Substitutions" section allows you to specify a champion and your preferred skin to display with that champion.

The "Extra Info" section allows you to toggle what is being show. A "1" is used when you want it to display, and a "0" is used when you don't want it to display.

In your README.md file you want to place the following code **without the curly braces**:
```md
{<!---LOL-STATS-START-HERE--->}
{<!---LOL-STATS-END-HERE--->}
```

This dictates where the generated statistics will be displayed.


This following code allows you to run the project manually. You can schedule using cron if you want to automate it. Ensure to have a secret named  "API_KEY" with the Riot API key for this action to work. Additionally, the code must be placed in the `.github/workflows` directory of the repository. Note that you may replace `@v0.1` with a release number of your choice for each successive version of the project.

```yml
name: Run readme-lol-stats

on:    
    workflow_dispatch:

jobs:
    build:    
        runs-on: ubuntu-latest
        steps:
            # Checkout current repo to runner
          - name: Checkout current repo
            uses: actions/checkout@v2 
            
            # Setup python
          - name: setup python
            uses: actions/setup-python@v4
            with:
                python-version: '3.9' 
        
            # Upgrade pip
          - name: Upgrade Pip
            run: |
                python -m pip install --upgrade pip
            
            # Run readme-lol-stats-action
          - name: Use readme-lol-stats-action
            uses: rithikasilva/readme-lol-stats@v0.1 
            with:
                source: ${{ github.event.repository.name }}
                api-key: ${{ secrets.API_KEY }}
            
            # Commit files to current repo
          - name: commit files
            run: |
                git config --local user.email "action@github.com"
                git config --local user.name "GitHub Action"
                git add -A
                git diff-index --quiet HEAD || (git commit -a -m "updated logs" --allow-empty)
            
            # Push changes to current repo
          - name: push changes
            uses: ad-m/github-push-action@v0.6.0
            with:
                github_token: ${{ secrets.GITHUB_TOKEN }}
                branch: main 
```


### Example Layout
Here is an example layout (best viewed with proper formatting [here](https://github.com/rithikasilva/readme-lol-stats)):
<!---LOL-STATS-START-HERE--->
<h3 align='center'> Data from Last 100 Matches for Doublelift</h3><table align='center'><tr></tr>
<tr align='left'><th><pre>Top 5 Recently Played Champions
-------------------------
<img src='readme-lol-items/Twitch.png' alt='drawing' width='20'/> Twitch           |███----------------------|  11.00%
<img src='readme-lol-items/Jinx.png' alt='drawing' width='20'/> Jinx             |███----------------------|  11.00%
<img src='readme-lol-items/Kaisa.png' alt='drawing' width='20'/> Kaisa            |███----------------------|   9.00%
<img src='readme-lol-items/Sivir.png' alt='drawing' width='20'/> Sivir            |███----------------------|   8.00%
<img src='readme-lol-items/MissFortune.png' alt='drawing' width='20'/> MissFortune      |███----------------------|   8.00%
-------------------------
Seconds CCing Enemies: 1124
Current Rank: Master <img src='rank_images/Emblem_Master.png' alt='drawing' width='20'/>
Most Played Position: Bottom <img src='position_images/Position_Master-Bot.png' alt='drawing' width='20'/>
Total Abilities Used: 19237
Total Solokills: 55
Total Takedowns: 1236
KDA: 627/477/609
Pentakills: 0
Quadrakills: 1
Triplekills: 10
Doublekills: 84
</pre></th><th><pre>Top 3 Champion Masteries
------------------------
<img align='center' src='readme-lol-items/Jhin_0.png' alt='drawing' width='50'/> Jhin: 335442 
<img align='center' src='readme-lol-items/Caitlyn_0.png' alt='drawing' width='50'/> Caitlyn: 244748 
<img align='center' src='readme-lol-items/Jinx_0.png' alt='drawing' width='50'/> Jinx: 214789 
</pre></th></tr></table>
<h6 align='center'>

[README Profile LoL Stats](https://github.com/marketplace/actions/readme-profile-lol-stats) by [rithikasiilva](https://github.com/rithikasilva)
</h6>
<!---LOL-STATS-END-HERE--->





*README Profile LoL Stats isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.*