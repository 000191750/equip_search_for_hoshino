import os
import base64
from hoshino import Service, R, priv
from hoshino.typing import *
from hoshino.util import FreqLimiter, concat_pic, pic2b64, silence

from PIL import Image, ImageDraw, ImageFont

try:
	import ujson as json
except:
	import json
	
from . import equipment_searcher
from . import spider

sv_help = '''
[装备查询] 搜索装备掉落
[下载装备图片] 下载装备的图片【请自行修改下载文件夹（需要一定编程知识）】
'''.strip()
sv = Service('equip_search', help_=sv_help, bundle='pcr查询')

@sv.on_prefix('下载装备图片')
async def equip_download(bot, ev: CQEvent):
	await spider.get_equip_img()
	await bot.finish(ev,'正在下载装备图片')

equip_list = {}
item_list = {}
@sv.on_prefix('装备查询')
async def equip_info(bot, ev: CQEvent):
	if ev.group_id:
		msg = 
	equip_name = ev.message.extract_plain_text()
	msg = ''
	if equip_name:
		equip_list = await equipment_searcher.get_equip_id(equip_name)
		if equip_list == 0:
			msg = f'未搜索到{equip_name}'
		else:
			m = 0
			for i in equip_list:
				if equip_list[i]['id'] < 110000:
					m = m + 1
			at = str(MessageSegment.at(ev.user_id))
			if m < 6 :
				msg = f'{at}找到以下{m}个装备，请选择\n'
			else:
				msg = f'{at}找到以下{m}个装备，数量过多仅显示前5个\n'
			n = 1
			for i in equip_list:
				id = equip_list[i]['id']
				name = equip_list[i]['name']
				if id < 110000:
					img = R.img(f'{id}.png')
					msg = msg + f'{n}. {img.cqcode} {name}\n'
					item_list[f'name_{n}'] = name
					n = n + 1
					if n == 6:
						break
	else:
		msg = '请输入装备查询+装备名进行查询'
	await bot.finish(ev, msg)

#map_list = {}
@sv.on_prefix('选择')
async def equip_select(bot, ev: CQEvent):
	msg = ''
	equip_selection = ev.message.extract_plain_text()
	if (equip_selection) and (equip_selection.isdigit() and int(equip_selection) <= len(item_list)):
		if item_list:
			name = item_list[f'name_{equip_selection}']
			equip_list = await equipment_searcher.get_equip_id(name)
			for i in equip_list:
				equip_id = equip_list[i]['id']
				if equip_id >= 110000:
					wave_list = await equipment_searcher.get_wave_id(equip_id)
					#sv.logger.info(map_list)
					num = 1
					for reward_id in wave_list:
						for wave_id in wave_list[reward_id]:
							if wave_id != 'odds':
								map_list = await equipment_searcher.get_map_name(wave_list[reward_id][wave_id])
								odds = wave_list[reward_id]['odds']
								map_name = map_list['name']
								msg = msg + f'{num}.{map_name}：{odds}%\n'
								num = num + 1
				else:
					img = R.img(f'{equip_id}.png')
					msg = f'{name}\n{img.cqcode}\n在以下地图可以刷取\n'
		# else:
		# 	msg = '请先查询装备'
	else:
		#msg = '请输入正确的编号。'
		item_list.clear()
	await bot.finish(ev, msg)