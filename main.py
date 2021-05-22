from menu import menu
import logging

if __name__ == "__main__":
    my_logger = logging.getLogger(__name__)
    my_logger.setLevel(logging.ERROR)
    file_handler = logging.FileHandler('file.log')
    file_handler.setLevel(logging.ERROR)
    log_format = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s', datefmt='%y-%m-%d %H:%M:%S')
    file_handler.setFormatter(log_format)
    my_logger.addHandler(file_handler)

    while True:
        choice = input("\nENTER 1 ---> sign-in"
                       "\nENTER 2 ---> sign-up"
                       "\nENTER 0 ---> quit\n")
        if not menu(choice, my_logger):
            break
