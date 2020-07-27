import random, string
import math

### generate a random string including letters and digits
def randnormalstring(lengths):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(lengths))

### generate a random string including letters & digits & punc
def randpuncstring(lengths):
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for x in range(lengths))


def writereport(documentname,):
    documentname = documentname +".text"
    with open(documentname,'a') as f :
            f.write("===================================================================================")
            #test_items_name = "TEST LENGTH:" + str(j) +"\n"
            f.write("TEST LENGTH:")
            for i in range(1000):
                a = randnormalstring(j)
                f.write(a)
                f.write("\n")
                
if __name__=="__main__":
    contentlenlist =[32]  
    for k in contentlenlist:
        with open('sens_randspecialletter.txt','a') as f :
    #         # f.write("===================================================================================")
    #         # test_items_name = "\nTEST LENGTH:" + str(j) +"\n"
    #         # f.write(test_items_name)
            if (k>=100):
                for i in range(10):
                    a = randpuncstring(k)
                    f.write(a)
                    f.write("\n")
            else:
                for i in range(100):
                    a = randpuncstring(k)
                    f.write(a)
                    f.write("\n")