#!/usr/bin/env python

import argparse
import gitlab
import os

gitlab_url = 'https://gitlab.com'
jira_url = 'https://verneglobal.atlassian.net'
jira_api_url = jira_url
jira_username = 'darren.birkett@verneglobal.com'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        default=False, dest='debug')
    parser.add_argument('--gitlab-private-token',
                        default=os.environ.get('VERNE_GITLAB_PRIVATE_TOKEN'),
                        dest='gitlab_private_token')
    parser.add_argument('--jira-api-token',
                        default=os.environ.get('VERNE_JIRA_API_TOKEN'),
                        dest='jira_api_token')
    args = parser.parse_args()
    return args


def get_projects(gl):
    # get all projects where I am owner
    return gl.projects.list(owned=True, all=True)


def update_project_jira_config(project, jira_url, jira_api_url,
                               jira_username, jira_password):
    # actually update the jira service config
    jira_service = project.services.get('jira')
    jira_service.url = jira_url
    jira_service.api_url = jira_api_url
    jira_service.username = jira_username
    jira_service.password = jira_password
    jira_service.active = True
    try:
        jira_service.save()
        print("Saved project JIRA Config OK")
    except:
        print("Something went wrong saving project JIRA config")

######################
#        main        #
######################


def main():

    args = get_args()
    jira_api_token = args.jira_api_token

    gl = gitlab.Gitlab(gitlab_url, private_token=args.gitlab_private_token)
    if args.debug:
        gl.enable_debug()

    projects = get_projects(gl)
    for project in projects:
        proj_name = project.name
        proj_id = project.id
        print("Parsing %s: %s" % (proj_id, proj_name))
        update_project_jira_config(project, jira_url, jira_api_url,
                                   jira_username, jira_api_token)


if __name__ == "__main__":
    main()
