from PIL import Image, ImageDraw, ImageFont


def create_badge(user_data: dict = None) -> None:
    """
    Creates a badge image with the user's profile picture and name.
    Args:
        user_data (dict): A dictionary containing user information, including the profile picture URL and name.
    """
    # Create a new RGB image (width=200, height=100), white background
    image = Image.new("RGB", (1000, 500), color="white")

    # Draw something on it
    draw = ImageDraw.Draw(image)

    # Add the profile picture in the left side
    profile_pic = Image.open("profile_picture.png")
    profile_pic = profile_pic.resize((360, 360))  # Resize to fit the badge
    # Paste it at (10, 25)
    image.paste(profile_pic, ((image.width // 2 - profile_pic.width) // 2,
                (image.height - profile_pic.height) // 2))

    # Set the font to Open Sans
    # Note: You may need to install the font or use a default one
    font = ImageFont.truetype("fonts/OpenSans-Regular.ttf", 40)

    draw.text((image.width // 2 + image.width * 5 // 100, (image.height // 2 - profile_pic.height // 2) + 20),
              user_data.get("nom"), fill="black", font=font)

    # Save to file
    image.save("badge.png")
