from PasswordPermutations import PasswordPermutations
from GeneralProcess import GeneralProcess
import time

def main():
    filename = 'test_fragments_easy.txt'
    perms = PasswordPermutations()
    perms.setMaxFragmentsPerPassword(3)
    perms.loadFragmentsFromFile(filename)
    #for i in range(40):
    #    print (str(i) + ': ' + perms.getPermutationByNum(i))
    while True:
        perm = perms.getNextPermutation()
        if (perm == False):
            print("Reached end of list")
            break
        print(perm)

def gpg():
    # TestPassword! is the key's password
    gp = GeneralProcess()
    gp.loadFragmentsFromFile('test_fragments.txt')
    gp.setMaxFragmentsPerPassword(3)
    gp.setCommand('gpg --batch --pinentry-mode loopback --passphrase="{{PASSWORD}}" --decrypt deleteme.tmp.gpg')
    #gp.findPassword()
    gp.findPasswordParallel()

start_time = time.time()
#main()
gpg()
end_time = time.time()
elapsed_time = end_time - start_time
elapsed_time_str = ("{:0." + str(3) + "f}").format(elapsed_time)
print('Run time: ', elapsed_time_str, ' secs')