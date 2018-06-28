import os
import sys, shutil
from random import shuffle

from Misc import processArguments, sortKey

params = {
    'file_ext': 'jpg',
    'out_file': 'list.txt',
    'folder_name': '.',
    'shuffle_files': 1,
    'del_empty': 0,
}
processArguments(sys.argv[1:], params)
file_ext = params['file_ext']
out_file = params['out_file']
folder_name = params['folder_name']
shuffle_files = params['shuffle_files']
del_empty = params['del_empty']

folder_name = os.path.abspath(folder_name)

print('Looking for files with extension {:s} in sub folders of {:s}'.format(file_ext, folder_name))

subfolders = [name for name in os.listdir(folder_name) if os.path.isdir(os.path.join(folder_name, name))]
try:
    subfolders.sort(key=sortKey)
except:
    subfolders.sort()

total_files = 0
counts_file = open('file_counts.txt', 'w')
files = []
empty_folders = []
for subfolder in subfolders:
    subfolders_path = os.path.join(folder_name, subfolder)
    src_files = [f for f in os.listdir(subfolders_path) if os.path.isfile(os.path.join(subfolders_path, f))]
    if file_ext:
        src_files = [f for f in src_files if f.endswith(file_ext)]
    src_files.sort(key=sortKey)

    n_files = len(src_files)

    if del_empty and n_files == 0:
        empty_folders.append(subfolders_path)
    total_files += n_files
    files += [os.path.join(subfolders_path, f) for f in src_files]
    text = '{}:\t{}\t{}'.format(subfolder, n_files, total_files)
    print(text)
    counts_file.write(text + '\n')

print('total_files: {}'.format(total_files))
counts_file.close()

if shuffle_files:
    shuffle(files)

out_fid = open(out_file, 'w')
for f in files:
    out_fid.write(f + '\n')
out_fid.close()
if del_empty and empty_folders:
    print('Removing empty folders:')
    for folder in empty_folders:
        shutil.rmtree(folder)
        print(folder)

