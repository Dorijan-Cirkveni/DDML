﻿# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file contains some of the options that can be changed to customize
# your Ren'Py game. It only contains the most common options... there
# is quite a bit more customization you can do.
#
# Lines beginning with two '#' marks are comments, and you shouldn't
# uncomment them. Lines beginning with a single '#' mark are
# commented-out code, and you may want to uncomment them when
# appropriate.

init -1 python hide:

    # Should we enable the use of developer tools? This should be
    # set to False before the game is released, so the user can't
    # cheat using developer tools.

    config.developer = True

    # These control the width and height of the screen.

    config.screen_width = 800
    config.screen_height = 600

    # This controls the title of the window, when Ren'Py is
    # running in a window.

    config.window_title = u"DDML 5.0"

    # These control the name and version of the game, that are reported
    # with tracebacks and other debugging logs.
    config.name = "DDML 5.0"
    config.version = "5.1.0R"

    #####################
    # Themes

    # We then want to call a theme function. themes.roundrect is
    # a theme that features the use of rounded rectangles. It's
    # the only theme we currently support.
    #
    # The theme function takes a number of parameters that can
    # customize the color scheme.

    theme.roundrect(
        # Theme: Roundrect
        # Color scheme: Basic Blue

        # The color of an idle widget face.
        widget = "#003c78",

        # The color of a focused widget face.
        widget_hover = "#0050a0",

        # The color of the text in a widget.
        widget_text = "#c8ffff",

        # The color of the text in a selected widget. (For
        # example, the current value of a preference.)
        widget_selected = "#ffffc8",

        # The color of a disabled widget face.
        disabled = "#404040",

        # The color of disabled widget text.
        disabled_text = "#c8c8c8",

        # The color of informational labels.
        label = "#ffffff",

        # The color of a frame containing widgets.
        frame = "#6496c8",

        # The background of the main menu. This can be a color
        # beginning with '#', or an image filename. The latter
        # should take up the full height and width of the screen.
        mm_root = "#dcebff",

        # The background of the game menu. This can be a color
        # beginning with '#', or an image filename. The latter
        # should take up the full height and width of the screen.
        gm_root = "#dcebff",

        # If this is True, the in-game window is rounded. If False,
        # the in-game window is square.
        rounded_window = False,

        # And we're done with the theme. The theme will customize
        # various styles, so if we want to change them, we should
        # do so below.
        )

    #####################
    # Help.

    # This lets you configure the help option on the Ren'Py menus.
    # It may be:
    # - A label in the script, in which case that label is called to
    #   show help to the user.
    # - A file name relative to the base directory, which is opened in a
    #   web browser.
    # - None, to disable help.
    config.help = "README.html"

    #####################
    # Transitions.

    # Used when entering the game menu from the game.
    config.enter_transition = None

    # Used when exiting the game menu to the game.
    config.exit_transition = None

    # Used between screens of the game menu.
    config.intra_transition = None

    # Used when entering the game menu from the main menu.
    config.main_game_transition = None

    # Used when returning to the main menu from the game.
    config.game_main_transition = None

    # Used when entering the main menu from the splashscreen.
    config.end_splash_transition = None

    # Used when entering the main menu after the game has ended.
    config.end_game_transition = None

    # Used when a game is loaded.
    config.after_load_transition = None

    # Used when the window is shown.
    config.window_show_transition = None

    # Used when the window is hidden.
    config.window_hide_transition = None


    #####################
    # This is the name of the directory where the game's data is
    # stored. (It needs to be set early, before any other init code
    # is run, so the persistent information can be found by the init code.)
python early:
    config.save_directory = "DDML5"

init -1 python hide:
    #####################
    # Default values of Preferences.

    # Note: These options are only evaluated the first time a
    # game is run. To have them run a second time, delete
    # game/saves/persistent

    # Should we start in fullscreen mode?

    config.default_fullscreen = False

    # The default text speed in characters per second. 0 is infinite.

    config.default_text_cps = 0

    #####################
    # More customizations can go here.

    config.sound = False
    config.quit_action = Quit(confirm=False)
    config.gl_resize = False
    config.window_icon = "images/logo.png"
    config.windows_icon = "images/logo32.png"
    config.has_autosave = False
    config.log_enable = False
    config.mouse_hide_time = None

    _game_menu_screen = None

    config.underlay = [
        renpy.Keymap(
            screenshot = _screenshot,
            reload_game = _reload_game,
            developer = _developer,
            quit = renpy.quit_event,
            iconify = renpy.iconify,
            help = _help,
            choose_renderer = renpy.curried_call_in_new_context("_choose_renderer"),
            console = _console.enter,
            profile_once = _profile_once,
            memory_profile = _memory_profile,
            self_voicing = Preference("self voicing", "toggle"),
            clipboard_voicing = Preference("clipboard voicing", "toggle"),
            debug_voicing = Preference("debug voicing", "toggle"),
            progress_screen = _progress_screen,
            ),
        ]

    config.rollback_enabled = False

# This section controls how to build Ren'Py. (Building the launcher is how
# we build Ren'Py distributions.)
init python:

    # We're building Ren'Py tonight.
    build.renpy = True

    # The version number that's supplied to the updater.
    build.version = "Ren'Py {}".format(config.version)

    # The name that's used for directories and archive files. For example, if
    # this is 'mygame-1.0', the windows distribution will be in the
    # directory 'mygame-1.0-win', in the 'mygame-1.0-win.zip' file.

    if 'RENPY_BUILD_VERSION' in os.environ:
        build.directory_name = "renpy-" + os.environ['RENPY_BUILD_VERSION']
    else:
        build.directory_name = "renpy-" + config.version.rsplit('.', 1)[0]

    # The name that's uses for executables - the program that users will run
    # to start the game. For example, if this is 'mygame', then on Windows,
    # users can click 'mygame.exe' to start the game.
    build.executable_name = "renpy"

    # If True, Ren'Py will include update information into packages. This
    # allows the updater to run.
    build.include_update = True

    # Allow empty directories, so we can distribute the images directory.
    build.exclude_empty_directories = False


    # Mac signing options.
    import os
    build.mac_identity = os.environ.get("RENPY_MAC_IDENTITY", None)
    build.mac_codesign_command = [ "/home/tom/ab/renpy-deps/mac/mac_sign_client.sh", "{identity}", "{app}" ]
    build.mac_create_dmg_command = [ "/home/tom/ab/renpy-deps/mac/mac_dmg_client.sh", "{identity}", "{volname}", "{sourcedir}", "{dmg}" ]
    build.mac_codesign_dmg_command = [ "/bin/true" ]


    # Clear out various file patterns.
    build.renpy_patterns = [ ]
    build.early_base_patterns = [ ]
    build.base_patterns = [ ]
    build.late_base_patterns = [ ]

    # We don't need to clear out the executable patterns, since they're
    # correct for Ren'Py.

    # Now, add the Ren'Py distribution in using classify_renpy.

    build.classify_renpy("**~", None)
    build.classify_renpy("**/#*", None)
    build.classify_renpy("**/thumbs.db", None)
    build.classify_renpy("**/.*", None)

    build.classify_renpy("rapt/**", "rapt")

    build.classify_renpy("renios/prototype/base/", None)
    build.classify_renpy("renios/prototype/prototype.xcodeproj/*.xcworkspace/", None)
    build.classify_renpy("renios/prototype/prototype.xcodeproj/xcuserdata/", None)
    build.classify_renpy("renios/prototype/**", "renios")
    build.classify_renpy("renios/buildlib/**", "renios")
    build.classify_renpy("renios/ios.py", "renios")
    build.classify_renpy("renios/version.txt", "renios")
    build.classify_renpy("renios/", "renios")

    build.classify_renpy("**.old", None)
    build.classify_renpy("**.new", None)
    build.classify_renpy("**.bak", None)
    build.classify_renpy("**.pyc", None)

    build.classify_renpy("**/log.txt", None)
    build.classify_renpy("**/traceback.txt", None)
    build.classify_renpy("**/errors.txt", None)
    build.classify_renpy("**/saves/", None)
    build.classify_renpy("**/tmp/", None)
    build.classify_renpy("**/.Editra", None)

    # main source.

    def source_and_binary(pattern, source="source", binary="binary"):
        """
        Classifies source and binary files beginning with `pattern`.
        .pyo, .rpyc, .rpycm, and .rpyb go into binary, everything
        else goes into source.
        """

        build.classify_renpy(pattern + "/**.pyo", binary)
        build.classify_renpy(pattern + "/**.rpyc", binary)
        build.classify_renpy(pattern + "/**.rpymc", binary)
        build.classify_renpy(pattern + "/**/cache/*", binary)

        build.classify_renpy(pattern + "/**", source)

    build.classify_renpy("renpy.py", "binary")
    source_and_binary("renpy")

    # games.
    build.classify_renpy("launcher/game/theme/", None)
    build.classify_renpy("gui/game/gui/", None)

    source_and_binary("launcher")
    source_and_binary("templates", binary=None)
    source_and_binary("gui", binary=None)

    source_and_binary("the_question")
    source_and_binary("tutorial")

    # docs.
    build.classify_renpy("doc/", "source")
    build.classify_renpy("doc/.doctrees/", None)
    build.classify_renpy("doc/_sources/", None)
    build.classify_renpy("doc/**", "source")
    build.classify_renpy("LICENSE.txt", "source")

    # module.
    build.classify_renpy("module/", "source")
    build.classify_renpy("module/*.c", "source")
    build.classify_renpy("module/gen/", "source")
    build.classify_renpy("module/gen/*.c", "source")
    build.classify_renpy("module/*.h", "source")
    build.classify_renpy("module/*.py*", "source")
    build.classify_renpy("module/include/", "source")
    build.classify_renpy("module/include/*.pxd", "source")
    build.classify_renpy("module/include/*.pxi", "source")
    build.classify_renpy("module/pysdlsound/", "source")
    build.classify_renpy("module/pysdlsound/*.py", "source")
    build.classify_renpy("module/pysdlsound/*.pyx", "source")

    # all-platforms binary.
    build.classify_renpy("lib/**/_renpysteam*", None)
    build.classify_renpy("lib/**/*steam_api*", None)
    build.classify_renpy("lib/*/renpy", None)
    build.classify_renpy("lib/*/renpy.exe", None)
    build.classify_renpy("lib/**", "binary")
    build.classify_renpy("renpy.sh", "binary")
    # renpy.app is now built from scratch from distribute.rpy.

    # jedit rules.
    build.classify_renpy("jedit/**", "jedit")

    # editra rules.
    build.classify_renpy("editra/", "editra-all")
    build.classify_renpy("editra/Editra.edit.py", "editra-all")
    build.classify_renpy("editra/Editra/**", "editra-linux editra-windows")
    build.classify_renpy("editra/Editra-mac.app/**", "editra-mac")
    build.classify_renpy("editra/lib/**", "editra-windows")
    build.classify_renpy("editra/editra.exe", "editra-windows")


    # Executable rules.
    build.executable("editra/Editra/Editra")

    # Packages.
    build.packages = [ ]

    build.package("sdk", "zip tar.bz2 dmg", "source binary")
    build.package("source", "tar.bz2", "source source_only", update=False)

    build.package("jedit", "zip", "jedit", dlc=True)
    build.package("editra-linux", "tar.bz2", "editra-all editra-linux", dlc=True)
    build.package("editra-mac", "zip", "editra-all editra-mac", dlc=True)
    build.package("editra-windows", "zip", "editra-all editra-windows", dlc=True)
    build.package("rapt", "zip", "rapt", dlc=True)
    build.package("renios", "zip", "renios", dlc=True)


# Enable the special launcher translation mode.
define config.translate_launcher = True
