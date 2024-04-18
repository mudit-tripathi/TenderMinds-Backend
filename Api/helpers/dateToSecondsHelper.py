from datetime import datetime, timezone

def date_string_to_timestamp(date_string, format_string="%d-%b-%Y %I:%M %p"):
    # Convert the date string to a timezone-aware datetime object assuming UTC
    date_object = datetime.strptime(date_string, format_string)
    date_object = date_object.replace(tzinfo=timezone.utc)
    # Convert the datetime object to a UNIX timestamp (seconds since epoch)
    timestamp = int(date_object.timestamp())
    return timestamp