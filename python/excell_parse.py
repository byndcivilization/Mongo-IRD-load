#!/usr/bin/python
from xlrd import cellname
import re
from datetime import datetime

from utils import na_check, split_str_array, get_cell, geocode


def parse(sheet, data):

	# creat ojbece where key = header name and value = columnm number
	labels = sheet.row(0)
	lkey = { str(labels[i]).replace("text:u","").replace("'","").lower(): i for i in range(0, len(labels)) }

	# test by iterating over one sheet
	nrows = sheet.nrows

	for row_index in range(1, nrows):
		#create document for each row
		data.append({})

		### ADD NAMES
		###
		# english names
		a = get_cell(sheet,'MainNameEn',row_index,lkey)
		if a:
			data[-1]['name_en'] = a

		# acronym
		a = get_cell(sheet,'Acronym',row_index,lkey)
		if a:
			data[-1]['acronym'] = a

		# main names
		a = get_cell(sheet,'MainName',row_index,lkey,str_split=True)
		if a:
			data[-1]['main_names'] = a

		# old names
		a = get_cell(sheet,'MainOldNames',row_index,lkey,str_split=True)
		if a:
			data[-1]['old_alias'] = a

		# parent organization
		a = get_cell(sheet,'Organization',row_index,lkey,str_split=True)
		if a:
			data[-1]['parent_org'] = a


		### ADD CONTACT DETAILS
		###
		# website
		a = get_cell(sheet,'Web',row_index,lkey)
		if a:
			data[-1]['website'] = a

		# email
		a = get_cell(sheet,'Email',row_index,lkey)
		if a:
			data[-1]['email_gen'] = a

		# contact established
		a = get_cell(sheet,'ContactEstablished',row_index,lkey)
		if a:
			data[-1]['contacted'] = a

		# contact person
		a = get_cell(sheet,'ContactPerson',row_index,lkey)
		if a:
			data[-1]['contact_person'] = (
				a,
				get_cell(sheet,'EmailContactPerson',row_index,lkey)
			)


		### ADD CHARACTERISTICS
		###
		# international
		a = get_cell(sheet,'International',row_index,lkey)
		if a:
			data[-1]['international'] = a

		# type
		org_type = get_cell(sheet,'Type',row_index,lkey)
		org_type_array = []
		if not org_type:
			pass
		else:
			for char in org_type:
				org_type_array.append(char)
			data[-1]["org_type"] = org_type_array

		# thematic area of foucus
		a = get_cell(sheet,'Subject',row_index,lkey,str_split=True)
		if a:
			data[-1]['subject'] = a

		# structure
		a = get_cell(sheet,'Structure',row_index,lkey)
		if a:
			data[-1]['structure'] = a
		# to create array you would need to differentiate between delimiter and sub list in ()
		# data[-1]["structure"] = split_str_array(structure, '; ',')

		# finances
		a = get_cell(sheet,'Finances',row_index,lkey)
		if a:
			data[-1]['finances'] = a

		# history
		a = get_cell(sheet,'History',row_index,lkey)
		if a:
			data[-1]['history'] = a

		# aim
		a = get_cell(sheet,'Aim',row_index,lkey)
		if a:
			data[-1]['aim'] = a

		# aimURL
		a = get_cell(sheet,'AimURL',row_index,lkey)
		if a:
			data[-1]['aim_URL'] = a

		# IRD definition
		a = get_cell(sheet,'IRDdefinition',row_index,lkey)
		if a:
			data[-1]['IRD_def'] = a

		# IRD definition URL
		a = get_cell(sheet,'IRDdefinitionURL',row_index,lkey)
		if a:
			data[-1]['IRD_def_URL'] = a

		# religious affiliation
		a = get_cell(sheet,'ReligiousAffiliation',row_index,lkey,str_split=True)
		if a:
			data[-1]['religious_affiliation'] = a

		# languages
		a = get_cell(sheet,'Languages',row_index,lkey,str_split=True)
		if a:
			data[-1]['languages'] = a

		# IRD definition
		a = get_cell(sheet,'Staff',row_index,lkey,str_split=True)
		if a:
			data[-1]['staff'] = a

		### ADD ACTIVITIES
		###
		# General activities
		a = get_cell(sheet,'Activities',row_index,lkey)
		if a:
			if a == 'No information':
				data[-1]['general_activities'] =['No information']
			elif a == 'See IRDActivities':
				data[-1]['general_activities'] =['See IRDActivities']
			else:
				# regex to match pattern of <number>. <text>: to create true key values
				activities = re.split('([0-9]{1,}\. [a-zA-Z \'\-!\0-9{1,}+,&]+:)',a)
				activity_array = []
				# activities = re.split('([0-9]{1,}\. [a-zA-Z ]+:)',a)
				activity_name_array = []
				activity_description_array = []
				for activity in activities:
					if activity == "":
						pass
					elif re.match('[0-9]\.',activity):
						activity = re.sub('[0-9]\. ','',activity)
						activity = re.sub(':','',activity)
						activity_name_array.append(activity)
					else:
						activity = activity.strip()
						activity_description_array.append(activity)
				for x in xrange(1,len(activity_name_array)):
					activity_array.append({'activity_name':activity_name_array[x],'activity_description':activity_description_array[x]})
				data[-1]['general_activities'] = activity_array

	
		# IRD activities -- need to apply abbove model to separate acitity name and activity description
		a = get_cell(sheet,'IRDActivities',row_index,lkey)
		if a:
			if a == 'No information':
				data[-1]['IRD_activities'] =['No information']
			else:
				IRD_activities_reg = re.split('[0-9]{1,2}\. ',get_cell(sheet,'IRDALocation',row_index,lkey))
				IRD_activities = re.split('[0-9]{1,2}\. ',a)
				IRD_activities_array = []
				del IRD_activities[0]
				del IRD_activities_reg[0]
				## turn on to look for ragged array match
				# if len(IRD_activities_reg) != len(IRD_activities):
				# 	print name_en
				# 	print IRD_activities_reg
				# 	print IRD_activities
				for x in xrange(1,len(IRD_activities)):
					region = re.split('[;\.]', IRD_activities_reg[x])
					region = [ i.strip() for i in region if i.strip() ]
					IRD_activity_obj = {
						'activity' : IRD_activities[x],
						'region' : region
					}
					IRD_activities_array.append(IRD_activity_obj)
				data[-1]['IRD_activities'] = IRD_activities_array



		# events
		a = get_cell(sheet,'Events',row_index,lkey,str_split=True)
		if a:
			data[-1]['events'] = a


		# publications
		a = get_cell(sheet,'Publications',row_index,lkey,str_split=True)
		if a:
			data[-1]['publications'] = a

		### RELATIONSHIPS
		###
		# IO relationships
		a = get_cell(sheet,'RelationsIO',row_index,lkey,str_split=True)
		if a:
			data[-1]['IO_relations'] = a

		# Other relationships
		a = get_cell(sheet,'RelationsOther',row_index,lkey,str_split=True)
		if a:
			data[-1]['other_relations'] = a

		# geocoding
		addr = {}
		geo = {}
		for i in 'AddressMain Address1 Address2 Address3 Address4 Address5 Address3AndMore'.split(' '):
			try:
				a = get_cell(sheet, i, row_index,lkey)
				#import ipdb; ipdb.set_trace()#
				if a:
					geo = geocode(a)
					geo['address'] = a
					addr[i] = geo
			except KeyError:
				pass
		if addr:
			data[-1]['adresses'] = addr

		### ADD ENTRY STAMP DETAILs
		###
		a = get_cell(sheet,'Entry',row_index,lkey)
		if not a:
			pass
		else:
			entry_value_array = split_str_array(a, ', ')
			entry_date = datetime.strptime(entry_value_array[1], "%d.%m.%Y").date()
			data[-1]["entry"] = {'author' : entry_value_array[0], 'date' : str(entry_date.year)+str(entry_date.month).zfill(2)+str(entry_date.day).zfill(2)}


	return data


if __name__ == '__main__':
	parse(sheet, data)