This project was made to convert pictures or video into ASCII art.

The AsciiArtTransformer class uses its transform method to convert
and save a video or image into a black and white
format completely made of ASCII characters.

The usage of the AsciiArtTransformer.transform method is as follows

"""
    transforms image or video into ascii art and saves the new
    representation

    example call:
        asciiArtTransformerInstance.transform('./test.mp4',
                                              './test_out.mp4',
                                              file_type='video',
                                              fine=True)

    Parameters:
        media_dir: string, file path to the media file to be transformed
        save_dir: string, save directory where ascii version should be
                    placed
        file_type: one of 'image' or 'video', what type of media is
                   being transformed
        fine: boolean, if False, media is scaled at a 1:1 ratio, ie, the
              output will have the same width and height as the original
              if True, the media will be scaled at a 1:4 ratio, ie, the
              output will have 4x the width and height of the input, and
              will be more detailed
    Returns:
        None

    Throws:
        ValueError
"""
