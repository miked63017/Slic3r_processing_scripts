#!/usr/bin/python
"""
Created by miked63017@gmail.com
Intended to reverse layers in Slic3r so that gcode can be generated for milling
Will have to take your model and make a negative of it
Create a solid block, probably the same size as the raw material you will be milling on, and subtract your model from inside that block
Ensure verbose gcode is on, I think its needed but not 100% sure
Probably need rectilinear or line for infill pattern
Play with infill percentage for optimum speed
Don't forget to adjust speeds and feeds, cutting/milling will most likely need to be done a lot slower that the printhead usually moves
Set this as post processing script

I used python since it seems to be the language of choice and the most likely to be setup in windows, I would have preferred to do this in perl or even ruby
Personally I use linux, so I could have used any of the above languages, but wanted to make something cross platform and Python seemed like an easy target
"""

import sys

f = open(sys.argv[1], "rb")
s = f.readlines()
f.close()

f = open(sys.argv[1], "wb")

LASTBLOCK = False
FIRSTLAYER = False
LAYERCHANGE = False
FIRSTBLOCK = True
code_list = [ ]
code_list_element_list = [ ]
layer_list = [ ]
pre_layer_list = [ "; Starting FIRSTBLOCK" ]
post_layer_list = [ ]
for line in s:
	if "M104 S0 ; turn off temperature" in line:
		LASTBLOCK = True
		LAYERCHANGE = False
		layer_list.append(code_list_element_list)
		post_layer_list.append("; END REVERSED LAYERS")
                post_layer_list.append("; Starting LASTBLOCK")
		post_layer_list.append(line)
	elif "move to next layer (0)" in line:
		FIRSTLAYER = True
		FIRSTBLOCK = False
		pre_layer_list.append("; END FIRSTBLOCK")
		pre_layer_list.append("; BEGIN REVERSED LAYERS")
		code_list_element_list = [ ]
		code_list_element_list.append(line)
	elif "move to next layer" in line:
		LAYERCHANGE = True
		FIRSTLAYER = False
		layer_list.append(code_list_element_list)
		code_list_element_list = [ ]
		code_list_element_list.append(line)
	elif FIRSTBLOCK:
		pre_layer_list.append(line)
	elif LAYERCHANGE:
		code_list_element_list.append(line)
	elif FIRSTLAYER:
		code_list_element_list.append(line)
	elif LASTBLOCK:
		post_layer_list.append(line)
layer_list.reverse()
for item in pre_layer_list:
  print>>f, item

for layers in layer_list:
  for item in layers:
    print>>f, item

for item in post_layer_list:
  print>>f, item

print>>f, " ; Done processing"
f.close()
