import pygit2;
from fastapi import APIRouter, Body, Response;
from pydantic import BaseModel;

class Repo(BaseModel):
    name: str;
    path: str;

repos = {};
router = APIRouter();

def getBranches(repo: pygit2.Repository, section):
    ret = [];
    branches = repo.branches;
    section = list(section);
    for b in section:
        b = branches[b];
        ret.append({
            'name': b.branch_name,
            'active': b.is_checked_out(),
        });
    return ret;

def getRepository(name: str, path: str = None):
    if name in repos:
        return repos[name];
    elif path is not None:
        repo = pygit2.discover_repository(path);
        if repo is not None:
            repo = pygit2.Repository(repo);
            repos[name] = repo;
            return repo;

    return None;

def getStatus(flags):
    if flags in [pygit2.GIT_STATUS_INDEX_DELETED, pygit2.GIT_STATUS_WT_DELETED]:
        return 'removed';
    if flags in [pygit2.GIT_STATUS_INDEX_MODIFIED, pygit2.GIT_STATUS_WT_MODIFIED]:
        return 'modified';
    if flags in [pygit2.GIT_STATUS_INDEX_NEW, pygit2.GIT_STATUS_WT_NEW]:
        return 'new';
    if flags is [pygit2.GIT_STATUS_INDEX_RENAMED, pygit2.GIT_STATUS_WT_RENAMED]:
        return 'renamed';
    # if flags is pygit2.GIT_STATUS_INDEX_TYPECHANGE:
    #     return 'type-changed';
    return 'unmodified';

@router.post('/')
async def post_Repository(path: str):
    pygit2.init_repository(path);

@router.put('/')
async def put_Repository(url: str, path: str):
    pygit2.clone_repository(url, path);

@router.post('/{name}/register')
async def post_RepositoryRegister(response: Response, name: str, path: str = Body(embed=True)):
    repo = getRepository(name, path);
    if repo is None:
        response.status_code = 404;

@router.get('/{repo}/branches')
async def get_RepositoryBranches(response: Response, repo: str):
    ret = {};
    repo = getRepository(repo);
    if repo is None:
        response.status_code = 404;
    else:
        local = getBranches(repo, repo.branches.local);
        remote = getBranches(repo, repo.branches.remote);
        ret = {
            'local': local,
            'remote': remote,
        };

    return ret;

@router.put('/{repo}/branches')
async def put_RepositoryBranches(response: Response, repo: str, branch: str = Body(embed=True)):
    repo = getRepository(repo);
    if repo is None:
        response.status_code = 404;
    else:
        branch = repo.lookup_reference(branch);
        repo.checkout(branch);

@router.get('/{repo}/commits')
async def get_RepositoryBranches(response: Response, repo: str, limit: int = 100):
    ret = [];
    repo = getRepository(repo);
    if repo is None:
        response.status_code = 404;
    else:
        for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL):
            ret.append({
                'author': {
                    'email': commit.author.email,
                    'name': commit.author.name,
                },
                'date': commit.commit_time,
                'message': commit.message,
            });

            if limit != -1 and len(ret) == limit:
                break;

    return ret;

@router.get('/{repo}/index')
async def get_RepositoryBranches(response: Response, repo: str):
    ret = [];
    repo = getRepository(repo);
    if repo is None:
        response.status_code = 404;
    else:
        repo.index.read();
        for entry in repo.index:
            status = repo.status_file(entry.path);
            ret.append({
                'path': entry.path,
                'status': getStatus(status),
            });

    return ret;

@router.get('/{repo}/status')
async def get_RepositoryBranches(response: Response, repo: str):
    ret = [];
    repo = getRepository(repo);
    if repo is None:
        response.status_code = 404;
    else:
        status = repo.status();
        for filepath, flags in status.items():
            if flags is not pygit2.GIT_STATUS_CURRENT:
                ret.append({
                    'path': filepath,
                    'status': getStatus(flags),
                });

    return ret;