#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.add_offset_to_pose_state import AddOffsetToPoseState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.text_to_float_state import TextToFloatState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 02 2021
@author: Ricardo_Kronenburg
'''
class place_part_on_agvSM(Behavior):
	'''
	Behavior to place part on agv
	'''


	def __init__(self):
		super(place_part_on_agvSM, self).__init__()
		self.name = 'place_part_on_agv'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:33 y:890, x:633 y:440
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['action_topic_namespace', 'agv_id', 'pose_order', 'gripper_service', 'part'])
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = ''
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.agv_pose_config = ''
		_state_machine.userdata.gripper_service = ''
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.pose_order = []
		_state_machine.userdata.pose_agv = []
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.part_height = ''
		_state_machine.userdata.part = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:158 y:34
			OperatableStateMachine.add('LookUpRefFrame',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='pose_config', index_title='robot', column_title='ref_frame_get_agv_pose'),
										transitions={'found': 'LookUpFrame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'agv_id', 'column_value': 'ref_frame'})

			# x:1186 y:524
			OperatableStateMachine.add('AddOffsetToPose',
										AddOffsetToPoseState(),
										transitions={'continue': 'ComputePlace'},
										autonomy={'continue': Autonomy.Off},
										remapping={'input_pose': 'pose_agv', 'offset_pose': 'pose_order', 'output_pose': 'pose_agv'})

			# x:1179 y:624
			OperatableStateMachine.add('ComputePlace',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'MoveToPlace', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'tool_link': 'tool_link', 'pose': 'pose_agv', 'offset': 'part_height_float', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1191 y:424
			OperatableStateMachine.add('GetAGVPose',
										GetObjectPoseState(),
										transitions={'continue': 'AddOffsetToPose', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'frame': 'frame', 'pose': 'pose_agv'})

			# x:924 y:724
			OperatableStateMachine.add('GripperDisable',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'Wait_4', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper_service'})

			# x:324 y:36
			OperatableStateMachine.add('LookUpFrame',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='pose_config', index_title='robot', column_title='frame_get_agv_pose'),
										transitions={'found': 'LookupPartHeight', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'agv_id', 'column_value': 'frame'})

			# x:485 y:59
			OperatableStateMachine.add('LookupPartHeight',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='part_heights', index_title='parts', column_title='part_height'),
										transitions={'found': 'PartHeightStrToFloat', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'part', 'column_value': 'part_height'})

			# x:1185 y:124
			OperatableStateMachine.add('LookupRobotConfig',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='pose_config', index_title='robot', column_title='agv_pose_config'),
										transitions={'found': 'MoveToPrePlace', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'agv_id', 'column_value': 'agv_pose_config'})

			# x:1171 y:724
			OperatableStateMachine.add('MoveToPlace',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperDisable', 'planning_failed': 'Wait_2', 'control_failed': 'Wait_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'action_topic_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1184 y:274
			OperatableStateMachine.add('MoveToPrePlace',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetAGVPose', 'planning_failed': 'Wait', 'control_failed': 'Wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'agv_pose_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:534 y:724
			OperatableStateMachine.add('MoveToPrePlace_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'Wait_3', 'control_failed': 'Wait_3', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'agv_pose_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:674 y:17
			OperatableStateMachine.add('PartHeightStrToFloat',
										TextToFloatState(),
										transitions={'done': 'AddHeight'},
										autonomy={'done': Autonomy.Off},
										remapping={'text_value': 'part_height', 'float_value': 'part_height_float'})

			# x:1407 y:274
			OperatableStateMachine.add('Wait',
										WaitState(wait_time=5),
										transitions={'done': 'MoveToPrePlace'},
										autonomy={'done': Autonomy.Off})

			# x:1207 y:824
			OperatableStateMachine.add('Wait_2',
										WaitState(wait_time=5),
										transitions={'done': 'MoveToPlace'},
										autonomy={'done': Autonomy.Off})

			# x:557 y:824
			OperatableStateMachine.add('Wait_3',
										WaitState(wait_time=5),
										transitions={'done': 'MoveToPrePlace_2'},
										autonomy={'done': Autonomy.Off})

			# x:757 y:724
			OperatableStateMachine.add('Wait_4',
										WaitState(wait_time=1),
										transitions={'done': 'MoveToPrePlace_2'},
										autonomy={'done': Autonomy.Off})

			# x:899 y:36
			OperatableStateMachine.add('AddHeight',
										AddNumericState(),
										transitions={'done': 'LookupRobotConfig'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'part_height_float', 'value_b': 'part_height_float', 'result': 'part_height_float'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
