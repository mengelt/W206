from RestarauntOrder import RestarauntOrder

def main():

    my_order = RestarauntOrder(0.0725)
    my_order.print_menu()

    customer_name = ""
    while customer_name == "":
        customer_name = input("Who is this order for? ")

        if customer_name == "":
            print("* Please enter a valid customer name")
    
    my_order.set_customer_name(customer_name)

    my_order.start_order()


if __name__ == "__main__":
    main()