import datetime

class RestarauntOrder:

    # class constant
    ITEM_MENU = {
        "sandwich" : (10, 10), 
        "salad" : (8, 8),
        "soup" : (6, 15),
        "coffee" : (5, 5),
        "tea" : (5, 5)}

    # default constructor
    def __init__(self, tax_rate):
        # default tax rate (Irvine, CA)
        self.__tax_rate = tax_rate
        self.__cart = {}

    def __calculate_total_price_with_tax__(self, subtotal):
        """calculates the grand total including tax"""
        total_price = 0

        ## basic validity check
        if len(subtotal) > 0:
            for item in subtotal:
                total_price += subtotal[item][1]
                
        tax = total_price * self.__tax_rate
        # calculate grand total price
        grand_total = total_price + tax
        return grand_total, tax

    def __calculate_total_time__(self, subtotal):
        total_time = 0
        ## basic validity check
        if len(subtotal) > 0:
            for item in subtotal:
                total_time += subtotal[item][2]

        return total_time

    def __print_receipt__(self):

        # get the additional dis
        date = datetime.date.today()
        
        # calculate the total price (grand total including tax)
        grand_total, tax = self.__calculate_total_price_with_tax__(self.__cart)
        
        # calculate total time in minutes
        total_time = self.__calculate_total_time__(self.__cart)
        
        # print the receipt in pretty format
        ## create receipt header
        output_str = "*************************************************\n"
        output_str += f"{self.__customer_name}, thanks for your order\n\n"
        output_str += "Items     qty       Price\n"
        ## create item list
        for key, vals in self.__cart.items():
            item_name = key
            qty = vals[0]
            price = vals[1]
            output_str += f"{item_name:<10}{qty:<10}{price:.2f}\n"
        ## add receipt tax and totals
        output_str += "\n"
        output_str += f"Tax       ${tax:.2f}\n"
        output_str += f"Total     ${grand_total:.2f}\n"
        ## add receipt footer
        output_str += f"{date},  Your order will be ready in {total_time} minutes\n"
        output_str += "***************************************************"
        
        print(output_str)

    def __get_tea_subtotal__(self):
        """return the total quantity, price, and preperation time
        input is everything required to include discounts
        future: even though there is not discount today, we keep
        a dedicated function to calculate tea grand total so it
        is easy to add in the future if we decide to
        """
        nb_tea = self.__cart["tea"]
        price_per_tea = self.ITEM_MENU["tea"][0]
        min_per_tea = self.ITEM_MENU["tea"][1]
        total_min = nb_tea * min_per_tea
        total_price = nb_tea * price_per_tea
        return nb_tea, total_price, total_min

    def __get_coffee_subtotal__(self):
        """return the total quantity, price, and preperation time
        input is everything required to include discounts
        future: even though there is not discount today, we keep
        a dedicated function to calculate coffee grand total so it
        is easy to add in the future if we decide to
        """
        nb_coffee = self.__cart["coffee"]
        price_per_coffee = self.ITEM_MENU["coffee"][0]
        min_per_coffee = self.ITEM_MENU["coffee"][1]
        total_time = nb_coffee * min_per_coffee
        total_price = nb_coffee * price_per_coffee
        return nb_coffee, total_price, total_time

    def __get_soup_subtotal__(self):
        """return the total quantity, price, and preperation time
        input is everything required to include discounts
        """
        soup_total = None
        nb_soup = self.__cart["soup"]
        nb_sandwich = self.__cart["sandwich"] if "sandwich" in self.__cart else 0
        nb_salad = self.__cart["salad"] if "salad" in self.__cart else 0
        price_per_soup = self.ITEM_MENU["soup"][0]
        min_per_salad = self.ITEM_MENU["soup"][1]
        total_time = nb_soup * min_per_salad
        # if ordered with a sandwich AND salad, apply the 20% discount
        if nb_sandwich > 0 or nb_salad > 0:
            # determine how many soups get discounted. Only discount a soup if there is matching
            # soup AND sandwich
            ## first, determine if we have less sandwiches or salads. This will determine the theorhetical
            ## maximum match to how many soups we can discount
            nb_max_possible_discount = nb_sandwich if nb_sandwich < nb_salad else nb_salad
            if nb_max_possible_discount < nb_soup:
                # apply discount to as many salads as soups, then add the full price of the difference
                total_price = nb_max_possible_discount * price_per_soup * 0.80
                total_price += (nb_soup - nb_max_possible_discount) * price_per_soup
                soup_total = nb_soup, total_price, total_time
            else:
                # apply discount to all soups
                total_price = nb_soup * price_per_soup * 0.80
                soup_total = nb_soup, total_price, total_time
        else:
            total_price = nb_soup * price_per_soup
            soup_total = nb_soup, total_price, total_time
        
        return soup_total

    def __get_salad_subtotal__(self):
        """return the total quantity, price, and preperation time
        input is everything required to include discounts
        """
        salad_total = None
        nb_salad = self.__cart["salad"]
        nb_soup = self.__cart["soup"] if "soup" in self.__cart else 0
        price_per_salad = self.ITEM_MENU["salad"][0]
        min_per_salad = self.ITEM_MENU["salad"][1]
        total_time = nb_salad * min_per_salad
        # if ordered with a soup, the 10% discount
        if nb_soup> 0:
            # determine how many salads get discounted. Only discount a salad if there is matching soup
            if nb_soup < nb_salad:
                # apply discount to as many salads as soups, then add the full price of the difference
                total_price = nb_soup * price_per_salad * 0.90
                total_price += (nb_salad - nb_soup) * price_per_salad
                salad_total = nb_salad, total_price, total_time
            else:
                # apply discount to all salads
                total_price = nb_salad * price_per_salad * 0.90
                salad_total = nb_salad, total_price, total_time
        else:
            total_price = nb_salad * price_per_salad
            salad_total = nb_salad, total_price, total_time
        
        return salad_total

    def __get_sandwich_subtotal__(self):
        """return the total quantity, price, and preperation time
        input is everything required to include discounts
        """
        sandwich_total = None
        nb_sandwich = self.__cart["sandwich"]
        price_per_sandwich = self.ITEM_MENU["sandwich"][0]
        min_per_sandwich = self.ITEM_MENU["sandwich"][1]
        total_time = nb_sandwich * min_per_sandwich
        # if 5 or more sandwiches are ordered, appy a 10% discount
        if nb_sandwich >= 5:
            total_price = nb_sandwich * price_per_sandwich * 0.90
            sandwich_total = nb_sandwich, total_price, total_time
        else:
            total_price = nb_sandwich * price_per_sandwich
            sandwich_total = nb_sandwich, total_price, total_time
            
        return sandwich_total

    def __calculate_subtotal__(self):
        subtotal_cart = {}

        # calculate sandwich total
        if "sandwich" in self.__cart:
            subtotal_cart["sandwich"] = self.__get_sandwich_subtotal__()
            
        # calculate salad total
        if "salad" in self.__cart:
            subtotal_cart["salad"] = self.__get_salad_subtotal__()
            
        # calculate salad total
        if "soup" in self.__cart:
            subtotal_cart["soup"] = self.__get_soup_subtotal__()
            
        # calculate coffee total
        if "coffee" in self.__cart:
            subtotal_cart["coffee"] = self.__get_coffee_subtotal__()
            
        # calculate tea total
        if "tea" in self.__cart:
            subtotal_cart["tea"] = self.__get_tea_subtotal__()
        
        self.__cart = subtotal_cart

    def __prompt_for_item_and_quantity__(self):  
        # get item type
        ## initial prompt for item type
        item = input("Please enter item you want to purchase:")
        ## basic validity check to make sure they enter a valid item
        while item not in self.ITEM_MENU:
            item = input(f"{item} is not available to purchase. Please enter item you want to purchase:")

        # get item quantity
        ## initial prompt for item quantity
        quantity = input("Please enter quantity that you want:")
        ## basic validity check
        while not quantity.isdigit():
            quantity = input(f"{quantity} is not a valid quantity. Please enter quantity that you want:")
        quantity = int(quantity)

        return item, quantity

    def __get_customer_order__(self):
        """Gets the order cart from the user
        Launches an interactive dialog with the user to get the
        items and quantity of items they want to purchase. Returns
        the item sub total - the \'cart\'
        """        
        
        # ask for more items over a loop
        is_order_more = "y"
        # enter loop prompt
        while is_order_more == 'y':
            # if user want to order more, prompt them for which item and quantity
            item, quantity = self.__prompt_for_item_and_quantity__()
            # add to running order order
            ## check if key exists. if it does, add to the existing quantity. otherwise, create the key and add the quantitiy
            if item in self.__cart:
                self.__cart[item] += quantity
            else:
                self.__cart[item] = quantity
            # prompt user if they would like to order more
            cart_items = sum(self.__cart.values())
            print(f"Your cart now has {cart_items} item{'' if cart_items == 1 else 's'}")
            is_order_more = input("Would you like to order more? (y)es or (n)o:")
            ## perform a basic validity check for the answer
            while is_order_more.lower() != "y" and is_order_more.lower() !=  "n":
                print("Invalid response.")
                is_order_more = input("Would you like to order more? (y)es or (n)o:")
            

    def __greet_customer__(self):
        print(f"\nWelcome, {self.__customer_name}!")

    def print_menu(self):
        print("Welcome to the W206 Restaraunt!")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("\nOur Menu:\n")
        print(f'{"Item":>12} {"Price":>12} {"Time to Make":>15}')
        for item in self.ITEM_MENU:
            
            cost = self.ITEM_MENU[item][0]
            time = self.ITEM_MENU[item][1]

            print(f"{item:>12} {cost:>12,.2f} {time:>15}")

        print("\n")

    def set_customer_name(self, customer_name):
        self.__customer_name = customer_name

    def start_order(self):

        self.__greet_customer__()

        # get the order from customer
        self.__get_customer_order__()

        # compute order details after applying discounts (item, quantity, price, and time)
        self.__calculate_subtotal__()

        # print receipt
        self.__print_receipt__()
