#! /bin/python3

#    _____   ____   ____ _______   __  __ ______   ____          _____   _____ ______ _____
#   |  __ \ / __ \ / __ \__   __| |  \/  |  ____| |  _ \   /\   |  __ \ / ____|  ____|  __ \
#   | |__) | |  | | |  | | | |    | \  / | |__    | |_) | /  \  | |  | | |  __| |__  | |__) |
#   |  _  /| |  | | |  | | | |    | |\/| |  __|   |  _ < / /\ \ | |  | | | |_ |  __| |  _  /
#   | | \ \| |__| | |__| | | |    | |  | | |____  | |_) / ____ \| |__| | |__| | |____| | \ \
#   |_|  \_\\____/ \____/  |_|    |_|  |_|______| |____/_/    \_\_____/ \_____|______|_|  \_\
#
#                                  ___,,___
#                              _,-='=- =-  -`"--.__,,.._
#                              ,-;// /  - -       -   -= - "=.
#                          ,'///    -     -   -   =  - ==-=\`.
#                          |/// /  =    `. - =   == - =.=_,,._ `=/|
#                          ///    -   -    \  - - = ,ndDMHHMM/\b  \\
#                      ,' - / /        / /\ =  - /MM(,,._`YQMML  `|
#                      <_,=^Kkm / / / / ///H|wnWWdMKKK#""-;. `"0\  |
#                              `""QkmmmmmnWMMM\""WHMKKMM\   `--. \> \
#                      hjm          `""'  `->>>    ``WHMb,.    `-_<@)
#                                                      `"QMM`.
#                                                      `>>>

import argparse
import os
import tempfile

from rootme import *
from badge import *


def parse_args():
    parser = argparse.ArgumentParser(
        description="RootMeBadger - Generate a badge for Root-Me progress")

    parser.add_argument("--user-id", type=int, required=True,
                        help="Your Root-Me User ID - you can find it in https://www.root-me.org/?page=preferences")
    parser.add_argument("--api-key", type=str, required=True,
                        help="Your Root-Me API KEY - you can find it in https://www.root-me.org/?page=preferences")
    parser.add_argument("--output", type=str, default=None,
                        help="Output filename for the badge")

    return parser.parse_args()


def main(args):

    # Retrieve base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Fetch user data from Root-Me API
    user_data = get_rootme_user_info(args.user_id, args.api_key)
    if (user_data.get('error')):
        print(f"Error fetching user data: {user_data['error']}")
        exit(1)

    # Download the profile picture

    with tempfile.NamedTemporaryFile(prefix='badger_pp_', suffix='.png') as tmp_file:
        tmp_profile_picture_path = tmp_file.name

        if (not download_rootme_image(user_data.get('logo_url'), tmp_profile_picture_path)):
            exit(1)

        # Retrieve the user's most played rubriques
        user_data["most_played"] = []
        for rub, v in get_most_played_rubriques(user_data)[:3]:
            user_data["most_played"].append(
                (rubrique_lookup_table[int(rub)], v))

        # Get the number of ranked users
        user_data["total_users"] = get_number_of_ranked_users(args.api_key)
        if (user_data["total_users"] < 0):
            exit(1)

        # Create the badge
        create_badge(user_data, BASE_DIR, tmp_profile_picture_path,
                     path_badge=args.output)

    exit(0)


if __name__ == "__main__":
    args = parse_args()
    main(args)
