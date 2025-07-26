import requests

rubrique_lookup_table = {
    68: "Web - Server",
    189: "App - Script",
    203: "App - System",
    208: "Forensic",
    69: "Cracking",
    16: "Web - Client",
    18: "Cryptanalysis",
    182: "Network",
    17: "Programming",
    67: "Steganography",
    70: "Realist",
}


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


def get_most_played_rubriques(user_data: dict) -> list:
    """
    Extracts the most played rubriques from user data.

    Args:
        user_data (dict): A dictionary containing user information.

    Returns:
        list: A list of the most played rubriques.
    """
    played_rubriques = {}
    for challenge in user_data.get('validations', []):
        id = challenge.get('id_rubrique', None)
        if played_rubriques.get(id) is None:
            played_rubriques[id] = 0
        played_rubriques[id] += 1

    return sorted(played_rubriques.items(), key=lambda x: x[1], reverse=True)


def get_number_of_users(api_key: str) -> int:
    """
    Fetches the total number of users from Root-Me.

    Args:
        api_key (str): The Root-Me API KEY.

    Returns:
        int: The total number of users.
    """
    url = "https://api.www.root-me.org/auteurs?debut_auteurs=9999999"

    try:
        response = requests.get(url, cookies={"api_key": api_key})
        response.raise_for_status()  # Raise an exception for HTTP errors

        return int(list(response.json()[0].items())[-1][1].get('id_auteur'))

    except requests.exceptions.RequestException as err:
        print(f"Error fetching user count: {err}")
        return -1


def get_number_of_ranked_users(api_key: str) -> int:
    """
    Fetches the total number of ranked users from Root-Me.

    Args:
        api_key (str): The Root-Me API KEY.
    Returns:
        int: The total number of ranked users.
    """
    url = "https://api.www.root-me.org/classement?debut_classement=9999999"

    try:
        response = requests.get(url, cookies={"api_key": api_key})
        response.raise_for_status()  # Raise an exception for HTTP errors

        return list(response.json()[0].items())[-1][1].get('place', -1)

    except requests.exceptions.RequestException as err:
        print(f"Error fetching ranked user count: {err}")
        return -1
