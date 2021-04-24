from menu import menu

while True:
    user = input("\nENTER 1 ---> Student"
                 "\nENTER 2 ---> Education Administrator"
                 "\nENTER 0 ---> quit\n")
    if not menu(user):
        break

# again = True
# while again:
#     user = input("\nENTER 1 ---> Student"
#                  "\nENTER 2 ---> Education Administrator"
#                  "\nENTER 0 ---> quit\n")
#     again = menu(user)
