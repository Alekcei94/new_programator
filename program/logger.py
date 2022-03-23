def write_log(text, number):
    print('\n' + text)
    path_in_data = "../logger/"
    if number == 0:
        f = open(path_in_data + 'logger_user.lg', 'a')
    elif number == 1:
        f = open(path_in_data + 'logger.lg', 'a')
    f.write(text + '\n')
    f.close()
