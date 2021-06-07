#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.text_to_float_state import TextToFloatState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 25 2021
@author: docent
'''
class pick_part_from_binSM(Behavior):
	'''
	pick's a specific part form a it's bin
	'''


	def __init__(self):
		super(pick_part_from_binSM, self).__init__()
		self.name = 'pick_part_from_bin'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		compute_joint_name = ['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
		part_list = ['gear_part','piston_rod_part','gasket_part']
		joint_names = ['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
		# x:83 y:840, x:683 y:440
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part', 'which_robot', 'action_topic_namespace', 'bin'], output_keys=['gripper_service', 'part_height_float'])
		_state_machine.userdata.part = ''
		_state_machine.userdata.robot_namespace = ''
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = ''
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.robot_config = ''
		_state_machine.userdata.locations = []
		_state_machine.userdata.bin = ''
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.pose = []
		_state_machine.userdata.zero = 0
		_state_machine.userdata.ref_frame_camera = 'world'
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.part_height_str = ''
		_state_machine.userdata.part_rotation = 0
		_state_machine.userdata.gripper_service = ''
		_state_machine.userdata.which_robot = ''
		_state_machine.userdata.robot1 = 'robot1'
		_state_machine.userdata.robot2 = 'robot2'
		_state_machine.userdata.robot_wait_pose = ''
		_state_machine.userdata.action_topic_namespace_wait = ''
		_state_machine.userdata.part_height_float = 0.0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:229 y:74
			OperatableStateMachine.add('LookupBinCameraTopic',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_configR1', index_title='bins', column_title='camera_topic'),
										transitions={'found': 'LookupBinCameraFrame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_topic'})

			# x:1379 y:724
			OperatableStateMachine.add('ComputePick',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'MoveToPick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'part_height_float', 'rotation': 'part_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1272 y:374
			OperatableStateMachine.add('DetectPart',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'MoveIdleRobotToWait', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame_camera', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:624 y:74
			OperatableStateMachine.add('EqualR1',
										EqualState(),
										transitions={'true': 'LookUpR1Config', 'false': 'EqualR2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'which_robot', 'value_b': 'robot1'})

			# x:624 y:174
			OperatableStateMachine.add('EqualR2',
										EqualState(),
										transitions={'true': 'LookUpR2Config', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'which_robot', 'value_b': 'robot2'})

			# x:835 y:74
			OperatableStateMachine.add('LookUpR1Config',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_configR1', index_title='bins', column_title='robot_pregrasp_pose'),
										transitions={'found': 'LookupGripperServiceR1', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_config'})

			# x:835 y:174
			OperatableStateMachine.add('LookUpR2Config',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_configR2', index_title='bins', column_title='robot_pregrasp_pose'),
										transitions={'found': 'LookupGripperServiceR2', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_config'})

			# x:1405 y:174
			OperatableStateMachine.add('LookupActionTopicNameSpaceR1',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_configR1', index_title='bins', column_title='action_topic_namespace'),
										transitions={'found': 'LookupPartHeight', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'action_topic_namespace_wait'})

			# x:1405 y:74
			OperatableStateMachine.add('LookupActionTopicNameSpaceR2',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_configR2', index_title='bins', column_title='action_topic_namespace'),
										transitions={'found': 'LookupPartHeight', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'action_topic_namespace_wait'})

			# x:427 y:74
			OperatableStateMachine.add('LookupBinCameraFrame',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_configR1', index_title='bins', column_title='camera_frame'),
										transitions={'found': 'EqualR1', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_frame'})

			# x:1026 y:74
			OperatableStateMachine.add('LookupGripperServiceR1',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_configR1', index_title='bins', column_title='gripper_service'),
										transitions={'found': 'LookupWaitPoseR2', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'gripper_service'})

			# x:1026 y:174
			OperatableStateMachine.add('LookupGripperServiceR2',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_configR2', index_title='bins', column_title='gripper_service'),
										transitions={'found': 'LookupWaitPoseR1', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'gripper_service'})

			# x:1659 y:215
			OperatableStateMachine.add('LookupPartHeight',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='part_heights', index_title='parts', column_title='part_height'),
										transitions={'found': 'PartHeightToFLoat', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'part', 'column_value': 'part_height_str'})

			# x:1235 y:174
			OperatableStateMachine.add('LookupWaitPoseR1',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_configR1', index_title='bins', column_title='robot_wait_pose'),
										transitions={'found': 'LookupActionTopicNameSpaceR1', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_wait_pose'})

			# x:1235 y:74
			OperatableStateMachine.add('LookupWaitPoseR2',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_configR2', index_title='bins', column_title='robot_wait_pose'),
										transitions={'found': 'LookupActionTopicNameSpaceR2', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_wait_pose'})

			# x:1384 y:467
			OperatableStateMachine.add('MoveIdleRobotToWait',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'MoveToPreGrasp', 'planning_failed': 'Wait_2', 'control_failed': 'Wait_2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_wait_pose', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace_wait', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1171 y:724
			OperatableStateMachine.add('MoveToPick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'ActivateGripper', 'planning_failed': 'Wait1', 'control_failed': 'Wait1'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'action_topic_namespace', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1384 y:624
			OperatableStateMachine.add('MoveToPreGrasp',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputePick', 'planning_failed': 'Wait', 'control_failed': 'Wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:584 y:724
			OperatableStateMachine.add('MoveToPreGrasp_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'Wait2', 'control_failed': 'Wait2', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_config', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1468 y:273
			OperatableStateMachine.add('PartHeightToFLoat',
										TextToFloatState(),
										transitions={'done': 'DetectPart'},
										autonomy={'done': Autonomy.Off},
										remapping={'text_value': 'part_height_str', 'float_value': 'part_height_float'})

			# x:757 y:724
			OperatableStateMachine.add('WachtEven',
										WaitState(wait_time=1),
										transitions={'done': 'MoveToPreGrasp_2'},
										autonomy={'done': Autonomy.Off})

			# x:1557 y:624
			OperatableStateMachine.add('Wait',
										WaitState(wait_time=5),
										transitions={'done': 'MoveToPreGrasp'},
										autonomy={'done': Autonomy.Off})

			# x:1207 y:824
			OperatableStateMachine.add('Wait1',
										WaitState(wait_time=5),
										transitions={'done': 'MoveToPick'},
										autonomy={'done': Autonomy.Off})

			# x:607 y:824
			OperatableStateMachine.add('Wait2',
										WaitState(wait_time=5),
										transitions={'done': 'MoveToPreGrasp_2'},
										autonomy={'done': Autonomy.Off})

			# x:1557 y:474
			OperatableStateMachine.add('Wait_2',
										WaitState(wait_time=5),
										transitions={'done': 'MoveIdleRobotToWait'},
										autonomy={'done': Autonomy.Off})

			# x:924 y:724
			OperatableStateMachine.add('ActivateGripper',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'WachtEven', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper_service'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	def pose(self, x, y):
		p = pose()
		p.position.x = x
		p.position.y = y
		return p

	def posestamped(self, x, y, z, frame):
		p = PoseStamped()
		p.header.frame_id = frame
		p.pose.position.x = x
		p.pose.position.y = y
		p.pose.position.z = z
		return p
	# [/MANUAL_FUNC]
