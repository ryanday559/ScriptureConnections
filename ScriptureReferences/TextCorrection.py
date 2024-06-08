import re, os
#â text â is a pattern for closed quotations
#WordâWord is a pattern for Word-Word
#â in the middle of a word is a pattern for '
#Ã± is ñ
#â is open quote
#â¦ is "..."

def text_correction(text):
    text = re.sub('â', '"', text)
    text = re.sub('â', '"', text)
    text = re.sub('â', '—', text)
    text = re.sub('â', "'", text)
    text = re.sub('Ã±', 'ñ', text)
    text = re.sub('â¦', '...', text)
    text = re.sub('Ã¡', 'á', text)
    text = re.sub('Ã¶', 'ö', text)
    return text

def directory_file_correction(directory):
    for filename in os.listdir(directory):
        print(f'Correcting: {filename}')
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            try:
                text = file.read()
            except UnicodeDecodeError:
                print(file)
        corrected_text = text_correction(text)
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as file:
            file.write(corrected_text)

if __name__ == '__main__':
    pass