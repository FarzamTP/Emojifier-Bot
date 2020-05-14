import string

def contains_punc(text):
    flag = False
    for p in string.punctuation:
        if p in text:
            flag = True
            break
    return flag

print(contains_punc("@asd"))