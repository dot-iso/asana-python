import asana
import argparse

def configure_client(service_account_token):
    # Construct the Asana client
    # https://developers.asana.com/docs/python-hello-world
    client = asana.Client.access_token(service_account_token)
    # Optional - give the client a name
    client.options['client_name'] = "set_project_owner"
    return client

def get_owner_gid(client, owner_email):
    # Gets the information about the target email user
    # https://developers.asana.com/docs/get-a-user
    try:
        result = client.users.get_user(owner_email)
        result = result['gid']
        print("Retrieved the GI for " + str(owner_email) + ": " + str(result))
    except Exception as error:
        print("Error getting owner info: " + str(error))
        result = False
    return result

def add_member_to_project(client, project_gid, owner_gid):
    # Adds the new owner as a member - required to be able to set them as an owner
    # https://developers.asana.com/docs/add-users-to-a-project
    try:
        result = client.projects.add_members_for_project(project_gid, {"members": owner_gid})
        restut = True
        print("Added " + str(owner_gid) + " as a member of the project (" + str(project_gid) + ").")
    except Exception as error:
        print("Error adding project member: " + str(error))
        result = False
    return result

def set_project_owner(client, project_gid, owner_gid):
    # Updates the owner of the project to the newly added member
    # https://developers.asana.com/docs/udpate-a-project
    try:
        result = client.projects.update_project(project_gid, {"owner": owner_gid})
        print("Set " + str(owner_gid) + " as the owner of the project (" + str(project_gid) + ").")
    except Exception as error:
        print("Error setting new owner: " + str(error))
    return

def main(service_account_token, project_gid, owner_email):
    # Configure Asana Client
    client = configure_client(service_account_token)
    # Get GID of new owner
    owner_gid = get_owner_gid(client, owner_email)
    if owner_gid == False:
        return
    else:
        None
    # Add owner as a member
    add_member = add_member_to_project(client, project_gid, owner_gid)
    # Set Project Owner
    if add_member:
        set_owner = set_project_owner(client, project_gid, owner_gid)
    else:
        None
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth", "-a", help="Service Account or Personal Access Token", dest="service_account_token", type=str, required=True)
    parser.add_argument("--project_gid", "-p", help="The project GID",dest="project_gid", type=str, required=True)
    parser.add_argument("--owner_email", "-o", help="The new project owner's email address", dest="owner_email", type=str, required=True)
    args = parser.parse_args()
    main(**vars(args))
    