import re

import html2text


def create_error_text(error_packs):
    error_sum_text = ''
    for error_pack in error_packs:
        error_text = html2text.html2text(str(error_pack))
        error_sum_text += error_text

    splitted = re.split('\*|\n', error_sum_text)

    for error in splitted:
        error.lstrip()

    results = []
    i = 0
    title = ''
    description = ''
    for text in splitted:
        temp = text[:]
        if temp.lstrip() == '':
            continue
        if i % 2 == 0:
            title = text
        else:
            description = text
            description = description.replace('This field is required.', 'این قسمت را پاسخ نداده اید')
            description = description.replace('The two password fields didn’t match.', 'عدم تطابق رمز عبور ها')
            description = description.replace('Enter a valid', 'با مقدار نا مناسب پر شده است')
            description = description.replace('Ensure this value has at most',
                                              'تعداد حروف به کار رفته بیشتر از حد کجاز است')
            description = description.replace('This password is too common.', 'رمز عبور شما بسیار ساده است')
            description = description.replace('Select a valid choice', 'مقدرا مناسب قرار دهید')
            description = description.replace('is not one of the available choices', 'مقدار مناسبی نیست')
            description = description.replace('This password is too short. It must contain at least 8 characters.',
                                              'رمز عبور شما کوتاه است. باید حداقل ۸ حرف باشد')
            results.append({'title': title, 'description': description})
        i += 1

    if results.__len__() == 0:
        return ''

    result = results[0].get('title') + ' : ' + results[0].get('description')
    return result
