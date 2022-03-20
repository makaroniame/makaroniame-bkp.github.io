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

MD_REGEX=r"\[(.*?)\]\((.*?)\)"

latex_qrs = {}



for post in posts:
    with open(f"_posts/{post}.md","r") as f:
        # text = f.read()
        text = "".join(f.readlines()[6:])
#        print(text)

        urls = re.findall(MD_REGEX, text)
        latex_qrs[post] = ""

        for i, url in enumerate(urls):
            wm_url = f"{WM_URL_PREFIX}{urllib.parse.quote_plus(url[1])}"
            wm_url_escaped = wm_url.replace("%","\\%")
            latex_qr = f"{i+1}:\n\\qrcode{{{wm_url_escaped}}}\n\\par\n"
            latex_qrs[post] += latex_qr

            # Use LaTex Hybrid mode to add superscripts
            # reference$^1$
            text = re.sub(MD_REGEX, f"{url[0]}$^{i+1}$", text, count=1, flags=re.MULTILINE) 

#            print(text)
    with open(f"_book/rsrc/{post}.md","w") as f:
        f.write(text)

    with open(f"_book//rsrc/{post}.tex","w") as f:
        f.write("\\begin{multicols}{2}\n")
        f.write(latex_qrs[post])
        f.write("\\end{multicols}\n")

    print(f"\\include{{rsrc/{post}.tex}}")

