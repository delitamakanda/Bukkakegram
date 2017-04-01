import cloudinary
def consts(request):
    return dict(
        ICON_EFFECTS = dict(
            format = "png",
            type = "facebook",
            transformation=[
                dict(height=100, width=100, crop="thumb", gravity="face", effect="sepia", radius=0),
                dict(angle=0),
            ]
        ),
        THUMBNAIL = {
            "class": "thumbnail inline", "format": "jpg", "crop": "fill", "height" : 150, "width" : 150,
        },
        CLOUDINARY_CLOUD_NAME = cloudinary.config().cloud_name
    )
