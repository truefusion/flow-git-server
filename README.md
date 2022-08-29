# flow-git-server

Git API server.

## API

| Verb | Path | Desc |
| ---- | ---- | ---- |
| GET | / | Load `/app/index.html` |
| POST | /{repo-name}/register | Register repository. |
| GET | /{repo-name}/branches | Get branches. |
| POST | /{repo-name}/branches | Create branch. |
| PUT | /{repo-name}/branches | Checkout branch. |