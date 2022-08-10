from api import get_user_top_items
from utils import handle_authorization
from constants import APP_DIR, GetTopItems, GetTopTimeRanges

import typer


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
    write: bool = typer.Option(False),
):
    get_user_top_items(
        access_token=token_info["access_token"],
        item_type=item_type.value,
        limit=limit,
        offset=offset,
        time_range=f"{time_range.value}_term",
        write=write,
    )


if __name__ == "__main__":
    app()
