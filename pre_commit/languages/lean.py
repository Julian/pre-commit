import contextlib
from typing import Generator
from typing import Sequence
from typing import Tuple

from pre_commit.envcontext import envcontext
from pre_commit.envcontext import PatchesT
from pre_commit.hook import Hook
from pre_commit.languages import helpers
from pre_commit.prefix import Prefix
from pre_commit.util import cmd_output_b

ENVIRONMENT_DIR = 'lean'
get_default_version = helpers.basic_get_default_version
install = helpers.no_install


def healthy(prefix: Prefix, language_version: str) -> bool:
    with in_env(prefix, language_version):
        retcode, _, _ = cmd_output_b('lean', '--version', retcode=None)
        return retcode == 0


def get_env_patch(venv: str) -> PatchesT:
    return ()


@contextlib.contextmanager
def in_env(
        prefix: Prefix,
        language_version: str,
) -> Generator[None, None, None]:
    target_dir = prefix.path(
        helpers.environment_dir(ENVIRONMENT_DIR, get_default_version()),
    )
    with envcontext(get_env_patch(target_dir)):
        yield


def run_hook(
        hook: Hook,
        file_args: Sequence[str],
        color: bool,
) -> Tuple[int, bytes]:
    with in_env(hook.prefix, hook.language_version):
        return helpers.run_xargs(hook, hook.cmd, file_args, color=color)
