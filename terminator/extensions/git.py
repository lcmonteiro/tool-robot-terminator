#!/usr/bin/env python3
###################################################################################################
###-           {Extension that handles git commands}                                           ##-#
###-                                                                                           ##-#
###-Authors:   Luis Monteiro                                                                   ##-#
###-Reviewers:                                                                                 ##-#
###################################################################################################
# comunity 
from logging     import getLogger  as logger
from git         import Repo

# framework
from robotworker.api import Pattern

# ---------------------------------------------------------------------------------------
# git initialization
# ---------------------------------------------------------------------------------------
def git_init(api, config):
    log = logger()
    # setup repositories
    api._git_repo = {}
    for name, params in config.get('repositories', {}).items():
        try:
            repo = None
            path = Pattern(params.get('path','.')).substitute(api.get_context())
            # check if repository exist if not clone it
            try:
                repo = Repo(path)
            except:
                repo = Repo.clone_from(params['uri'], path)
            # add repository
            api._git_repo[name] = repo
        except Exception as ex:
            log.error(ex)
    # save reference name
    api._git_reference = config.get('reference', 'point')

# ---------------------------------------------------------------------------------------
# git position
# ---------------------------------------------------------------------------------------
def git_position(api, repo, position):
    pass

# ---------------------------------------------------------------------------------------
# git combine
# ---------------------------------------------------------------------------------------
def git_combine(api, repo, position):
    pass

# ---------------------------------------------------------------------------------------
# git command
# ---------------------------------------------------------------------------------------
def git_cmd(api, repo, cmd, *args):
    getattr(api._git_repo[repo].git, cmd)(*args) 

# ---------------------------------------------------------------------------------------
# extension register
# ---------------------------------------------------------------------------------------
REGISTER = {
    'name' :'git',
    'init' : git_init,
    'func' : [
        git_position,
        git_combine,
        git_cmd,
    ] 
}
###################################################################################################
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------
###################################################################################################
