# Copyright 2004-2020 Tom Rothamel <pytom@bishoujo.us>
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

init python:
    # This can be one of None, "available", "not-available", or "error".
    #
    # It must be None for a release.
    UPDATE_SIMULATE = os.environ.get("RENPY_UPDATE_SIMULATE", None)

    PUBLIC_KEY = "renpy_public.pem"

    CHANNELS_URL = "https://www.renpy.org/channels.json"

    version_tuple = renpy.version(tuple=True)

    def check_dlc(name):
        """
        Returns true if the named dlc package is present.
        """

        return name in updater.get_installed_packages()

    def add_dlc(name, restart=False):
        """
        Adds the DLC package, if it doesn't already exist.

        Returns True if the DLC is installed, False otherwise.
        """

        dlc_url = "http://update.renpy.org/{}/updates.json".format(".".join(str(i) for i in version_tuple[:-1]))

        state = updater.get_installed_state()

        if state is not None:
            base_name = state.get("sdk", {}).get('base_name', '')

            if base_name.startswith("renpy-nightly-"):
                dlc_url = "http://nightly.renpy.org/{}/updates.json".format(base_name[6:])

        return renpy.invoke_in_new_context(updater.update, dlc_url, add=[name], public_key=PUBLIC_KEY, simulate=UPDATE_SIMULATE, restart=restart)

    # Strings so they can be translated.

    _("Release")
    _("{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games.")

    _("Prerelease")
    _("A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games.")

    _("Experimental")
    _("Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer.")

    _("Nightly")
    _("The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all.")

    # Newly added functions. Signed, MPDS
    # Update: GET OUT OF MY HEAD

    filter_keywords=set()
    
    def display_keywords():
        return "Search phrases:\n"+"\n".join(filter_keywords)

    def add_keyword(temp='monika'):
        if temp!="":
            filter_keywords.add(temp)
        return

    def remove_keyword(temp="monika"):
        if temp!="":
            if temp in filter_keywords:
                filter_keywords.remove(temp)
        return




screen update_channel(channels, criteria):

    frame:
        style_group "l"
        style "l_root"

        window:

            has viewport:
                scrollbars "vertical"
                mousewheel True

            has vbox

            label _("DD Mod Club Mod List")

            add HALF_SPACER

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    has vbox

                    text _("Select the mod you will like to download. Afterwards return to the main menu and install it like normal with DDML.")
                    if len(criteria)!=0:
                        python:
                            filter_keywords.clear()
                            filter_keywords|=set(criteria.split(','))
                            dsply_kwds=display_keywords()
                            good_marker=True
                        text _(dsply_kwds) style "l_small_text"

                        add SPACER
                        python:
                            chosen_channels=list()
                            for c in channels:
                                good_marker=True
                                search_kwds=c["modSearch"]
                                for eee in filter_keywords:
                                    if eee not in search_kwds:
                                        good_marker=False
                                        break
                                if good_marker:
                                    chosen_channels.append(c)
                            channels=chosen_channels
                        text "Found {} mods that are tagged with all search phrases:".format(len(chosen_channels)) style "l_small_text"
                    for c in channels:
                        add SPACER

                        textbutton c["modName"].replace("[", "").replace("]", "") action OpenURL(c["modUploadURL"])

                        add HALF_SPACER

                        #$$ date = _strftime(__("%B %d, %Y"), time.localtime(c["timestamp"]))

                        #text "[date] • [c[pretty_version]] [current!t]" style "l_small_text"

                        add HALF_SPACER

                        text c["modShortDescription"] style "l_small_text"

    textbutton _("Return") action Jump("front_page") style "l_left_button"


screen updater:

    frame:
        style "l_root"

        frame:
            style_group "l_info"

            has vbox

            if u.state == u.ERROR:
                text _("An error has occured:")
            elif u.state == u.CHECKING:
                text _("Checking for updates.")
            elif u.state == u.UPDATE_NOT_AVAILABLE:
                text _("Ren'Py is up to date.")
            elif u.state == u.UPDATE_AVAILABLE:
                text _("[u.version] is now available. Do you want to install it?")
            elif u.state == u.PREPARING:
                text _("Preparing to download the update.")
            elif u.state == u.DOWNLOADING:
                text _("Downloading the update.")
            elif u.state == u.UNPACKING:
                text _("Unpacking the update.")
            elif u.state == u.FINISHING:
                text _("Finishing up.")
            elif u.state == u.DONE:
                text _("The update has been installed. Ren'Py will restart.")
            elif u.state == u.DONE_NO_RESTART:
                text _("The update has been installed.")
            elif u.state == u.CANCELLED:
                text _("The update was cancelled.")

            if u.message is not None:
                add SPACER
                text "[u.message!q]"

            if u.progress is not None:
                add SPACER

                frame:
                    style "l_progress_frame"

                    bar:
                        range 1.0
                        value u.progress
                        style "l_progress_bar"

        label _("Ren'Py Update") style "l_info_label"

    if u.can_cancel:
        textbutton _("Cancel") action u.cancel style "l_left_button"

    if u.can_proceed:
        textbutton _("Proceed") action u.proceed style "l_right_button"

label update:

    python hide:
        criteria = ""
        criteria = interface.input(
            _("Mod search phrases"),
            _("""Please insert search phrases separated by commas.
Spaces placed before and after search phrases will be included in them.
Place ' on start of phrase to search by prefix.
Place ' on end of phrase to search by suffix.
Place ' on both to search full phrase only.

Leave blank for the full list."""),
            allow=interface.TRANSLATE_LETTERS+"' ,",
            cancel=Jump("front_page"),
            default="",
        )
        interface.processing(_("Fetching the mod list..."))

        import urllib2
        import json
        import ssl

        # Disabled due to obsoleteness but it may be useful in code someday
        
        # with interface.error_handling(_("Downloading a updated mod list...")):
        #     url = "https://www.dokidokimodclub.com/api/mod/"
        #     headers = {'Authorization': 'Api-Key qR2Tjbe7.mEQ1w5atlsgSbnlsxilOe4GyRxwoy7As'}
        #     context = ssl._create_unverified_context()
        #     req = urllib2.Request(url=url, headers=headers)
        #     response = urllib2.urlopen(req, context=context)
        #     the_page = response.read()

        with interface.error_handling(_("Decoding the mod list...")):
            ddmc_data = config.basedir + '/ddmc.json'
            with open(ddmc_data, 'r') as f:
                channels = json.load(f)
        
        renpy.call_screen("update_channel", channels, criteria)

    jump front_page

