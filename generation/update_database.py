import os
import sys
import json
import datetime

from github import Github
from github.GithubException import UnknownObjectException, RateLimitExceededException


def read_step_info(step_file):
    def read_value(identifier):
        value = read_line(line, identifier)
        if not value:
            extended_line = line + next(lines).strip(' \t\r\n')
            value = read_line(extended_line, identifier)

        return value

    name = category = icon_path = None
    lines = iter(step_file.splitlines())
    for line in lines:
        line = line.strip()

        if line.startswith("super"):
            name = read_value("__init__")
        elif line.startswith("self._category"):
            category = read_value("=")
            if icon_path:
                break
        elif line.startswith("self._icon"):
            icon_path = read_value("QImage")
            if category:
                break

    return name, category, icon_path


def read_line(line, identifier):

    value = None
    for quote in ["'", '"']:
        start = line.find(quote, line.find(identifier) + len(identifier))
        if start == -1:
            continue
        end = line.find(quote, start + 1)
        value = line[start:end].strip(' "\'\t\r\n')

    return value


def read_file(file):
    with open(file, "r") as file:
        return json.load(file)


def write_file(file, data):
    with open(file, "w") as file:
        json.dump(data, file, default=lambda o: o.__dict__, sort_keys=True, indent=2))


def check_plugins_for_updates():
    def check_plugin_info():
        name = repo.name
        updated_at = repo.updated_at.timestamp()
        if (name not in plugin_database.keys()) or (database_timestamp < updated_at):
            step_paths = [
                f'mapclientplugins/{name}/step.py',
                f'mapclientplugins/{name}step/step.py',
                f'mapclientplugins/{name[name.find(".") + 1:]}/step.py',
                f'mapclientplugins/{name[name.find(".") + 1:]}step/step.py'
            ]
            step_file = None
            for step_path in step_paths:
                try:
                    step_file = repo.get_contents(step_path).decoded_content.decode()
                except UnknownObjectException:
                    continue
                else:
                    formatted_name, category, icon_path = read_step_info(step_file)
                    icon_name = ""
                    url = repo.url
                    version = get_latest_version(step_path)
                    plugin_database[name] = {"_name": formatted_name, "_category": category, "_icon": icon_name, "_url": url,
                                             "_version": version}
                    break
            if not step_file:
                print(f"GitHub repository \"{repo.full_name}\" in not a valid MAP-Client plugin.")

    # TODO: Once all MAP plugins have versioned-releases, update this with a version retrieval directly from the repo releases.
    def get_latest_version(step_path):
        init_file_path = os.path.dirname(step_path) + "/__init__.py"
        init_file = repo.get_contents(init_file_path).decoded_content.decode()
        version = ""
        lines = iter(init_file.splitlines())
        for line in lines:
            line = line.strip()
            if line.startswith("__version__"):
                version = read_line(line, "=")

        return version

    plugin_sources = read_file("plugin_sources.json")
    plugin_database = read_file("plugin_database.json")
    database_timestamp = datetime.datetime.fromisoformat(sys.argv[1].replace("Z", "+00:00")).timestamp()
    url_submission = sys.argv[2]

    plugin_orgs = plugin_sources["plugin_organizations"]
    plugin_repos = plugin_sources["plugin_repositories"]
    if url_submission:
        plugin_repos.append(url_submission)
        plugin_sources["plugin_repositories"] = plugin_repos

    g = Github(os.environ["GITHUB_TOKEN"])
    i = 0
    while i < 2:
        try:
            for organisation in plugin_orgs:
                org = g.get_organization(organisation)
                for repo in org.get_repos():
                    check_plugin_info()

            for repository in plugin_repos:
                repo = g.get_repo(repository)
                check_plugin_info()

            break
        except RateLimitExceededException:
            i += 1
            if i < 2:
                g = authenticate_github_user()

    write_file("plugin_database.json", plugin_database)
    write_file("plugin_sources.json", plugin_sources)


if __name__ == '__main__':
    check_plugins_for_updates()
