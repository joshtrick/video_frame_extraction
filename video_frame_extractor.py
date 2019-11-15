import cv2
import os
import argparse
import sys
import time


# Argument Parser
parser = argparse.ArgumentParser(description='Video frames extraction')

parser.add_argument('-i',
        action = 'store',
        dest = 'input',
        help = 'Input video',
        required = True)

parser.add_argument('-o',
        action = 'store',
        dest = 'output',
        help = 'Output path (default: same as input video source)')

parser.add_argument('-e',
        type = int,
        action = 'store',
        dest = 'ex_time',
        default = 1,
        help = 'Extract one frame per EX_TIME frames. (default: full extraction)')


args = parser.parse_args()



# Check if video exist
if not os.path.exists(args.input):
    print('Video does not exist.')
    exit()

input_src = os.path.split(args.input)


# Output directory
output_folder = input_src[1].replace(".", "_")
if args.output == None:
    output_dir = os.path.join(input_src[0], ('frames_' + output_folder))
else:
    output_dir = os.path.join(args.output, ('frames_' + output_folder))

if not os.path.exists(output_dir):
    os.mkdir(output_dir)


# Extraction rate
ex_numerator = 1
ex_denominator = args.ex_time


ex_r = ex_numerator/ex_denominator


# Start extraction
print('Processing      : %s'   % (args.input))

cap = cv2.VideoCapture(args.input)
frame_nu = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)


# Print summary
print('Number of Frames: %d'   % (frame_nu))
print('Frame Rate      : %.1f' % (fps))
print('Frame Size      : %dx%d'% (frame_w, frame_h))
print('Extraction Rate : 1/%d' % (ex_denominator))
print('Output Path     : %s'   % (output_dir))


# Start extraction
frame_len = 0
if frame_nu > 0:
    i = int(frame_nu)
    while(i >= 1):
        frame_len += 1
        i /= 10

i = 0
j = 0

tic = time.time()
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    if j < ex_numerator:
        cv2.imwrite(os.path.join(output_dir, 'frame_'+str(i).zfill(frame_len)+'.jpg'), frame)
    j += 1
    i += 1
    if j == ex_denominator:
        j = 0
# Progress bar
    prg_count_0 = round(50*(i+1)/frame_nu)
    prg_count_1 = round(100*(i+1)/frame_nu)
    sys.stdout.write('\r')
    sys.stdout.write("Progress        : [%-50s] %d%%" % ('='*prg_count_0, prg_count_1))
    sys.stdout.flush()

toc = time.time()
proc_time = toc - tic

print()
print('Finished.')
print('Time spent      : %.2fs'% (proc_time))
cap.release()
cv2.destroyAllWindows()
