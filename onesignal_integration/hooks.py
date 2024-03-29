from . import __version__ as app_version

app_name = "onesignal_integration"
app_title = "Onesignal Integration"
app_publisher = "Akhilam INC"
app_description = "One signal push notification integration"
app_email = "raaj@akhilaminc.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/onesignal_integration/css/onesignal_integration.css"
# app_include_js = "/assets/onesignal_integration/js/onesignal_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/onesignal_integration/css/onesignal_integration.css"
# web_include_js = "/assets/onesignal_integration/js/onesignal_integration.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "onesignal_integration/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "onesignal_integration.utils.jinja_methods",
#	"filters": "onesignal_integration.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "onesignal_integration.install.before_install"
# after_install = "onesignal_integration.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "onesignal_integration.uninstall.before_uninstall"
# after_uninstall = "onesignal_integration.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "onesignal_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }


doc_events = {
     "*": {
            "validate"                      : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
            "onload"                        : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
            "before_insert"                 : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
            "after_insert"                  : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
            "before_naming"                 : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
            "before_change"                 : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
            "before_update_after_submit"    : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
            "before_validate"               : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
            "before_save"                   : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
            "autoname"                      : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
		    "on_update"                     : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
		    "on_cancel"                     : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
		    "on_trash"                      : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
		    "on_submit"                     : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
		    "on_update_after_submit"        : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
            "on_change"                     : ["onesignal_integration.onesignal_integration.doctype.one_signal_notification.one_signal_notification.run_one_signal_notifications"],
	},


}
# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"onesignal_integration.tasks.all"
#	],
#	"daily": [
#		"onesignal_integration.tasks.daily"
#	],
#	"hourly": [
#		"onesignal_integration.tasks.hourly"
#	],
#	"weekly": [
#		"onesignal_integration.tasks.weekly"
#	],
#	"monthly": [
#		"onesignal_integration.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "onesignal_integration.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "onesignal_integration.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "onesignal_integration.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"onesignal_integration.auth.validate"
# ]
