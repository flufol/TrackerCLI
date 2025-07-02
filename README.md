## A simple CLI for tracker habits or whatever you want.

### Requires:
rich  
pyfiglet  
python3.8+  

### Setup
I symlinked this to my usr/local/bin/ so I can just call it anywhere  

### How to use
`mark-day` marks the current day by default, its arugments are:  
`status`: the status to set it to.  
`--day`:  choose a specific day between 1-7 (monday-sunday) to mark.  

`display-week`: displays the days of the week and their statuses, its arugment is:  
`week`: choose the week the display (1-52). 

`streak`: shows the current streak of fully completed weeks in big ascii letters.  

### TODO
Support multiple different trackers (e.g., exercice, read).  
Summaries for the month, week, or year. Like a calender.  
Reminders for missed days.  
