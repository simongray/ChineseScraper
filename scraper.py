import requests

r = requests.get('http://www.zein.se/patrick/3000char.html')
r.encoding = 'GB2312'  # as written in page source
character_page = r.text

dataset = []

for line in r.text.split('<TR><TD ALIGN="CENTER">')[1:]:  # remove beginning of html document
    parts = line.split('</TD><TD ALIGN="CENTER"><FONT SIZE=+2>')

    # separate into three parts: rank, hanzi, and description
    rank = int(parts[0])
    hanzi = parts[1][0]
    description_start = parts[1].find('[')
    description_end = -12
    description = parts[1][description_start:description_end]

    # remove font tag
    description = description.replace('</FONT>', '')

    # replace double-quotes with single-quotes
    description = description.replace('"', "'")

    # replace colons (used as delimiter) with equals sign
    description = description.replace(':', '=')

    # remove newlines
    description = description.replace('\n', '')
    description = description.replace('\r', '')

    # special rule for final part
    if rank == 3000:
        description = description[0:-32]

    dataset.append(
        {
            'rank': rank,
            'hanzi': hanzi,
            'description': description
        }
    )

for chunk in [0, 500, 1000, 1500, 2000, 2500]:
    with open(str(chunk)+'-'+str(chunk+500)+'.txt', 'w') as hanzi_file:
        for row in dataset:
            if chunk < row['rank'] < chunk + 500:
                hanzi_file.write(row['hanzi'])
                hanzi_file.write(': ')
                hanzi_file.write(row['description'])
                hanzi_file.write('<BR><BR>rank = ' + str(row['rank']))
                hanzi_file.write('\n')