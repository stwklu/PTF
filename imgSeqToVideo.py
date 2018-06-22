import cv2
import sys
import os, shutil

from Misc import processArguments, sortKey, resizeAR

params = {
    'src_path': '.',
    'save_path': 'example.mkv',
    'img_ext': 'jpg',
    'show_img': 1,
    'del_src': 0,
    'start_id': 0,
    'n_frames': 0,
    'width': 0,
    'height': 0,
    'fps': 30,
    'codec': 'H264',
}

processArguments(sys.argv[1:], params)
src_path = params['src_path']
save_path = params['save_path']
img_ext = params['img_ext']
show_img = params['show_img']
del_src = params['del_src']
start_id = params['start_id']
n_frames = params['n_frames']
width = params['width']
height = params['height']
fps = params['fps']
codec = params['codec']

print('Reading source images from: {}'.format(src_path))

src_file_list = [k for k in os.listdir(src_path) if k.endswith('.{:s}'.format(img_ext))]
total_frames = len(src_file_list)
if total_frames <= 0:
    raise SystemError('No input frames found')
print('total_frames: {}'.format(total_frames))
src_file_list.sort(key=sortKey)

save_dir = os.path.dirname(save_path)
if save_dir and not os.path.isdir(save_dir):
    os.makedirs(save_dir)

if height <= 0 or width <= 0:
    temp_img = cv2.imread(os.path.join(src_path, src_file_list[0]))
    height, width, _ = temp_img.shape

fourcc = cv2.VideoWriter_fourcc(*codec)
video_out = cv2.VideoWriter(save_path, fourcc, fps, (width, height))

if video_out is None:
    raise IOError('Output video file could not be opened: {}'.format(save_path))

print('Saving output video of size {}x{} to {}'.format(width, height, save_path))

frame_id = start_id
pause_after_frame = 0
while True:
    filename = src_file_list[frame_id]
    file_path = os.path.join(src_path, filename)
    if not os.path.exists(file_path):
        raise SystemError('Image file {} does not exist'.format(file_path))

    image = cv2.imread(file_path)

    image = resizeAR(image, width, height)

    if show_img:
        cv2.imshow('frame', image)
        k = cv2.waitKey(1 - pause_after_frame) & 0xFF
        if k == ord('q') or k == 27:
            break
        elif k == 32:
            pause_after_frame = 1 - pause_after_frame

    video_out.write(image)

    frame_id += 1
    sys.stdout.write('\rDone {:d} frames '.format(frame_id - start_id))
    sys.stdout.flush()

    if n_frames > 0 and (frame_id - start_id) >= n_frames:
        break

    if frame_id >= total_frames:
        break

sys.stdout.write('\n')
sys.stdout.flush()

video_out.release()

if show_img:
    cv2.destroyAllWindows()
if del_src:
    print('Removing source folder {}'.format(src_path))
    shutil.rmtree(src_path)