from utils import handle_authorization
from constants import SPOTIFY_API_BASE_URL

import json
from datetime import date

import httpx
from rich import print


def get_user_top_items(
    access_token: str,
    item_type: str,
    limit: int = 20,
    offset: int = 0,
    time_range: str = "medium_term",
    write: bool = False,
):
    """Get the current user's top artists or tracks based on calculated affinity. Requires 'user-top-read' scope.

    Parameters
    ----------
    access_token : str
        Access token for authenticated user
    item_type : str
        The type of entity to return. Valid values: "artists" or "tracks"
    limit : int
        The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50.
    offset : int
        The index of the first item to return. Default: 0 (the first item). Use with limit to get the next set of items.
    time_range : str
        Over what time frame the affinities are computed.
        Valid values: "long_term" (calculated from several years of data and including all new data as it becomes available),
        "medium_term" (approximately last 6 months), "short_term" (approximately last 4 weeks).
        Default: medium_term
    """
    url = f"{SPOTIFY_API_BASE_URL}/me/top/{item_type}"
    params = {
        "limit": limit,
        "offset": offset,
        "time_range": time_range,
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    response = httpx.get(url=url, params=params, headers=headers)

    if response.status_code == 200:
        if write:
            with open(
                f"top_{limit}_{item_type}_{time_range}-{date.today()}.json", "w"
            ) as top_file:
                json.dump(response.json(), top_file)
    else:
        print(f"Error {response.status_code}: {response.text}")


if __name__ == "__main__":
    token_info = handle_authorization(save_files=True)
    get_user_top_items(token_info["access_token"], item_type="artists", write=True)
