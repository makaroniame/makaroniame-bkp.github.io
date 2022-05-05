import re
import urllib
import urllib.parse

posts = [
    "2020-04-30-kompina_sto_la",
    "2020-05-29-venezueliani_aiora",
    "2020-07-02-koinoviopagida",
    "2020-08-07-magnitofonaki",
    "2021-05-26-eyxh_sto_kansas",
    "2022-03-19-monopetro",
]

WM_URL_PREFIX="http://web.archive.org/web/"

URL_REGEX=r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[^\)\.,]"

MD_URL_REGEX=r"\[(.*?)\]\((.*?)\)"

latex_qrs = {}

def wayback_machine(url):
    wm_url = f"{WM_URL_PREFIX}{url[1]}"
    # urllib.parse.quote_plus()
    # wm_url = wm_url.replace("%","\\%")
    return wm_url


for post in posts:
    with open(f"_posts/{post}.md","r") as f:
        # Get the text skipping the Jekyll lines
        text = "".join(f.readlines()[6:])

        urls = re.findall(MD_URL_REGEX, text)
        latex_qrs[post] = ""

        for i, url in enumerate(urls):
            # make url tuple mutable
            url = list(url)
            # Youtube does not get through with
            # Wayback Machine URLs
            if (
                not url[1].startswith("https://www.youtube.com") and
                not url[1].startswith("https://youtube.com") and
                not url[1].startswith("https://youtu.be")
                ):

                url[1] = wayback_machine(url)
            # Place the QRcode
            # The <3 is Python Formatting:
            # https://docs.python.org/3/library/string.html#format-specification-mini-language
            latex_qr = f"{i+1:<3}:\n\\qrcode{{{url[1]}}}\n\\par\n"
            latex_qrs[post] += latex_qr

            # Use LaTex Hybrid mode to add superscripts
            # reference$^{1}$
            # see: https://latex-tutorial.com/subscript-superscript-latex/
            text = re.sub(MD_URL_REGEX, f"{url[0]}$^{{{i+1}}}$", text, count=1, flags=re.MULTILINE)

#            print(text)
    with open(f"_book/rsrc/{post}.md","w") as f:
        f.write(text)

    with open(f"_book//rsrc/{post}.tex","w") as f:
        f.write("\\begin{multicols}{2}\n")
        f.write(latex_qrs[post])
        f.write("\\end{multicols}\n")

    print(f"\\include{{rsrc/{post}.tex}}")

## Create Back Cover text
BACKCOVER_POST_LINES = [39,40]
BACKCOVER_POST = posts[0]

BACKCOVER_TEXT = ""
with open(f"_posts/{BACKCOVER_POST}.md","r") as f:
    line_list = f.readlines()[BACKCOVER_POST_LINES[0]: BACKCOVER_POST_LINES[1]]
    BACKCOVER_TEXT = "".join(line_list)

with open(f"_book/rsrc/backcover-text.md","w") as f:
    f.write(BACKCOVER_TEXT)

print("\\markdownInput{rsrc/backcover-text.md}")
