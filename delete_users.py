import csv
import asana
import argparse

def configure_client(service_account_token):
    # Construct the Asana client
    # https://developers.asana.com/docs/python-hello-world
    client = asana.Client.access_token(service_account_token)
    # Optional - give the client a name
    client.options['client_name'] = "move_projects"
    return client

def parse_email(csv_path):
    # Get the list of user emails from the csv file
    emails = []
    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row['Email Address']
            emails.append(email)
    return emails

def delete_users(client, org_id, user):
    # https://developers.asana.com/docs/remove-a-user-from-a-workspace-or-organization
    try:
        result = client.workspaces.remove_user_for_workspace(org_id, {"user":user})
        print("Successfully deleted " + user)
        return_bool = True
    except (asana.error.NotFoundError) as error:
        print(user + " not found. Nothing to delete.")
        return_bool = True
    except (asana.error.InvalidRequestError, asana.error.ServerError) as error:
        print("Error while deleting " + user + ": " + error.message)
        return_bool = False
    except (asana.error.RateLimitEnforcedError) as error:
        print("You've hit a rate limit. PLease retry after given amount of time: " + error.retry_after)
        return_bool = False
    except (asana.error.ForbiddenError) as error:
        print("Only accounts with administrative privledges can remove a user from the workspace.")
        return_bool = False
    return return_bool

def main(service_account_token, mode, csv_path, org_id):
    # Configure Client
    client = configure_client(service_account_token)
    # Get the emails from the CSV file
    emails = parse_email(csv_path)
    # Delete
    for email in emails:
        if mode.lower() == 'action':
            result = delete_users(client, org_id, email)
            if result == False:
                break
        else:
            print("[Dry Run] Delete: " + str(email))
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth", "-a", help="Service Account or Personal Access Token", dest="service_account_token", type=str, required=True)
    parser.add_argument("--mode", "-m", choices=['dry_run', 'action'], help="Mode to run the script", dest="mode", type=str, default="dry_run")
    parser.add_argument("--csv", "-c", help="Path to the CSV file", dest="csv_path", type=str, required=True)
    parser.add_argument("--organization_id", "-o", help="Organization or Workspace ID", dest="org_id", type=str, required=True)
    args = parser.parse_args()
    main(**vars(args))
