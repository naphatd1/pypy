import datetime
from locale import setlocale, LC_ALL

def anonymize_text(text, prefix_len=3, suffix_len=1, asterisk_len=5):
    if not isinstance(text, str):
        raise TypeError("Input text must be a string")
    if prefix_len < 0 or suffix_len < 0 or asterisk_len < 0:
        raise ValueError("Length parameters must be non-negative")
    
    total_length = len(text)
    anonymized_part = "*" * asterisk_len
    if total_length <= prefix_len + suffix_len:
        return anonymized_part  # Handle very short strings

    anonymized_part = text[:prefix_len] + anonymized_part + text[-suffix_len:]
    return anonymized_part

def get_thai_date_string(date=None):
  """
  This function formats a date object (defaults to today) 
  in Thai locale format with Buddhist Era (BE) year.

  Args:
      date (datetime.date, optional): Date object to format. Defaults to None (today's date).

  Returns:
      str: Formatted date string in Thai with BE year.
  """

  # Set locale to Thai
#   setlocale(LC_ALL, 'th_TH.UTF-8')

  # Get the date (use provided date or today)
  if date is None:
    date = datetime.date.today()

  # Calculate Buddhist Era (BE) year
  be_year = date.year + 543

  # Format the date with locale-specific format codes and custom year format
  formatted_date = date.strftime('%-d %B %Y'.replace("%Y", str(be_year)))

  return formatted_date

def prepend_date(filename):
  """Prepends the current date and time in ISO8601 format with timezone 
  information (without microseconds) to the filename.

  Args:
      filename: The original filename (string).

  Returns:
      A string with the ISO8601 formatted date and time prepended to the filename.
  """
  now = datetime.datetime.now()
  formatted_date = now.astimezone().strftime("%Y%m%dT%H%M%S")  # Include timezone offset

  # Consider adding a separator between timestamp and filename (e.g., "_")
  return f"{formatted_date}_{filename}"
