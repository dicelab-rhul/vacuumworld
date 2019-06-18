from GridWorld.GridEnvironment import GridPhysics, GridAmbient
from GridWorld.GridEnvironmentActuator import MovementActuator,CleaningDirtActuator, DropDirtActuator,CommunicationActuator
from GridWorld.GridSensor import CommunicationSensor,VisionSensor


from GenericAgent.Agent import AgentBody
from BasicBuildingBlock.Coordinate import Coordinate
from GridWorld.Orientation_Direction import Orientation
from GridWorld.EntityType import CellType, AgentColor,DirtColor
from GridWorldAction import  ChangeOrientationAction,ForwardMoveMentAction,SpeakAction
from GridWorld.GridEnvironment import GridEnvironment
from GridWorld.AllocationMap import PhysicalAllocationMap
from GridWorld.GridPerception import VisionPerception,GridVisionPerception,VWGridVisionPerception,VWCommunicationPerception,VWActionResultPerception
from GridWorld.VAgent import CleaningAgentMind,CleaningAgentBody 
from GridWorld.Actor import UserMind,UserBody 

from GridWorld.ActionType import ActionType
from GridWorld.Object import Dirt


phy = GridPhysics({VisionSensor:[VisionPerception,GridVisionPerception,VWGridVisionPerception,VWActionResultPerception], 
                   CommunicationSensor:[VWCommunicationPerception]})


act1=MovementActuator()
act2=CommunicationActuator()

act3=MovementActuator()
act4=CommunicationActuator()

act5=MovementActuator()
act6=CommunicationActuator()

act7=CleaningDirtActuator()
act8=CleaningDirtActuator()
act9=CleaningDirtActuator()

act10=DropDirtActuator()
act11=MovementActuator()



#act8=CommunicationActuator()


s1=VisionSensor()
s2=CommunicationSensor()
s3=VisionSensor()
s4=CommunicationSensor()
s5=VisionSensor()
s6=CommunicationSensor()

s7=VisionSensor()


sensorList=[s1,s2,s3,s4,s5,s6]  # sensors available in the environment


ag1 = CleaningAgentBody(CleaningAgentMind(), [act1,act2,act7], [s1,s2],Orientation.EAST,AgentColor.GREEN)
ag2 = CleaningAgentBody(CleaningAgentMind(), [act3,act4,act8], [s3,s4],Orientation.WEST,AgentColor.ORANGE)
ag3= CleaningAgentBody(CleaningAgentMind(), [act5,act6,act9], [s5,s6],Orientation.NORTH,AgentColor.WHITE)
#ag4= CleaningAgentBody(CleaningAgentMind(), [act5,act6,act9], [s5,s6],Orientation.NORTH,AgentColor.WHITE)

#user=UserBody(UserMind(),[act10,act11],[s7],Orientation.EAST)


d1= Dirt(DirtColor.GREEN)
d2= Dirt(DirtColor.ORANGE)

agents=[ag1,ag2,ag3]#,user]



p=PhysicalAllocationMap(5,5)  # specifying the grid 


print("_______________________________________________________________________________")
print("________AFTER PLACING AGENT______________")
print("                                                                               ")
                                                                                                                                                                                                                                                                                                                                                                                                                               
p.placeEntity(Coordinate(1,0),ag1.getID(),CellType.AGENT,ag1.getOrientation(),ag1.getColor())
p.placeEntity(Coordinate(2,3),d1.getID(),CellType.DIRT,None,d1.getColor())
p.placeEntity(Coordinate(2,0),d2.getID(),CellType.DIRT,None,d2.getColor())
p.placeEntity(Coordinate(0,3),ag2.getID(),CellType.AGENT,ag2.getOrientation(),ag2.getColor())
p.placeEntity(Coordinate(4,3),ag3.getID(),CellType.AGENT,ag3.getOrientation(),ag3.getColor())
#p.placeEntity(Coordinate(2,3),user.getID(),CellType.USER,user.getOrientation(),None)


                                                                                                                                                                    
amb= GridAmbient(agents,[d1,d2],p)

actionList=list(ActionType)
e= GridEnvironment(phy,amb,actionList,sensorList)#,[])
e.simulate(4 )












# -*- coding: utf-8 -*-

