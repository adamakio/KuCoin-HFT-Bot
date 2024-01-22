import os


def create_executable(lang="esp"):
    os.system(
        f"pyinstaller --clean -y -F -n atprofit --distpath=exec_{lang}/dist --workpath=exec_{lang}/build --specpath=exec_{lang} executable.py"
    )


create_executable()
