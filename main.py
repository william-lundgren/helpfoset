
class User:
    def __init__(self, name, prio, group, food_pref, answer, email):
        self.name = name
        self.email = email
        self.prio = prio
        self.group = group
        self.food_pref = food_pref
        self.answer = answer

    def __repr__(self):
        return f"{self.name}, {self.prio}, {self.group}, {self.food_pref if self.food_pref != '' else 'Tom'}, " \
               f"{self.food_pref if self.food_pref != '' else 'Tom'}, {self.email}"


# List of all the users at the event
users = []

with open("anmalda_till_glowfesten.csv", "r") as file:
    lines = file.readlines()
    for line in lines[1:]:

        person = line.split('"')
        if len(person) > 1:
            person[1] = person[1].replace(",", "|")
        person = "".join(person)
        person = person.split(",")
        for i, ele in enumerate(person):
            person[i] = ele.replace("|", ",")

        user = User(*person)
        users.append(user)
        print(user)

has_spot = []

for user in users:
    if user.prio.lower() in ("föset", "foset", "fos", "fös"):
        has_spot.append(user)
        users.remove(user)
print(users)
print(has_spot)