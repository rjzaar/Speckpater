from distutils.core import setup
import py2exe
import glob
import sys
sys.argv.append("py2exe")
sys.argv.append("--bundle")
sys.argv.append("2")
setup(
    #console=["main.py"],
    #zipfile=None,
    windows = [
        {
            "script": "main.py",
            "icon_resources": [(1, "bibledave.ico")]
        }
    ],
    data_files=[(".", glob.glob("./*.py") +
                 glob.glob("./*.ttf") +
		 glob.glob("./*.txt")),
                ("enemies", glob.glob("enemies/*.py")),
                ("images",
                 glob.glob("images/*.png") +
                 glob.glob("images/*.gif")),
                ("levels", glob.glob("levels/*.py") +
                 glob.glob("levels/*.lev") +
                 glob.glob("levels/*.tga") +
                 glob.glob("levels/*.png") +
                 glob.glob("levels/*.py")),
                ("levels/tilesets",
                 glob.glob("levels/tilesets/*.py") +
                 glob.glob("levels/tilesets/*.png")),
                ("locales",
                 glob.glob("locales/*.pot") +
                 glob.glob("locales/*.bat")),
                ("locales/en/LC_MESSAGES",
                 glob.glob("locales/en/LC_MESSAGES/*.mo") +
                 glob.glob("locales/en/LC_MESSAGES/*.po")),
                ("locales/fi/LC_MESSAGES",
                 glob.glob("locales/fi/LC_MESSAGES/*.mo") +
                 glob.glob("locales/fi/LC_MESSAGES/*.po")),
                ("pgu", glob.glob("pgu/*.py")),
                ("pgu/gui",
                 glob.glob("pgu/gui/*.py")),
                ("pgu/gui/default",
                 glob.glob("pgu/gui/default/*.png") +
                 glob.glob("pgu/gui/default/*.xcf") +
                 glob.glob("pgu/gui/default/*.tga") +
                 glob.glob("pgu/gui/default/*.txt")),
                ("sounds",
                 glob.glob("sounds/*.ogg") +
                 glob.glob("sounds/*.wav"))])
