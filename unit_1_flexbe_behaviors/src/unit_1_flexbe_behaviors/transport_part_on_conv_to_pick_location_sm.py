#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from flexbe_states.subscriber_state import SubscriberState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 07 2021
@author: Ricardo Kronenburg
'''
class transport_part_on_conv_to_pick_locationSM(Behavior):
	'''
	Transports a part on the conveyor to the pick location.
	'''


	def __init__(self):
		super(transport_part_on_conv_to_pick_locationSM, self).__init__()
		self.name = 'transport_part_on_conv_to_pick_location'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:983 y:140, x:383 y:340
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.start_conveyorbelt = 99
		_state_machine.userdata.stop_conveyorbelt = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:73 y:74
			OperatableStateMachine.add('Start_conveyor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'wait_for_part', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'start_conveyorbelt'})

			# x:723 y:74
			OperatableStateMachine.add('Stop_conveyor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'finished', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'stop_conveyorbelt'})

			# x:451 y:74
			OperatableStateMachine.add('wait_for_part',
										SubscriberState(topic="/ariac/break_beam_1_change", blocking=True, clear=True),
										transitions={'received': 'Stop_conveyor', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
