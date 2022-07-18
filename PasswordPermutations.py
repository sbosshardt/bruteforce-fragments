import math

class PasswordPermutations:
    fragments = []
    max_fragments_per_password = 5
    permutation_counter = 0
#    allow_repeated_fragments = False

    def loadFragmentsFromFile(self, filename):
        fragments = []
        file = open(filename, 'r')
        lines = file.readlines()
        self.setFragments(fragments)
        for line in lines:
            fragment = line.strip()
            if (fragment):
                fragments.append(fragment)
        self.setFragments(fragments)

    def setFragments(self, fragments):
        self.fragments = fragments

    def setMaxFragmentsPerPassword(self, max):
        self.max_fragments_per_password = max

    def maxPermutations(self):
        max = 0
        for n in range(self.max_fragments_per_password + 1):
            max += len(self.fragments) ** n
        max = max - 1
        return int(max)

    def getPermutationByNum(self, perm_num):
        password = ""
        if (perm_num >= len(self.fragments)):
            rightplace = int(perm_num % len(self.fragments))
            leftplaces = int(math.floor((perm_num - len(self.fragments)) / len(self.fragments)))
            password = self.getPermutationByNum(leftplaces) + self.getPermutationByNum(rightplace)
        else:
            password = self.fragments[perm_num]
        return password

    def getNextPermutation(self):
        permutations = self.getNextNPermutations(1)
        return permutations[0]

    def getNextNPermutations(self, num_permutations):
        permutations = []
        if len(self.fragments) == 0:
            raise Exception('Cannot get permutations prior to setting fragments.')
        upper_perm_num = int(min(self.permutation_counter + num_permutations, self.maxPermutations()))
        if (upper_perm_num == self.permutation_counter):
            return [False]
        for perm_num in range(self.permutation_counter, upper_perm_num):
            permutation = self.getPermutationByNum(perm_num)
            permutations.append(permutation)
            self.permutation_counter += 1
        return permutations

