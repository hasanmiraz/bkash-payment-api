# import environ
# 
# env = environ.Env()
# environ.Env.read_env("paymentIntegrationBkash\.env")
# print(env('NAME'))
def whatTechTheyUse(**kwargs):
    result = []
    for key, value in kwargs.items():
        print(key)
        print(value)


data = {
    "a":"b",
    "v":"d"
}

whatTechTheyUse(name1 = "a", name2 = 1, name3 = ["abc",1], name4 = data )