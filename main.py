import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
cor_contacts_list = [contacts_list[0]]

for row in contacts_list[1:]:
    new_row = row[:]
    fio = " ".join(new_row[0:3]).strip()
    fio_splitted = fio.split()
    if len(fio_splitted) == 3:
        new_row[0], new_row[1], new_row[2] = fio_splitted
    elif len(fio_splitted) == 2:
        new_row[0], new_row[1] = fio_splitted
        new_row[2] = ''
    elif len(fio_splitted) == 1:
        new_row[0] = fio_splitted[0]
        new_row[1] = new_row[2] = ''
    cor_contacts_list.append(new_row)


phone_pattern = r"(\+7|8)?\s*\(?(\d{3})\)?\s*[-\s]?(\d{1,3})[-\s]?(\d{2})[-\s]?(\d{2})(?:\s*[ (]?доб\.?\s*(\d+)[)]?)?"
phrase_pattern = r"доб"
for phones in cor_contacts_list[1:]:
    if re.findall(phrase_pattern, phones[5]):
        replacement_pattern = r"+7(\2)\3-\4-\5 доб.\6"
        phones[5] = re.sub(phone_pattern, replacement_pattern, phones[5])
    else:
        replacement_pattern = r"+7(\2)\3-\4-\5"
        phones[5] = re.sub(phone_pattern, replacement_pattern, phones[5])


header = cor_contacts_list[0]
idx = {name: i for i, name in enumerate(header)}
merged = {}
for row in cor_contacts_list[1:]:
    key = (row[idx['lastname']], row[idx['firstname']])
    if key not in merged:
        merged[key] = row[:]
    else:
        existing = merged[key]
        for field in ['surname', 'organization', 'position', 'phone', 'email']:
            i = idx[field]
            if not existing[i] and row[i]:
                existing[i] = row[i]
result = [header] + list(merged.values())


with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)
