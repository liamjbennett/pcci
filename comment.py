#!/usr/bin/env python

# from pdb import set_trace; set_trace()

import redis
from github import Github
import config
import time

# puppet-community-ci+test+3+1424905505+FAIL


def main_loop():
    while True:
        comment_to_make = r.lpop('completed')
        if comment_to_make is None:
            print "looping"
            time.sleep(5)
        else:
            comment(comment_to_make)


def comment(comment_to_make):
    org, project, pr, ts, success = comment_to_make.split('+')
    print "Considering: {0}".format(comment_to_make)
    print "org: {0}, project: {1}, pr {2}".format(org, project, pr)

    if project not in config.commentable:
        return

    pr_object = g.get_repo(org + "/" + project).get_pull(int(pr))
    sha = pr_object.head.sha
    print "sha: {0}".format(sha)
    commits = pr_object.get_commits()
    commit = None
    for c in commits:
        if c.sha == sha:
            commit = c
            break

    if success == 'PASS':
        status = 'success'
    else:
        status = 'failure'
    commit.create_status(status,
                         target_url="{0}{1}".format(config.rooturl,
                                                    comment_to_make),
                         description="PCCI Voting System",
                         context="continuous-integration/pcci")


if __name__ == "__main__":

    g = Github(config.pccibottoken)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    main_loop()
