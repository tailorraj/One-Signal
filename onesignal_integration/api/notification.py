import frappe

@frappe.whitelist(allow_guest=True)
def get_notification_list():
    try:
        if "user_id" not in frappe.local.form_dict.keys():
            create_response("400","Bad request. User ID parameter is mendatory for this request")
            return
        
        
        notification_list = frappe.get_list("Onesignal Notification Log",{"user_id":frappe.local.form_dict.user_id},["head","message","is_read","type","content_name","content_type","name","creation"])

        if len(notification_list) == 0:
            create_response("200","No notification found!")
            return
        else:
            create_response("200","Notification Fetched",notification_list)
            return

    except Exception as e:
        create_response("417","something went wrong",e)
        return
        
@frappe.whitelist()
def mark_notification_as_read(notification_id):
    try:
        for noti in notification_id:
            notification_doc = frappe.get_doc("Onesignal Notification Log",noti)
            notification_doc.is_read = 1
            res = notification_doc.save(ignore_permissions=1)
        create_response("200","Notification {} mark as read".format(res))
        return

    except Exception as e:
        create_response("417","something went wrong",e)
        return

        


def create_response(status,message,data=None):
    frappe.local.response.http_status_code = status
    frappe.local.response.message = message
    if data:
        frappe.local.response.data = data