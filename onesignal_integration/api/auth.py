import frappe

@frappe.whitelist()
def logout(user):
    try:
        user = frappe.get_doc("User",user)
        user.api_key = None
        user.api_secret = None
        user.save(ignore_permissions = True)
        mobile_device = frappe.db.get_value("User Mobile Device",{"user":user.name},"name")
        if mobile_device:
            frappe.db.set_value("User Mobile Device",mobile_device,"mobile_device_id","")
        create_response("200","Successfully Logged Out")
    except Exception as e:
        create_response("417","something went wrong",e)
        return

def create_response(status,message,data=None):
    frappe.local.response.http_status_code = status
    frappe.local.response.message = message
    if data:
        frappe.local.response.data = data



