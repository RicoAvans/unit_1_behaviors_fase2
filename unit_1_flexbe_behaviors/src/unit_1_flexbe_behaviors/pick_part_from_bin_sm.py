#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.end_assignment_state import EndAssignment
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
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
		# x:83 y:840, x:733 y:390
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['robot_namespace', 'part'])
		_state_machine.userdata.part = 'gasket_part'
		_state_machine.userdata.robot_namespace = ''
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic_namespace = '/ariac/arm1'
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

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:43 y:74
			OperatableStateMachine.add('Start',
										StartAssignment(),
										transitions={'continue': 'GetPartLocation'},
										autonomy={'continue': Autonomy.Off})

			# x:243 y:824
			OperatableStateMachine.add('Finish',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})

			# x:424 y:74
			OperatableStateMachine.add('GetBinFromLocations',
										GetItemFromListState(),
										transitions={'done': 'LookupBinCameraTopic', 'invalid_index': 'failed'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'locations', 'index': 'zero', 'item': 'bin'})

			# x:223 y:74
			OperatableStateMachine.add('GetPartLocation',
										GetMaterialLocationsState(),
										transitions={'continue': 'GetBinFromLocations'},
										autonomy={'continue': Autonomy.Off},
										remapping={'part': 'part', 'material_locations': 'locations'})

			# x:827 y:74
			OperatableStateMachine.add('LookupBinCameraFrame',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_config', index_title='bins', column_title='camera_frame'),
										transitions={'found': 'LookupBinPreGrasp', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_frame'})

			# x:629 y:74
			OperatableStateMachine.add('LookupBinCameraTopic',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_config', index_title='bins', column_title='camera_topic'),
										transitions={'found': 'LookupBinCameraFrame', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'camera_topic'})

			# x:1035 y:74
			OperatableStateMachine.add('LookupBinPreGrasp',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='bin_config', index_title='bins', column_title='robot1_config'),
										transitions={'found': 'DetectPart', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'bin', 'column_value': 'robot_config'})

			# x:1234 y:167
			OperatableStateMachine.add('MoveToPreGrasp',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Finish', 'planning_failed': 'Wait', 'control_failed': 'Wait', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1457 y:174
			OperatableStateMachine.add('Wait',
										WaitState(wait_time=5),
										transitions={'done': 'MoveToPreGrasp'},
										autonomy={'done': Autonomy.Off})

			# x:1222 y:74
			OperatableStateMachine.add('DetectPart',
										DetectPartCameraAriacState(time_out=0.5),
										transitions={'continue': 'MoveToPreGrasp', 'failed': 'failed', 'not_found': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame_camera', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
