import json
import sys

RICH_AVAILABLE = True
try:
    from rich import print as rprint
except ImportError:
    rprint = print  # type: ignore
    RICH_AVAILABLE = False


def dump(name: str, obj):
    rprint(f"<{name} dump>", file=sys.stderr)
    if RICH_AVAILABLE:
        rprint(obj, file=sys.stderr)
    else:
        rprint(
            json.dumps(
                obj, indent=4, sort_keys=True, default=lambda o: "<not serializable>"
            ),
            file=sys.stderr,
        )
    rprint(f"</{name} dump>", file=sys.stderr)
