import pysrt
import nltk.data
import os


dir_path = 'your_path'
qa_file = open('qa_series.txt', 'w')


def check_sentense(sent):
    if len(sent.split()) > 2 and 'swsub.com' not in sent and ']' not in sent and '-->' not in sent \
            and sent[len(sent) - 1] == '?' and 'переведено' not in sent and '(' not in sent and '<i>' not in sent:
        return True
    else:
        return False


def handle_sent(sent):
    if  sent[0] == '-' or sent[0] == '–':
        sent = sent[1:len(sent)-1]
    return sent.replace('\n', ' ').strip() + '\n'


def get_qa_from_file(file_parh):
    try:
        subs = pysrt.open(file_parh, encoding='cp1251')
    except UnicodeDecodeError:
        subs = pysrt.open(file_parh)
    sub_str = ''
    for i in subs:
        sub_str += i.text + ' '

    tokenizer = nltk.data.load('tokenizers/punkt/russian.pickle')
    sentence = tokenizer.tokenize(sub_str)

    for j in range(len(sentence)):
        if check_sentense(sentence[j]):
            try:
                if '\n' in sentence[j] + sentence[j + 1]:
                    if sentence[j + 1][len(sentence[j + 1]) - 1] != '?':
                        qa_file.write(handle_sent(sentence[j]))
                        qa_file.write(handle_sent(sentence[j + 1]))
            except IndexError:
                continue


for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith(".srt"):
            file_parh = os.path.join(root, file)
            get_qa_from_file(file_parh)






