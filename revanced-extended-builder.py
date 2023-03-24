from concurrent.futures import ThreadPoolExecutor
from json import load
from os import path, system, remove
from re import search
from shutil import rmtree
from sys import exit
from urllib.request import Request, urlopen

ZULU_JAVA_EXE = r"C:\Program Files\Zulu\zulu-17\bin\java.exe"


def delete_old_items():
    items = [
        "options.toml",
        "output",
        "revanced-cache",
        "revanced-cache-yt",
        "revanced-cache-ytm",
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
    def download_file(filename, url):
        data = load(urlopen(url))
        assets = data["assets"]
        extension = filename.split(".")[-1]
        for asset in assets:
            if asset["name"].endswith(extension):
                download_url = asset["browser_download_url"]
                response = urlopen(download_url)
                open(filename, "wb").write(response.read())
                print(f'Downloaded {filename} ({data["tag_name"]})')

    filenames_urls = {
        "revanced-cli.jar": "https://api.github.com/repos/revanced/revanced-cli/releases/latest",
        "revanced-integrations.apk": "https://api.github.com/repos/inotia00/revanced-integrations/releases/latest",
        "revanced-patches.jar": "https://api.github.com/repos/inotia00/revanced-patches/releases/latest",
    }
    with ThreadPoolExecutor() as executor:
        for filename, url in filenames_urls.items():
            executor.submit(download_file, filename, url)


def get_url(url, search_term):
    response = urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}))
    html = response.read().decode("utf-8")
    pattern = f'href="([^"]*{search_term}[^"]*)"'
    match = search(pattern, html)
    if match:
        return "https://www.apkmirror.com" + match.group(1)


def download_apk(url, filename, version):
    download_link = get_url(get_url(url, "key="), "key=")
    response = urlopen(Request(download_link, headers={"User-Agent": "Mozilla/5.0"}))
    with open(filename, "wb") as apk_file:
        apk_file.write(response.read())
    print(f"Downloaded {filename} (v{version.replace('-', '.')})")


def download_youtube():
    data = load(urlopen("https://github.com/inotia00/revanced-patches/releases/latest/download/patches.json"))
    patch = next(p for p in data if p["compatiblePackages"][0]["name"] == "com.google.android.youtube")
    version = patch["compatiblePackages"][0]["versions"][-1].replace(".", "-")
    url = f"https://www.apkmirror.com/apk/google-inc/youtube/youtube-{version}-release/youtube-{version}-2-android-apk-download/"
    download_apk(url, "youtube.apk", version)


def download_youtube_music():
    homepage = "https://www.apkmirror.com/apk/google-inc/youtube-music/"
    version = get_url(homepage, "/apk/google-inc/youtube-music/youtube-music-")[69:-9]
    url = f"{homepage}youtube-music-{version}-release/youtube-music-{version}-android-apk-download/"
    download_apk(url, "youtube-music.apk", version)


def build_youtube():
    system(rf'"{ZULU_JAVA_EXE}" -jar revanced-cli.jar -a youtube.apk -b revanced-patches.jar -m revanced-integrations.apk -e custom-branding-name --keystore=revanced-extended-builder.keystore -t=revanced-cache-yt -o output\YouTube-ReVanced-Extended.apk')


def build_youtube_music():
    system(rf'"{ZULU_JAVA_EXE}" -jar revanced-cli.jar -a youtube-music.apk -b revanced-patches.jar -m revanced-integrations.apk --keystore=revanced-extended-builder.keystore -t=revanced-cache-ytm -o output\YouTube-Music-ReVanced-Extended.apk')


def main():
    while True:
        print("0. ALL")
        print("1. Delete old items")
        print("2. Download dependencies")
        print("3. Download YouTube")
        print("4. Download YouTube Music")
        print("5. Build YouTube")
        print("6. Build YouTube Music")
        print("7. Exit")
        choice = int(input(""))
        if choice == 0:
            delete_old_items()
            with ThreadPoolExecutor() as executor:
                executor.submit(download_dependencies)
                executor.submit(download_youtube)
                executor.submit(download_youtube_music)
            with ThreadPoolExecutor() as executor:
                executor.submit(build_youtube)
                executor.submit(build_youtube_music)
            exit()
        elif choice == 1:
            delete_old_items()
        elif choice == 2:
            download_dependencies()
        elif choice == 3:
            download_youtube()
        elif choice == 4:
            download_youtube_music()
        elif choice == 5:
            build_youtube()
        elif choice == 6:
            build_youtube_music()
        else:
            exit()


if __name__ == "__main__":
    main()
