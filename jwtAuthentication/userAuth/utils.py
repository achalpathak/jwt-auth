
def user_profile_photo_path(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / profile_photo / <user.id>.<ext>/ 
    return 'profile_photo/{0}.{1}'.format(instance.user.id, '.' + filename.split('.')[-1])