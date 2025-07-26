from PIL import Image, ImageDraw, ImageFont


def get_rank_logo(points: int, base_dir: str) -> Image:
    """
    Returns the rank logo based on the user's points.

    Args:
        points (int): The user's points.
        base_dir (str): The base directory.

    Returns:
        Image: The rank logo image.
    """
    if points < 100:
        return Image.open(f"{base_dir}/assets/visitor.png")
    elif points < 500:
        return Image.open(f"{base_dir}/assets/curious.png")
    elif points < 2481:
        return Image.open(f"{base_dir}/assets/trainee.png")
    elif points < 4463:
        return Image.open(f"{base_dir}/assets/insider.png")
    elif points < 10562:
        return Image.open(f"{base_dir}/assets/enthusiast.png")
    elif points < 16852:
        return Image.open(f"{base_dir}/assets/hacker.png")
    elif points < 24285:
        return Image.open(f"{base_dir}/assets/elite.png")
    else:
        return Image.open(f"{base_dir}/assets/legend.png")


def create_badge(user_data: dict, base_dir: str, path_profile_picture: str, path_badge: str = None) -> None:
    """
    Creates a badge image with the user's profile picture and name.
    Args:
        user_data (dict): A dictionary containing user information, including the profile picture URL and name.
        base_dir (str): The base directory.
        path_profile_picture (str): The path to the profile picture.
    """

    # Check if path_badge is provided, otherwise set a default path
    if path_badge is None:
        path_badge = f"{base_dir}/badge.png"

    # Create a white background
    image = Image.new("RGB", (800, 400), color="white")

    # Load fonts
    font_bold = ImageFont.truetype(
        f"{base_dir}/fonts/OpenSans_Condensed-Regular.ttf", 40)
    ascent_font_bold, descent_font_bold = font_bold.getmetrics()

    font = ImageFont.truetype(
        f"{base_dir}/fonts/OpenSans_Condensed-Regular.ttf", 30)
    ascent_font, descent_font = font.getmetrics()

    font_mini = ImageFont.truetype(
        f"{base_dir}/fonts/OpenSans_Condensed-Regular.ttf", 18)
    ascent_font_mini, descent_font_mini = font_mini.getmetrics()

    font_italic = ImageFont.truetype(
        f"{base_dir}/fonts/OpenSans_Condensed-Italic.ttf", 20)
    ascent_font_italic, descent_font_italic = font_italic.getmetrics()

    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)

    # Calculate positions
    border = image.height * 5 // 100
    profice_pic_size = image.height - border * 2
    rootme_logo_size = image.height * 20 // 100
    logo_pos_x = 3 * border + profice_pic_size
    text_pos_x = logo_pos_x + font_bold.size + border
    text_pos_y = int(1.8 * border)
    logo_size = font_bold.size
    line_height = logo_size * 40 // 100 + text_pos_y

    # Add the profile picture in the left side
    profile_pic = Image.open(path_profile_picture)
    profile_pic = profile_pic.resize(
        (profice_pic_size, profice_pic_size))

    # Paste image in the center of the left side of the badge
    image.paste(profile_pic, (border, border))

    # Add the Root-Me logo in the right side
    rootme_logo = Image.open(f"{base_dir}/assets/rootme_logo.png")
    rootme_logo = rootme_logo.resize(
        (rootme_logo_size, rootme_logo_size))

    # Row 1
    y1 = text_pos_y
    rank_logo = get_rank_logo(int(user_data.get("score", 0)), base_dir)
    rank_logo = rank_logo.resize(
        (logo_size, logo_size))
    image.paste(rank_logo, (logo_pos_x, y1), rank_logo)

    draw.text((text_pos_x, y1 - ascent_font_bold + logo_size),
              user_data.get("nom"), fill="black", font=font_bold)

    # Row 2: User Rank
    y2 = y1 + line_height
    points_logo = Image.open(f"{base_dir}/assets/points.png")
    points_logo = points_logo.resize(
        (logo_size, logo_size))
    image.paste(points_logo, (logo_pos_x, y2), points_logo)

    draw.text((text_pos_x, y2 - ascent_font + logo_size),
              f"{user_data.get("score")} Points", fill="black", font=font)

    # Row 3: User Position
    y3 = y2 + line_height
    classement_logo = Image.open(f"{base_dir}/assets/classement.png")
    classement_logo = classement_logo.resize(
        (logo_size, logo_size))
    image.paste(classement_logo, (logo_pos_x, y3), classement_logo)

    user_position = user_data.get("position")
    total_users = user_data.get("total_users")

    draw.text((text_pos_x, y3 - ascent_font + logo_size),
              f"{user_position} / {total_users} ({round(100 * user_position / total_users, 2)}%)", fill="black", font=font)

    # Paste the Root-Me logo in the bottom right corner
    image.paste(rootme_logo, (image.width - rootme_logo.width,
                              border // 4), rootme_logo)

    y_medal = y3 + line_height + int(4.5 * border)
    # Paste Silver Medal
    x1_medal = text_pos_x - int(1.2 * border)

    silver_medal_logo = Image.open(f"{base_dir}/assets/silver_medal.png")

    ratio = (logo_size / silver_medal_logo.width) * 0.75
    silver_medal_logo = silver_medal_logo.resize(
        (int(silver_medal_logo.width * ratio), int(silver_medal_logo.height * ratio)))
    image.paste(silver_medal_logo, (x1_medal, y_medal), silver_medal_logo)

    draw.text((x1_medal + silver_medal_logo.width // 2, y_medal + silver_medal_logo.height + descent_font_mini),
              f"{user_data["most_played"][1][0]} ({user_data["most_played"][1][1]})", fill="black", font=font_mini, anchor="mt")

    # Paste Gold Medal
    x2_medal = x1_medal + logo_size + 4 * border

    gold_medal_logo = Image.open(f"{base_dir}/assets/gold_medal.png")
    gold_medal_logo = gold_medal_logo.resize(
        (int(gold_medal_logo.width * ratio), int(gold_medal_logo.height * ratio)))
    image.paste(gold_medal_logo, (x2_medal,
                y_medal - int(border * 1.5)), gold_medal_logo)

    draw.text((x2_medal + gold_medal_logo.width // 2, y_medal - int(border * 1.5) + gold_medal_logo.height + descent_font_mini),
              f"{user_data["most_played"][0][0]} ({user_data["most_played"][0][1]})", fill="black", font=font_mini, anchor="mt")

    # Paste Bronze Medal
    x3_medal = x2_medal + logo_size + 4 * border

    bronze_medal_logo = Image.open(f"{base_dir}/assets/bronze_medal.png")
    bronze_medal_logo = bronze_medal_logo.resize(
        (int(bronze_medal_logo.width * ratio), int(bronze_medal_logo.height * ratio)))
    image.paste(bronze_medal_logo, (x3_medal, y_medal), bronze_medal_logo)

    draw.text((x3_medal + bronze_medal_logo.width // 2, y_medal + bronze_medal_logo.height + descent_font_mini),
              f"{user_data["most_played"][2][0]} ({user_data["most_played"][2][1]})", fill="black", font=font_mini, anchor="mt")

    # Most Played Rubriques
    draw.text((x2_medal + gold_medal_logo.width // 2, y_medal - int(border * 2) - ascent_font_italic),
              "Most Played", fill="black", font=font_italic, anchor="mt")

    # Save to file
    print(path_badge)
    image.save(path_badge)
