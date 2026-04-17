import os
import datetime
from github import Github, Auth

def get_github_client():
    token = os.getenv('GITHUB_TOKEN')
    auth = Auth.Token(token)
    return Github(auth=auth)

def check_inactivity(issue_or_pr, inactivity_days):
    last_update = issue_or_pr.updated_at
    if datetime.datetime.now(datetime.timezone.utc) - last_update > datetime.timedelta(days=inactivity_days):
        return True
    return False

def add_clock_reaction(issue_or_pr):
    issue_or_pr.add_reaction('⏰')

def process_issues(repo, inactivity_days):
    issues = repo.get_issues(state='open')
    for issue in issues:
        if check_inactivity(issue, inactivity_days):
            add_clock_reaction(issue)

def process_prs(repo, inactivity_days):
    prs = repo.get_pulls(state='open')  # Cambié de get_pull_requests a get_pulls
    for pr in prs:
        if check_inactivity(pr, inactivity_days):
            add_clock_reaction(pr)

def main():
    repo_owner = os.getenv('REPO_OWNER')
    repo_name = os.getenv('REPO_NAME')
    inactivity_days = int(os.getenv('INACTIVITY_DAYS'))
    client = get_github_client()
    repo = client.get_repo(f'{repo_owner}/{repo_name}')
    process_issues(repo, inactivity_days)
    process_prs(repo, inactivity_days)

if __name__ == '__main__':
    main()
