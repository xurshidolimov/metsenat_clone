from telegram.tasks import send_message_to_telegram


def add_student(instance):
    send_message_to_telegram.delay(
       f"Talaba qo'shildi.\n "
       f"F. I. SH: {instance.full_name}\n"
       f"Telefon  raqami: +{instance.phone_number}\n"
       f"Unversitet: {instance.university_name}\n"
       f"Talabalik turi: {instance.degree_type}\n"
       f"Kontrakt miqdori: {instance.payment_amount}"
    )


def edit_student(instance):
    send_message_to_telegram.delay(
        f"Talaba tahrirlandi. \n"
        f"F. I. SH: {instance.full_name}\n"
        f"Telefon  raqami: +{instance.phone_number}\n"
        f"Unversitet: {instance.university_name}\n"
        f"Talabalik turi: {instance.degree_type}\n"
        f"Kontrakt miqdori: {instance.payment_amount}\n"
        f"Ajratilgan summa: {instance.amount_spent}"
    )


def add_sponsor(instance):
    send_message_to_telegram.delay(
        f"Homiy qo'shildi. \n"
        f"F. I. SH: {instance.full_name}\n"
        f"Telefon  raqami: +{instance.phone_number}\n"
        f"Homiy turi: {instance.sponsor_type}\n"
        f"Tashkilot nomi: {instance.organization_name}\n"
        f"Holati: {instance.status}\n"
        f"To'lov turi: {instance.payment_type}\n"
        f"Homiylik summasi: {instance.payment_amount}"
    )


def edit_sponsor(instance):
    send_message_to_telegram.delay(
        f"Homiy tahrirlandi.\n "
        f"F. I. SH: {instance.full_name}\n"
        f"Telefon  raqami: +{instance.phone_number}\n"
        f"Homiy turi: {instance.sponsor_type}\n"
        f"Tashkilot nomi: {instance.organization_name}\n"
        f"Holati: {instance.status}\n"
        f"To'lov turi: {instance.payment_type}\n"
        f"Homiylik summasi: {instance.payment_amount}\n"
        f"Sarflangan summa: {instance.amount_spent}"
    )

