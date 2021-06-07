#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.get_agv_status_state import GetAgvStatusState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.notify_shipment_ready_state import NotifyShipmentReadyState
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_logistics_flexbe_states.get_products_from_shipment_state import GetProductsFromShipmentState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
from ariac_support_flexbe_states.substract_numeric_state import SubstractNumericState
from unit_1_flexbe_behaviors.pick_part_from_bin_sm import pick_part_from_binSM
from unit_1_flexbe_behaviors.place_part_on_agv_sm import place_part_on_agvSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 02 2021
@author: Ricardo Kronenburg
'''
class transport_part_form_bin_to_agvSM(Behavior):
	'''
	transports a part from a bin to an agv, given an order-id
	'''


	def __init__(self):
		super(transport_part_form_bin_to_agvSM, self).__init__()
		self.name = 'transport_part_form_bin_to_agv'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(pick_part_from_binSM, 'pick_part_from_bin')
		self.add_behavior(place_part_on_agvSM, 'place_part_on_agv')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1733 y:870, x:733 y:440, x:1440 y:836
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'no_agv_present'])
		_state_machine.userdata.action_topic_namespace = ''
		_state_machine.userdata.part = ''
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.index_zero = 0
		_state_machine.userdata.agv_pose_config = ''
		_state_machine.userdata.pose_order = []
		_state_machine.userdata.ProductIterator = 0
		_state_machine.userdata.value_1 = 1
		_state_machine.userdata.agv_ready = 'ready_to_deliver'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:73 y:74
			OperatableStateMachine.add('GetOrderState',
										GetOrderState(),
										transitions={'continue': 'GetProductsFromShipment'},
										autonomy={'continue': Autonomy.Off},
										remapping={'order_id': 'order_id', 'shipments': 'shipments', 'number_of_shipments': 'number_of_shipments'})

			# x:293 y:74
			OperatableStateMachine.add('GetAgvStatus',
										GetAgvStatusState(),
										transitions={'continue': 'IsAgvReady', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'agv_id': 'agv_id', 'agv_state': 'agv_state'})

			# x:1124 y:74
			OperatableStateMachine.add('GetBinFromLocations',
										GetItemFromListState(),
										transitions={'done': 'GetActionTopicNamespace', 'invalid_index': 'failed'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'locations', 'index': 'index_zero', 'item': 'bin'})

			# x:722 y:74
			OperatableStateMachine.add('GetPartFromProductsState',
										GetPartFromProductsState(),
										transitions={'continue': 'GetPartLocations', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'ProductIterator', 'type': 'part', 'pose': 'pose_order'})

			# x:923 y:74
			OperatableStateMachine.add('GetPartLocations',
										GetMaterialLocationsState(),
										transitions={'continue': 'GetBinFromLocations'},
										autonomy={'continue': Autonomy.Off},
										remapping={'part': 'part', 'material_locations': 'locations'})

			# x:214 y:174
			OperatableStateMachine.add('GetProductsFromShipment',
										GetProductsFromShipmentState(),
										transitions={'continue': 'GetAgvStatus', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'shipments': 'shipments', 'index': 'index_zero', 'shipment_type': 'shipment_type', 'agv_id': 'agv_id', 'products': 'products', 'number_of_products': 'number_of_products'})

			# x:1535 y:74
			OperatableStateMachine.add('GetWichRobot',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='pose_config', index_title='robot', column_title='which_robot'),
										transitions={'found': 'pick_part_from_bin', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'agv_id', 'column_value': 'which_robot'})

			# x:524 y:74
			OperatableStateMachine.add('IsAgvReady',
										EqualState(),
										transitions={'true': 'GetPartFromProductsState', 'false': 'no_agv_present'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_state', 'value_b': 'agv_ready'})

			# x:1524 y:574
			OperatableStateMachine.add('IterReset',
										SubstractNumericState(),
										transitions={'done': 'NotifyShipmentReady'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'ProductIterator', 'result': 'ProductIterator'})

			# x:1526 y:667
			OperatableStateMachine.add('NotifyShipmentReady',
										NotifyShipmentReadyState(),
										transitions={'continue': 'finished', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'agv_id': 'agv_id', 'shipment_type': 'shipment_type', 'success': 'success', 'message': 'message'})

			# x:1524 y:474
			OperatableStateMachine.add('ProdIterEqNumProd',
										EqualState(),
										transitions={'true': 'IterReset', 'false': 'GetPartFromProductsState'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'number_of_products'})

			# x:1524 y:374
			OperatableStateMachine.add('ProductIteratorPlus1',
										AddNumericState(),
										transitions={'done': 'ProdIterEqNumProd'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'ProductIterator', 'value_b': 'value_1', 'result': 'ProductIterator'})

			# x:1520 y:171
			OperatableStateMachine.add('pick_part_from_bin',
										self.use_behavior(pick_part_from_binSM, 'pick_part_from_bin'),
										transitions={'finished': 'place_part_on_agv', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part': 'part', 'which_robot': 'which_robot', 'action_topic_namespace': 'action_topic_namespace', 'bin': 'bin', 'gripper_service': 'gripper_service', 'part_height_float': 'part_height_float'})

			# x:1520 y:271
			OperatableStateMachine.add('place_part_on_agv',
										self.use_behavior(place_part_on_agvSM, 'place_part_on_agv'),
										transitions={'finished': 'ProductIteratorPlus1', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'action_topic_namespace': 'action_topic_namespace', 'agv_id': 'agv_id', 'pose_order': 'pose_order', 'gripper_service': 'gripper_service', 'part': 'part'})

			# x:1322 y:74
			OperatableStateMachine.add('GetActionTopicNamespace',
										LookupFromTableState(parameter_name='/ariac_tables_unit1', table_name='pose_config', index_title='robot', column_title='action_topic_namespace'),
										transitions={'found': 'GetWichRobot', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'agv_id', 'column_value': 'action_topic_namespace'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
