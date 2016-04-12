import aiml


kernel = aiml.Kernel()

kernel.learn("test.xml")

while True:
    print(kernel.respond(input()))