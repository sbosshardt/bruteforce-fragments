from PasswordPermutations import PasswordPermutations
import subprocess, shlex, time

class GeneralProcess(PasswordPermutations):
    perms = None
    command = ''
    expected_return_value = 0
    concurrency = 3
    processes = {}

    def setCommand(self, command):
        self.command = command

    def setExpectedReturnValue(self, value):
        self.expected_return_value = value

    def findPassword(self):
        if not self.command:
            raise Exception('Command must be defined.')
        if self.command.find('{{PASSWORD}}') == -1:
            raise Exception('Command should contain a "{{PASSWORD}}" substring, for substitution use.')
        while True:
            pass_guess = self.getNextPermutation()
            if (pass_guess == False):
                break
            print ('Attempting password: ' + pass_guess)
            escaped_pass_guess = pass_guess.replace('"', '\\"')
            cmd = self.command.replace('{{PASSWORD}}', escaped_pass_guess)
            process_output = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            returnval = process_output.returncode
            if (returnval == 0):
                print ('Password recovered: ' + pass_guess)
                return 0
        print('Password not found.')
        return 1

    def findPasswordParallel(self):
        print("Running in parallel process mode, concurrency: ", self.concurrency)
        if not self.command:
            raise Exception('Command must be defined.')
        if self.command.find('{{PASSWORD}}') == -1:
            raise Exception('Command should contain a "{{PASSWORD}}" substring, for substitution use.')
        password_found = False
        can_continue = True
        proc_keys_to_del = []
        while can_continue:
            if can_continue and len(self.processes) < self.concurrency:
                num_to_spawn = self.concurrency - len(self.processes)
                pass_guesses_to_try = self.getNextNPermutations(num_to_spawn)
                if (pass_guesses_to_try[0] == False):
                    if (len(self.processes) > 0):
                        continue
                for pass_guess in pass_guesses_to_try:
                    print ('Attempting password: ' + pass_guess)
                    escaped_pass_guess = pass_guess.replace('"', '\\"')
                    cmd = self.command.replace('{{PASSWORD}}', escaped_pass_guess)
                    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.processes[pass_guess] = proc
            for pass_guess, process in self.processes.items():
                returnval = process.poll()
                if (returnval is not None):
                    if (returnval == 0):
                        print ('Password recovered: ' + pass_guess)
                        password_found = pass_guess
                        can_continue = False
                    else:
                        print ('Password incorrect: ' + pass_guess)
                    proc_keys_to_del.append(pass_guess)
            if (can_continue == False) and (len(self.processes) > 0):
                for pass_guess, process in self.processes.items():
                    process.kill()
                for pass_guess, process in self.processes.items():
                    outs, errs = process.communicate()
                    proc_keys_to_del.append(pass_guess)
                # remove duplicates that may have cropped up
                proc_keys_to_del = list(set(proc_keys_to_del))
            if (len(proc_keys_to_del) > 0):
                for key in proc_keys_to_del:
                    del self.processes[key]
                proc_keys_to_del = []
            else:
                time.sleep(0.01)
