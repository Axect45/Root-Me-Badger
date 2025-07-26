from PIL import Image, ImageDraw, ImageFont


def get_rank_logo(points: int) -> Image:
    """
    Returns the rank logo based on the user's points.

    Args:
        points (int): The user's points.

    Returns:
        Image: The rank logo image.
    """
    if points < 100:
        return Image.open("assets/visitor.png")
    elif points < 500:
        return Image.open("assets/curious.png")
    elif points < 2481:
        return Image.open("assets/trainee.png")
    elif points < 4463:
        return Image.open("assets/insider.png")
    elif points < 10562:
        return Image.open("assets/enthusiast.png")
    elif points < 16852:
        return Image.open("assets/hacker.png")
    elif points < 24285:
        return Image.open("assets/elite.png")
    else:
        return Image.open("assets/legend.png")


def create_badge(user_data: dict = None) -> None:
    """
    Creates a badge image with the user's profile picture and name.
    Args:
        user_data (dict): A dictionary containing user information, including the profile picture URL and name.
    """
    # Create a new RGB image (width=200, height=100), white background
    image = Image.new("RGB", (800, 400), color="white")

    # Set the font to Open Sans
    # Note: You may need to install the font or use a default one
    font_bold = ImageFont.truetype(
        "fonts/OpenSans_Condensed-Regular.ttf", 40)

    # Get font metrics
    ascent_font_bold, descent_font_bold = font_bold.getmetrics()

    font = ImageFont.truetype(
        "fonts/OpenSans_Condensed-Regular.ttf", 30)

    # Get font metrics
    ascent_font, descent_font = font.getmetrics()

    font_mini = ImageFont.truetype(
        "fonts/OpenSans_Condensed-Regular.ttf", 18)

    # Get font metrics
    ascent_font_mini, descent_font_mini = font_mini.getmetrics()

    font_italic = ImageFont.truetype(
        "fonts/OpenSans_Condensed-Italic.ttf", 20)

    # Get font metrics
    ascent_font_italic, descent_font_italic = font_italic.getmetrics()

    # Draw something on it
    draw = ImageDraw.Draw(image)

    border = image.height * 5 // 100
    profice_pic_size = image.height - border * 2
    rootme_logo_size = image.height * 20 // 100
    logo_pos_x = 3 * border + profice_pic_size
    text_pos_x = logo_pos_x + font_bold.size + border
    text_pos_y = int(1.8 * border)

    # Add the profile picture in the left side
    profile_pic = Image.open("profile_picture.png")
    profile_pic = profile_pic.resize(
        (profice_pic_size, profice_pic_size))

    # Paste image in the center of the left side of the badge
    image.paste(profile_pic, (border, border))

    # Add the Root-Me logo in the right side
    rootme_logo = Image.open("assets/rootme_logo.png")
    rootme_logo = rootme_logo.resize(
        (rootme_logo_size, rootme_logo_size))

    # Logo Size
    logo_size = font_bold.size

    # Line Height
    line_height = logo_size * 40 // 100 + text_pos_y

    # Row 1
    y1 = text_pos_y
    rank_logo = get_rank_logo(int(user_data.get("score", 0)))
    rank_logo = rank_logo.resize(
        (logo_size, logo_size))
    image.paste(rank_logo, (logo_pos_x, y1), rank_logo)

    draw.text((text_pos_x, y1 - ascent_font_bold + logo_size),
              user_data.get("nom"), fill="black", font=font_bold)

    # Row 2: User Rank
    y2 = y1 + line_height
    points_logo = Image.open("assets/points.png")
    points_logo = points_logo.resize(
        (logo_size, logo_size))
    image.paste(points_logo, (logo_pos_x, y2), points_logo)

    draw.text((text_pos_x, y2 - ascent_font + logo_size),
              f"{user_data.get("score")} Points", fill="black", font=font)

    # Row 3: User Position
    y3 = y2 + line_height
    classement_logo = Image.open("assets/classement.png")
    classement_logo = classement_logo.resize(
        (logo_size, logo_size))
    image.paste(classement_logo, (logo_pos_x, y3), classement_logo)

    user_position = user_data.get("position")
    total_users = user_data.get("total_users")

    draw.text((text_pos_x, y3 - ascent_font + logo_size),
              f"{user_position} / {total_users} ({round(100 * user_position / total_users, 2)}%)", fill="black", font=font)

    # Paste the Root-Me logo in the bottom right corner
    # image.paste(rootme_logo, (image.width - rootme_logo.width,
    #                          image.height - rootme_logo.height - border // 4), rootme_logo)
    image.paste(rootme_logo, (image.width - rootme_logo.width,
                              border // 4), rootme_logo)

    # Quote
    # draw.text(((image.width + profice_pic_size - rootme_logo_size) // 2, image.height - border),
    #          '“x86 - 0xdeadbeef”', fill="black", font=font_italic, anchor="mb")

    y_medal = y3 + line_height + int(4.5 * border)
    # Paste Silver Medal
    x1_medal = text_pos_x - int(1.2 * border)

    silver_medal_logo = Image.open("assets/silver_medal.png")

    ratio = (logo_size / silver_medal_logo.width) * 0.75
    silver_medal_logo = silver_medal_logo.resize(
        (int(silver_medal_logo.width * ratio), int(silver_medal_logo.height * ratio)))
    image.paste(silver_medal_logo, (x1_medal, y_medal), silver_medal_logo)

    draw.text((x1_medal + silver_medal_logo.width // 2, y_medal + silver_medal_logo.height + descent_font_mini),
              f"{user_data["most_played"][1][0]} ({user_data["most_played"][1][1]})", fill="black", font=font_mini, anchor="mt")

    # Paste Gold Medal
    x2_medal = x1_medal + logo_size + 4 * border

    gold_medal_logo = Image.open("assets/gold_medal.png")
    gold_medal_logo = gold_medal_logo.resize(
        (int(gold_medal_logo.width * ratio), int(gold_medal_logo.height * ratio)))
    image.paste(gold_medal_logo, (x2_medal,
                y_medal - int(border * 1.5)), gold_medal_logo)

    draw.text((x2_medal + gold_medal_logo.width // 2, y_medal - int(border * 1.5) + gold_medal_logo.height + descent_font_mini),
              f"{user_data["most_played"][0][0]} ({user_data["most_played"][0][1]})", fill="black", font=font_mini, anchor="mt")

    # Paste Bronze Medal
    x3_medal = x2_medal + logo_size + 4 * border

    bronze_medal_logo = Image.open("assets/bronze_medal.png")
    bronze_medal_logo = bronze_medal_logo.resize(
        (int(bronze_medal_logo.width * ratio), int(bronze_medal_logo.height * ratio)))
    image.paste(bronze_medal_logo, (x3_medal, y_medal), bronze_medal_logo)

    draw.text((x3_medal + bronze_medal_logo.width // 2, y_medal + bronze_medal_logo.height + descent_font_mini),
              f"{user_data["most_played"][2][0]} ({user_data["most_played"][2][1]})", fill="black", font=font_mini, anchor="mt")

    # Most Played Rubriques
    draw.text((x2_medal + gold_medal_logo.width // 2, y_medal - int(border * 2) - ascent_font_italic),
              "Most Played", fill="black", font=font_italic, anchor="mt")

    # Save to file
    image.save("badge.png")
