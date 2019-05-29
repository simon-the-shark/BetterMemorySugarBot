from infusionset_reminder.settings import LANGUAGE_CODE

if LANGUAGE_CODE == "pl":
    # notifications texts
    languages_infusion_successful = ".\n\n Zmień zestaw infuzyjny w {} dni i {} godzin."
    languages_infusion_over = ".\n\n Twój termin zmiany zestawu infuzyjnego minął."
    languages_infusion_unsuccessful_reading = '.\n\nZestaw infuzyjny: nie udało się zczytać danych'
    languages_infusion_unsuccessful_processing = '.\n\n Zestaw infuzyjny: nie udało się przetworzyć danych'
    languages_sensor_successful = "\n\n Zmień sensor CGM w {} dni i {} godzin"
    languages_sensor_over = "\n\n Twój termin zmiany sensora CGM minął."
    languages_sensor_unsuccessful_reading = '\n\nSensor CGM: nie udało się zczytać danych'
    languages_sensor_unsuccessful_processing = '\n\nSensor CGM: nie udało się przetworzyć danych'
    # label tags
    languages_number_of_sender = "NUMER NADAWCY"
    languages_destination_number = "NUMER OBIORCY "
    languages_ifttt_label = "WYWOŁUJ IFTTT (WYSYŁAJ WEBHOOKI)"
    languages_sms_label = "WYSYŁAJ SMSy"
    languages_language_label = "JĘZYK"
    languages_time_label = "GODZINA POWIADOMIENIA. Proszę wprowadzić CZAS UTC"
    # actions
    languages_add_action = "DODAJ"
    languages_added_action = "DODANO"
    languages_change_action = "ZMIEŃ"
    languages_changed_action = "ZMIENIONO"
else:
    # notifications texts
    languages_infusion_successful = ".\n\n Your infusion set should be changed in {} days and {} hours."
    languages_infusion_over = ".\n\n Your infusion set change has already passed"
    languages_infusion_unsuccessful_reading = ".\n\nInfusion set: unsuccessful data reading"
    languages_infusion_unsuccessful_processing = ".\n\n Infusion set: unsuccessful data processing"
    languages_sensor_successful = "\n\n Your CGM sensor should be changed in {} days and {} hours."
    languages_sensor_over = "\n\n Your CGM sensor change has already passed"
    languages_sensor_unsuccessful_reading = '\n\nCGM sensor: unsuccessful data reading'
    languages_sensor_unsuccessful_processing = "\n\nCGM sensor: unsuccessful data processing"
    # label tags
    languages_number_of_sender = "NUMBER OF SENDER"
    languages_destination_number = "DESTINATION NUMBER "
    languages_ifttt_label = "TRIGGER IFTTT (SEND WEBHOOKS)"
    languages_sms_label = "SEND SMS"
    languages_language_label = "LANGUAGE"
    languages_time_label = "NOTIFICATION TIME. Please give UTC TIME"
    # actions
    languages_add_action = "ADD"
    languages_added_action = "ADDED"
    languages_change_action = "CHANGE"
    languages_changed_action = "CHANGED"
