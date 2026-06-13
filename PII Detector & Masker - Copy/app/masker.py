def mask_value(value, pii_type):
    if pii_type == "EMAIL":
        user, domain = value.split("@")
        return user[:1] + "***@" + domain
    if pii_type == "PHONE":
        return "******" + value[-4:]
    return value
