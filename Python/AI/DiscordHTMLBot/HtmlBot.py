import discord
from discord.ext import commands
import random
from config import TOKEN
import os

prefix = "!"
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')

@bot.command(name='hello', help='Sends a greeting message.')
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello {author.mention}!. You can use the !clear and !create_site commands.')

@bot.command(name='clear')
async def clear(ctx):
    # Permission check
    if ctx.author.guild_permissions.manage_messages:
        # Clear all messages
        await ctx.channel.purge(limit=None)
        await ctx.send("All messages have been cleared.")
    else:
        await ctx.send("You do not have sufficient permissions to use this command. You need the manage messages permission.")

@bot.command(name='create_site', help='Describes the site you imagine with basic information and generates the HTML code automatically.')
async def create_site(ctx):
    await ctx.send("Provide the following basic information for the site:\n1. Title\n2. Subtitle\n3. Main Text\n4. Text Color\n5. Background Color\n6. Photo URLs (Write each URL on a new line)\n\nSpecify CSS properties for:\n- Font Family\n- Text Alignment\n- Image Alignment\n- Font Size\n- Border Color\n- Border Style\n- Border Radius")

    site_data = await get_site_data(ctx)
    html_code = generate_html(site_data)

    # Write HTML code to a text file
    with open("site.html", "w", encoding="utf-8") as file:
        file.write(html_code)

    # Send the file to the Discord channel
    file_path = os.path.abspath("site.html")
    with open(file_path, "rb") as file:
        file_contents = discord.File(file, filename="site.html")
        await ctx.send("Here is the automatically generated HTML file for your imagined site:", file=file_contents)

async def get_site_data(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        await ctx.send("Number of Pages:")
        page_count_message = await bot.wait_for("message", check=check, timeout=60)
        page_count = int(page_count_message.content)

        pages = []
        for i in range(page_count):
            await ctx.send(f"\n--- Page {i + 1} ---")
            page_data = await ask_user_for_page_data(ctx)
            pages.append(page_data)

        return {
            "page_count": page_count,
            "pages": pages
        }

    except TimeoutError:
        await ctx.send("Timeout. Please try again.")
        return {}

async def ask_user_for_page_data(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send("Title:")
    title_message = await bot.wait_for("message", check=check, timeout=60)
    title = title_message.content

    await ctx.send("Subtitle:")
    subtitle_message = await bot.wait_for("message", check=check, timeout=60)
    subtitle = subtitle_message.content

    await ctx.send("Main Text:")
    main_text_message = await bot.wait_for("message", check=check, timeout=60)
    main_text = main_text_message.content

    await ctx.send("Text Color:")
    text_color_options = ["red", "blue", "green", "yellow", "black", "orange", "random", "rgb"]
    text_color = await ask_user_choice(ctx, "Choose Text Color:", text_color_options)

    if text_color == "rgb":
        await ctx.send("RGB Code (e.g., 255,0,0):")
        rgb_code_message = await bot.wait_for("message", check=check, timeout=60)
        text_color = f"rgb({rgb_code_message.content})"

    await ctx.send("Background Color:")
    background_color_options = ["white", "red", "grey", "blue", "silver", "random", "rgb"]
    background_color = await ask_user_choice(ctx, "Choose Background Color:", background_color_options)

    if background_color == "rgb":
        await ctx.send("RGB Code (e.g., 255,0,0):")
        rgb_code_message = await bot.wait_for("message", check=check, timeout=60)
        background_color = f"rgb({rgb_code_message.content})"

    await ctx.send("Photo URLs (Write each URL on a new line):")
    image_urls_message = await bot.wait_for("message", check=check, timeout=60)
    image_urls = image_urls_message.content.split('\n')

    css_options = {
        "font_family": ["Arial, sans-serif", "Verdana, sans-serif", "Georgia, serif", "Times New Roman, serif", "random"],
        "text_alignment": ["left", "center", "right", "random"],
        "image_alignment": ["left", "random", "right"],
        "font_size": ["8px", "12px", "14px", "16px", "20px", "24px", "random"],
        "border_color": ["white", "red", "random", "rgb"],
        "border_style": ["solid", "dotted", "dashed", "random"],
        "border_radius": ["5px", "10px", "15px", "random"]
    }

    css_properties = {}
    for property_name, options in css_options.items():
        css_properties[property_name] = await ask_user_choice(ctx, f"Choose {property_name.replace('_', ' ').title()}:", options)

        if css_properties[property_name] == "rgb":
            await ctx.send(f"{property_name.replace('_', ' ').title()} RGB Code (e.g., 255,0,0):")
            rgb_code_message = await bot.wait_for("message", check=check, timeout=60)
            css_properties[property_name] = f"rgb({rgb_code_message.content})"

    return {
        "title": title,
        "subtitle": subtitle,
        "main_text": main_text,
        "text_color": text_color,
        "background_color": background_color,
        "image_urls": image_urls,
        "css_properties": css_properties
    }

def generate_html(site_data):
    html_code = f"""
<html>
    <head>
        <title>{site_data['pages'][0]['title']}</title>
        <style>
            body {{
                font-family: {site_data['pages'][0]['css_properties']['font_family']};
                color: {site_data['pages'][0]['text_color']};
                background-color: {site_data['pages'][0]['background_color']};
            }}
            h1, h2, p {{
                text-align: {site_data['pages'][0]['css_properties']['text_alignment']};
            }}
            img {{
                display: block;
                margin-left: auto;
                margin-right: auto;
                float: {site_data['pages'][0]['css_properties']['image_alignment']};
                border: {site_data['pages'][0]['css_properties']['border_color']} {site_data['pages'][0]['css_properties']['border_style']} {site_data['pages'][0]['css_properties']['border_radius']};
            }}
            #navigation {{
                display: {'' if site_data['page_count'] > 1 else 'none'};
                text-align: center;
                padding: 10px;
                background-color: #f2f2f2;
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
            }}
            #navigation a {{
                padding: 14px 16px;
                text-decoration: none;
                font-size: 17px;
                color: black;
            }}
            #navigation a:hover {{
                background-color: #ddd;
                color: black;
            }}
        </style>
        <script>
            function showPage(pageNumber) {{
                var pages = document.querySelectorAll('.page');
                for (var i = 0; i < pages.length; i++) {{
                    pages[i].style.display = 'none';
                }}
                document.getElementById('page' + pageNumber).style.display = 'block';
            }}
        </script>
    </head>
    <body>
        <div id="navigation">
            {"".join([f'<a href="javascript:void(0);" onclick="showPage({i + 1});">{i + 1}. {site_data["pages"][i]["title"]}</a>' for i in range(site_data['page_count'])])}
        </div>
        {''.join([generate_page_html(site_data['pages'][i], i + 1) for i in range(site_data['page_count'])])}
    </body>
</html>
"""
    return html_code

def generate_page_html(page_data, page_number):
    return f"""
        <div class="page" id="page{page_number}" style="display: {'block' if page_number == 1 else 'none'};">
            <h1>{page_data['title']}</h1>
            <h2>{page_data['subtitle']}</h2>
            <p>{page_data['main_text']}</p>
            {"".join([f'<img src="{url}" alt="Photo">' for url in page_data['image_urls']])}
        </div>
    """

async def ask_user_choice(ctx, question, options):
    options_text = "\n".join([f"{index + 1}. {option}" for index, option in enumerate(options)])
    message_text = f"{question}\n{options_text}\n\nPlease specify your choice (e.g., 1)."
    
    await ctx.send(message_text)

    def check(message):
        return (
            message.author == ctx.author
            and message.channel == ctx.channel
            and message.content.isdigit()
            and 1 <= int(message.content) <= len(options)
        )

    response = await bot.wait_for("message", check=check, timeout=60)
    choice_index = int(response.content) - 1
    return options[choice_index]

bot.run(TOKEN)
