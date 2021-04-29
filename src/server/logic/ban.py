from time import time

class BanSystem:
    def __init__(self, users):
        self.attempts = {}
        self.ban_times = {}
        for user in users.keys():
            self.attempts[user] = 0
            self.ban_times[user] = 0

    def ban(self, username, attempts, ban_time):
        self.attempts[username] = attempts
        self.ban_times[username] = ban_time

    def attempt(self, username):
        attempts = self.attempts[username]
        print(username)
        if attempts + 1 >= 3:
            self.ban(username, attempts + 1, time() + 60 * 60)
        else:
            self.attempts[username] = attempts + 1

    def is_banned(self, username):
        if self.attempts[username] < 3:
            return False

        if time() > self.ban_times[username]:
            self.attempts[username] = 0
            self.ban_times[username] = 0
            return False
        return True

    def get_attempts(self, username):
        return self.attempts[username]
