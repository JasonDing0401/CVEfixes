import json
import subprocess

exist_repos = set()
with open("/home/ding/dlvp/dl-vulnerability-detection/data/commits/summary/bugzilla_redhat_commits_summary.json", "r") as f:
    dic_lst = json.load(f)
    for dic in dic_lst:
        exist_repos.add(dic["repo_url"])
with open("/home/ding/dlvp/dl-vulnerability-detection/data/commits/summary/snykio_commits_summary.json", "r") as f:
    dic_lst = json.load(f)
    for dic in dic_lst:
        exist_repos.add(dic["repo_url"])
        
clone_repos = set()
with open("cvefixes.json", "r") as f:
    dic_lst = json.load(f)
    for dic in dic_lst:
        clone_repos.add(dic["repo_url"])

# 2487
print(f"total repos {len(clone_repos)}======")
count = 0
for repo in clone_repos:
    if repo in exist_repos:
        continue
    repo = repo + ".git"
    subprocess.call(["git", "clone", repo], cwd="/scr/dlvp_local_data/repos")
    count += 1

# 1522
print(f"cloned repos {count}======")