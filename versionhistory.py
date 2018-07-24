# versionhistory.py
# used to create versioned changelog files form GitHub commit data

import requests

# the name of the github repository to query
REPO = "lucko/LuckPerms"

# get all commit entries
commits = []
page = 1;

while True:
	response = requests.get("https://api.github.com/repos/" + REPO + "/commits?per_page=100&page=" + str(page)).json()
	if len(response) == 0:
		break

	for commit in response:
		sha = commit["sha"]
		message = commit["commit"]["message"]
		commits.append([message, sha])

	page += 1

# get all tags
tags = {}
response = requests.get("https://api.github.com/repos/" + REPO + "/tags").json()
for tag in response:
	name = tag["name"]
	sha = tag["commit"]["sha"]
	tags[sha] = name

# form output
ver = "v0.1"
patch = 0

for commit in reversed(commits):
	commitTitle = commit[0].splitlines()[0]
	commitSha = commit[1]

	if commitSha in tags:
		ver = tags[commitSha]
		patch = 0
	
	print(ver + "." + str(patch) + " - " + commitTitle)
	patch += 1
