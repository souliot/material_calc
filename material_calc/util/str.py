def strip_by_line(data: str):
  res = ""
  lines = data.split("\n")
  for line in lines:
    new_line = line.strip()
    res += new_line+"\n"

  return res
