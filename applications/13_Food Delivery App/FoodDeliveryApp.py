# Single Responsibility Principle (The role of the class is only payment processing.)
# Open/Closed Principle (By separating each method, the new payment method can be easily added in the future.)
class PaymentMethod:
    def process(self):
        raise NotImplementedError("Must implement process() method")

# Liskov Substitution Principle (Inheritate PaymentMethod.)    
class CardPayment(PaymentMethod):
    def process(self):
        print("Processing card payment...")
        return True
    
# Liskov Substitution Principle (Inheritate PaymentMethod.)
class CashPayment(PaymentMethod):
    def process(self):
        print("Processing cash payment...")
        return True

# Single Responsibility Principle (The role of the class is only delivery assignment.)
# Open/Closed Principle (By separating each method, the new delivery method can be easily added in the future.)
class DeliveryMethod:
    def assign(self):
        raise NotImplementedError("Must implement assign() method")

# Liskov Substitution Principle (Inheritate DeliveryMethod.)
class DriverDelivery(DeliveryMethod):
    def assign(self):
        print("Assigning a driver...")
        return "A driver"
    
# Liskov Substitution Principle (Inheritate DeliveryMethod.)
class RobotDelivery(DeliveryMethod):
    def assign(self):
        print("Assigning a robot...")
        return "A robot" 

# Single Responsibility Principle (The role of the class is only sending notification.)
# Open/Closed Principle (By separating each method, the new notification service can be easily added in the future.)
class NotificationService:
    def send(self):
        raise NotImplementedError("Must implement send() method")

# Liskov Substitution Principle (Inheritate NotificationService.)
class MailNotification(NotificationService):
    def send(self):
        return "The restaurant is making the food you ordered. The food will be delivered to your place in around 45 minitues."

# Liskov Substitution Principle (Inheritate NotificationService.)
class SMSNotification(NotificationService):
    def send(self):
        return "The food is delivered to your place."


# Dependency Inversion Principle (The main class below does not relay on specific child classes such as CardPayment.
class FoodDeliveryApp:
    def __init__(self, payment_method: PaymentMethod, delivery_method: DeliveryMethod, notification_service: NotificationService):
        self.payment_method = payment_method
        self.delivery_method = delivery_method
        self.notification_service = notification_service
        
    def place_order(self, customer_name, food_item):
        print(f"\nNew order for {customer_name}: {food_item}")
        if not self.payment_method.process():
            print("Payment failed.")
            return
        driver_or_robot = self.delivery_method.assign()
        print(f"{driver_or_robot} assigned for delivery.")
        message = self.notification_service.send()
        print(f"{message}")


# Test
card = CardPayment()
driver = DriverDelivery()
notification = MailNotification()

app = FoodDeliveryApp(card, driver,notification)
app.place_order("Yuichiro", "Sushi")
    