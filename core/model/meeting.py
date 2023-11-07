


class Meeting:
    def __init__(self, name = '', week = '', day = '', time = '', user_id = 0, id = ''):
        self.name = name
        self.week = week
        self.day = day
        self.time = time
        self.user_id = user_id
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_week(self, week):
        self.week = week

    def set_day(self, day):
        self.day = day

    def set_time(self, time):
        self.time = time    

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_id(self, id):
        self.id = id                

    def print_meeting(self):
        print(f'{self.name}\n{self.week}\n{self.day}\n{self.time}\n{self.user_id}\n{self.id}')