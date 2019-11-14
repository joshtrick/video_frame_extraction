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
        help = 'input video',
        required = True)

parser.add_argument('-o',
        action = 'store',
        dest = 'output',
        help = 'output path (default: same as input video source)')

parser.add_argument('--half',
        action = 'store_true',
        help = 'set extraction rate as 0.5 (default: 1.0)')

parser.add_argument('--quarter',
        action = 'store_true',
        help = 'set extraction rate as 0.25 (default: 1.0)')

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

if args.half and not args.quarter:
    ex_denominator = 2
elif args.quarter and not args.half:
    ex_denominator = 4
elif not (args.quarter and args.half):
    ex_denominator = 1
else:
    print('Please specify ONLY one extraction rate: default for 1.0, --half for 0.5, and --quarter for 0.25.')
    exit()

ex_r = ex_numerator/ex_denominator


# Start extraction
print('Processing      : %s'   % (args.input))

cap = cv2.VideoCapture(args.input)
frame_nu = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)


# Print summary
print('Number of Frames: %d'   % (frame_nu))
print('Frame Rate      : %.1f' % (fps))
print('Extraction Rate : %.1f' % (ex_r))
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
    prg_count = round(50*(i+1)/frame_nu)
    sys.stdout.write('\r')
    sys.stdout.write("Progress        : [%-50s] %d%%" % ('='*prg_count, 2*prg_count))
    sys.stdout.flush()

toc = time.time()
proc_time = toc - tic

print()
print('Finished.')
print('Time spent      : %.2fs'% (proc_time))
cap.release()
cv2.destroyAllWindows()
