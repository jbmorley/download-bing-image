import objc

from CoreFoundation import CFUUIDCreateFromString
from Foundation import NSBundle


bndl = NSBundle.bundleWithPath_(objc.pathForFramework('/System/Library/Frameworks/ApplicationServices.framework/'
                                                      'Versions/A/Frameworks/HIServices.framework/'
                                                      'Versions/A/HIServices'))
objc.loadBundleFunctions(bndl, globals(), [
    (u'DesktopPictureCopyDisplayForSpace', b'^{__CFDictionary=}Ii^{__CFString=}'),
    (u'DesktopPictureSetDisplayForSpace', b'vI^{__CFDictionary=}ii^{__CFString=}'),
])
bndl = NSBundle.bundleWithPath_(objc.pathForFramework('/System/Library/Frameworks/CoreGraphics.framework/Versions/A/'
                                                      'CoreGraphics'))
objc.loadBundleFunctions(bndl, globals(), [
    (u'_CGSDefaultConnection', b'i'),
    (u'CGSCopyManagedDisplaySpaces', b'^{__CFArray=}i', '', {'retval': {'already_retained': True}}),
    (u'CGMainDisplayID', b'I'),
    (u'CGSGetDisplayForUUID', b'I^{__CFUUID=}'),
])


class OSXSpace(object):
    def __init__(self, uuid, display_uuid, managed_space_id, id64, type, wsid):
        self.uuid = uuid
        self.display_uuid = display_uuid
        self.managed_space_id = managed_space_id
        self.id64 = id64
        self.type = type
        self.wsid = wsid

    def __repr__(self):
        return "<OSXSpace uuid:'%s' managedSpaceID:%d>" % (self.uuid, self.managed_space_id)

    def __str__(self):
        return "<OSXSpace uuid:'%s' displayUUID:'%s' managedSpaceID:%d id64:%d, type:%d, wsid:%d>" % (
            self.uuid, self.display_uuid, self.managed_space_id, self.id64, self.type, self.wsid
        )


def set_wallpaper(wallpaper_path):
    spaces_per_display_info = CGSCopyManagedDisplaySpaces(_CGSDefaultConnection())
    all_spaces = []

    for display_space_info in spaces_per_display_info:
        display_uuid = display_space_info['Display Identifier']
        for space_info in display_space_info['Spaces']:
            space = OSXSpace(space_info['uuid'],
                             display_uuid,
                             space_info['ManagedSpaceID'],
                             space_info.get('id64', 0),
                             space_info.get('type', 0),
                             space_info.get('wsid', 0))
            all_spaces.append(space)

    for space in all_spaces:
        display_uuid = CFUUIDCreateFromString(None, space.display_uuid)
        display_id = CGSGetDisplayForUUID(display_uuid)
        DesktopPictureSetDisplayForSpace(display_id, {'ImageFilePath': wallpaper_path}, 0, 0, space.uuid)
