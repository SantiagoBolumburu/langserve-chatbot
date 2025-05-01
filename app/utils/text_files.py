def load_text_file(file_path):
  try:
    with open(file_path, 'r') as file:
      content = file.read()
    return content
  except FileNotFoundError:
    print(f"Error: File not found at '{file_path}'")
    return None
  except Exception as e:
    print(f"An error occurred: {e}")
    return None