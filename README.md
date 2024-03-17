# sdxl-trainer-tools
A collection of small scripts to prepare images for SDXL finetuning

sd-resize-1m.py resizes images to 1M pixels so that the dimensions are divisible by 64. There is no padding, so it just brutely resizes the images for now.
sd-crop-1k.py automatically cuts larger images up to pieces of 1024x1024px. The idea is to include details of larger images in the training set along with the complete versions made with the first resizing script.
