# Copyright (c) 2023, Akhilam INC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate,parse_val,add_to_date
from six import string_types
import json
from frappe import _
from onesignal_integration.onesignal_integration.doctype.one_signal_settings.one_signal_settings import send_push_notification

class OneSignalNotification(Document):
	def get_alert_documents_for_today(self):
		'''get list of documents that will be triggered today'''
		docs = []

		diff_days = self.days_in_advance
		if self.event=="Days After":
			diff_days = -diff_days

		reference_date = add_to_date(nowdate(), days=diff_days)
		reference_date_start = reference_date + ' 00:00:00.000000'
		reference_date_end = reference_date + ' 23:59:59.000000'

		doc_list = frappe.get_all(self.document_type,
			fields='name',
			filters=[
				{ self.date_changed: ('>=', reference_date_start) },
				{ self.date_changed: ('<=', reference_date_end) }
			])

		for d in doc_list:
			doc = frappe.get_doc(self.document_type, d.name)

			if self.condition and not frappe.safe_eval(self.condition, None, get_context(doc)):
				continue

			docs.append(doc)
		return docs

	def validate(self):
		self.check_field_exist_in_doctype()
		self.validate_condition()	


	def check_field_exist_in_doctype(self):
		if not self.receiver_field:
			frappe.throw("Please Set Receiver Field!")

	def validate_condition(self):
		temp_doc = frappe.new_doc(self.document_type)
		if self.condition:
			try:
				frappe.safe_eval(self.condition, None, get_context(temp_doc))
			except Exception:
				frappe.throw(_("The Condition '{0}' is invalid").format(self.condition))

	def send(self, doc):		
		context = get_context(doc)		
		context = {"doc": doc, "alert": self, "comments": None}
		if doc.get("_comments"):
			context["comments"] = json.loads(doc.get("_comments"))
		self.send_one_signal_notification(doc, context)

	def send_one_signal_notification(self, doc, context):		
		
		message= frappe.render_template(self.message, context)
		# frappe.msgprint(str(doc.get(context['alert'].receiver_field)))
		# frappe.msgprint(str(self.party_type))
		device_id = frappe.db.get_value("User Mobile Device",{"party":doc.get(context['alert'].receiver_field),"party_type":self.party_type},"device_id")
		notification = {"title" : context['alert'].one_signal_title, "message":message}
		data = {
			"doctype":doc.doctype,
			"docname":doc.name
		}
		
		res = send_push_notification(device_id, notification, data, self.type,self.html_head,self.html_message)
	
@frappe.whitelist()
def run_one_signal_notifications(doc, method):
	
	'''Run notifications for this method'''
	if frappe.flags.in_import or frappe.flags.in_patch or frappe.flags.in_install:
		return

	if doc.flags.one_signal_notifications_executed==None:
		doc.flags.one_signal_notifications_executed = []

	if doc.flags.one_signal_notifications == None:
		alerts = frappe.cache().hget('one_signal_notifications', doc.doctype)
		if alerts==None:
			alerts = frappe.get_all('One Signal Notification', fields=['name', 'event'],filters={'enabled': 1, 'document_type': doc.doctype})
		doc.flags.one_signal_notifications = alerts

	if not doc.flags.one_signal_notifications:
		return

	def _evaluate_alert(alert):
		if not alert.name in doc.flags.one_signal_notifications_executed:
			evaluate_alert(doc, alert.name, alert.event)
			doc.flags.one_signal_notifications_executed.append(alert.name)

	event_map = {
		"on_update": "Save",
		"after_insert": "New",
		"on_submit": "Submit",
		"on_cancel": "Cancel"
	}

	if not doc.flags.in_insert:
		
		event_map['validate'] = 'Value Change'
		event_map['before_change'] = 'Value Change'
		event_map['before_update_after_submit'] = 'Value Change'
	
	for alert in doc.flags.one_signal_notifications:
		event = event_map.get(method, None)
		if event and alert.event == event:
			_evaluate_alert(alert)
		elif alert.event=='Method' and method == alert.method:
			_evaluate_alert(alert)

def evaluate_alert(doc, alert, event):	
	try:		
		if isinstance(alert, string_types):			
			alert = frappe.get_doc("One Signal Notification", alert)
		context = get_context(doc)
		if alert.condition:			
			if not frappe.safe_eval(alert.condition, None, context):
				
				return
	

		if event=="Value Change" and not doc.is_new():
			try:
				db_value = frappe.db.get_value(doc.doctype, doc.name, alert.value_changed)
			except Exception as e:
				if frappe.db.is_missing_column(e):
					alert.db_set('enabled', 0)
					frappe.log_error('Notification {0} has been disabled due to missing field'.format(alert.name))
					return
				else:
					raise
			db_value = parse_val(db_value)
			if (doc.get(alert.value_changed) == db_value) or (not db_value and not doc.get(alert.value_changed)):
			
				return # value not changed
			

		if event != "Value Change" and not doc.is_new():
			doc = frappe.get_doc(doc.doctype, doc.name)
		alert.send(doc)
	
	except Exception as e:
		error_log = frappe.log_error(message=frappe.get_traceback(), title=str(e))
		frappe.throw(_("Error in Notification: {}".format(
			frappe.utils.get_link_to_form('Error Log', error_log.name))))


def get_context(doc):
	return {"doc": doc, "nowdate": nowdate, "frappe.utils": frappe.utils}


def trigger_daily_alerts():
	trigger_notifications(None, "daily")


def trigger_notifications(doc, method=None):
	if frappe.flags.in_import or frappe.flags.in_patch:
		# don't send notifications while syncing or patching
		return

	if method == "daily":
		doc_list = frappe.get_all('One Signal Notification',
			filters={
				'event': ('in', ('Days Before', 'Days After')),
				'enabled': 1
			})
		for d in doc_list:
			alert = frappe.get_doc("One Signal Notification", d.name)

			for doc in alert.get_alert_documents_for_today():
				evaluate_alert(doc, alert, alert.event)
				frappe.db.commit()

