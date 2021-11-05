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

def get_tasks_in_project(client, project_list, team_gid):
    # Couln't get https://developers.asana.com/docs/get-task-count-of-a-project to return any results so using
    # https://developers.asana.com/docs/get-tasks-from-a-project
    # Create an empty list
    empty_project_list = []
    # Check the task count within each project
    for project in project_list:
        project_gid = project['gid']
        project_name = project['name']
        try:
            result = client.tasks.get_tasks_for_project(project_gid)
            result = list(result)
        except Exception as error:
            print("Failed to get task count for " + project_name + " (" + str(project_gid) + ").")
            break
        project_count = len(result)
        if project_count == 0:
            empty_project_list.append(project_gid)
            output_empty_projects(project_gid, project_name, team_gid)
        else:
            None
        return empty_project_list

def output_empty_projects(project_gid, project_name, team_gid):
    with open(team_gid + "_empty_projects.csv", "a") as output_file:
        output_file.write(project_gid + "," + project_name + "\n")
    return

def main(service_account_token, team_gid):
    # Configure Client
    client = configure_client(service_account_token)
    # Get the projects in the team
    team_projects = get_projects_in_team(client, team_gid)
    # Send all the projects to get checked for tasks
    empty_projects = get_tasks_in_project(client, team_projects, team_gid)
    # Output the count of emptry projects to console
    num_of_empty_projects = len(empty_projects)
    print(team_gid + " has " + str(num_of_empty_projects) + " empty projects.")
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth", "-a", help="Service Account or Personal Access Token", dest="service_account_token", type=str, required=True)
    parser.add_argument("--team", "-t", help="Team gid", dest="team_gid", type=str, required=True)
    args = parser.parse_args()
    main(**vars(args))
