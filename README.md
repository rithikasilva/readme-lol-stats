### Notes
This is still in alpha, so an API key for the Riot API is required for this to work. Additionally, expect breaking changes to be made. Reference a specific tag when calling the action if you seek stability.

### Usage
There must be a folder titled `readme-lol-items` in the repository that you wish to use this action in. Additionally, a file titled `config.json` with the following contents must exist:

```json
{
    "Summoner Name": "{Your Summoner Name}",
    "Platform Routing Region Code": "(Your Code)",
    "Regional Routing Name": "(Your Region Name)",
    "Matches": 10,
    "Target File": "README.md",
    "Toggle Credit": true,
    "Skin Substitutions": {
        "Caitlyn": "Battle Academia Caitlyn"
    },
    "Extra Info": {
        "Seconds of CC": true,
        "Display Rank": true,
        "Main Lane": true,
        "Ability Count": true,
        "Solokills": true,
        "Takedowns": true,
        "Mastery": true,
        "K/D/A": true,
        "Pentakills": true,
        "Quadrakills": true,
        "Triplekills": true,
        "Doublekills": true
    }
} 
```
The values for `Platform Routing Region Code` are one of the following: `br1`, `eun1`, `euw1`, `jp1`, `kr`, `la1`, `la2`, `na1`, `oc1`, `tr1`, `ru`, `ph2`, `sg2`, `th2`, `tw2`, and `vn2`. The values for `Regional Routing Name` are one of the following: `americas`, `asia`, `europe`, and `sea`.


The "Skin Substitutions" section allows you to specify a champion and your preferred skin to display with that champion.

The "Extra Info" section allows you to toggle what is being show. A "1" is used when you want it to display, and a "0" is used when you don't want it to display.

In your README.md file you want to place the following code **without the curly braces**:
```md
{<!---LOL-STATS-START-HERE--->}
{<!---LOL-STATS-END-HERE--->}
```

This dictates where the generated statistics will be displayed.


This following code allows you to run the project manually. You can schedule using cron if you want to automate it. Ensure to have a repository secret named  `API_KEY` with the Riot API key for this action to work. Additionally, the code must be placed in the `.github/workflows` directory of the repository. Note that you may replace `@master` with a release tag of your choice for each successive version of the project.

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
            uses: rithikasilva/readme-lol-stats@master
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
Here is an example layout (best viewed in GitHub Dark Mode with proper formatting [here](https://github.com/rithikasilva/readme-lol-stats)):
<!---LOL-STATS-START-HERE--->
<h3 align='center'> Data from Last 10 Matches for Doublelift</h3><table align='center'><tr></tr>
<tr align='left'><th><pre>Top 3 Recently Played Champions
-------------------------
<img src='readme-lol-items/loading_Smolder.gif' alt='drawing' width='400'/>
<img src='readme-lol-items/loading_Jhin.gif' alt='drawing' width='400'/>
<img src='readme-lol-items/loading_Varus.gif' alt='drawing' width='400'/>
-------------------------
<img align='center' src='readme-lol-items/extra_info.gif' alt='drawing' width='350'/></pre></th><th><pre>Top 3 Champion Masteries
------------------------
<img align='center' src='readme-lol-items/mastery.gif' alt='drawing' width='320'/> </pre></th></tr></table>
<h6 align='center'>

[README Profile LoL Stats](https://github.com/marketplace/actions/readme-profile-lol-stats) by [rithikasiilva](https://github.com/rithikasilva)
</h6>
<!---LOL-STATS-END-HERE--->





*README Profile LoL Stats isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.*
