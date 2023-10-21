booking_type = 1 #0:normal 1:rebooking 2:cancellation

MRP1 = 10000
x = 9 #x:rating
MRP2 = 0
refund = 0


def collect_MRP1():
    print(f"Transaction completed with amount {MRP1}")

def call_add_page():
    print("THIS IS AN ADVERTISMENT/SURVEY")
    #add page

def rebooking_overhead():
    global MRP2
    MRP2 - 0.1*MRP1
    print(f"Booking price:{MRP1}")
    print(f"Additional rebooking overhead:{MRP2}")
    print(f"Please pay total amount:{MRP1+MRP2}")
    #transaction page

if __name__ == "__main__":
    if booking_type == 0:
        if x == 10:
            collect_MRP1()
        else:
            x = x + 1
            print(f"rating increased to:{x}")
            collect_MRP1()
    elif booking_type == 1:
        if x == 10:
            x = x - 1
            print(f"rating decreased to:{x}")
            collect_MRP1()
        else:
            if x < 5 and x > 0:
                call_add_page()
                x = x - 1
                print(f"rating decreased to:{x}")
                rebooking_overhead()
            else:
                call_add_page()
                x = x - 1
                print(f"rating decreased to:{x}")
                print(f"Total amount to be paid:{MRP1}")
    else:
        if x == 10:
            x = x - 1
            print(f"rating decreased to:{x}")
            refund = MRP1 - 0.1*MRP1
        else:
            if x < 5 and x > 0:
                call_add_page()
                x = x - 1
                print(f"rating decreased to:{x}")
                refund = MRP1 - 0.2*MRP1
            else:
                call_add_page()
                x = x - 1
                refund = MRP1 - 0.3*MRP1
            



