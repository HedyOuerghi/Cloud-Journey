import requests
import sys

def fetch_user(username):
        """
    Fetch public information about a GitHub user.

    Args:
        username (str): GitHub username.

    Returns:
        dict | None: User data, or None if the user does not exist.

    Raises:
        requests.exceptions.RequestException: On network or HTTP errors.
    """
    response = requests.get("https://api.github.com/users/" + username, timeout=10)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <github_username>", file=sys.stderr)
        sys.exit(1)
    username = sys.argv[1]
    try:
        user_info = fetch_user(username)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user info: {e}", file=sys.stderr)
        sys.exit(1)
    if user_info is None:
        print(f"{'User':<14}: '{username}' not found.", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"{'User':<14}: '{user_info['login']}'")
        print(f"{'Name':<14}: {user_info['name'] or '(Not Set)'}")
        print(f"{'Public Repos':<14}: {user_info['public_repos']}")
        print(f"{'Created At':<14}: {user_info['created_at']}")


if __name__ == "__main__":
    main()