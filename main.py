#GroceryStoreSim.py
#Name:
#Date:
#Assignment:
import simpy
import random


eventLog = []         
waitingShoppers = []  
idleTime = 0           



def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 20) 
    shoppingTime = items // 2     
    yield env.timeout(shoppingTime)

   
    waitingShoppers.append((id, items, arrive, env.now))



def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)  

        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1  
        yield env.timeout(checkoutTime)

      
        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))



def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(2)  


def processResults():
    totalWait = 0
    totalShoppers = 0
    totalItems = 0
    totalShoppingTime = 0
    maxWait = 0

    for e in eventLog:
        waitTime = e[4] - e[3]  
        shoppingTime = e[3] - e[2]  
        totalWait += waitTime
        totalItems += e[1]
        totalShoppingTime += shoppingTime
        totalShoppers += 1
        if waitTime > maxWait:
            maxWait = waitTime

    avgWait = totalWait / totalShoppers if totalShoppers > 0 else 0
    avgItems = totalItems / totalShoppers if totalShoppers > 0 else 0
    avgShopping = totalShoppingTime / totalShoppers if totalShoppers > 0 else 0

    print("=== Simulation Results ===")
    print(f"Total shoppers: {totalShoppers}")
    print(f"Average items purchased: {avgItems:.2f}")
    print(f"Average shopping time: {avgShopping:.2f} minutes")
    print(f"Average wait time: {avgWait:.2f} minutes")
    print(f"Max wait time: {maxWait:.2f} minutes")
    print(f"Total idle time (all checkers): {idleTime} minutes")



def main():
    numberCheckers = 5  
    simLength = 180      

    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=simLength)

    print(f"Shoppers still waiting at end: {len(waitingShoppers)}")
    processResults()


if __name__ == '__main__':
    main()

