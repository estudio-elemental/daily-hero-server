from src.core.monsters.domain.monster import Monster


rat = Monster(
    level=1,
    exp_earn=50,
    name="Rato",
    hp=2,
    _attack=3,
    _defense=1,
)

wolf = Monster(
    level=2,
    exp_earn=90,
    name="Lobo",
    hp=5,
    _attack=4,
    _defense=1,
)

lancer_goblin = Monster(
    level=3,
    exp_earn=150,
    name="Goblin Lanceiro",
    hp=9,
    _attack=6,
    _defense=2,
)

orc = Monster(
    level=4,
    exp_earn=190,
    name="Orc Guerreiro",
    hp=11,
    _attack=8,
    _defense=3,
)

atroz_spider = Monster(
    level=4,
    exp_earn=240,
    name="Aranha atroz",
    hp=15,
    _attack=10,
    _defense=4,
)

monsters = [
    rat,
    wolf,
    lancer_goblin,
    orc,
    atroz_spider,
]