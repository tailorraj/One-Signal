# Copyright (c) 2023, Akhilam INC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests

class OneSignalSettings(Document):
	pass


def send_push_notification(user_ids,notification,data,type,html_head,html_message):
	settings_doc = frappe.get_doc("One Signal Settings")
	app_id = settings_doc.get_password("app_id")
	api_key = settings_doc.get_password("one_signal_api_key")
	frappe.msgprint(str(notification))
	frappe.msgprint(str(user_ids))
	frappe.msgprint(str(type))
	frappe.msgprint(str(html_head))
	frappe.msgprint(str(html_message))
	frappe.msgprint(str(app_id))
	frappe.msgprint(str(api_key))
	
	# url = "https://onesignal.com/api/v1/notifications"
	# player_ids = frappe.db.get_all('User Device',filters=[["user_id", "in", user_ids]],fields=["player_id"],pluck='player_id')
	# payload = {
	#	 "include_player_ids": player_ids,
	#	 "app_id":app_id,
	#	 "headings":{"en":notification["title"]},
	#	 "contents": {"en": notification["message"]},
	#	 "ios_badgeType": "Increase",
	#	 "ios_badgeCount":1,
	#	 "data": data,
	# }
	# headers = {
	#	 "Accept": "application/json",
	#	 "Authorization": "Basic "+api_key,
	#	 "Content-Type": "application/json"
	# }
	# response = requests.post(url, json=payload, headers=headers)
	create_push_notification_log(user_ids,notification["title"],notification["message"],data,type,html_head,html_message)


def create_push_notification_log(user_ids,head,message,content,icon_type,html_head,html_message):
	if html_message:
		replace_with = f"<img src=\"{frappe.utils.get_url()}"
		html_message = html_message.replace("<img src=\"",replace_with)
	
	notification_log = frappe.get_doc({
		"doctype":"Onesignal Notification Log", 
		"head": head,
		"message":message,
		"html_head":html_head,
		"html_message":html_message,
		"content_name": content["docname"],
		"content_type": content["doctype"],
		"user_mobile_device_id":user_ids,
		"is_read":False,
		"type":icon_type})
	notification_log.insert(ignore_permissions = True)