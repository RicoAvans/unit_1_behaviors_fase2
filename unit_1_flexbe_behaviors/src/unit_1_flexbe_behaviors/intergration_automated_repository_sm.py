#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.dummy_state import DummyState
from ariac_flexbe_states.end_assignment_state import EndAssignment
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from unit_1_flexbe_behaviors.transport_part_form_bin_to_agv_sm import transport_part_form_bin_to_agvSM
from unit_2_flexbe_behaviors.transport_part_converyor_to_pick_location_sm import Transport_part_converyor_to_pick_locationSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 07 2021
@author: Ricardo Kronenburg en Koen Manschot
'''
class IntergrationautomatedrepositorySM(Behavior):
	'''
	Picks part from conveyor and puts it on the designated bin, and places orders on the AGV and sends the AGV away when done.
	'''


	def __init__(self):
		super(IntergrationautomatedrepositorySM, self).__init__()
		self.name = 'Intergration automated repository'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(Transport_part_converyor_to_pick_locationSM, 'Transport_part_converyor_to_pick_location')
		self.add_behavior(Transport_part_converyor_to_pick_locationSM, 'Transport_part_converyor_to_pick_location_2')
		self.add_behavior(transport_part_form_bin_to_agvSM, 'transport_part_form_bin_to_agv')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1679 y:843, x:652 y:500
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.orders_day_amount = 2
		_state_machine.userdata.orders_done = 0
		_state_machine.userdata.value1 = 1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:43 y:74
			OperatableStateMachine.add('Start',
										StartAssignment(),
										transitions={'continue': 'Transport_part_converyor_to_pick_location'},
										autonomy={'continue': Autonomy.Off})

			# x:1124 y:474
			OperatableStateMachine.add('CheckIfAllOrdersDone',
										EqualState(),
										transitions={'true': 'Transport_part_converyor_to_pick_location_2', 'false': 'Transport_part_converyor_to_pick_location'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'orders_done', 'value_b': 'orders_day_amount'})

			# x:1343 y:767
			OperatableStateMachine.add('Dummy2',
										DummyState(),
										transitions={'done': 'Transport_part_converyor_to_pick_location_2'},
										autonomy={'done': Autonomy.Off})

			# x:621 y:42
			OperatableStateMachine.add('DummyState',
										DummyState(),
										transitions={'done': 'Transport_part_converyor_to_pick_location'},
										autonomy={'done': Autonomy.Off})

			# x:1543 y:774
			OperatableStateMachine.add('End',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})

			# x:270 y:121
			OperatableStateMachine.add('Transport_part_converyor_to_pick_location',
										self.use_behavior(Transport_part_converyor_to_pick_locationSM, 'Transport_part_converyor_to_pick_location'),
										transitions={'finished': 'transport_part_form_bin_to_agv', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:1314 y:621
			OperatableStateMachine.add('Transport_part_converyor_to_pick_location_2',
										self.use_behavior(Transport_part_converyor_to_pick_locationSM, 'Transport_part_converyor_to_pick_location_2'),
										transitions={'finished': 'Dummy2', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:797 y:121
			OperatableStateMachine.add('transport_part_form_bin_to_agv',
										self.use_behavior(transport_part_form_bin_to_agvSM, 'transport_part_form_bin_to_agv'),
										transitions={'finished': 'AddToOrderIndex', 'failed': 'failed', 'no_agv_present': 'DummyState'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'no_agv_present': Autonomy.Inherit})

			# x:1124 y:274
			OperatableStateMachine.add('AddToOrderIndex',
										AddNumericState(),
										transitions={'done': 'CheckIfAllOrdersDone'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'orders_done', 'value_b': 'value1', 'result': 'orders_done'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
