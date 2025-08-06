from time import sleep

from src.core.fight.domain.fight import Fight
from src.core.hero.domain.hero import Hero
from monster_mock import monsters


hero = Hero(
    level=1,
    exp=0,
    max_hp=5,
    hp=5,
    _attack=4,
    _defense=1,
)

def main():
    print("Bem-vindo ao Hero Daily Game!")
    sleep(2)
    print("Aqui você deverá enfrentar desafios diários e matar monstros para evoluir e enfrentar novos desafios. Vamos nessa?\n""")
    sleep(4)
    while True:

        print("Escolha uma ação:")
        print("1- Dormir")
        print("2- Lutar")
        print("3- Consultar vida")
        print("4- Consultar exp")
        user_choice = input("Digite o número escolhido: ")
        try:
            int(user_choice)
        except:
            continue

        if int(user_choice) == 1:
            hero.rest()
            print("Descansando...")
            sleep(1)
            print("ZZzzzz")
            sleep(1)
            print("zzZZzz")
            sleep(1)
            print("zzzzZZ")
            sleep(1)
            print("Você acorda plenamente recuperado")
            print()
        elif int(user_choice) == 2:
            if hero.hp <= 0:
                print("Você não pode lutar, precisa descansar pra recuperar a vida.")
                print()
                sleep(2)
                continue

            count = 1
            print()
            print("Vamos lutar!")
            for monster in monsters:
                if monster.level <= hero.level:
                    print(f"Digite {count} para enfrentar {monster.name}")
                    count += 1

            print()
            user_choice = input("Digite o número escolhido: ")
            sleep(1)
            print("Vamos lá!!")
            sleep(2)
            print()


            fight1 = Fight(hero, monsters[int(user_choice)-1])
            fight1.start()

        elif int(user_choice) == 3:
            print()
            print(f"Vida do herói: {hero.hp}/{hero.max_hp}")
            print()
            sleep(1)

        elif int(user_choice) == 4:
            print()
            print(f"Experiência do herói: {hero.exp} | Level {hero.level}")
            print()
            sleep(1)
    
        else:
            print("Valor digitado inválido")


if __name__ == "__main__":
    main()
