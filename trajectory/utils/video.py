import os
import numpy as np
import skvideo.io

def _make_dir(filename):
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.makedirs(folder)

def save_video(filename, video_frames, fps=60, video_format='mp4'):
    assert fps == int(fps), fps
    _make_dir(filename)

    skvideo.io.vwrite(
        filename,
        video_frames,
        inputdict={
            '-r': str(int(fps)),
        },
        outputdict={
            '-f': video_format,
            '-pix_fmt': 'yuv420p', # '-pix_fmt=yuv420p' needed for osx https://github.com/scikit-video/scikit-video/issues/74
        }
    )

def save_video_tensorboard(summary_writer, video_frames, fps=10, tag="plan", step=0):
    black = np.zeros_like(video_frames)[:3]
    black[::2] += 1
    video_frames_finish = np.concatenate([video_frames, black], axis = 0)
    formatted_video_frames = np.transpose(np.expand_dims(video_frames_finish, 0), (0,1,4,2,3))
    summary_writer.add_video(tag, formatted_video_frames, global_step=step, fps=1)

def save_videos(filename, summary_writer, *video_frames, to_tensorboard_only=False, **kwargs):
    ## video_frame : [ N x H x W x C ]
    video_frames = np.concatenate(video_frames, axis=2)
    if not to_tensorboard_only:
        save_video(filename, video_frames, **kwargs)
    save_video_tensorboard(summary_writer, video_frames, **kwargs)
