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
from rootme import *
from badge import *


def main():
    parser = argparse.ArgumentParser(
        description="RootMeBadger - Generate a badge for Root-Me progress")

    parser.add_argument("--user-id", type=int, required=True,
                        help="Your Root-Me User ID - you can find it in https://www.root-me.org/?page=preferences")
    parser.add_argument("--api-key", type=str, required=True,
                        help="Your Root-Me API KEY - you can find it in https://www.root-me.org/?page=preferences")
    parser.add_argument("--output", type=str, default="badge.png",
                        help="Output filename for the badge")

    args = parser.parse_args()

    user_data = get_rootme_user_info(args.user_id, args.api_key)
    if (user_data.get('error')):
        print(f"Error fetching user data: {user_data['error']}")
        exit(1)

    print(f"User data fetched successfully: {user_data}")

    if (not download_rootme_image(user_data.get('logo_url'), "profile_picture.png")):
        exit(1)

    create_badge(user_data)


if __name__ == "__main__":
    main()
