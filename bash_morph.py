#!/usr/bin/env python3

import os
import sys
import glob
import subprocess
from datetime import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips

def main(args=None):

    if len(args) == 0:
        print("No input arguments found. Exiting...")
        sys.exit()

    # Take in directory of image frames.
    print(args)
    input_file_dir = args[0]
    print("Reading in [", input_file_dir, "/] directory...")
    # GTH: Safeguard against invalid directory paths or invalid image frames.

    # Instantiate cache_run.bash script.

    # Safeguard against missing cache_run.bash
    # Check if cache_run.bash script already exists.
    # If true, delete it.
    output_bash_file_name = 'cache_run.bash'
    if os.path.exists(output_bash_file_name):
        os.remove(output_bash_file_name)
    f = open(output_bash_file_name, "w")
    
    input_file_list = sorted(glob.glob(input_file_dir + "/*.png"))
    command_1 = "python3 morph.py -s "
    command_2 = " -t "
    # GTH: Safeguard against non-png image files.
    # Iterate through all image frames
    previous_image_filename = input_file_list[0]
    for index in range(1, len(input_file_list)):
        # Generate lines and write to cache_run.bash script.
        # print("start file = ", previous_image_filename)
        current_image_filename = input_file_list[index]
        # print("dest file = ", current_image_filename)
        print("Command printed - [ " +  command_1 + previous_image_filename + command_2 + current_image_filename + " ]")
        f.write(command_1 + previous_image_filename + command_2 + current_image_filename + '\n')

        previous_image_filename = current_image_filename
    
    
    # Complete writing to cache_run.bash script.
    f.close()

    # Run cache_run.bash script.
    # GTH: Wait for user designation based on consideration to run later.
    rc = subprocess.run(['bash', 'cache_run.bash'])
    print("Completed running [ cache_run.bash ]")

    # Append all resulting videos and save file to clear directory path with line printed for user.
    output_file_dir = "output/"
    output_video_list = sorted(glob.glob(output_file_dir + "/*.mp4"))

    video_array = []
    for index in range(0, len(output_video_list)):
        video_filename = output_video_list[index]
        print(video_filename)
        temp_clip = VideoFileClip(video_filename)
        video_array.append(temp_clip)

    final_clip= concatenate_videoclips(video_array)
    now = datetime.now()
    timestamp = now.strftime("%b-%d-%Y-%H-%M-%S")
    output_video_filename = timestamp + '.mp4'
    print("Writing final video file to [", output_video_filename, "]")
    final_clip.write_videofile("output.mp4")

    # Clear out all videos out of output/ directory
    del_video_files = glob.glob(output_file_dir + "/*.mp4")
    for file in del_video_files:
        os.remove(file)



if __name__=="__main__":
    main(sys.argv[1:])