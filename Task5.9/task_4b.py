# #!/usr/bin/env python
# # coding: utf-8

# # In[5]:


# '''
# *****************************************************************************************
# *
# *				===============================================
# *		   		Nirikshak Bot (NB) Theme (eYRC 2020-21)
# *				===============================================
# *
# *  This script is to implement Task 4B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
# *  
# *  This software is made available on an "AS IS WHERE IS BASIS".
# *  Licensee/end user indemnifies and will keep e-Yantra indemnified from
# *  any and all claim(s) that emanate from the use of the Software or 
# *  breach of the terms of this agreement.
# *  
# *  e-Yantra - An MHRD (now MOE) project under National Mission on Education using ICT (NMEICT)
# *
# *****************************************************************************************
# '''

# # Team ID:		  NB_2182
# # Author List:	  	 Yatharth Bhargava, Pranav Mittal
# # Filename:		 task_4b.py
# # Functions:		 calculate_path_from_maze_image, send_data_to_draw_path, 
# # 					convert_path_to_pixels, traverse_path,getBallCoordinates
# #				   [ Comma separated list of functions in this file ]
# # Global variables: client_id, setpoint, start_coord, end_coord
# # 					[ List of global variables defined in this file ]


# ####################### IMPORT MODULES #######################
# ## You are not allowed to make any changes in this section. ##
# ## You have to implement this task with the three available ##
# ## modules for this task (numpy,opencv,os,sys,traceback)	##
# ##############################################################
# import numpy as np
# import cv2
# import os, sys
# import traceback
# import time
# ##############################################################

# # Importing the sim module for Remote API connection with CoppeliaSim
# try:
# 	import sim
	
# except Exception:
# 	print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
# 	print('\n[WARNING] Make sure to have following files in the directory:')
# 	print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
# 	sys.exit()

# #Import 'task_1b.py' file as module
# try:
# 	import task_1b

# except ImportError:
# 	print('\n[ERROR] task_1b.py file is not present in the current directory.')
# 	print('Your current directory is: ', os.getcwd())
# 	print('Make sure task_1b.py is present in this current directory.\n')
# 	sys.exit()
	
# except Exception as e:
# 	print('Your task_1b.py throwed an Exception. Kindly debug your code!\n')
# 	traceback.print_exc(file=sys.stdout)
# 	sys.exit()


# # Import 'task_1a_part1.py' file as module
# try:
# 	import task_1a_part1

# except ImportError:
# 	print('\n[ERROR] task_1a_part1.py file is not present in the current directory.')
# 	print('Your current directory is: ', os.getcwd())
# 	print('Make sure task_1a_part1.py is present in this current directory.\n')
# 	sys.exit()
	
# except Exception as e:
# 	print('Your task_1a_part1.py throwed an Exception. Kindly debug your code!\n')
# 	traceback.print_exc(file=sys.stdout)
# 	sys.exit()


# # Import 'task_2a.py' file as module
# try:
# 	import task_2a

# except ImportError:
# 	print('\n[ERROR] task_2a.py file is not present in the current directory.')
# 	print('Your current directory is: ', os.getcwd())
# 	print('Make sure task_2a.py is present in this current directory.\n')
# 	sys.exit()
	
# except Exception as e:
# 	print('Your task_2a.py throwed an Exception. Kindly debug your code!\n')
# 	traceback.print_exc(file=sys.stdout)
# 	sys.exit()

# # Import 'task_2b.py' file as module
# try:
# 	import task_2b

# except ImportError:
# 	print('\n[ERROR] task_2b.py file is not present in the current directory.')
# 	print('Your current directory is: ', os.getcwd())
# 	print('Make sure task_2b.py is present in this current directory.\n')
# 	sys.exit()
	
# except Exception as e:
# 	print('Your task_2b.py throwed an Exception. Kindly debug your code!\n')
# 	traceback.print_exc(file=sys.stdout)
# 	sys.exit()

# # Import 'task_3.py' file as module
# try:
# 	import task_3

# except ImportError:
# 	print('\n[ERROR] task_3.py file is not present in the current directory.')
# 	print('Your current directory is: ', os.getcwd())
# 	print('Make sure task_3.py is present in this current directory.\n')
# 	sys.exit()
	
# except Exception as e:
# 	print('Your task_3.py throwed an Exception. Kindly debug your code!\n')
# 	traceback.print_exc(file=sys.stdout)
# 	sys.exit()


# # Import 'task_4a.py' file as module
# try:
# 	import task_4a

# except ImportError:
# 	print('\n[ERROR] task_4a.py file is not present in the current directory.')
# 	print('Your current directory is: ', os.getcwd())
# 	print('Make sure task_4a.py is present in this current directory.\n')
# 	sys.exit()
	
# except Exception as e:
# 	print('Your task_4a.py throwed an Exception. Kindly debug your code!\n')
# 	traceback.print_exc(file=sys.stdout)
# 	sys.exit()


# # Global variable "client_id" for storing ID of starting the CoppeliaSim Remote connection
# # NOTE: DO NOT change the value of this "client_id" variable here
# client_id = -1

# # Global list "setpoint" for storing target position of ball on the platform/top plate
# # The 0th element stores the x pixel and 1st element stores the y pixel
# # NOTE: DO NOT change the value of this "setpoint" list
# setpoint = [0, 0]

# # Global tuple to store the start and end cell coordinates of the maze
# # The 0th element stores the row and 1st element stores the column
# # NOTE: DO NOT change the value of these tuples
# start_coord = (0,4)
# end_coord = (9,5)

# # You can add your global variables here
# ##############################################################

# ##############################################################


# # In[6]:


# ################# ADD UTILITY FUNCTIONS HERE #################
# ## You can define any utility functions for your code.	  ##
# ## Please add proper comments to ensure that your code is   ##
# ## readable and easy to understand.						 ##
# ##############################################################
# def getBallData(client_id,vision_sensor_handle,flag):
	
# 	vision_sensor_image, image_resolution, return_code = task_2a.get_vision_sensor_image(client_id,vision_sensor_handle)
# 	# print(client_id,vision_sensor_handle)
# 	if ((return_code == sim.simx_return_ok) and (len(image_resolution) == 2) and (len(vision_sensor_image) > 0)):
# 		# print('\nImage captured from Vision Sensor in CoppeliaSim successfully!')
# 		pass
# 	else:
# 		#start loop again
# 		return None


# 	# Get the transformed vision sensor image captured in correct format
# 	try:
# 		# print(vision_sensor_image[0:20])
# 		transformed_image = task_2a.transform_vision_sensor_image(vision_sensor_image, image_resolution)
# 		# print(vision_sensor_handle,client_id)
# 		# cv2.imshow("cropped", transformed_image)
# 		# cv2.waitKey(0)
# 		# cv2.destroyAllWindows()
# 		# print(transformed_image[0][0:20])
# 		if (type(transformed_image) is np.ndarray):
# 			# Get the resultant warped transformed vision sensor image after applying Perspective Transform
# 			try:
# 				warped_img = task_1b.applyPerspectiveTransform(transformed_image)
# 				if(flag):
# 					warped_img = warped_img[80:1200, 80:1200]
# 					warped_img = cv2.resize(warped_img, (1280, 1280))
# 					# print(warped_img[0][0:20])
# 					# cv2.imshow("cropped", warped_img)
# 					# cv2.waitKey(0)
# 					#cv2.imshow("warped",warped_img)
# 					#cv2.waitKey(0)
# 					# cv2.destroyAllWindows()
# 				if (type(warped_img) is np.ndarray):
# 					# Get the 'shapes' dictionary by passing the 'warped_img' to scan_image function
# 					try:
# 						shapes = task_1a_part1.scan_image(warped_img)
# 						if (type(shapes) is dict and shapes!={}):
# 							# print('\nShapes detected by Vision Sensor are: ')
# 							# print(shapes)
# 							# Storing the detected x and y centroid in center_x and center_y variable repectively
# 							# return shapes
# 							if( type(shapes['Circle'][0]) is list ):
# 								return None
# 							else:
# 								return shapes
# 						elif(type(shapes) is not dict):
# 							#print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.')
# 							#print('Stop the CoppeliaSim simulation manually.')
# 							return None

# 					except Exception:
# 						print('\n[ERROR] Your scan_image function in task_1a_part1.py throwed an Exception. Kindly debug your code!')
# 						print('Stop the CoppeliaSim simulation manually.\n')
# 						traceback.print_exc(file=sys.stdout)
# 						print()
# 						sys.exit()

# 				else:
# 					print('\n[ERROR] applyPerspectiveTransform function is not configured correctly, check the code.')
# 					print('Stop the CoppeliaSim simulation manually.')
# 					print()
# 					sys.exit()

# 			except Exception:
# 				print(".",end="")
# 				print('\n[ERROR] Your applyPerspectiveTransform function in task_1b.py throwed an Exception. Kindly debug your code!')
# 				print('Stop the CoppeliaSim simulation manually.\n')
# 				traceback.print_exc(file=sys.stdout)
# 				print()
# 				sys.exit()

# 		else:
# 			print('\n[ERROR] transform_vision_sensor_image function in task_2a.py is not configured correctly, check the code.')
# 			print('Stop the CoppeliaSim simulation manually.')
# 			print()
# 			sys.exit()

# 	except Exception:
# 		print('\n[ERROR] Your transform_vision_sensor_image function in task_2a.py throwed an Exception. Kindly debug your code!')
# 		print('Stop the CoppeliaSim simulation manually.\n')
# 		traceback.print_exc(file=sys.stdout)
# 		print()
# 		sys.exit()
# 	return None

# ##############################################################


# # In[7]:


# # NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# def calculate_path_from_maze_image(img_file_path):
# 	"""
# 	Purpose:
# 	---
# 	This function reads the image from `img_file_path` input, applies
# 	Perspective Transform and computes the encoded maze array by calling
# 	applyPerspectiveTransform and detectMaze functions from task_1b.py.

# 	It then calls the find_path function from task_4a.py to compute the path
# 	between start and end coordinate values declared globally.

# 	Input Arguments:
# 	---
# 	`img_file_path` :  [ str ]
# 		File path of maze image.
	
# 	Returns:
# 	---
# 	`maze_array` 	:   [ nested list of lists ]
# 		encoded maze in the form of a 2D array
	
# 	`path` :  [ list of tuples ]
# 		path between start and end coordinates

# 	Example call:
# 	---
# 	maze_array, path = calculate_path_from_maze_image(img_file_path)
	
# 	"""

# 	# read the 'maze00.jpg' image file
# 	input_img = cv2.imread(img_file_path)

# 	if type(input_img) is np.ndarray:

# 		try:
# 			# get the resultant warped maze image after applying Perspective Transform
# 			warped_img = task_1b.applyPerspectiveTransform(input_img)

# 			if type(warped_img) is np.ndarray:

# 				try:
# 					# get the encoded maze in the form of a 2D array
# 					maze_array = task_1b.detectMaze(warped_img)

# 					if (type(maze_array) is list) and (len(maze_array) == 10):
# 						print('\nEncoded Maze Array = %s' % (maze_array))
# 						print('\n============================================')

# 						try:
# 							path = task_4a.find_path(maze_array, start_coord, end_coord)

# 							if (type(path) is list):

# 								print('\nPath calculated between %s and %s is = %s' % (start_coord, end_coord, path))
# 								print('\n============================================')
							
# 							else:
# 								print('It seems that path is of type ', type(path),'.\n Make sure that is a list.')
						
# 						except Exception:
# 							print('\n[ERROR] Your find_path function in \'task_4a.py\' throwed an Exception, kindly debug your code!')
# 							traceback.print_exc(file=sys.stdout)
# 							print()
# 							sys.exit()

# 					else:
# 						print('\n[ERROR] maze_array returned by detectMaze function in \'task_1b.py\' is not returning maze array in expected format!, check the code.')
# 						print()
# 						sys.exit()
				
# 				except Exception:
# 					print('\n[ERROR] Your detectMaze function in \'task_1b.py\' throwed an Exception, kindly debug your code!')
# 					traceback.print_exc(file=sys.stdout)
# 					print()
# 					sys.exit()
			
# 			else:
# 				print('\n[ERROR] applyPerspectiveTransform function in \'task_1b.py\' is not returning the warped maze image in expected format!, check the code.')
# 				print()
# 				sys.exit()

# 		except Exception:
# 			print('\n[ERROR] Your applyPerspectiveTransform function in \'task_1b.py\' throwed an Exception, kindly debug your code!')
# 			traceback.print_exc(file=sys.stdout)
# 			print()
# 			sys.exit()
	
# 	else:
# 		print('\n[ERROR] .jpg was not read correctly, something went wrong!')
# 		print()
# 		sys.exit()

# 	return maze_array, path


# # In[8]:


# def send_data_to_draw_path(rec_client_id, path,table_number):
# 	"""
# 	Purpose:
# 	---
# 	This function should:
# 	1. Convert and 
# 	2. Send a flattened path to LUA's drawPath() function.
	
# 	Teams are free to choose logic for this conversion.

# 	We have provided an example code for the above.

# 	Suppose [(1, 5), (2, 5)] is the path given as input to this function. 
# 	To visualize this path, it needs to be converted to CoppeliaSim coordinates.

# 	The following points should be considered:

# 	1. The entire maze is 1m x 1m in CoppeliaSim coordinates. Dividing this by 10 rows and 
# 	10 columns, we get the size of each cell to be 10cm x 10cm.

# 	2. The x axis of CoppeliaSim corresponds to the row and y axis corresponds to the column.

# 	3. The x and y origin of CoppeliaSim coincides with the center of 4th and 5th row as well
# 	as column. When row and column are both 0, the corresponding CoppeliaSim coordinates are
# 	(-0.5,-0.5). Since we need the path from the center of the cell, an offset of 45cm is required.
	
# 						0.45m								0.5m
# 		 |←-----------------------------→|←----------------------------------→|
# 		 |								 |									  |
# 	 0	 |	 1		 2		 3		 4	 |	 5		 6 		 7		 8		 9|
# 	 _	 |	 _	 	 _	 	 _	 	 _	 |	 _	 	 _	 	 _	 	 _	 	 _|_ _ _ _ _ _ _ 
# 	|_|  |  |_|		|_| 	|_| 	|_|  |	|_| 	|_| 	|_| 	|_| 	|_|		0		↑
# 		 |	 							 |													|
# 	 _	 	 _	 	 _	 	 _	 	 _	 |	 _	 	 _	 	 _	 	 _	 	 _				|
# 	|_| 	|_|		|_| 	|_| 	|_|  |	|_| 	|_| 	|_| 	|_| 	|_|		1		|
# 										 |													|
# 	 _	 	 _	 	 _	 	 _	 	 _	 |	 _	 	 _	 	 _	 	 _	 	 _				|
# 	|_| 	|_|		|_| 	|_| 	|_|  |	|_| 	|_| 	|_| 	|_| 	|_|		2		|0.5m
# 										 |													|
# 	 _	 	 _	 	 _	 	 _	 	 _	 |	 _	 	 _	 	 _	 	 _	 	 _				|
# 	|_| 	|_|		|_| 	|_| 	|_|  |	|_| 	|_| 	|_| 	|_| 	|_|		3		|
# 										 |													|
# 	 _	 	 _	 	 _	 	 _	 	 _	 |	 _	 	 _	 	 _	 	 _	 	 _				|
# 	|_| 	|_|		|_| 	|_| 	|_|  |	|_| 	|_| 	|_| 	|_| 	|_|		4		|
# 									   (0,0) _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _↓
# 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _
# 	|_| 	|_|		|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_|		5

# 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _
# 	|_| 	|_|		|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_|		6

# 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _
# 	|_| 	|_|		|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_|		7

# 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _
# 	|_| 	|_|		|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_|		8

# 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _
# 	|_| 	|_|		|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_|		9
# 	|		|
# 	| 0.1m	|
# 	|←-----→|


# 	Using the above information we map the cell coordinates to the CoppeliaSim coordinates.
# 	The formula comes out to be:

# 	CoppeliaSim_coordinate=(((10*row_or_column_number) - 45)/100) m

# 	Hence the CoppeliaSim coordinates for the above example will be:

# 	coppelia_sim_coord_path = [-0.35, 0.05, -0.25, 0.05]

# 	Here we are sending a simple list with alternate x and y coordinates.

# 	NOTE: You are ALLOWED to change this function according to your logic.
# 		  Visualization of this path in the scene is MANDATORY.
	
# 	Input Arguments:
# 	---
# 	`rec_client_id` 	:  [ integer ]
# 		the client_id generated from start connection remote API, should be stored in a global variable

# 	`path` 	:  [ list ]
# 		Path returned from task_4a.find_path() function.
	
# 	Returns:
# 	---
	
# 	path_drawing_object_handle
# 	Example call:
# 	---
# 	send_data_to_draw_path(rec_client_id,path)
	
# 	"""
# 	#global client_id
# 	client_id = rec_client_id

# 	##############	IF REQUIRED, CHANGE THE CODE FROM HERE	##############
# 	coppelia_sim_coord_path = []
	
# 	for coord in path:
# 		for element in coord:
# 			coppelia_sim_coord_path.append(((10*element) - 45)/100)
	
# 	print('\n============================================')
# 	print('\nPath sent to drawPath function of Lua script is \n')
# 	print(coppelia_sim_coord_path)
	
# 	# _,_ = sim.simxGetPingTime(client_id)
# 	inputBuffer = bytearray()
# 	return_code,retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id,'top_plate_respondable_t'+str(table_number)+'_1', sim.sim_scripttype_customizationscript, 'drawPath', [],coppelia_sim_coord_path,[str(table_number)],inputBuffer,sim.simx_opmode_blocking)
# 	#print(retInts,retFloats, retStrings, retBuffer)
# 	# _,_ = sim.simxGetPingTime(client_id)
# 	if(len(retInts)==0):
# 		return -1
# 	return retInts[0]
# 	##################################################


# # In[ ]:


# def convert_path_to_pixels(path):
# 	"""
# 	Purpose:
# 	---
# 	This function should convert the obtained path (list of tuples) to pixels.
# 	Teams are free to choose the number of points and logic for this conversion.

# 	Input Arguments:
# 	---
# 	`path` 	:  [ list ]
# 		Path returned from task_4a.find_path() function.

# 	Returns:
# 	---
# 	`pixel_path` : [ type can be decided by teams ]

# 	Example call:
# 	---
# 	pixel_path = convert_path_to_pixels(path)

# 	"""
# 	##############	ADD YOUR CODE HERE	##############
# 	#the size of image is 1280x1280
# 	#the coordinates for path are
# 	#(0,0),(0,1)(0,2)(0,3)(0,4)(0,5)(0,6)(0,7)(0,8)(0,9)
# 	#(1,0),(1,1)(1,2)...................(1,7),(1,8)(1,9)
# 	#..................................................
# 	#(8,0),(8,1)(8,2)...................(8,7),(8,8)(8,9)
# 	#(9,0),(9,1)(9,2)(9,3)(9,4)(9,5)(9,6)(9,7)(9,8)(9,9)
# 	#the pixels in image
# 	#x(right)/y(down)-

# 	#0,1,...................1280
# 	#0,............................
# 	#1 ,............................
# 	#. ,............................
# 	#. ,............................
# 	#1280, .....................

# 	pixel_path=[]
# 	wh=1280/10
	
# 	for i in range(len(path)):
# 		cX=path[i][1]
# 		cY=path[i][0]
# 		pixel_path+=[[wh*cX+wh/2,wh*cY+wh/2]]
		
# 	##################################################	
# 	return pixel_path


# # In[ ]:


# def traverse_path(client_id,prev_pixel_path,vision_sensor_handle,revolute_handle,table_number):

# 	"""
# 	Purpose:
# 	---
# 	This function should make the ball traverse the calculated path.

# 	Teams are free to choose logic for this function.

# 	NOTE: Refer the code of main function in task_3.py.

# 	Input Arguments:
# 	---
# 	`pixel_path` : [ type can be decided by teams ]

# 	Returns:
# 	---
# 	None

# 	Example call:
# 	---
# 	traverse_path(pixel_path)

# 	"""

# 	##############	ADD YOUR CODE HERE	#############
# 	'''
# 	Here we have implemented a logic to optimize the path/pixel_path. The pixel_path  that we have got from
# 	tash_4a has each node at a distance of 1 unit from each other. In the case of straight lines in path we can skip
# 	some of the in between nodes this helps in rdeucing the time becuase ball travels better and wihout sudden 
# 	change in the set point. 

# 	lets suppose that our path is -[[(1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1)]] 
# 	then we can convert this path to [[(1, 4), (1, 1), (3, 1)]] 

# 		|_1,1_| 	|_1,2_| 	|_1,3_| 	|_1,4_|
# 		|_2,1_| 	|_2,2_| 	|_2,3_| 	|_2,4_|
# 		|_3,1_| 	|_3,2_| 	|_3,3_| 	|_3,4_|
# 		|_4,1_| 	|_4,2_| 	|_4,3_| 	|_4,4_|
# 		|_5,1_| 	|_5,2_| 	|_5,3_| 	|_5,4_|
# 	We have done this optimization in the pixel_path that we got as an argument in this function.
# 	for that we have to use the previous pixel coordinates(i-1) and just future coordinates(i+1) and 
# 	if both the pixel coordinates do not match completely this implies that there is a turn at i.
# 	'''
# 	_,_ = sim.simxGetPingTime(client_id)
# 	return_code_signal,start=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_buffer)
# 	if(return_code_signal== 0):
# 		try:
# 			now=float(start)
# 		except Exception:
# 			start=0


# 	if(len(prev_pixel_path)>=1):
# 		pixel_path = [[prev_pixel_path[0][0]-1,prev_pixel_path[0][1]-1]]
# 	for i in range(len(prev_pixel_path)):
# 		pixel_path.append(prev_pixel_path[i])		
# 	# pixel_path.append([1292.8, 704.0])
# 	pixel_path=shortenPath(pixel_path)
# 	# pixel_path=customizePixelPath(pixel_path)
# 	print("Final Path in Table ",table_number,": ",pixel_path)

# 	# loop from start to a point less than end,as dst=src+1

# 	try:
# 		#print( "client_id=", client_id, "pixel_path" , pixel_path, "vision_sensor_handle", vision_sensor_handle, "revolute_handle", revolute_handle )
# 		# setTiltInTable(client_id,revolute_handle,setpoint)
# 		# task_3.setAngles(client_id,revolute_handle,[-30,-30])
# 		# time.sleep(2) 
# 		# task_3.setAngles(client_id,revolute_handle,[30,30])
# 		# task_3.setAngles(client_id,revolute_handle,[0,0])
# 		z=1	
# 		setpoint=[0,0]
# 		ITerm=np.array([0,0],dtype="float64")
# 		lastInput=np.array([0,0],dtype="float64")
# 		lastTime=0
# 		Input=np.array([0,0],dtype="float64")
# 		lastOutput=np.array([0,0],dtype="float64")
# 		summation=np.array([0,0],dtype="float64")
# 		Output=np.array([0,0],dtype="float64")
# 		# this is a kind of flag variable which will help in setting the last coordinates of ball for the first frame of run, 
# 		# which is used in the calculation of derivative term in PID calculation.
# 		prev_x=pixel_path[0][0]
# 		prev_y=pixel_path[0][1]
# 		#print("prev-x=",prev_x)
# 		#print("prev-y=",prev_y)
# 		for i in range(len(pixel_path)-1):
# 			#true loop until ball reached destination
# 			# if( (i+2)<(len(pixel_path))and(pixel_path[i+2][0]==prev_x or pixel_path[i+2][1]==prev_y)):
# 			# 	prev_x=pixel_path[i+1][0]
# 			# 	prev_y=pixel_path[i+1][1]
# 			# 	# print("prev-x=",prev_x)
# 			# 	# print("prev-y=",prev_y)
# 			# 	continue
# 			src=pixel_path[i]
# 			dst=pixel_path[i+1]

# 			# print(dst)
# 			prev_x=pixel_path[i+1][0]
# 			prev_y=pixel_path[i+1][1]
# 			setpoint=[dst[0],dst[1]]
# 			summation=np.array([0,0],dtype='float64')
# 			ITerm=np.array([0,0],dtype='float64')
# 			# print("STARTING JOURNEY TO:",(dst[0]-640)/1280,(dst[1]-640)/1280)
# 			temp=0
# 			print ("Traversing to ",setpoint," in table ",table_number,end="")
# 			if((((dst[0]-src[0])**2+(dst[1]-src[1])**2)<128*128) or (dst[2]==0)):
# 				#normal kp ,ki,kd
# 				print(" in slow mode")
# 				dst[2]=0
# 				kp=np.array([0.050,0.040],dtype='float64')
# 				ki=np.array([0.001,0.001],dtype='float64')#ki=ki*SampleTime
# 				kd=np.array([0.14,0.14],dtype='float64')#kd=kd/SampleTime
# 			else:
# 				#fast kp,ki,kd
# 				print(" in fast mode")
# 				dst[2]=1
# 				kp=np.array([0.030,0.030],dtype='float64')
# 				ki=np.array([0.001,0.001],dtype='float64')#ki=ki*SampleTime
# 				kd=np.array([0.145,0.145],dtype='float64')#kd=kd/SampleTime
				
			
# 			timechange = 0
# 			while(True):			
				
# 				shapes= getBallData(client_id,vision_sensor_handle,True) 
# 				if (shapes==None):
# 					continue
# 				center_x = shapes['Circle'][1]
# 				center_y = shapes['Circle'][2]
# 				# print(dst)
# 				#print("center_x = ",center_x,"center_y",center_y)
# 				if((center_x==None) or (center_y==None)):
# 					continue

# 				if(z==1):
# 					lastInput=task_3.coordinateTransform([center_x,center_y])
# 					z=0
# 				return_code_signal,now=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_buffer)
# 				if(return_code_signal== 0):
# 					try:
# 						now=float(now)
# 					except Exception:
# 						continue
# 					#print("Now=",now)
# 				else:
# 					continue
# 				#now=float(now)
# 				dist=(center_x-dst[0])**2+(center_y-dst[1])**2
# 				if((dst[2]==1) and (dist<1000)):
# 					#fast mode simply pass to next setpoint
# 					break
# 				elif(dst[2]==0):
# 					#might have to slow down or stop here
# 					if(dist<8000):
# 						kd=np.array([0.135,0.135],dtype='float64')
# 					if(dist<2500):
# 						kd=np.array([0.3,0.3],dtype='float64')
# 					if( dist< 1000):
# 						timechange=timechange+(now-temp)
# 						# print (now)
# 					temp=now
# 					# timechange=0
# 					#  Ball has to stay at each optimized set point under the threshold value for about 0.7 sec 
# 					# this help in stability of the ball while traversal. 
# 					if(timechange>=1):
# 						break

# 				#print("Calling PID")
# 				try:
# 					# print("setpoint = ",setpoint,end=" ")
# 					ITerm,lastInput,lastTime,Input,lastOutput,summation,Output= task_3.control_logic(setpoint,client_id,center_x,center_y,ITerm,lastInput,lastTime,Input,lastOutput,summation,Output,kp,ki,kd)
# 					#print( "ITerm=", ITerm, "lastInput", lastInput, "lastTime", lastTime, "Input", Input, "lastOutput", lastOutput, "summation", summation, "Output", Output)
# 					# print("revolute_handle = ",revolute_handle)
# 					task_3.setAngles(client_id,revolute_handle,Output) 
# 					# time.sleep(0.05)
# 				except:
# 					print('\n[ERROR] Your control_logic function throwed an Exception. Kindly debug your code!')
# 					print('Stop the CoppeliaSim simulation manually.\n')
# 					#traceback.print_exc(file=sys.stdout)
# 					#print()
# 					#sys.exit()
# 				lastInput = task_3.coordinateTransform([center_x,center_y])
			
# 	except:
# 		print('\n[ERROR] Your control_logic function throwed an Exception. Kindly debug your code!')
# 		print('Stop the CoppeliaSim simulation manually.\n')
# 		#traceback.print_exc(file=sys.stdout)
# 		#print()
# 		#sys.exit()
# 	setTiltInTable(client_id,revolute_handle,setpoint)
	
# 	print("Finished Traversing ",table_number)
# 	_,_ = sim.simxGetPingTime(client_id)
# 	return_code_signal,end=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_buffer)
# 	if(return_code_signal== 0):
# 		try:
# 			end=float(end)
# 			print("Total time taken to traverse Table "+str(table_number)+" is "+str(end-start))
# 		except Exception:
# 			pass
# 	print("=====================================================================================")
# 	##################################################
# def setTiltInTable(client_id,revolute_handle,out_coord):
	
# 	Output=[0,0]
# 	print("out_coord = ",out_coord)
# 	if(out_coord[0]<=70):
# 		Output=[-45,45]#left decrease
# 	if(out_coord[0]>=1205):
# 		Output=[45,-45]#right decreacre
# 	if(out_coord[1]>=1205):
# 		Output=[45,45]#bottom decrease
# 	if(out_coord[1]<=70):
# 		Output=[-45,-45]#top decrease
# 	task_3.setAngles(client_id,revolute_handle,Output)
# def customizePixelPath(pixel_path):
# 	copy=[[pixel_path[0][0],pixel_path[0][1],0]]
# 	ratio=[4,1]
# 	for i in range(1,len(pixel_path)-1):
# 		copy.append([pixel_path[i][0],pixel_path[i][1],0])
# 		if((pixel_path[i+1][0]-pixel_path[i][0])**2 + (pixel_path[i+1][1]-pixel_path[i][1])**2)<= 128*128 :
# 			continue
# 		coord=[-1,-1,1]
# 		#getting an extra setpoint before destination
# 		coord[0]=(ratio[0]*pixel_path[i+1][0]+ratio[1]*pixel_path[i][0])/(ratio[0]+ratio[1])
# 		coord[1]=(ratio[0]*pixel_path[i+1][1]+ratio[1]*pixel_path[i][1])/(ratio[0]+ratio[1])
# 		copy.append(coord)
# 	# copy.append([pixel_path[len(pixel_path)-2][0],pixel_path[len(pixel_path)-2][1],0])
# 	copy.append([pixel_path[len(pixel_path)-1][0],pixel_path[len(pixel_path)-1][1],0])
# 	#in starting check if it is closer to first point or secnd point , if second then simply pass
# 	# if((((pixel_path[i+1][0]-pixel_path[i][0])**2+(pixel_path[i+1][1]-pixel_path[i][1])**2)<128*128) or (pixel_path[i+1][2]==0)):
# 	# 	#normal kp ,ki,kd
# 	# 	pass
# 	# else:
# 	# 	#fast kp,ki,kd
# 	# 	pass
# 	return copy
# def shortenPath(pixel_path):
# 	path=pixel_path.copy()
#     #storing the previous index
# 	prev_x=-1
# 	#count the number of x that have had the same value as x, till present existing in the path
# 	#if count=1 and x==prev_x,meaning now 3 consecutive times x has been same
# 	#we delete the prev_node , so the cnt stays 1
# 	cnt_x=0#number of x that have been common
# 	prev_y=-1
# 	cnt_y=0
# 	#print(prev_x,prev_y)
# 	n=len(path)
# 	i=0
# 	while(i<n):

# 		x=path[i][0]
# 		y=path[i][1]
# 		#see if there are coordinates such that x are same in continuation
# 		if(x==prev_x):
# 			if(cnt_x==1):
# 				#remove the coodrdinate before
# 				#as this coordinate(x,y) and (prev_prev_x,prev_prev_y) are sufficient for this line
# 				#print((prev_x,prev_y))
# 				#print("deleted ",prev_x," ",prev_y)
# 				path.remove([prev_x,prev_y])
# 				i-=1#we dont want ncrement in i so to neutralise i+=1 in future
# 			else:
# 				cnt_x=1#if x is same and xnt_x==0, cnt_x=1 , for next time
# 		else:
# 			cnt_x=0#if x are not same
			
# 		#see if there are coordinates such that y are same in continuation
# 		#for documentation see x above
# 		if(y==prev_y):
# 			if(cnt_y==1):
# 				#more 
# 				#remove the coodrdinate before
# 				#print("deleted ",prev_x," ",prev_y)
# 				path.remove([prev_x,prev_y])
# 				i-=1
# 			else:
# 				cnt_y=1
			
# 		else:
# 			cnt_y=0
# 		#storing the previous coordinates
# 		prev_x=x
# 		prev_y=y
# 		i+=1#moving to the next node
# 		n=len(path)#as we keep on deleting the nodes , we need to update the n
# 		#print(x," ",y," ",cnt_x," ",cnt_y)
# 	return path

# # In[ ]:


# # NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# # 
# # Function Name:	main
# #		Inputs:	None
# #	   Outputs:	None
# #	   Purpose:	This part of the code is only for testing your solution. The function does the following:
# # 						- imports 'task_1b' file as module
# # 						- imports 'task_1a_part1' file as module
# #						- imports 'task_2a' file as module
# #						- imports 'task_2b' file as module
# #						- imports 'task_3' file as module
# #						- imports 'task_4a' file as module
# # 						- takes 'maze00.jpg' image file as input
# # 						- calls calculate_path_from_maze_image() function 
# # 						- calls init_remote_api_server() function in 'task_2a' to connect with CoppeliaSim Remote API server
# #						- then calls send_data() function in 'task_2b' to send maze array data to LUA script
# # 						- then calls start_simulation() function in 'task_2a' to start the simulation
# #						- then calls init_setup() in 'task_3' function to store the required handles in respective global variables and complete initializations if required
# #						- then calls send_data_to_draw_path() function to draw the calculated path in LUA script
# #						- then calls convert_path_to_pixels() function to get the path in terms of pixels so that it can be fed as setpoint to the control logic
# #						- then calls traverse_path() function to make the ball follow the path calculated
# # 						- then calls stop_simulation() function in 'task_2a' to stop the current simulation
# #						- then calls exit_remote_api_server() function in 'task_2a' to disconnect from the server

# # NOTE: Write your solution ONLY in the space provided in the above functions. Main function should NOT be edited.

# # if __name__ == "__main__":

# # 	# path directory of images in 'test_cases' folder
# # 	img_dir_path = 'test_cases/'

# # 	# path to 'maze00.jpg' image file
# # 	file_num = 0
# # 	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

# # 	print('\n============================================')
# # 	print('\nFor maze0' + str(file_num) + '.jpg')
	
# # 	if os.path.exists(img_file_path):
		
# # 		try:
# # 			maze_array,path = calculate_path_from_maze_image(img_file_path)
		
# # 		except Exception:
# # 			print('\n[ERROR] Your calculate_path_from_maze_image() function throwed an Exception. Kindly debug your code!')
# # 			print('Stop the CoppeliaSim simulation manually.\n')
# # 			traceback.print_exc(file=sys.stdout)
# # 			print()
# # 			sys.exit()
# # 	else:
# # 		print('\n[ERROR] maze0' + str(file_num) + '.jpg not found. Make sure "test_cases" folder is present in current directory.')
# # 		print('Your current directory is: ', os.getcwd())
# # 		sys.exit()

# # 	# Initiate the Remote API connection with CoppeliaSim server
# # 	print('\nConnection to CoppeliaSim Remote API Server initiated.')
# # 	print('Trying to connect to Remote API Server...')

# # 	try:
# # 		client_id = task_2a.init_remote_api_server()

# # 		if (client_id != -1):
# # 			print('\nConnected successfully to Remote API Server in CoppeliaSim!')

# # 			try:
# # 				# Send maze array data to CoppeliaSim via Remote API
# # 				return_code = task_2b.send_data(client_id,maze_array)

# # 				if (return_code == sim.simx_return_ok):
# # 					# Starting the Simulation
# # 					try:
# # 						return_code = task_2a.start_simulation()

# # 						if (return_code == sim.simx_return_novalue_flag):
# # 							print('\nSimulation started correctly in CoppeliaSim.')
							
# # 							# Storing the required handles in respective global variables.
# # 							try:
# # 								task_3.init_setup(client_id)
# # 								try:
# # 									send_data_to_draw_path(client_id,path)
								
# # 								except Exception:
# # 									print('\n[ERROR] Your send_data_to_draw_path() function throwed an Exception. Kindly debug your code!')
# # 									print('Stop the CoppeliaSim simulation manually.\n')
# # 									traceback.print_exc(file=sys.stdout)
# # 									print()
# # 									sys.exit()
							
# # 							except Exception:
# # 								print('\n[ERROR] Your init_setup() function throwed an Exception. Kindly debug your code!')
# # 								print('Stop the CoppeliaSim simulation manually if started.\n')
# # 								traceback.print_exc(file=sys.stdout)
# # 								print()
# # 								sys.exit()
						
# # 						else:
# # 							print('\n[ERROR] Failed starting the simulation in CoppeliaSim!')
# # 							print('start_simulation function in task_2a.py is not configured correctly, check the code!')
# # 							print()
# # 							sys.exit()

# # 					except Exception:
# # 						print('\n[ERROR] Your start_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
# # 						print('Stop the CoppeliaSim simulation manually.\n')
# # 						traceback.print_exc(file=sys.stdout)
# # 						print()
# # 						sys.exit()
				
# # 				else:
# # 					print('\n[ERROR] Failed sending data to CoppeliaSim!')
# # 					print('send_data function in task_2b.py is not configured correctly, check the code!')
# # 					print()
# # 					sys.exit()

# # 			except Exception:
# # 				print('\n[ERROR] Your send_data function throwed an Exception, kindly debug your code!')
# # 				traceback.print_exc(file=sys.stdout)
# # 				print()
# # 				sys.exit()
		
# # 		else:
# # 			print('\n[ERROR] Failed connecting to Remote API server!')
# # 			print('[WARNING] Make sure the CoppeliaSim software is running and')
# # 			print('[WARNING] Make sure the Port number for Remote API Server is set to 19997.')
# # 			print('[ERROR] OR init_remote_api_server function in task_2a.py is not configured correctly, check the code!')
# # 			print()
# # 			sys.exit()

# # 	except Exception:
# # 		print('\n[ERROR] Your init_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
# # 		print('Stop the CoppeliaSim simulation manually if started.\n')
# # 		traceback.print_exc(file=sys.stdout)
# # 		print()
# # 		sys.exit()

# # 	try:
# # 		pixel_path = convert_path_to_pixels(path)
# # 		print('\nPath calculated between %s and %s in pixels is = %s' % (start_coord, end_coord, pixel_path))
# # 		print('\n============================================')

# # 		try:
# # 			traverse_path(pixel_path)
		
# # 		except Exception:
# # 			print('\n[ERROR] Your traverse_path() function throwed an Exception. Kindly debug your code!')
# # 			print('Stop the CoppeliaSim simulation manually.\n')
# # 			traceback.print_exc(file=sys.stdout)
# # 			print()
# # 			sys.exit()
	
# # 	except Exception:
# # 		print('\n[ERROR] Your convert_path_to_pixels() function throwed an Exception. Kindly debug your code!')
# # 		print('Stop the CoppeliaSim simulation manually.\n')
# # 		traceback.print_exc(file=sys.stdout)
# # 		print()
# # 		sys.exit()
	
# # 	try:
# # 		return_code = task_2a.stop_simulation()
		
# # 		if (return_code == sim.simx_return_novalue_flag):
# # 			print('\nSimulation stopped correctly.')

# # 			# Stop the Remote API connection with CoppeliaSim server
# # 			try:
# # 				task_2a.exit_remote_api_server()

# # 				if (task_2a.start_simulation() == sim.simx_return_initialize_error_flag):
# # 					task_3.setAngles(np.array([0,0]))
# # 					print('\nDisconnected successfully from Remote API Server in CoppeliaSim!')

# # 				else:
# # 					print('\n[ERROR] Failed disconnecting from Remote API server!')
# # 					print('[ERROR] exit_remote_api_server function in task_2a.py is not configured correctly, check the code!')

# # 			except Exception:
# # 				print('\n[ERROR] Your exit_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
# # 				print('Stop the CoppeliaSim simulation manually.\n')
# # 				traceback.print_exc(file=sys.stdout)
# # 				print()
# # 				sys.exit()
		
# # 		else:
# # 			print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
# # 			print('[ERROR] stop_simulation function in task_2a.py is not configured correctly, check the code!')
# # 			print('Stop the CoppeliaSim simulation manually.')
# # 			print()
# # 			sys.exit()

# # 	except Exception:
# # 		print('\n[ERROR] Your stop_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
# # 		print('Stop the CoppeliaSim simulation manually.\n')
# # 		traceback.print_exc(file=sys.stdout)
# # 		print()
# # 		sys.exit()

#!/usr/bin/env python
# coding: utf-8

# In[5]:


'''
*****************************************************************************************
*
*				===============================================
*		   		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*				===============================================
*
*  This script is to implement Task 4B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD (now MOE) project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:		  NB_2182
# Author List:	  	 Yatharth Bhargava, Pranav Mittal
# Filename:		 task_4b.py
# Functions:		 calculate_path_from_maze_image, send_data_to_draw_path, 
# 					convert_path_to_pixels, traverse_path,getBallCoordinates
#				   [ Comma separated list of functions in this file ]
# Global variables: client_id, setpoint, start_coord, end_coord
# 					[ List of global variables defined in this file ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy,opencv,os,sys,traceback)	##
##############################################################
import numpy as np
import cv2
import os, sys
import traceback
import time
##############################################################

# Importing the sim module for Remote API connection with CoppeliaSim
try:
	import sim
	
except Exception:
	print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
	print('\n[WARNING] Make sure to have following files in the directory:')
	print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
	sys.exit()

#Import 'task_1b.py' file as module
try:
	import task_1b

except ImportError:
	print('\n[ERROR] task_1b.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure task_1b.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your task_1b.py throwed an Exception. Kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()


# Import 'task_1a_part1.py' file as module
try:
	import task_1a_part1

except ImportError:
	print('\n[ERROR] task_1a_part1.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure task_1a_part1.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your task_1a_part1.py throwed an Exception. Kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()


# Import 'task_2a.py' file as module
try:
	import task_2a

except ImportError:
	print('\n[ERROR] task_2a.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure task_2a.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your task_2a.py throwed an Exception. Kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()

# Import 'task_2b.py' file as module
try:
	import task_2b

except ImportError:
	print('\n[ERROR] task_2b.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure task_2b.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your task_2b.py throwed an Exception. Kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()

# Import 'task_3.py' file as module
try:
	import task_3

except ImportError:
	print('\n[ERROR] task_3.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure task_3.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your task_3.py throwed an Exception. Kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()


# Import 'task_4a.py' file as module
try:
	import task_4a

except ImportError:
	print('\n[ERROR] task_4a.py file is not present in the current directory.')
	print('Your current directory is: ', os.getcwd())
	print('Make sure task_4a.py is present in this current directory.\n')
	sys.exit()
	
except Exception as e:
	print('Your task_4a.py throwed an Exception. Kindly debug your code!\n')
	traceback.print_exc(file=sys.stdout)
	sys.exit()


# Global variable "client_id" for storing ID of starting the CoppeliaSim Remote connection
# NOTE: DO NOT change the value of this "client_id" variable here
client_id = -1

# Global list "setpoint" for storing target position of ball on the platform/top plate
# The 0th element stores the x pixel and 1st element stores the y pixel
# NOTE: DO NOT change the value of this "setpoint" list
setpoint = [0, 0]

# Global tuple to store the start and end cell coordinates of the maze
# The 0th element stores the row and 1st element stores the column
# NOTE: DO NOT change the value of these tuples
start_coord = (0,4)
end_coord = (9,5)

# You can add your global variables here
##############################################################

##############################################################


# In[6]:


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.	  ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.						 ##
##############################################################
def getBallData(client_id,vision_sensor_handle,flag):
	
	vision_sensor_image, image_resolution, return_code = task_2a.get_vision_sensor_image(client_id,vision_sensor_handle)
	# print(client_id,vision_sensor_handle)
	if ((return_code == sim.simx_return_ok) and (len(image_resolution) == 2) and (len(vision_sensor_image) > 0)):
		# print('\nImage captured from Vision Sensor in CoppeliaSim successfully!')
		pass
	else:
		#start loop again
		return None


	# Get the transformed vision sensor image captured in correct format
	try:
		# print(vision_sensor_image[0:20])
		transformed_image = task_2a.transform_vision_sensor_image(vision_sensor_image, image_resolution)
		# print(vision_sensor_handle,client_id)
		# cv2.imshow("cropped", transformed_image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()
		# print(transformed_image[0][0:20])
		if (type(transformed_image) is np.ndarray):
			# Get the resultant warped transformed vision sensor image after applying Perspective Transform
			try:
				warped_img = task_1b.applyPerspectiveTransform(transformed_image)
				if(flag):
					warped_img = warped_img[80:1200, 80:1200]
					warped_img = cv2.resize(warped_img, (1280, 1280))
					# print(warped_img[0][0:20])
					# cv2.imshow("cropped", warped_img)
					# cv2.waitKey(0)
					#cv2.imshow("warped",warped_img)
					#cv2.waitKey(0)
					# cv2.destroyAllWindows()
				if (type(warped_img) is np.ndarray):
					# Get the 'shapes' dictionary by passing the 'warped_img' to scan_image function
					try:
						shapes = task_1a_part1.scan_image(warped_img)
						if (type(shapes) is dict and shapes!={}):
							# print('\nShapes detected by Vision Sensor are: ')
							# print(shapes)
							# Storing the detected x and y centroid in center_x and center_y variable repectively
							# return shapes
							if( type(shapes['Circle'][0]) is list ):
								return None
							else:
								return shapes
						elif(type(shapes) is not dict):
							#print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.')
							#print('Stop the CoppeliaSim simulation manually.')
							return None

					except Exception:
						print('\n[ERROR] Your scan_image function in task_1a_part1.py throwed an Exception. Kindly debug your code!')
						print('Stop the CoppeliaSim simulation manually.\n')
						traceback.print_exc(file=sys.stdout)
						print()
						sys.exit()

				else:
					print('\n[ERROR] applyPerspectiveTransform function is not configured correctly, check the code.')
					print('Stop the CoppeliaSim simulation manually.')
					print()
					sys.exit()

			except Exception:
				print(".",end="")
				print('\n[ERROR] Your applyPerspectiveTransform function in task_1b.py throwed an Exception. Kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()

		else:
			print('\n[ERROR] transform_vision_sensor_image function in task_2a.py is not configured correctly, check the code.')
			print('Stop the CoppeliaSim simulation manually.')
			print()
			sys.exit()

	except Exception:
		print('\n[ERROR] Your transform_vision_sensor_image function in task_2a.py throwed an Exception. Kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()
	return None

##############################################################


# In[7]:


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def calculate_path_from_maze_image(img_file_path):
	"""
	Purpose:
	---
	This function reads the image from `img_file_path` input, applies
	Perspective Transform and computes the encoded maze array by calling
	applyPerspectiveTransform and detectMaze functions from task_1b.py.

	It then calls the find_path function from task_4a.py to compute the path
	between start and end coordinate values declared globally.

	Input Arguments:
	---
	`img_file_path` :  [ str ]
		File path of maze image.
	
	Returns:
	---
	`maze_array` 	:   [ nested list of lists ]
		encoded maze in the form of a 2D array
	
	`path` :  [ list of tuples ]
		path between start and end coordinates

	Example call:
	---
	maze_array, path = calculate_path_from_maze_image(img_file_path)
	
	"""

	# read the 'maze00.jpg' image file
	input_img = cv2.imread(img_file_path)

	if type(input_img) is np.ndarray:

		try:
			# get the resultant warped maze image after applying Perspective Transform
			warped_img = task_1b.applyPerspectiveTransform(input_img)

			if type(warped_img) is np.ndarray:

				try:
					# get the encoded maze in the form of a 2D array
					maze_array = task_1b.detectMaze(warped_img)

					if (type(maze_array) is list) and (len(maze_array) == 10):
						print('\nEncoded Maze Array = %s' % (maze_array))
						print('\n============================================')

						try:
							path = task_4a.find_path(maze_array, start_coord, end_coord)

							if (type(path) is list):

								print('\nPath calculated between %s and %s is = %s' % (start_coord, end_coord, path))
								print('\n============================================')
							
							else:
								print('It seems that path is of type ', type(path),'.\n Make sure that is a list.')
						
						except Exception:
							print('\n[ERROR] Your find_path function in \'task_4a.py\' throwed an Exception, kindly debug your code!')
							traceback.print_exc(file=sys.stdout)
							print()
							sys.exit()

					else:
						print('\n[ERROR] maze_array returned by detectMaze function in \'task_1b.py\' is not returning maze array in expected format!, check the code.')
						print()
						sys.exit()
				
				except Exception:
					print('\n[ERROR] Your detectMaze function in \'task_1b.py\' throwed an Exception, kindly debug your code!')
					traceback.print_exc(file=sys.stdout)
					print()
					sys.exit()
			
			else:
				print('\n[ERROR] applyPerspectiveTransform function in \'task_1b.py\' is not returning the warped maze image in expected format!, check the code.')
				print()
				sys.exit()

		except Exception:
			print('\n[ERROR] Your applyPerspectiveTransform function in \'task_1b.py\' throwed an Exception, kindly debug your code!')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()
	
	else:
		print('\n[ERROR] .jpg was not read correctly, something went wrong!')
		print()
		sys.exit()

	return maze_array, path


# In[8]:


def send_data_to_draw_path(rec_client_id, path,table_number):
	"""
	Purpose:
	---
	This function should:
	1. Convert and 
	2. Send a flattened path to LUA's drawPath() function.
	
	Teams are free to choose logic for this conversion.

	We have provided an example code for the above.

	Suppose [(1, 5), (2, 5)] is the path given as input to this function. 
	To visualize this path, it needs to be converted to CoppeliaSim coordinates.

	The following points should be considered:

	1. The entire maze is 1m x 1m in CoppeliaSim coordinates. Dividing this by 10 rows and 
	10 columns, we get the size of each cell to be 10cm x 10cm.

	2. The x axis of CoppeliaSim corresponds to the row and y axis corresponds to the column.

	3. The x and y origin of CoppeliaSim coincides with the center of 4th and 5th row as well
	as column. When row and column are both 0, the corresponding CoppeliaSim coordinates are
	(-0.5,-0.5). Since we need the path from the center of the cell, an offset of 45cm is required.
	
						0.45m								0.5m
		 |←-----------------------------→|←----------------------------------→|
		 |								 |									  |
	 0	 |	 1		 2		 3		 4	 |	 5		 6 		 7		 8		 9|
	 _	 |	 _	 	 _	 	 _	 	 _	 |	 _	 	 _	 	 _	 	 _	 	 _|_ _ _ _ _ _ _ 
	|_|  |  |_|		|_| 	|_| 	|_|  |	|_| 	|_| 	|_| 	|_| 	|_|		0		↑
		 |	 							 |													|
	 _	 	 _	 	 _	 	 _	 	 _	 |	 _	 	 _	 	 _	 	 _	 	 _				|
	|_| 	|_|		|_| 	|_| 	|_|  |	|_| 	|_| 	|_| 	|_| 	|_|		1		|
										 |													|
	 _	 	 _	 	 _	 	 _	 	 _	 |	 _	 	 _	 	 _	 	 _	 	 _				|
	|_| 	|_|		|_| 	|_| 	|_|  |	|_| 	|_| 	|_| 	|_| 	|_|		2		|0.5m
										 |													|
	 _	 	 _	 	 _	 	 _	 	 _	 |	 _	 	 _	 	 _	 	 _	 	 _				|
	|_| 	|_|		|_| 	|_| 	|_|  |	|_| 	|_| 	|_| 	|_| 	|_|		3		|
										 |													|
	 _	 	 _	 	 _	 	 _	 	 _	 |	 _	 	 _	 	 _	 	 _	 	 _				|
	|_| 	|_|		|_| 	|_| 	|_|  |	|_| 	|_| 	|_| 	|_| 	|_|		4		|
									   (0,0) _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _↓
	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _
	|_| 	|_|		|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_|		5

	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _
	|_| 	|_|		|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_|		6

	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _
	|_| 	|_|		|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_|		7

	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _
	|_| 	|_|		|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_|		8

	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _	 	 _
	|_| 	|_|		|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_| 	|_|		9
	|		|
	| 0.1m	|
	|←-----→|


	Using the above information we map the cell coordinates to the CoppeliaSim coordinates.
	The formula comes out to be:

	CoppeliaSim_coordinate=(((10*row_or_column_number) - 45)/100) m

	Hence the CoppeliaSim coordinates for the above example will be:

	coppelia_sim_coord_path = [-0.35, 0.05, -0.25, 0.05]

	Here we are sending a simple list with alternate x and y coordinates.

	NOTE: You are ALLOWED to change this function according to your logic.
		  Visualization of this path in the scene is MANDATORY.
	
	Input Arguments:
	---
	`rec_client_id` 	:  [ integer ]
		the client_id generated from start connection remote API, should be stored in a global variable

	`path` 	:  [ list ]
		Path returned from task_4a.find_path() function.
	
	Returns:
	---
	
	path_drawing_object_handle
	Example call:
	---
	send_data_to_draw_path(rec_client_id,path)
	
	"""
	#global client_id
	client_id = rec_client_id

	##############	IF REQUIRED, CHANGE THE CODE FROM HERE	##############
	coppelia_sim_coord_path = []
	
	for coord in path:
		for element in coord:
			coppelia_sim_coord_path.append(((10*element) - 45)/100)
	
	print('\n============================================')
	print('\nPath sent to drawPath function of Lua script is \n')
	print(coppelia_sim_coord_path)
	
	# _,_ = sim.simxGetPingTime(client_id)
	inputBuffer = bytearray()
	return_code,retInts, retFloats, retStrings, retBuffer = sim.simxCallScriptFunction(client_id,'top_plate_respondable_t'+str(table_number)+'_1', sim.sim_scripttype_customizationscript, 'drawPath', [],coppelia_sim_coord_path,[str(table_number)],inputBuffer,sim.simx_opmode_blocking)
	#print(retInts,retFloats, retStrings, retBuffer)
	# _,_ = sim.simxGetPingTime(client_id)
	if(len(retInts)==0):
		return -1
	return retInts[0]
	##################################################


# In[ ]:


def convert_path_to_pixels(path):
	"""
	Purpose:
	---
	This function should convert the obtained path (list of tuples) to pixels.
	Teams are free to choose the number of points and logic for this conversion.

	Input Arguments:
	---
	`path` 	:  [ list ]
		Path returned from task_4a.find_path() function.

	Returns:
	---
	`pixel_path` : [ type can be decided by teams ]

	Example call:
	---
	pixel_path = convert_path_to_pixels(path)

	"""
	##############	ADD YOUR CODE HERE	##############
	#the size of image is 1280x1280
	#the coordinates for path are
	#(0,0),(0,1)(0,2)(0,3)(0,4)(0,5)(0,6)(0,7)(0,8)(0,9)
	#(1,0),(1,1)(1,2)...................(1,7),(1,8)(1,9)
	#..................................................
	#(8,0),(8,1)(8,2)...................(8,7),(8,8)(8,9)
	#(9,0),(9,1)(9,2)(9,3)(9,4)(9,5)(9,6)(9,7)(9,8)(9,9)
	#the pixels in image
	#x(right)/y(down)-

	#0,1,...................1280
	#0,............................
	#1 ,............................
	#. ,............................
	#. ,............................
	#1280, .....................

	pixel_path=[]
	wh=1280/10
	
	for i in range(len(path)):
		cX=path[i][1]
		cY=path[i][0]
		pixel_path+=[[wh*cX+wh/2,wh*cY+wh/2]]
		
	##################################################	
	return pixel_path


# In[ ]:


def traverse_path(client_id,prev_pixel_path,vision_sensor_handle,revolute_handle,table_number):

	"""
	Purpose:
	---
	This function should make the ball traverse the calculated path.

	Teams are free to choose logic for this function.

	NOTE: Refer the code of main function in task_3.py.

	Input Arguments:
	---
	`pixel_path` : [ type can be decided by teams ]

	Returns:
	---
	None

	Example call:
	---
	traverse_path(pixel_path)

	"""

	##############	ADD YOUR CODE HERE	#############
	'''
	Here we have implemented a logic to optimize the path/pixel_path. The pixel_path  that we have got from
	tash_4a has each node at a distance of 1 unit from each other. In the case of straight lines in path we can skip
	some of the in between nodes this helps in rdeucing the time becuase ball travels better and wihout sudden 
	change in the set point. 

	lets suppose that our path is -[[(1, 4), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1)]] 
	then we can convert this path to [[(1, 4), (1, 1), (3, 1)]] 

		|_1,1_| 	|_1,2_| 	|_1,3_| 	|_1,4_|
		|_2,1_| 	|_2,2_| 	|_2,3_| 	|_2,4_|
		|_3,1_| 	|_3,2_| 	|_3,3_| 	|_3,4_|
		|_4,1_| 	|_4,2_| 	|_4,3_| 	|_4,4_|
		|_5,1_| 	|_5,2_| 	|_5,3_| 	|_5,4_|
	We have done this optimization in the pixel_path that we got as an argument in this function.
	for that we have to use the previous pixel coordinates(i-1) and just future coordinates(i+1) and 
	if both the pixel coordinates do not match completely this implies that there is a turn at i.
	'''
	_,_ = sim.simxGetPingTime(client_id)
	return_code_signal,start=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_buffer)
	if(return_code_signal== 0):
		try:
			now=float(start)
		except Exception:
			start=0


	if(len(prev_pixel_path)>=1):
		pixel_path = [[prev_pixel_path[0][0]-1,prev_pixel_path[0][1]-1]]
	for i in range(len(prev_pixel_path)):
		pixel_path.append(prev_pixel_path[i])		
	# pixel_path.append([1292.8, 704.0])
	pixel_path=shortenPath(pixel_path)
	pixel_path=customizePixelPath(pixel_path)
	print("Final Path in Table ",table_number,": ",pixel_path)

	# loop from start to a point less than end,as dst=src+1

	try:
		#print( "client_id=", client_id, "pixel_path" , pixel_path, "vision_sensor_handle", vision_sensor_handle, "revolute_handle", revolute_handle )
		# setTiltInTable(client_id,revolute_handle,setpoint)
		# task_3.setAngles(client_id,revolute_handle,[-30,-30])
		# time.sleep(2) 
		# task_3.setAngles(client_id,revolute_handle,[30,30])
		# task_3.setAngles(client_id,revolute_handle,[0,0])
		z=1	
		setpoint=[0,0]
		ITerm=np.array([0,0],dtype="float64")
		lastInput=np.array([0,0],dtype="float64")
		lastTime=0
		Input=np.array([0,0],dtype="float64")
		lastOutput=np.array([0,0],dtype="float64")
		summation=np.array([0,0],dtype="float64")
		Output=np.array([0,0],dtype="float64")
		# this is a kind of flag variable which will help in setting the last coordinates of ball for the first frame of run, 
		# which is used in the calculation of derivative term in PID calculation.
		prev_x=pixel_path[0][0]
		prev_y=pixel_path[0][1]
		#print("prev-x=",prev_x)
		#print("prev-y=",prev_y)
		for i in range(len(pixel_path)-1):
			#true loop until ball reached destination
			# if( (i+2)<(len(pixel_path))and(pixel_path[i+2][0]==prev_x or pixel_path[i+2][1]==prev_y)):
			# 	prev_x=pixel_path[i+1][0]
			# 	prev_y=pixel_path[i+1][1]
			# 	# print("prev-x=",prev_x)
			# 	# print("prev-y=",prev_y)
			# 	continue
			src=pixel_path[i]
			dst=pixel_path[i+1]

			# print(dst)
			prev_x=pixel_path[i+1][0]
			prev_y=pixel_path[i+1][1]
			setpoint=[dst[0],dst[1]]
			summation=np.array([0,0],dtype='float64')
			ITerm=np.array([0,0],dtype='float64')
			# print("STARTING JOURNEY TO:",(dst[0]-640)/1280,(dst[1]-640)/1280)
			temp=0
			print ("Traversing to ",setpoint," in table ",table_number,end="")
			if((((dst[0]-src[0])**2+(dst[1]-src[1])**2)<128*128) or (dst[2]==0)):
				#normal kp ,ki,kd
				print(" in slow mode")
				dst[2]=0
				kp=np.array([0.0350,0.0350],dtype='float64')
				ki=np.array([0.001,0.001],dtype='float64')#ki=ki*SampleTime
				kd=np.array([0.14,0.14],dtype='float64')#kd=kd/SampleTime
			else:
				#fast kp,ki,kd
				print(" in fast mode")
				dst[2]=1
				kp=np.array([0.030,0.030],dtype='float64')
				ki=np.array([0.001,0.001],dtype='float64')#ki=ki*SampleTime
				kd=np.array([0.145,0.145],dtype='float64')#kd=kd/SampleTime
				
			
			timechange = 0
			while(True):			
				
				shapes= getBallData(client_id,vision_sensor_handle,True) 
				if (shapes==None):
					continue
				center_x = shapes['Circle'][1]
				center_y = shapes['Circle'][2]
				# print(dst)
				#print("center_x = ",center_x,"center_y",center_y)
				if((center_x==None) or (center_y==None)):
					continue

				if(z==1):
					lastInput=task_3.coordinateTransform([center_x,center_y])
					z=0
				return_code_signal,now=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_buffer)
				if(return_code_signal== 0):
					try:
						now=float(now)
					except Exception:
						continue
					#print("Now=",now)
				else:
					continue
				#now=float(now)
				dist=(center_x-dst[0])**2+(center_y-dst[1])**2
				if((dst[2]==1) and (dist<1000)):
					#fast mode simply pass to next setpoint
					break
				elif(dst[2]==0):
					#might have to slow down or stop here
					if(dist<8000):
						kd=np.array([0.135,0.135],dtype='float64')
					if(dist<2500):
						kd=np.array([0.3,0.3],dtype='float64')
					if( dist< 1000):
						timechange=timechange+(now-temp)
						# print (now)
					temp=now
					# timechange=0
					#  Ball has to stay at each optimized set point under the threshold value for about 0.7 sec 
					# this help in stability of the ball while traversal. 
					if(timechange>=1):
						break

				#print("Calling PID")
				try:
					# print("setpoint = ",setpoint,end=" ")
					ITerm,lastInput,lastTime,Input,lastOutput,summation,Output= task_3.control_logic(setpoint,client_id,center_x,center_y,ITerm,lastInput,lastTime,Input,lastOutput,summation,Output,kp,ki,kd)
					#print( "ITerm=", ITerm, "lastInput", lastInput, "lastTime", lastTime, "Input", Input, "lastOutput", lastOutput, "summation", summation, "Output", Output)
					# print("revolute_handle = ",revolute_handle)
					task_3.setAngles(client_id,revolute_handle,Output) 
					# time.sleep(0.05)
				except:
					print('\n[ERROR] Your control_logic function throwed an Exception. Kindly debug your code!')
					print('Stop the CoppeliaSim simulation manually.\n')
					#traceback.print_exc(file=sys.stdout)
					#print()
					#sys.exit()
				lastInput = task_3.coordinateTransform([center_x,center_y])
			
	except:
		print('\n[ERROR] Your control_logic function throwed an Exception. Kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually.\n')
		#traceback.print_exc(file=sys.stdout)
		#print()
		#sys.exit()
	setTiltInTable(client_id,revolute_handle,setpoint)
	
	print("Finished Traversing ",table_number)
	_,_ = sim.simxGetPingTime(client_id)
	return_code_signal,end=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_buffer)
	if(return_code_signal== 0):
		try:
			end=float(end)
			print("Total time taken to traverse Table "+str(table_number)+" is "+str(end-start))
		except Exception:
			pass
	print("=====================================================================================")
	##################################################
def setTiltInTable(client_id,revolute_handle,out_coord):
	
	Output=[0,0]
	print("out_coord = ",out_coord)
	if(out_coord[0]<=70):
		Output=[-45,45]#left decrease
	if(out_coord[0]>=1205):
		Output=[45,-45]#right decreacre
	if(out_coord[1]>=1205):
		Output=[45,45]#bottom decrease
	if(out_coord[1]<=70):
		Output=[-45,-45]#top decrease
	task_3.setAngles(client_id,revolute_handle,Output)
def customizePixelPath(pixel_path):
	copy=[[pixel_path[0][0],pixel_path[0][1],0]]
	ratio=[4,1]
	for i in range(1,len(pixel_path)-1):
		copy.append([pixel_path[i][0],pixel_path[i][1],0])
		if((pixel_path[i+1][0]-pixel_path[i][0])**2 + (pixel_path[i+1][1]-pixel_path[i][1])**2)<= 128*128 :
			continue
		coord=[-1,-1,1]
		#getting an extra setpoint before destination
		coord[0]=(ratio[0]*pixel_path[i+1][0]+ratio[1]*pixel_path[i][0])/(ratio[0]+ratio[1])
		coord[1]=(ratio[0]*pixel_path[i+1][1]+ratio[1]*pixel_path[i][1])/(ratio[0]+ratio[1])
		copy.append(coord)
	# copy.append([pixel_path[len(pixel_path)-2][0],pixel_path[len(pixel_path)-2][1],0])
	copy.append([pixel_path[len(pixel_path)-1][0],pixel_path[len(pixel_path)-1][1],0])
	#in starting check if it is closer to first point or secnd point , if second then simply pass
	# if((((pixel_path[i+1][0]-pixel_path[i][0])**2+(pixel_path[i+1][1]-pixel_path[i][1])**2)<128*128) or (pixel_path[i+1][2]==0)):
	# 	#normal kp ,ki,kd
	# 	pass
	# else:
	# 	#fast kp,ki,kd
	# 	pass
	return copy
def shortenPath(pixel_path):
	path=pixel_path.copy()
    #storing the previous index
	prev_x=-1
	#count the number of x that have had the same value as x, till present existing in the path
	#if count=1 and x==prev_x,meaning now 3 consecutive times x has been same
	#we delete the prev_node , so the cnt stays 1
	cnt_x=0#number of x that have been common
	prev_y=-1
	cnt_y=0
	#print(prev_x,prev_y)
	n=len(path)
	i=0
	while(i<n):

		x=path[i][0]
		y=path[i][1]
		#see if there are coordinates such that x are same in continuation
		if(x==prev_x):
			if(cnt_x==1):
				#remove the coodrdinate before
				#as this coordinate(x,y) and (prev_prev_x,prev_prev_y) are sufficient for this line
				#print((prev_x,prev_y))
				#print("deleted ",prev_x," ",prev_y)
				path.remove([prev_x,prev_y])
				i-=1#we dont want ncrement in i so to neutralise i+=1 in future
			else:
				cnt_x=1#if x is same and xnt_x==0, cnt_x=1 , for next time
		else:
			cnt_x=0#if x are not same
			
		#see if there are coordinates such that y are same in continuation
		#for documentation see x above
		if(y==prev_y):
			if(cnt_y==1):
				#more 
				#remove the coodrdinate before
				#print("deleted ",prev_x," ",prev_y)
				path.remove([prev_x,prev_y])
				i-=1
			else:
				cnt_y=1
			
		else:
			cnt_y=0
		#storing the previous coordinates
		prev_x=x
		prev_y=y
		i+=1#moving to the next node
		n=len(path)#as we keep on deleting the nodes , we need to update the n
		#print(x," ",y," ",cnt_x," ",cnt_y)
	return path

# In[ ]:


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
#		Inputs:	None
#	   Outputs:	None
#	   Purpose:	This part of the code is only for testing your solution. The function does the following:
# 						- imports 'task_1b' file as module
# 						- imports 'task_1a_part1' file as module
#						- imports 'task_2a' file as module
#						- imports 'task_2b' file as module
#						- imports 'task_3' file as module
#						- imports 'task_4a' file as module
# 						- takes 'maze00.jpg' image file as input
# 						- calls calculate_path_from_maze_image() function 
# 						- calls init_remote_api_server() function in 'task_2a' to connect with CoppeliaSim Remote API server
#						- then calls send_data() function in 'task_2b' to send maze array data to LUA script
# 						- then calls start_simulation() function in 'task_2a' to start the simulation
#						- then calls init_setup() in 'task_3' function to store the required handles in respective global variables and complete initializations if required
#						- then calls send_data_to_draw_path() function to draw the calculated path in LUA script
#						- then calls convert_path_to_pixels() function to get the path in terms of pixels so that it can be fed as setpoint to the control logic
#						- then calls traverse_path() function to make the ball follow the path calculated
# 						- then calls stop_simulation() function in 'task_2a' to stop the current simulation
#						- then calls exit_remote_api_server() function in 'task_2a' to disconnect from the server

# NOTE: Write your solution ONLY in the space provided in the above functions. Main function should NOT be edited.

# if __name__ == "__main__":

# 	# path directory of images in 'test_cases' folder
# 	img_dir_path = 'test_cases/'

# 	# path to 'maze00.jpg' image file
# 	file_num = 0
# 	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

# 	print('\n============================================')
# 	print('\nFor maze0' + str(file_num) + '.jpg')
	
# 	if os.path.exists(img_file_path):
		
# 		try:
# 			maze_array,path = calculate_path_from_maze_image(img_file_path)
		
# 		except Exception:
# 			print('\n[ERROR] Your calculate_path_from_maze_image() function throwed an Exception. Kindly debug your code!')
# 			print('Stop the CoppeliaSim simulation manually.\n')
# 			traceback.print_exc(file=sys.stdout)
# 			print()
# 			sys.exit()
# 	else:
# 		print('\n[ERROR] maze0' + str(file_num) + '.jpg not found. Make sure "test_cases" folder is present in current directory.')
# 		print('Your current directory is: ', os.getcwd())
# 		sys.exit()

# 	# Initiate the Remote API connection with CoppeliaSim server
# 	print('\nConnection to CoppeliaSim Remote API Server initiated.')
# 	print('Trying to connect to Remote API Server...')

# 	try:
# 		client_id = task_2a.init_remote_api_server()

# 		if (client_id != -1):
# 			print('\nConnected successfully to Remote API Server in CoppeliaSim!')

# 			try:
# 				# Send maze array data to CoppeliaSim via Remote API
# 				return_code = task_2b.send_data(client_id,maze_array)

# 				if (return_code == sim.simx_return_ok):
# 					# Starting the Simulation
# 					try:
# 						return_code = task_2a.start_simulation()

# 						if (return_code == sim.simx_return_novalue_flag):
# 							print('\nSimulation started correctly in CoppeliaSim.')
							
# 							# Storing the required handles in respective global variables.
# 							try:
# 								task_3.init_setup(client_id)
# 								try:
# 									send_data_to_draw_path(client_id,path)
								
# 								except Exception:
# 									print('\n[ERROR] Your send_data_to_draw_path() function throwed an Exception. Kindly debug your code!')
# 									print('Stop the CoppeliaSim simulation manually.\n')
# 									traceback.print_exc(file=sys.stdout)
# 									print()
# 									sys.exit()
							
# 							except Exception:
# 								print('\n[ERROR] Your init_setup() function throwed an Exception. Kindly debug your code!')
# 								print('Stop the CoppeliaSim simulation manually if started.\n')
# 								traceback.print_exc(file=sys.stdout)
# 								print()
# 								sys.exit()
						
# 						else:
# 							print('\n[ERROR] Failed starting the simulation in CoppeliaSim!')
# 							print('start_simulation function in task_2a.py is not configured correctly, check the code!')
# 							print()
# 							sys.exit()

# 					except Exception:
# 						print('\n[ERROR] Your start_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
# 						print('Stop the CoppeliaSim simulation manually.\n')
# 						traceback.print_exc(file=sys.stdout)
# 						print()
# 						sys.exit()
				
# 				else:
# 					print('\n[ERROR] Failed sending data to CoppeliaSim!')
# 					print('send_data function in task_2b.py is not configured correctly, check the code!')
# 					print()
# 					sys.exit()

# 			except Exception:
# 				print('\n[ERROR] Your send_data function throwed an Exception, kindly debug your code!')
# 				traceback.print_exc(file=sys.stdout)
# 				print()
# 				sys.exit()
		
# 		else:
# 			print('\n[ERROR] Failed connecting to Remote API server!')
# 			print('[WARNING] Make sure the CoppeliaSim software is running and')
# 			print('[WARNING] Make sure the Port number for Remote API Server is set to 19997.')
# 			print('[ERROR] OR init_remote_api_server function in task_2a.py is not configured correctly, check the code!')
# 			print()
# 			sys.exit()

# 	except Exception:
# 		print('\n[ERROR] Your init_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
# 		print('Stop the CoppeliaSim simulation manually if started.\n')
# 		traceback.print_exc(file=sys.stdout)
# 		print()
# 		sys.exit()

# 	try:
# 		pixel_path = convert_path_to_pixels(path)
# 		print('\nPath calculated between %s and %s in pixels is = %s' % (start_coord, end_coord, pixel_path))
# 		print('\n============================================')

# 		try:
# 			traverse_path(pixel_path)
		
# 		except Exception:
# 			print('\n[ERROR] Your traverse_path() function throwed an Exception. Kindly debug your code!')
# 			print('Stop the CoppeliaSim simulation manually.\n')
# 			traceback.print_exc(file=sys.stdout)
# 			print()
# 			sys.exit()
	
# 	except Exception:
# 		print('\n[ERROR] Your convert_path_to_pixels() function throwed an Exception. Kindly debug your code!')
# 		print('Stop the CoppeliaSim simulation manually.\n')
# 		traceback.print_exc(file=sys.stdout)
# 		print()
# 		sys.exit()
	
# 	try:
# 		return_code = task_2a.stop_simulation()
		
# 		if (return_code == sim.simx_return_novalue_flag):
# 			print('\nSimulation stopped correctly.')

# 			# Stop the Remote API connection with CoppeliaSim server
# 			try:
# 				task_2a.exit_remote_api_server()

# 				if (task_2a.start_simulation() == sim.simx_return_initialize_error_flag):
# 					task_3.setAngles(np.array([0,0]))
# 					print('\nDisconnected successfully from Remote API Server in CoppeliaSim!')

# 				else:
# 					print('\n[ERROR] Failed disconnecting from Remote API server!')
# 					print('[ERROR] exit_remote_api_server function in task_2a.py is not configured correctly, check the code!')

# 			except Exception:
# 				print('\n[ERROR] Your exit_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
# 				print('Stop the CoppeliaSim simulation manually.\n')
# 				traceback.print_exc(file=sys.stdout)
# 				print()
# 				sys.exit()
		
# 		else:
# 			print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
# 			print('[ERROR] stop_simulation function in task_2a.py is not configured correctly, check the code!')
# 			print('Stop the CoppeliaSim simulation manually.')
# 			print()
# 			sys.exit()

# 	except Exception:
# 		print('\n[ERROR] Your stop_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
# 		print('Stop the CoppeliaSim simulation manually.\n')
# 		traceback.print_exc(file=sys.stdout)
# 		print()
# 		sys.exit()

