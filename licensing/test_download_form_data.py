import json


text = "------WebKitFormBoundaryJKNdq3lljBUDGFOO\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\niroyzis@gmail.com\r\n------WebKitFormBoundaryJKNdq3lljBUDGFOO\r\nContent-Disposition: form-data; name=\"action\"\r\n\r\ndownload\r\n------WebKitFormBoundaryJKNdq3lljBUDGFOO\r\nContent-Disposition: form-data; name=\"os\"\r\n\r\nmacos\r\n------WebKitFormBoundaryJKNdq3lljBUDGFOO--\r\n"


body = {}
lines = text.split("\r\n")
name, value = "", ""
for line in lines:
    if "Content-Disposition:" in line:
        name = line.split("name=")[-1].replace('\"', '')
    elif line and "--" not in line:
        body[name] = line
print(json.dumps(body, indent=2))


# ------WebKitFormBoundaryJKNdq3lljBUDGFOO\r\n
# Content-Disposition: form-data; name=\"email\"\r\n
# \r\n
# iroyzis@gmail.com\r\n
# ------WebKitFormBoundaryJKNdq3lljBUDGFOO\r\n
# Content-Disposition: form-data; name=\"action\"\r\n
# \r\n
# download\r\n
# ------WebKitFormBoundaryJKNdq3lljBUDGFOO\r\n
# Content-Disposition: form-data; name=\"os\"\r\n
# \r\n
# macos\r\n
# ------WebKitFormBoundaryJKNdq3lljBUDGFOO--
# \r\n


