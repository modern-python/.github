import dataclasses
import io
import json
import os
import pathlib
import re
import subprocess
import tarfile
import typing
import urllib.request

from census import registry


MAX_TEXT_FILE_BYTES: typing.Final = 512 * 1024
_REMOTE_NAME: typing.Final = re.compile(r"modern-python/(?P<name>[^/\s]+?)(?:\.git)?\s*$")


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class RepoSnapshot:
    name: str
    files: typing.Mapping[str, str]
    description: str | None = None
    topics: tuple[str, ...] | None = None
    homepage: str | None = None

    def read(self, path: str) -> str | None:
        return self.files.get(path)

    def has_dir(self, prefix: str) -> bool:
        wanted = prefix.rstrip("/") + "/"
        return any(path.startswith(wanted) for path in self.files)

    def workflow_names(self) -> frozenset[str]:
        prefix = ".github/workflows/"
        return frozenset(path.removeprefix(prefix) for path in self.files if path.startswith(prefix))


def github_token() -> str | None:
    if token := os.environ.get("GITHUB_TOKEN"):
        return token
    try:
        return subprocess.run(["gh", "auth", "token"], check=True, capture_output=True, text=True).stdout.strip()  # noqa: S607
    except (OSError, subprocess.CalledProcessError):
        return None


def _get(url: str, token: str | None) -> bytes:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "modern-python-census"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)  # noqa: S310
    with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310
        return response.read()


def _files_from_tarball(payload: bytes) -> dict[str, str]:
    files: dict[str, str] = {}
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        for member in archive:
            if not member.isfile() or member.size > MAX_TEXT_FILE_BYTES:
                continue
            path = member.name.split("/", 1)[1] if "/" in member.name else member.name
            extracted = archive.extractfile(member)
            if extracted is None:
                continue
            try:
                files[path] = extracted.read().decode("utf-8")
            except UnicodeDecodeError:
                continue
    return files


def load_from_github(token: str | None = None) -> list[RepoSnapshot]:
    token = token or github_token()
    listing = json.loads(_get(f"https://api.github.com/orgs/{registry.ORG}/repos?per_page=100&type=public", token))
    snapshots = []
    for repo in sorted(listing, key=lambda item: item["name"]):
        if repo["archived"] or repo["name"] in registry.EXCLUDED_REPOS:
            continue
        tarball = _get(
            f"https://api.github.com/repos/{registry.ORG}/{repo['name']}/tarball/{repo['default_branch']}", token
        )
        snapshots.append(
            RepoSnapshot(
                name=repo["name"],
                files=_files_from_tarball(tarball),
                description=repo.get("description"),
                topics=tuple(repo.get("topics") or ()),
                homepage=repo.get("homepage") or None,
            ),
        )
    return snapshots


def _remote_name(checkout: pathlib.Path) -> str | None:
    config = checkout / ".git" / "config"
    if not config.is_file():
        return None
    for line in config.read_text(encoding="utf-8").splitlines():
        if "url" in line and (match := _REMOTE_NAME.search(line)):
            return match.group("name")
    return None


def _files_from_checkout(checkout: pathlib.Path) -> dict[str, str]:
    files: dict[str, str] = {}
    skipped_dirs = {".git", ".venv", "node_modules", "__pycache__", ".ruff_cache", ".pytest_cache", "site"}
    for path in checkout.rglob("*"):
        if not path.is_file() or skipped_dirs & set(path.relative_to(checkout).parts):
            continue
        if path.stat().st_size > MAX_TEXT_FILE_BYTES:
            continue
        try:
            files[path.relative_to(checkout).as_posix()] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
    return files


def load_from_local(root: pathlib.Path) -> list[RepoSnapshot]:
    snapshots = []
    for checkout in sorted(root.iterdir()):
        name = _remote_name(checkout)
        if name is None or name in registry.EXCLUDED_REPOS:
            continue
        snapshots.append(RepoSnapshot(name=name, files=_files_from_checkout(checkout)))
    return snapshots
