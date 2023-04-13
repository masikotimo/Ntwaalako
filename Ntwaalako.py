from lnd_grpc import Client
from constants import lnd_dir, tls_cert_path, grpc_port, grpc_host,macaroon_path,network,tls_cert_path1,macaroon_path1,grpc_port1
import hashlib
import secrets

lnd = Client(lnd_dir = lnd_dir,macaroon_path= macaroon_path, tls_cert_path= tls_cert_path,network = network,grpc_host= grpc_host,grpc_port=grpc_port)

lnd1 = Client(lnd_dir = lnd_dir,macaroon_path= macaroon_path1, tls_cert_path= tls_cert_path1,network = network,grpc_host= grpc_host,grpc_port=grpc_port1)

preimage = secrets.token_bytes(32)
class Driver:
    def __init__(self, driver_id, wallet_balance):
        self.driver_id = driver_id
        self.wallet_balance = wallet_balance

    def receive_payment(self, amount):
        self.wallet_balance += amount
        print("Payment received from rider.")

    def get_wallet_balance(self):
        return self.wallet_balance


class Ride:
    def __init__(self, rider_id, driver_id, destination, cost):
        self.rider_id = rider_id
        self.driver_id = driver_id
        self.destination = destination
        self.cost = cost
        self.is_completed = False
        self.preimage = b""

    def complete_ride(self):
        self.is_completed = True

    def set_preimage(self,image):
        self.preimage = image

    def get_preimage(self):
        return self.preimage 

class Rider:
    def __init__(self, rider_id, wallet_balance):
        self.rider_id = rider_id
        self.wallet_balance = wallet_balance

    def request_ride(self, driver_id, destination, cost):
        if self.wallet_balance >= cost:
            ride = Ride(self.rider_id, driver_id, destination, cost)


            

            invoice = lnd.add_hold_invoice(value= int(cost) ,memo="pay_for_ride",hash = preimage )
            payment_request = invoice.payment_request
            print("Payment Request:", payment_request)
            print("Payment Request:", invoice)

            ride.set_preimage(payment_request)
            self.wallet_balance -= cost
            return ride
        else:
            print("Insufficient balance in rider's wallet.")
            return None

    def pay_hold_invoice(self, ride,driver:Driver):
        if not ride.is_completed:
            self.wallet_balance -= ride.cost
            driver.receive_payment(ride.cost)

            print("checking",ride.get_preimage())
            print("type of ",type(ride.get_preimage()))

            resp = lnd1.settle_invoice(preimage=preimage)
            print("Settle Invoice Response:", resp)
            ride.complete_ride()
            print("Hold invoice paid successfully.")
        else:
            print("Ride has already been completed.")




if __name__ == '__main__':
    # Sample usage

    # Create riders and drivers
    rider1 = Rider(1, 50)
    rider2 = Rider(2, 30)
    driver1 = Driver(101, 0)

    # Rider1 requests a ride
    ride1 = rider1.request_ride(driver_id=101, destination='A', cost=20)
    if ride1:
        # Rider1 pays hold invoice
        print('yeah')
        rider1.pay_hold_invoice(ride1,driver1)

    # Rider2 requests a ride
    # ride2 = rider2.request_ride(driver_id=101, destination='A', cost=25)
    # if ride2:
    #     # Rider2 pays hold invoice
    #     rider2.pay_hold_invoice(ride2,driver1)

    print(driver1.get_wallet_balance())
