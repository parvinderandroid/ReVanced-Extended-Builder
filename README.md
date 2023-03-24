# **ReVanced Extended Builder**

# Table of Contents

- [About](#about)
- [Requirements](#requirements)
- [How to use?](#how-to-use)
- [Credits](#credits)

# About

This is a simple python script for building YouTube ReVanced Extended and YouTube Music ReVanced Extended.

On the press of a single button, this script will:

* Download the latest version of `revanced-cli.jar`, `revanced-patches.jar`, `revanced-integrations.apk`, `youtube.apk`, `youtube-music.apk`
* Build YouTube ReVanced Extended
* Build YouTube Music ReVanced Extended

I made this for my personal use, but thought I'd share here in case anyone is interested.

The main feature of this builder is that you don't need to download any patches or APKs manually. It automatically downloads and builds using the latest available version of all dependencies

# Requirements

* Vanced MicroG installed on phone
  * https://github.com/inotia00/VancedMicroG/releases/latest/download/microg.apk
  * Only needed if you want to sign in using your Google account
* Zulu JDK 17
  * https://www.azul.com/downloads/
  * I recommend downloading the zip and extracting it somewhere. Just remember where you extracted it and add that path to the `ZULU_JAVA_EXE` variable in the program
* Python installed on system
  * I have only tested with Python 3.11.2
* Below pip libraries installed on system:
    ```
	pip install requests beautifulsoup4
	```

# How to use?

* Double click `Build.py`
* Type 0
* Press Enter

# Credits

* [ReVanced Team](https://github.com/revanced/)
* [inotia00](https://github.com/inotia00/)
* [APKMirror](https://www.apkmirror.com/)
