# asana-python
 Python based Asana scripts to perform Admin type tasks.

## Installation
1. Download this package
1. Install requirements
```bash
pip3 install -r requirements.txt
```
## move_projects.py
`move_projects.py` moves all the projects contained in one team to another. I came up with this when we did a bulk delete of users and it created a number of projects in called "User's Previously Assigned Tasks" in a team that wasn't owned by the Asana admins.  

There are 2 main functions, comments in the script explain how to use one or the other:  
`main`  
* This one will move ALL projects from one team to another.  

`main_alt`  
* This one will move ONLY projects that have "Previously Assigned Tasks" in the name.  

The `TOKEN` can be a Service Account Token or a Personal Access Token of an Admin.

The `SOURCE_GID` and `DESTINATION_GID` can be found in the URL when navigating to the team's pages.
```bash
python3 move_projects.py -a [TOKEN] -s [SOURCE_GID] -d [DESTINATION_GID]
```

## find_empty_projects.py
`find_empty_projects.py` will look at the specified team and return a count of how many projects in it are empty (no tasks). It will also generate a .CSV file with the 'gid' and 'Name' of the project and place that in the working directory.  

The `TOKEN` can be a Service Account Token or a Personal Access Token of an Admin.

The `TEAM_GID` can be found in the URL when navigating to the team's pages.

```bash
python3 find_empty_projects.py -a [TOKEN] -t [TEAM_GID]
```  

## delete_users.py
`delete_users.py` is designed to look at the .CSV generated when an Admin uses the "Export CSV" button from the 'Member' tab in the Admin console. But it can use any .CSV that has `Email Address` as the header.  

A couple things to note:
* On Asana's end, the delete request is done as a job. If that job takes longer than 2 minutes the API times out. So for people with a large number of resources tied to their account, you may experience some odd behavior. 
* Users can be restored via the UI in the Admin console. There's no API to restore at this time.

The `TOKEN` can be a Service Account Token or a Personal Access Token of an Admin.

The `MODE` is either `dry_run` or `action`. Pretty self explanitory

The `PATH_TO_CSV` is the path to the csv with the "Email Address" header and list of people you want to delete.

The `ORG_ID` can be found by looking at the URL when in the Admin Console.

```bash
python3 delete_users.py -a [TOKEN] -m [MODE] -c [PATH_TO_CSV] -o [ORG_ID]
```

## Buy me a Coffee / Tip?
*coming soon!*

## Disclaimer
I am not associated with, nor do I work for Asana. Use of these scripts is at your own risk. I take no responsibility for any issues that come from using these scripts.