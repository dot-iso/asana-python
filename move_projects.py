import asana
import argparse

def configure_client(service_account_token):
    # Construct the Asana client
    # https://developers.asana.com/docs/python-hello-world
    client = asana.Client.access_token(service_account_token)
    # Optional - give the client a name
    client.options['client_name'] = "move_projects"
    return client

def get_projects_in_team(client, team_gid):
    # https://developers.asana.com/docs/get-a-teams-projects
    try:
        result = client.projects.get_projects_for_team(team_gid)
    except Exception as error:
        print("Failed to get projects for team. Error: " + str(error))
        result = []
    return result

def move_project(client, project_gid, dest_team_gid):
    # https://developers.asana.com/docs/update-a-project
    try:
        result = client.projects.update_project(project_gid, {"team": dest_team_gid})
    except Exception as error:
        print("Failed to get projects for team. Error: " + str(error))
    return

def main(service_account_token, source_team_gid, dest_team_gid):
    # Configure Asana Client
    client = configure_client(service_account_token)
    # Get all the projects in the source team
    all_projects = get_projects_in_team(client, source_team_gid)
    # Itterate through the 'generator' object and move the project to the destination team
    for project in all_projects:
        project_gid = project['gid']
        project_name = project['name']
        print("Moving \"" + project_name + "\" (" + str(project_gid) + ")")
        move_project(client, project_gid, dest_team_gid)
    return

def main_alt(service_account_token, source_team_gid, dest_team_gid):
    # Configure Asana Client
    client = configure_client(service_account_token)
    # Get all the projects in the source team
    all_projects = get_projects_in_team(client, source_team_gid)
    # Itterate through the 'generator' object and move the project to the destination team
    for project in all_projects:
        project_gid = project['gid']
        project_name = project['name']
        if "Previously Assigned Tasks" in project_name:
            print("Moving \"" + project_name + "\" (" + str(project_gid) + ")")
            move_project(client, project_gid, dest_team_gid)
        else:
            print(project_name + " (" + str(project_gid) + ") needs to stay in place.")
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth", "-a", help="Service Account or Personal Access Token", dest="service_account_token", type=str, required=True)
    parser.add_argument("--source-team", "-s", help="The GID for the source team", dest="source_team_gid", type=str, required=True)
    parser.add_argument("--destination-team", "-d", help="The GID for the destination team", dest="dest_team_gid", type=str, required=True)
    args = parser.parse_args()
    # To move ALL projects from one team to another
    # If using this one, comment out Line 69
    main(**vars(args))
    # To move ONLY projects that contain "Previously Assigned Tasks"
    # If using this one, comment out Line 65
    #main_alt(**vars(args))