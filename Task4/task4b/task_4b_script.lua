--[[
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This Lua script is to implement Task 4B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
]]--


--[[
# Team ID:			2182
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_4b_lua
# Functions:        createWall, receiveData, generateHorizontalWalls, 
#                   generateVerticalWalls, deleteWalls, createMaze, sysCall_init, sysCall_beforeSimulation
#                   sysCall_afterSimulation, sysCall_cleanup,setWallLocation,deleteWall
#                    [ Comma separated list of functions in this file ]
# Global variables:	 maze_array
# 					[ List of global variables defined in this file ]
]]--

--[[
##################### GLOBAL VARIABLES #######################
## You can add global variables in this section according   ##
## to your requirement.                                     ##
## DO NOT TAMPER WITH THE ALREADY DEFINED GLOBAL VARIABLES. ##
##############################################################
]]--

maze_array = {}
base_children_list={} --Do not change or delete this variable
baseHandle = -1       --Do not change or delete this variable

--############################################################

--[[
##################### HELPER FUNCTIONS #######################
## You can add helper functions in this section according   ##
## to your requirement.                                     ##
## DO NOT MODIFY OR CHANGE THE ALREADY DEFINED HELPER       ##
## FUNCTIONS                                                ##
##############################################################
--]]
function setWallLocation(pos,ori,name,parent)
    --make a wall element based on the info sent as arguments 
    local wallObjectHandle=createWall()
    sim.setObjectOrientation(wallObjectHandle, -1,ori)
    sim.setObjectPosition(wallObjectHandle,-1,pos)
    --print(name)
    sim.setObjectName(wallObjectHandle,name)
    
    --sim.setObjectParent(wallObjectHandle,parent,true)
end
function deleteWall(name)
    --delete the wall element of that name if it exists
    local handle=sim.getObjectHandle(name)
    if(handle~=-1)
    then
        sim.removeObject(handle)
    end
end
function getObjectCoordinates(name,base)
    local handle=sim.getObjectHandle(name)
    --gets the border coodrdinates of the base to be used to make walls relative to the position of relative to respective top_plate_respondable 
    return sim.getObjectPosition(handle,-1)
end
function getObjectSize(name)
    --gets the object size
    local handle=sim.getObjectHandle(name)
    --returns the geometric shape/size of according to handle
    --number result,number pureType,table_4 dimensions=sim.getShapeGeomInfo(number shapeHandle)
    result,pureType,dimensions=sim.getShapeGeomInfo(handle)
    --dimensions[1]: X-size or diameter of the pure shape. Undefined if the shape is a compound shape or not pure.
    --dimensions[2]: Y-size of the pure shape. Undefined if the shape is a compound shape or not pure.
    --dimensions[3]: Z-size or height of the pure shape. Undefined if the shape is a compound shape or not pure.
    --dimensions[4]: Inside scaling. Undefined if the shape is a compound shape or not pure.
    return dimensions
end
function getWallZValue()
    --gets the z value calculated according to the base
    --dimensions of wall {0.09, 0.01, 0.1}
    local dimensions=getObjectSize("top_plate_respondable_1")
    local z=dimensions[3]
    return z/2+0.1/2
end
function deleteExit(number)
    --wrong function need debugging
    --number is index of table
    --deleting extra walls according to table number
    --for Table4(Center),Exit points are Vertical_wall-(4,0),vertical_wall-(5,9),horizontal_wall-(9,4)
    --for Table1(Right),Exit points are Horizontal_wall-(0,4),vertical_wall-(4,9),horizontal_wall-(9,5)
    --for Table2(Bottom),Exit points are Vertical_wall-(5,0),vertical_wall-(4,9),horizontal_wall-(9,5)
    --for Table3(Left),Exit points are Vertical_wall-(5,0),horizontal_wall-(0,4),horizontal_wall-(9,5)
    --the names of walls start from one where as wall number start from 1
    --FORMAT:list[table][i][1]==1,remove horizontal else remove veritcal at list[table][i][2]xlist[table][i][3]
    if(number>4) or (number<1)
    then
        return
    end
    list={{{1,1,5},{-1,5,11},{1,11,6}},
            {{-1,6,1},{-1,5,11},{1,11,6}},
            {{-1,6,1},{1,1,5},{1,11,6}},
            {{-1,5,1},{-1,6,11},{1,11,5}}}
    for i=1,3,1
    do
        --print(i)
        --print(list[number][i])
        if(list[number][i][1]==1)
        then
            name="H_WallSegment_"..list[number][i][2].."x"..list[number][i][3]
            sim.removeObject(sim.getObjectHandle(name))
        else
            name="V_WallSegment_"..list[number][i][2].."x"..list[number][i][3]
            sim.removeObject(sim.getObjectHandle(name))
        end
    end
end
--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION
**************************************************************
	Function Name : createWall()
	Purpose:
	---
	Creates a black-colored wall of dimensions 90cm x 10cm x 10cm

	Input Arguments:
	---
	None
	
	Returns:
	---
	wallObjectHandle : number
	
	returns the object handle of the wall created
	
	Example call:
	---
	wallObjectHandle = createWall()
**************************************************************	
]]--
function createWall()
	wallObjectHandle = sim.createPureShape(0, 8, {0.09, 0.01, 0.1}, 0.0001, nil)
	--Refer https://www.coppeliarobotics.com/helpFiles/en/regularApi/simCreatePureShape.htm to understand the parameters passed to this function
	sim.setShapeColor(wallObjectHandle, nil, sim.colorcomponent_ambient_diffuse, {0, 0, 0})
	sim.setObjectInt32Parameter(wallObjectHandle,sim.shapeintparam_respondable_mask,65280)
	--Refer https://www.coppeliarobotics.com/helpFiles/en/apiFunctions.htm#sim.setObjectInt32Parameter to understand the various parameters passed. 	
	--The walls should only be collidable with the ball and not with each other.
	--Hence we are enabling only the local respondable masks of the walls created.
	sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_collidable)
    --sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_renderable)
	--Walls may have to be set as renderable........................... 
	--This is required to make the wall as collidable
	return wallObjectHandle
end

--############################################################

--[[
**************************************************************
	Function Name : receiveData()
	Purpose:
	---
	Receives data via Remote API. This function is called by 
	simx.callScriptFunction() in the python code (task_2b.py)

	Input Arguments:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	These 4 variables represent the data being passed from remote
	API client(python) to the CoppeliaSim scene
	
	Example call:
	---
	Shall be called from the python script
**************************************************************	
]]--
function receiveData(inInts,inFloats,inStrings,inBuffer)

	--*******************************************************
	--               ADD YOUR CODE HERE
    --make 2D array from received 1D array
    --print(inInts)
    --print(maze_array)
    maze_array={}
    if(inInts==nil)
    then
        return
    end
    wall=10
    for i=1,#inInts,wall
    do
        local sub_list={}
        for j=i,wall+i-1,1
        do
            table.insert(sub_list,inInts[j])
        end
        table.insert(maze_array,sub_list)
    end
    --print(maze_array)
    --maze_array=inInts

	--*******************************************************
	return inInts, inFloats, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : generateHorizontalWalls()
	Purpose:
	---
	Generates all the Horizontal Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	generateHorizontalWalls()
**************************************************************	
]]--
function generateHorizontalWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
    --[[(x,y)==(row,col)==(i,j)==ixj
    1x1 1x2 1x3 1x4 ..... 1x10
    2x1 2x2 ................
    .
    .
    10x1 10x2 ........... 10x10
    11x1 11x2 ........... 11x10
    ]]--
    --[[Axis in simulation coordinate system
    y-0,1,2,3,................
    x
    0
    1
    2
    .
    .
    .
    
    ]]--(0,0) at 5x5
    local base=getObjectCoordinates("top_plate_respondable_1")
    
    local wall=10
    local x_gap=0.1
    local y_gap=0.1
    local z_value=getWallZValue()
    --pos={-0.01*5,0.05-0.1*5,0.08}
    --starting position is the top left corner
    --format = midpoint of x/y_gap +/- measure of distance to the edge of the base + coordinate of base
    local pos={-x_gap*wall/2+base[1],y_gap/2-y_gap*wall/2+base[2],z_value+base[3]}
    local ori={0,0,math.pi/2}
    
    --local parent=sim.getObjectHandle("Base")
    local parent=-1
    for i=1,wall+1,1
    do
        for j=1,wall,1
        do
            local name="H_WallSegment_"..i.."x"..j
            --print(pos)
            setWallLocation(pos,ori,name,parent)
            --print(pos)
            --adding 0.01 to y,going left to right 
            --pos[2]=pos[2]+0.1
            pos[2]=pos[2]+y_gap
        end
        --reseting values of y , going left to right
        --pos[2]=0.05-0.1*5
        pos[2]=y_gap/2-y_gap*wall/2
        --adding 0.01 to x , coming one level down
        --pos[1]=pos[1]+0.1
        pos[1]=pos[1]+x_gap
    end
	--*******************************************************
end

--[[
**************************************************************
	Function Name : generateVerticalWalls()
	Purpose:
	---
	Generates all the Vertical Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	generateVerticalWalls()
**************************************************************	
]]--
function generateVerticalWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
    --[[(x,y)==(row,col)==(i,j)==ixj
    1x1 1x2 1x3 1x4 ..... 1x10 1x11
    2x1 2x2 ................   2x11
    .
    .
    10x1 10x2 ........... 10x10 10x11
    ]]--
    --[[Axis in simulation coordinate system
    y-0,1,2,3,................
    x
    0
    1
    2
    .
    .
    .
    
    ]]--(0,0) at 5x5
    local base=getObjectCoordinates("top_plate_respondable_1")
    local wall=10
    local x_gap=0.1
    local y_gap=0.1
    local z_value=getWallZValue()
    --pos={0.05-0.1*5,-0.1*5,0.08}
    --format = midpoint of x/y_gap +/- measure of distance to the edge of the base + coordinate of base
    local pos={x_gap/2-x_gap*wall/2+base[1],-y_gap*wall/2+base[2],z_value+base[3]}
    local ori={0,0,0}
    
    --local parent=sim.getObjectHandle("Base")
    local parent=-1
    
    for i=1,wall,1
    do
        for j=1,wall+1,1
        do
            local name="V_WallSegment_"..i.."x"..j
            --print(pos)
            setWallLocation(pos,ori,name,parent)
            --print(pos)
            --adding 0.01 to y,going left to right 
            --pos[2]=pos[2]+0.1
            pos[2]=pos[2]+y_gap
        end
        --reseting values of y , going left to right
        --pos[2]=-0.1*5
        pos[2]=-y_gap*wall/2
        --adding 0.01 to x , coming one level down
        --pos[1]=pos[1]+0.1
        pos[1]=pos[1]+x_gap
    end
    

	--*******************************************************
end

--[[
**************************************************************
	Function Name : deleteWalls()
	Purpose:
	---
	Deletes all the grouped walls in the given scene

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	deleteWalls()
**************************************************************	
]]--
function deleteWalls()
    --print("DELETING WALLS.")
	--*******************************************************
	--               ADD YOUR CODE HERE
    --"V_WallSegment_"..i.."x"..j[1-10,1-11]
    --"H_WallSegment_"..i.."x"..j[1-11,1-10]
    local wall=10
    --deleting all wall except i==j
    --removing runtime error on objectHandle not found
    local savedState=sim.getInt32Parameter(sim.intparam_error_report_mode)
    sim.setInt32Parameter(sim.intparam_error_report_mode,0)
    
    for i=1,wall,1
    do
        for j=1,wall,1
        do
            if(i==j)
            then
                --deleting (i,i) where i==(1:10)
                name="V_WallSegment_"..i.."x"..j
                deleteWall(name)
                name="H_WallSegment_"..j.."x"..i
                deleteWall(name)
                break
            end
            --deleting the (i,j) where i,j==(1:10,1:10)
            name="V_WallSegment_"..i.."x"..j
            deleteWall(name)
            name="H_WallSegment_"..i.."x"..j
            deleteWall(name)
            --deleting the (i,j) where i,j==(1:10,1:10)
            name="V_WallSegment_"..j.."x"..i
            deleteWall(name)
            
            name="H_WallSegment_"..j.."x"..i
            deleteWall(name)
        end
    end
    --deleting the 11th row/col of wall
    for i=1,wall,1
    do
        name="V_WallSegment_"..i.."x11"
        deleteWall(name)
        name="H_WallSegment_11x"..i
        deleteWall(name)
    end
    deleteWall("walls_1")
    --reseting runtime error on objectHandle not found
    sim.setInt32Parameter(sim.intparam_error_report_mode,savedState)
    
	--*******************************************************
end


--[[
**************************************************************
  YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT PARAMETERS FOR THIS
						  FUNCTION
**************************************************************
	Function Name : createMaze()
	Purpose:
	---
	Creates the maze in the given scene by deleting specific 
	horizontal and vertical walls

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	createMaze()
**************************************************************	
]]--
function createMaze()
	
	--*******************************************************
	--               ADD YOUR CODE HERE
    --Horizontal walls
    --[[(x,y)==(row,col)==(i,j)==ixj
    1x1 1x2 1x3 1x4 ..... 1x10
    2x1 2x2 ................
    .
    .
    10x1 10x2 ........... 10x10
    11x1 11x2 ........... 11x10
    ]]--
    --Vertical walls
    --[[(x,y)==(row,col)==(i,j)==ixj
    1x1 1x2 1x3 1x4 ..... 1x10 1x11
    2x1 2x2 ................   2x11
    .
    .
    10x1 10x2 ........... 10x10 10x11
    ]]--
    --[[Axis in simulation coordinate system
    y-0,1,2,3,................
    x
    0
    1
    2
    .
    .
    .
    
    ]]--(0,0) at 5x5
    --*******************************************************
    --[[maze_array={{3, 10, 10, 14, 7, 11, 10, 10, 10, 6},
 {5, 3, 14, 3, 8, 6, 3, 10, 6, 5},
 {5, 1, 6, 1, 14, 9, 8, 14, 5, 5},
 {5, 5, 9, 12, 3, 6, 3, 10, 12, 13},
 {13, 5, 7, 11, 12, 5, 5, 11, 2, 14},
 {11, 8, 4, 3, 14, 9, 12, 3, 4, 7},
 {7, 3, 12, 9, 10, 10, 10, 4, 5, 5},
 {5, 5, 3, 6, 3, 10, 10, 12, 5, 5},
 {5, 9, 12, 9, 12, 3, 10, 10, 12, 5},
 {9, 10, 10, 10, 14, 13, 11, 10, 10, 12}}
]]--
    if(#maze_array==0)
    then
        return
    end
    --west=1,north=2,east=4,south=8
    
    local wall=10
    --checking value of mazearray for alternate cells,no wall are common
    --deleteing accordingly,as no repeated deletion of walls can be allowed
    
    for i=1,wall,1
    do
        for j=i%2+1,wall,2
        do
            local roi=maze_array[i][j]
            local west=roi%2
            roi=math.floor(roi/2)
            local north=roi%2
            roi=math.floor(roi/2)
            local east=roi%2
            roi=math.floor(roi/2)
            local south=roi%2
            --circumsiding wall for ixj roi ith row,jth col
            --west=ixj, north=ixj,south=i+1xj,east=ixj+1
            if(west==0)
            then
                name="V_WallSegment_"..i.."x"..j
                sim.removeObject(sim.getObjectHandle(name))
            end
            if(north==0)
            then
                name="H_WallSegment_"..i.."x"..j
                sim.removeObject(sim.getObjectHandle(name))
            end
            if(east==0)
            then
                name="V_WallSegment_"..i.."x"..j+1
                sim.removeObject(sim.getObjectHandle(name))
            end
            if(south==0)
            then
                name="H_WallSegment_"..(i+1).."x"..j
                sim.removeObject(sim.getObjectHandle(name))
            end
        end
    end
    --print("Maze Complete")
	--*******************************************************
end
--[[
	Function Name : groupWalls()
	Purpose:
	---
	Groups the various walls in the scene to one object.
	The name of the new grouped object should be set as 'walls_1'.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	groupWalls()
**************************************************************	
]]--

function groupWalls()
	--*******************************************************
	--               ADD YOUR CODE HERE
    
    --V_WallSegment_"..i.."x"..j,i=1:10,j=1:11
    --H_WallSegment_"..i.."x"..j,i=1:11,j=1:10
    --number shapeHandle=sim.groupShapes(table shapeHandles, bool merge=false)
    --number result=sim.setObjectName(number objectHandle,string objectName)
    --removing runtime error on objectHandle not found
    local savedState=sim.getInt32Parameter(sim.intparam_error_report_mode)
    sim.setInt32Parameter(sim.intparam_error_report_mode,0)
    
    local wall =10
    local handles={}
    --get all the handles of walls
    for i=1,wall+1,1
    do
        for j=1,wall,1
        do
            vHandle=sim.getObjectHandle("V_WallSegment_"..j.."x"..i)
            hHandle=sim.getObjectHandle("H_WallSegment_"..i.."x"..j)
            if(vHandle~=-1)
            then
                table.insert(handles,vHandle)
            end
            if(hHandle~=-1)
            then
                table.insert(handles,hHandle)
            end
            
        end
    end
    wallsGroupHandle=sim.groupShapes(handles,false)
    result=sim.setObjectName(wallsGroupHandle,"walls_1")
    --print(wallsGroupHandle)
    --set walls_1 as child of force_sensor_tp_1
    --print(sim.getObjectHandle("force_sensor_pw_1"))
    sim.setObjectParent(wallsGroupHandle,sim.getObjectHandle("force_sensor_pw_1"),true)
    
    --reseting runtime error on objectHandle not found
    sim.setInt32Parameter(sim.intparam_error_report_mode,savedState)
	
	--*******************************************************
end

--[[
	Function Name : addToCollection()
	Purpose:
	---
	Adds the 'walls_1' grouped object to the collection 'colliding_objects'.  

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	addToCollection()
**************************************************************	
]]--

function addToCollection()
	--*******************************************************
	--               ADD YOUR CODE HERE
    --number result=sim.addObjectToCollection(number collectionHandle,number objectHandle,number what,number options)
    --sim.handle_tree,sim.handle_single
    wallGrp=sim.getObjectHandle("walls_1")
    collHandle=sim.getCollectionHandle("colliding_objects")
    result=sim.addObjectToCollection(collHandle,wallGrp,sim.handle_single,2)
    --print(wallGrp)
    --print(collHandle)
    --print(result)
    --print(sim.getObjectHandle("pegs_1"))
    --print(sim.getCollectionObjects(collHandle))
	--*******************************************************
end

--[[
	******************************************************************************
			YOU ARE ALLOWED TO MODIFY THIS FUNCTION DEPENDING ON YOUR PATH. 
	******************************************************************************
	Function Name : drawPath(inInts,path,inStrings,inBuffer)
	Purpose:
	---
	Builds blue coloured lines in the scene according to the
	path generated from the python file. 

	Input Arguments:
	---
	inInts : Table of Ints
	inFloats : Table of Floats (containing the path generated)
	inStrings : Table of Strings
	inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	Example call:
	---
	Shall be called from the python script
**************************************************************	
]]--
function drawPath(inInts,path,inStrings,inBuffer)
	posTable=sim.getObjectPosition(wallsGroupHandle,-1)
	print('=========================================')
	print('Path received is as follows: ')
	print(path)
	if not lineContainer then
		_lineContainer=sim.addDrawingObject(sim.drawing_lines,1,0,wallsGroupHandle,99999,{0.2,0.2,1})
		sim.addDrawingObjectItem(_lineContainer,nil)
		if path then
			local pc=#path/2
			for i=1,pc-1,1 do
				lineDat={path[(i-1)*2+1],path[(i-1)*2+2],posTable[3]-0.03,path[(i)*2+1],path[(i)*2+2],posTable[3]-0.03}
				sim.addDrawingObjectItem(_lineContainer,lineDat)
			end
		end
	end
	return inInts, path, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : sysCall_init()
	Purpose:
	---
	Can be used for initialization of parameters
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_init()
	--*******************************************************
	--               ADD YOUR CODE HERE
	--*******************************************************
end

--[[
**************************************************************
		YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION.
		YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT 
		PARAMETERS ONLY FOR CREATEMAZE() FUNCTION
**************************************************************
	Function Name : sysCall_beforeSimulation()
	Purpose:
	---
	This is executed before simulation starts
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_beforeSimulation()
	
	generateHorizontalWalls()
	generateVerticalWalls()
	createMaze()--You can define your own input and output parameters only for this function
    groupWalls()
	addToCollection()
end

--[[
**************************************************************
		YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION. 
**************************************************************
	Function Name : sysCall_afterSimulation()
	Purpose:
	---
	This is executed after simulation ends
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_afterSimulation()
	-- is executed after a simulation ends
	deleteWalls()
    evaluation_screen_respondable=sim.getObjectHandle('evaluation_screen_respondable@silentError')
    if(evaluation_screen_respondable~=-1) then
        sim.removeModel(evaluation_screen_respondable)
    end
end

function sysCall_cleanup()
	-- do some clean-up here
end

-- See the user manual or the available code snippets for additional callback functions and details
