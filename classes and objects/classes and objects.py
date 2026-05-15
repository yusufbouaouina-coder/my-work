class mob():
    def __init__(self, hp, dmg, speed):
        self.hp = hp
        self.dmg = dmg
        self.speed = speed

creeper = mob(2,3,4.5)
print(creeper.hp, creeper.dmg, creeper.speed)