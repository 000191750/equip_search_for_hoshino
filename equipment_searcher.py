import base64
import os
import hoshino
from hoshino import aiorequests, config, util, log

try:
	import ujson as json
except:
	import json
	
logger = log.new_logger('equip_search', hoshino.config.DEBUG)

equip_list = {}
async def get_equip_id(name):
	equip_list.clear()
	equip = await aiorequests.get('https://mahomaho-insight.info/cached/master/equipment_data.json')
	equip_data = await equip.json()
	for i in equip_data:
		if name in equip_data[i]['equipment_name']:
			if i not in equip_list:
				equip_list[i] = {}
			equip_list[i]['id'] = equip_data[i]['equipment_id']
			equip_list[i]['name'] = equip_data[i]['equipment_name']
	if len(equip_list):
		return equip_list
	else:
		return 0

reward_ids = {}
async def get_wave_id(equip_id):
	reward_ids.clear()
	reward = await aiorequests.get('https://mahomaho-insight.info/cached/master/enemy_reward_data.json')
	reward_data = await reward.json()
	wave = await aiorequests.get('https://mahomaho-insight.info/cached/master/wave_group_data.json')
	wave_data = await wave.json()
	num = 1
	for i in reward_data:
		for j in reward_data[i]:
			if reward_data[i][j] == equip_id:
				reward_id = reward_data[i]['drop_reward_id']
				if reward_id not in reward_ids:
					reward_ids[reward_id] = {}
				#id = reward_data[i]['drop_reward_id']
				#reward_ids[reward_id]['id'] = id
				for n in range(6):
					r_id = f'reward_id_{n}'
					if j == r_id:
						odds = f'odds_{n}'
				reward_ids[reward_id]['odds'] = reward_data[i][odds]
				num = num + 1
	a = 1
	for r in reward_ids:
		for x in wave_data:
			for y in wave_data[x]:
				if wave_data[x][y] == r:
					wave_id = f'wave_id_{a}'
					reward_ids[r][wave_id] = wave_data[x]['wave_group_id']
					a = a + 1
	return reward_ids

map_list = {}			
async def get_map_name(wave_id):
	quest = await aiorequests.get('https://mahomaho-insight.info/cached/master/quest_data.json')
	quest_data = await quest.json()
	num = 1
	for quest_id in quest_data:
		for wave in quest_data[quest_id]:
			if quest_data[quest_id][wave] == wave_id:
				if quest_data[quest_id]['daily_limit'] == 0:
					map_list['name'] = quest_data[quest_id]['quest_name']
					num = num + 1
				elif quest_data[quest_id]['daily_limit'] == 3:
					quest_name = quest_data[quest_id]['quest_name'] + '(H)'
					map_list['name'] = quest_name
	return map_list