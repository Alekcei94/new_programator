
def new_parth_logger(number):
    global path_in_data
    if number == 0:
        f = open(path_in_data + 'logger_user.lg', 'w')
    elif number == 1:
        f = open(path_in_data + 'logger.lg', 'w')
    f.close()


def write_log(text, number):
    global path_in_data
    if number == 0:
        f = open(path_in_data + 'logger_user.lg', 'a')
    elif number == 1:
        f = open(path_in_data + 'logger.lg', 'a')
    f.write(text + '\n')
    f.close()
