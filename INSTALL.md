# Install ZhangLuo

This is the installation guide for AI agents and people. Proceed when the user asks to install or use ZhangLuo.
Follow the host application's permissions. Do not treat a repository URL alone as permission to install software.

## AI installation sequence

1. Identify the active agent and operating system. Find a working Python 3.10+ (`python`, `python3`, or `py -3`).
   If Python is missing, explain that prerequisite and use the platform's normal approved installation process.
2. Clone `https://github.com/SUAT-ZhangLab/ZhangLuo.git` into a new working directory, or download and extract the repository ZIP.
   Keep existing directories intact. Read this file and `install.py` before running it.
3. From the repository root, run `python install.py --check`.
4. Install for the active agent with one of the commands below. Do not ask the user to perform routine steps that your tools can complete.
5. Run `python <installed-directory>/zhangluo.py doctor`. Report the actual directory and result.
6. Explain how to reload skills or start a new session. Codex uses `$zhangluo`; Claude Code uses `/zhangluo`.
   A successful file check does not prove the host has reloaded the skill. Confirm recognition in the host when possible.
7. Do not install Docker, build an image, obtain API keys, or run model services just to finish the basic skill installation.
   Configure the container runner only when the user's task needs it.

## Choose the target

| Agent | Command | Default destination |
|---|---|---|
| Codex | `python install.py --agent codex` | `~/.agents/skills/zhangluo` |
| Codex using the older skill directory | `python install.py --agent codex-legacy` | `$CODEX_HOME/skills/zhangluo`, otherwise `~/.codex/skills/zhangluo` |
| Claude Code (local) | `python install.py --agent claude` | `~/.claude/skills/zhangluo` |
| Another agent with SKILL.md support | `python install.py --agent generic --destination "/actual/skill/path/zhangluo"` | The specified directory |

Use the active host's established skill location if it differs from these defaults; `--destination` overrides the default.
Do not install duplicate copies in multiple discovery locations. An existing identical install is left as-is;
an existing directory with different contents is preserved and reported. For an update, use a new destination or review and back up the existing copy first.

The installer copies a complete skill, not a link to the cloned checkout. The installed copy can work after the checkout is moved.
It changes only its destination directory and does not install packages or change global settings.
The repository root is also compatible with skill installers that accept a repository path of `.` with the name `zhangluo`.

## Use without installing a skill

Open this repository in the agent and ask it to read `AGENTS.md` and `SKILL.md`.
Run `python zhangluo.py doctor` from its root. Use an explicitly selected research directory for each task.
A chat-only agent can read the methods but cannot execute local programs without command/file tools.

## Optional Docker runner

Start a Docker daemon supporting Linux containers, then run from the repository or installed skill directory:

```sh
docker build -t zhangluo-runner:0.1.0 -f config/era.Dockerfile config
python zhangluo.py doctor --container
```

Windows with Docker installed only in WSL can use:

```powershell
Get-Content config/era.Dockerfile -Raw | wsl.exe -d Ubuntu-22.04 -u root --cd / --exec sh -c 'systemctl start docker && docker build -t zhangluo-runner:0.1.0 -'
$env:ZHANGLUO_DOCKER_MODE = 'wsl'
$env:ZHANGLUO_WSL_DISTRO = 'Ubuntu-22.04'
python zhangluo.py doctor --container
```

`ZHANGLUO_DOCKER_MODE` accepts `auto` (default), `native`, or `wsl`. Auto prefers a `docker` command on PATH;
otherwise Windows uses WSL. `ZHANGLUO_WSL_DISTRO` selects the actual distribution.
Do not silently switch to running generated candidate code directly on the host if Docker is unavailable.

The runner accepts JSON requests up to about 8 MiB, outputs up to about 1 MiB, and defaults to 60 seconds.
It uses a non-root container, no network, a read-only root filesystem, and no host mounts.
Large datasets, R, GPU and file batch work require an appropriate environment chosen for the task.

## Installation references

- [Codex skill locations](https://developers.openai.com/codex/skills)
- [Claude Code local skills](https://code.claude.com/docs/en/skills)
