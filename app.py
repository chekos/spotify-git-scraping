from pathlib import Path
from datetime import datetime as dt

import typer
from rich import print
from pytz import timezone

from api import get_user_top_items, get_user_recently_played
from constants import (
    APP_DIR,
    GetTopItems,
    GetTopTimeRanges,
    GetRecentlyPlayedDirections,
)
from utils import handle_authorization, handle_response


def init():
    if not APP_DIR.exists():
        APP_DIR.mkdir()
    global token_info
    token_info = handle_authorization(save_files=True)


app = typer.Typer(callback=init)


@app.command()
def get_top(
    item_type: GetTopItems = typer.Argument(
        GetTopItems.artists, case_sensitive=False, help="The type of entity to return."
    ),
    limit: int = typer.Option(
        20, help="The maximum number of items to return.", min=0, max=50
    ),
    offset: int = typer.Option(
        0,
        help="The index of the first item to return. Default: 0 (the first item). Use with limit to get the next set of items.",
    ),
    time_range: GetTopTimeRanges = typer.Option(
        GetTopTimeRanges.medium_term,
        help="""Over what time frame the affinities are computed. Valid values:
        'long' (calculated from several years of data and including all new data as it becomes available),
        'medium' (approximately last 6 months), 'short' (approximately last 4 weeks).""",
    ),
    write: bool = False,
    filename: Path = typer.Option("", help="File to write output to."),
):
    response = get_user_top_items(
        access_token=token_info["access_token"],
        item_type=item_type.value,
        limit=limit,
        offset=offset,
        time_range=f"{time_range.value}_term",
    )
    # filename value was entered
    if filename != Path("."):
        filename = filename.with_suffix(".json")

    # write is true but not filename was entered
    if write and filename == Path("."):
        filename = Path(typer.prompt("Output filename")).with_suffix(".json")

    data = handle_response(response, write=write, filename=filename)

    if not write:
        print(data)


@app.command()
def get_recently_played(
    direction: GetRecentlyPlayedDirections = typer.Argument(
        GetRecentlyPlayedDirections.before,
        case_sensitive=False,
        help="Whether to get items 'before' or 'after' `timestamp`.",
    ),
    timestamp: dt = typer.Argument(
        "2022-08-10", help="Time to start getting items from."
    ),
    limit: int = typer.Option(
        20, help="The maximum number of items to return.", min=1, max=50
    ),
    time_zone: str = typer.Option("America/Tijuana", help="Timezone"),
    write: bool = False,
    filename: Path = typer.Option("", help="File to write output to."),
):
    # transform date from timestamp to unix timestamp in milliseconds
    timestamp = timestamp.replace(tzinfo=timezone(time_zone))
    timestamp = int(timestamp.timestamp()) * 1_000

    response = get_user_recently_played(
        access_token=token_info["access_token"],
        timestamp=timestamp,
        direction=direction,
        limit=limit,
    )

    # filename value was entered
    if filename != Path("."):
        filename = filename.with_suffix(".json")

    # write is true but not filename was entered
    if write and filename == Path("."):
        filename = Path(typer.prompt("Output filename")).with_suffix(".json")

    data = handle_response(response, write=write, filename=filename)

    if not write:
        print(data)


if __name__ == "__main__":
    app()
