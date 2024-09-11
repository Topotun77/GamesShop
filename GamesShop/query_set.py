from task1.models import Buyer, Game

Game.objects.all()
Buyer.objects.create(name='Alex', balance=100, age=27)
Buyer.objects.create(name='Rosa', balance=10, age=10)
Buyer.objects.create(name='Pasha', balance=1000, age=39)

Game.objects.create(title='Tetris', cost=5, size=3, description='Легендарная игра')
Game.objects.create(title='World of Tanks', cost=49.99, size=233.345, description='Массовая многопользовательская онлайн-игра', age_limited=True)
Game.objects.create(title='New Game', cost=199.999, size=3765, description='Очень новая игра', age_limited=True)

Game.objects.get(id=1).buyer.set((1, 2, 3))
Game.objects.get(id=2).buyer.set((1, 3))
Game.objects.get(id=3).buyer.set((3,))
