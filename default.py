#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc,xbmcgui,xbmcaddon
import resources.lib.ColorPicker as colorpicker

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id').decode("utf-8")
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")

def get_params():
    '''extract the params from the called script path'''
    params = {}
    for arg in sys.argv:
        arg = arg.decode("utf-8")
        if arg == 'script.skin.helper.colorpicker' or arg == 'default.py':
            continue
        elif "=" in arg:
            paramname = arg.split('=')[0]
            paramvalue = arg.replace(paramname+"=","")
            params[paramname] = paramvalue
            params[paramname.upper()] = paramvalue
    return params

def wait_for_skinshortcuts_window():
    '''wait untill skinshortcuts is active window (because of any animations that may have been applied)'''
    for i in range(40):
        if not xbmc.getCondVisibility("Window.IsActive(DialogSelect.xml) | Window.IsActive(script-skin_helper_service-ColorPicker.xml) | Window.IsActive(DialogKeyboard.xml)"):
            break
        else: xbmc.sleep(100)


#MAIN ENTRY POINT
if __name__ == "__main__":
    params = get_params()
    if params:
        colorPicker = colorpicker.ColorPicker("script-skin_helper_service-ColorPicker.xml", ADDON_PATH, "Default", "1080i")
        colorPicker.skinstring = params.get("SKINSTRING","")
        colorPicker.win_property = params.get("WINPROPERTY","")
        colorPicker.active_palette = params.get("PALETTE","")
        colorPicker.header_label = params.get("HEADER","")
        propname = params.get("SHORTCUTPROPERTY","")
        colorPicker.shortcut_property = propname
        colorPicker.doModal()

        #special action when we want to set our chosen color into a skinshortcuts property
        if propname and not isinstance(colorPicker.result, int):
            wait_for_skinshortcuts_window()
            xbmc.sleep(400)
            current_window = xbmcgui.Window( xbmcgui.getCurrentWindowDialogId() )
            current_window.setProperty("customProperty", propname)
            current_window.setProperty("customValue",colorPicker.result[0])
            xbmc.executebuiltin("SendClick(404)")
            xbmc.sleep(250)
            current_window.setProperty("customProperty", "%s.name" %propname)
            current_window.setProperty("customValue",colorPicker.result[1])
            xbmc.executebuiltin("SendClick(404)")
        del colorPicker
