from os import path, system, _exit, remove
from shutil import rmtree
from bs4 import BeautifulSoup
from requests import get
from undetected_chromedriver import Chrome, ChromeOptions

ZULU_JAVA_EXE = r"C:\Program Files\Zulu\zulu-17\bin\java.exe"


def delete_old_items():
    items = [
        "options.toml",
        "output",
        "revanced-cache",
        "revanced-cli.jar",
        "revanced-integrations.apk",
        "revanced-patches.jar",
        "youtube-music.apk",
        "youtube.apk",
    ]
    for item in items:
        if path.exists(item):
            (remove if path.isfile(item) else rmtree)(item)
            print("Deleted", item)


def download_dependencies():
    filenames_urls = {
        "revanced-cli.jar": "https://api.github.com/repos/revanced/revanced-cli/releases/latest",
        "revanced-integrations.apk": "https://api.github.com/repos/inotia00/revanced-integrations/releases/latest",
        "revanced-patches.jar": "https://api.github.com/repos/inotia00/revanced-patches/releases/latest",
    }
    for filename, url in filenames_urls.items():
        data = get(url).json()
        assets = data["assets"]
        extension = filename.split(".")[-1]
        for asset in assets:
            if asset["name"].endswith(extension):
                download_url = asset["browser_download_url"]
                response = get(download_url)
                open(filename, "wb").write(response.content)
                print(f'Downloaded {filename} ({data["tag_name"]})')


def get_url(url, search_term):
    config = ChromeOptions()
    config.add_argument("--headless=new")
    driver = Chrome(options=config)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and search_term in href:
            return "https://www.apkmirror.com" + href


def apk_download(url, filename, version):
    download_link = get_url(get_url(url, "key="), "key=")
    r = get(download_link, headers={"User-Agent": "Mozilla/5.0"})
    with open(filename, "wb") as f:
        f.write(r.content)
    print(f"Downloaded {filename} (v{version.replace('-', '.')})")


def download_youtube():
    data = get("https://github.com/inotia00/revanced-patches/releases/latest/download/patches.json").json()
    patch = next(p for p in data if p["compatiblePackages"][0]["name"] == "com.google.android.youtube")
    version = patch["compatiblePackages"][0]["versions"][-1].replace(".", "-")
    url = f"https://www.apkmirror.com/apk/google-inc/youtube/youtube-{version}-release/youtube-{version}-2-android-apk-download/"
    apk_download(url, "youtube.apk", version)


def download_youtube_music():
    homepage = "https://www.apkmirror.com/apk/google-inc/youtube-music/"
    version = get_url(homepage, "/apk/google-inc/youtube-music/youtube-music-")[69:-9]
    url = f"{homepage}youtube-music-{version}-release/youtube-music-{version}-android-apk-download/"
    apk_download(url, "youtube-music.apk", version)


def build_youtube():
    system(rf'"{ZULU_JAVA_EXE}" -jar revanced-cli.jar -a youtube.apk -b revanced-patches.jar -m revanced-integrations.apk -e custom-branding-name --keystore=parvinder.keystore -o output\YouTube-ReVanced-Extended.apk')


def build_youtube_music():
    system(rf'"{ZULU_JAVA_EXE}" -jar revanced-cli.jar -a youtube-music.apk -b revanced-patches.jar -m revanced-integrations.apk --keystore=parvinder.keystore -o output\YouTube-Music-ReVanced-Extended.apk')


options = [
    "ALL",
    "Delete old items",
    "Download dependencies",
    "Download YouTube",
    "Download YouTube Music",
    "Build YouTube",
    "Build YouTube Music",
    "Exit",
]
functions = [
    delete_old_items,
    download_dependencies,
    download_youtube,
    download_youtube_music,
    build_youtube,
    build_youtube_music,
]
while True:
    for i, option in enumerate(options):
        print(f"{i}. {option}")
    choice = int(input(""))
    if choice == 0:
        for function in functions:
            function()
        _exit(1)
    elif 0 < choice < len(options) - 1:
        functions[choice - 1]()
    else:
        _exit(1)
