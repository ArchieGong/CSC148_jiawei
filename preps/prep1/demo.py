class Tune:
    title: str
    artist: str
    length: int
    play_by: dict[str,int]
    def __init__(self, title:str, artist:str, length:int) -> None:
        self.title = title
        self.artist = artist
        self.length = length
        self.play_by = {}
    def play(self, user:str) -> None:
        if user not in self.play_by:
            self.play_by[user]=0
        self.play_by[user] += 1
    def played_by(self, user:str)->int:
        return self.play_by.get(user,0)
t=Tune('afterglow', 'ed', 50)

t=Tune('a','b',50)
t.play('g')
t.play('g')
print(t.played_by('g'))
