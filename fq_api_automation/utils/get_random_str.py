import random,string

def random_str(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

if __name__ == '__main__':
    print(random_str(15))