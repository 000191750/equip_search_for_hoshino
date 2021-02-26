import requests
import json
import os

path = './img/'

async def get_equip_img():
	resp = requests.get('https://mahomaho-insight.info/cached/master/equipment_data.json')
	equipment_data = resp.json()
	print(f'有{len(equipment_data)}个装备图，开始下载')

	if not os.path.exists(path):
		os.mkdir(path)
		
	i = 0
	for i in equipment_data:
		equip_id = equipment_data[i]['equipment_id']
		equip_img = path + f'{equip_id}.png'
		url = f'https://mahomaho-insight-cos-1302341499.cos.ap-shanghai.myqcloud.com/image/equipments/icon_equipment_{equip_id}.png'
		print(f'正在下载{equip_img}')
		# with open('equip_id.json', "w", encoding = 'utf8') as f:
			# json.dump(equipment_data,f,ensure_ascii=False, indent=2
		if not os.path.exists(equip_img):
			r = requests.get(url)
			print(r)
			with open(equip_img,'wb') as f:
				f.write(r.content)
			print("图片下载成功")
		else:
			print("图片已经存在.")
			
