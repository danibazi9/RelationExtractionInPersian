import json
import requests


def remove_extra_whitespaces(word):
    if len(word) >= 1:
        if word[0] == ' ':
            word = word[1:]
        if word[-1] == ' ':
            word = word[:-1]

    return word


sentences_file = open('../data/sentence_broken/sentences.json', 'r', encoding='utf8')
results = open('../data/sentence_broken/sentences_with_relations.json', 'w', encoding='utf8')

seraji_request_url = 'http://127.0.0.1:8000/api/seraji'

sentences_json = json.load(sentences_file)

counter = 0
subject_counter = 1
error_counter = 0
dataset = []

for sentence_dict in sentences_json:
    try:
        response = requests.post(seraji_request_url, json={'input_text': sentence_dict['text']})
        output_text = response.json()['output_text']

        subj_index = output_text.find('?a:')
        obj_index = output_text.find('?b:')
        if subj_index != -1 and obj_index != -1:
            subject = output_text[subj_index + 3:obj_index].strip()
            if sentence_dict['subject'] in subject or subject in sentence_dict['subject']:
                object = output_text[obj_index + 3:output_text.find('\n', obj_index + 3)]
                if 'SOMETHING' not in object and len(subject) >= 2:
                    relation = output_text[output_text.find('?a') + 2: output_text.find('?b')]

                    subject = remove_extra_whitespaces(subject)
                    object = remove_extra_whitespaces(object)
                    relation = remove_extra_whitespaces(relation)
                    dataset.append(
                        {
                            'id': subject_counter,
                            'text': sentence_dict['text'],
                            'subject': subject,
                            'object': object,
                            'relation': relation
                        }
                    )
                    subject_counter += 1
                    # if subject_counter >= 6:
                    #     break

                    print('Subject counter: {}'.format(subject_counter))

        counter += 1
        print(str(counter) + " from 31363 (", end='')
        print("%4.2f" % ((counter / 31363) * 100), end='')
        print("%)")

        # if counter >= 29000:
        #     break
    except:
        error_counter += 1
        print('Error #{} occurred!'.format(error_counter))

results.write(json.dumps(dataset, ensure_ascii=False))
results.close()
