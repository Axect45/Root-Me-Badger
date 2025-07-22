import requests


def get_rootme_user_info(user_id: int, api_key: str) -> dict:
    """
    Fetches Root-Me user information by user ID.

    Args:
        user_id (int): The Root-Me user ID.
        api_key (str): The Root-Me API KEY.

    Returns:
        dict: A dictionary containing user information if successful, or an error message.
    """

    url = f"https://api.www.root-me.org/auteurs/{user_id}"

    try:
        response = requests.get(url, cookies={"api_key": api_key})
        response.raise_for_status()  # Raise an exception for HTTP errors

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error occurred: {req_err}"}
    except Exception as err:
        return {"error": f"An unexpected error occurred: {err}"}


def download_rootme_image(url_path: str, save_path: str) -> bool:
    """
    Downloads an image from a given URL and saves it to the specified path.

    Args:
        url_path (str): The URL path of the image to download from root-me.org.
        save_path (str): The local path where the image will be saved.

    Returns:
        bool: True if the download was successful, False otherwise.
    """

    url = f"https://api.www.root-me.org/{url_path}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        with open(save_path, 'wb') as file:
            file.write(response.content)

        return True

    except requests.exceptions.RequestException as err:
        print(f"Error downloading image: {err}")
        return False
