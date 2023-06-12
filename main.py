"""
Modèle de départ pour la programmation Arcade.
Il suffit de modifier les méthodes nécessaires à votre jeu.
"""
import random
import arcade
from attack_animation import AttackAnimation, AttackType
from game_state import GameState

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45  # 

class MyGame(arcade.Window):
    """
   La classe principale de l'application

   NOTE: Vous pouvez effacer les méthodes que vous n'avez pas besoin.
   Si vous en avez besoin, remplacer le mot clé "pass" par votre propre code.
   """

    PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
    PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
    COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2.5
    ATTACK_FRAME_WIDTH = 154 / 2
    ATTACK_FRAME_HEIGHT = 154 / 2
    PLAYER_ATTACK_X = 140
    PLAYER_ATTACK_Y = 100
    PLAYER_ATTACK_OFFSET = 120
    PLAYER_ATTACK_LARGEUR = 105
    ORDINATEUR_ATTACK_Y = 100

    MESSAGE_NOUVELLE_RONDE = "Appuyer sur 'ESPACE' pour commencer une nouvelle ronde!"
    MESSAGE_NOUVELLE_PARTIE = "Appuyer sur 'ESPACE' pour commencer une nouvelle partie!"
    MESSAGE_START = "Appuyer sur une image pour faire une attaque"
    MESSAGE_ORDI_GAGNE_RONDE = "L'ordinateur a gagné la ronde!"
    MESSAGE_JOUER_GAGNE_RONDE = "Vous avez gagné la ronde!"
    MESSAGE_EGALITE = "Égalité!"
    MESSAGE_JOUER_GAGNE = "Vous avez gagne la partie!"
    MESSAGE_JOUER_GAGNE_2 = "La partie est terminée"

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK_OLIVE)

        self.player = arcade.Sprite("assets/faceBeard.png")
        self.computer = arcade.Sprite("assets/compy.png")
        self.players = arcade.SpriteList()
        self.rock = AttackAnimation(AttackType.ROCK)
        self.paper = AttackAnimation(AttackType.PAPER)
        self.scissors = AttackAnimation(AttackType.SCISSORS)
        self.attack_list = arcade.SpriteList()

        self.player_score = 0
        self.computer_score = 0
        self.player_attack_type = None
        self.computer_attack_type = None
        self.player_attack_chosen = False
        self.player_won_round = False
        self.computer_won_round = False
        self.game_state = GameState.NOT_STARTED

    def setup(self):
        """
       Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
       fois si vous recommencer une nouvelle partie.
       """
        # C'est ici que vous allez créer vos listes de sprites et vos sprites.
        # Prenez note que vous devriez attribuer une valeur à tous les attributs créés dans __init__

        self.player.center_x = self.PLAYER_IMAGE_X
        self.player.center_y = self.PLAYER_IMAGE_Y
        self.computer.center_x = self.COMPUTER_IMAGE_X
        self.computer.center_y = self.COMPUTER_IMAGE_Y
        self.players.append(self.player)
        self.players.append(self.computer)
        self.rock.center_x = self.PLAYER_ATTACK_X
        self.rock.center_y = self.PLAYER_ATTACK_Y
        self.paper.center_x = self.rock.center_x + self.PLAYER_ATTACK_OFFSET
        self.paper.center_y = self.PLAYER_ATTACK_Y
        self.scissors.center_x = self.paper.center_x + self.PLAYER_ATTACK_OFFSET
        self.scissors.center_y = self.PLAYER_ATTACK_Y
        self.attack_list.append(self.rock)
        self.attack_list.append(self.paper)
        self.attack_list.append(self.scissors)

    def validate_victory(self):
        """
       Utilisé pour déterminer qui obtient la victoire (ou s'il y a égalité)
       Rappel: après avoir validé la victoire, il faut changer l'état de jeu
       """
        # On choisi attack type aléatoire
        self.computer_attack_type = random.choice(list(AttackType))

        if self.computer_attack_type == self.player_attack_type:
            # personne n'a pas gagne
            self.player_won_round = False
            self.computer_won_round = False
        elif ((self.computer_attack_type == AttackType.ROCK and self.player_attack_type == AttackType.SCISSORS)
              or (self.computer_attack_type == AttackType.PAPER and self.player_attack_type == AttackType.ROCK)
              or (self.computer_attack_type == AttackType.SCISSORS and self.player_attack_type == AttackType.PAPER)):
            # ordinateur a gagne
            self.computer_score += 1
            self.player_won_round = False
            self.computer_won_round = True
        elif ((self.player_attack_type == AttackType.ROCK and self.computer_attack_type == AttackType.SCISSORS)
              or (self.player_attack_type == AttackType.PAPER and self.computer_attack_type == AttackType.ROCK)
              or (self.player_attack_type == AttackType.SCISSORS and self.computer_attack_type == AttackType.PAPER)):
            # jouer a gagne
            self.player_score += 1
            self.player_won_round = True
            self.computer_won_round = False

    def draw_possible_attack(self):
        """
       Méthode utilisée pour dessiner toutes les possibilités d'attaque du joueur
       (si aucune attaque n'a été sélectionnée, il faut dessiner les trois possibilités)
       (si une attaque a été sélectionnée, il faut dessiner cette attaque)
       """
        self.attack_list.draw()
        self.draw_squares()

    def draw_squares(self):
        arcade.draw_rectangle_outline(self.PLAYER_ATTACK_X, self.PLAYER_ATTACK_Y, 50, 50, [240, 1, 1])
        arcade.draw_rectangle_outline(self.PLAYER_ATTACK_X + 1 * self.PLAYER_ATTACK_OFFSET, self.PLAYER_ATTACK_Y, 50,
                                      50, [240, 1, 1])
        arcade.draw_rectangle_outline(self.PLAYER_ATTACK_X + 2 * self.PLAYER_ATTACK_OFFSET, self.PLAYER_ATTACK_Y, 50,
                                      50, [240, 1, 1])
        arcade.draw_rectangle_outline(self.COMPUTER_IMAGE_X, self.ORDINATEUR_ATTACK_Y, 50,
                                      50, [240, 1, 1])

    def draw_computer_attack(self):
        """
       Méthode utilisée pour dessiner les possibilités d'attaque de l'ordinateur
       """
        computer_attack_sprite = None
        if self.computer_attack_type == AttackType.ROCK:
            computer_attack_sprite = arcade.Sprite("assets/srock.png")
        elif self.computer_attack_type == AttackType.PAPER:
            computer_attack_sprite = arcade.Sprite("assets/spaper.png")
        elif self.computer_attack_type == AttackType.SCISSORS:
            computer_attack_sprite = arcade.Sprite("assets/scissors.png")

        if computer_attack_sprite is not None:
            computer_attack_sprite.center_x = self.COMPUTER_IMAGE_X
            computer_attack_sprite.scale = 0.5
            computer_attack_sprite.center_y = 100
            computer_attack_sprite.draw()

    def draw_scores(self):
        """
       Montrer les scores du joueur et de l'ordinateur
       """
        arcade.draw_text(f"Le pointage de joueur est {self.player_score}", 100, 40, arcade.color.WHITE, 16)
        arcade.draw_text(f"Le pointage de l'ordinateur est {self.computer_score}", 600, 40, arcade.color.WHITE, 16)
        # pass

    def draw_instructions(self):
        """
       Dépendemment de l'état de jeu, afficher les instructions d'utilisation au joueur (appuyer sur espace, ou sur une image)
       """
        if self.game_state == GameState.NOT_STARTED:
            arcade.draw_text(self.MESSAGE_NOUVELLE_PARTIE,
                             0,
                             SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 4,
                             arcade.color.TURQUOISE,
                             35,
                             width=SCREEN_WIDTH,
                             align="center")
        if self.game_state == GameState.ROUND_DONE:
            if self.player_won_round:
                msg_resultat = self.MESSAGE_JOUER_GAGNE_RONDE
            elif self.computer_won_round:
                msg_resultat = self.MESSAGE_ORDI_GAGNE_RONDE
            else:
                msg_resultat = self.MESSAGE_EGALITE
            arcade.draw_text(self.MESSAGE_NOUVELLE_RONDE,
                             0,
                             SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 3,
                             arcade.color.TURQUOISE,
                             35,
                             width=SCREEN_WIDTH,
                             align="center")
            arcade.draw_text(msg_resultat,
                             0,
                             SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 6,
                             arcade.color.TURQUOISE,
                             35,
                             width=SCREEN_WIDTH,
                             align="center")
        if self.game_state == GameState.ROUND_ACTIVE:
            arcade.draw_text(self.MESSAGE_START,
                            0,
                            SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 4,
                            arcade.color.TURQUOISE,
                            35,
                            width=SCREEN_WIDTH,
                            align="center")
        if self.game_state == GameState.GAME_OVER:
            msg_resultat = self.MESSAGE_ORDI_GAGNE_RONDE
            if self.player_score == 3:
                msg_resultat = self.MESSAGE_JOUER_GAGNE
            arcade.draw_text(msg_resultat,
                             0,
                             SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 6,
                             arcade.color.TURQUOISE,
                             35,
                             width=SCREEN_WIDTH,
                             align="center")

    def on_draw(self):
        """
       C'est la méthode que Arcade invoque à chaque "frame" pour afficher les éléments
       de votre jeu à l'écran.
       """

        # Cette commande permet d'effacer l'écran avant de dessiner. Elle va dessiner l'arrière
        # plan selon la couleur spécifié avec la méthode "set_background_color".
        arcade.start_render()

        # Display title
        arcade.draw_text(SCREEN_TITLE,
                         0,
                         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                         arcade.color.BLACK_BEAN,
                         60,
                         width=SCREEN_WIDTH,
                         align="center")

        self.draw_instructions()
        self.players.draw()

        if self.game_state != GameState.NOT_STARTED:
            self.draw_possible_attack()
            self.draw_scores()
            self.draw_computer_attack()

    def on_update(self, delta_time):
        """
       Toute la logique pour déplacer les objets de votre jeu et de
       simuler sa logique vont ici. Normalement, c'est ici que
       vous allez invoquer la méthode "update()" sur vos listes de sprites.
       Paramètre:
           - delta_time : le nombre de milliseconde depuis le dernier update.
       """
        # vérifier si le jeu est actif (ROUND_ACTIVE) et continuer l'animation des attaques
        # si le joueur a choisi une attaque, générer une attaque de l'ordinateur et valider la victoire
        # changer l'état de jeu si nécessaire (GAME_OVER)
        if self.game_state == GameState.ROUND_DONE:
            self.attack_list.on_update()

        if self.game_state == GameState.ROUND_ACTIVE and self.player_attack_chosen:
            self.validate_victory()

            self.draw_scores()
            # self.player_attack_chosen = False
            self.player_attack_chosen = False
            # self.rock.visible = True
            self.game_state = GameState.ROUND_DONE
            if self.player_score == 3 or self.computer_score == 3:
                self.game_state = GameState.GAME_OVER

    def on_key_press(self, key, key_modifiers):
        """
       Cette méthode est invoquée à chaque fois que l'usager tape une touche
       sur le clavier.
       Paramètres:
           - key: la touche enfoncée
           - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?

       Pour connaître la liste des touches possibles:
       http://arcade.academy/arcade.key.html
       """
        if 32 == key:
            if GameState.NOT_STARTED == self.game_state:
                self.game_state = GameState.ROUND_ACTIVE
                self.attack_visible()
            elif GameState.ROUND_DONE == self.game_state:
                # N'oubliez pas de remettre à faux ou 0 toutes variables qui sert à la validation
                self.attack_visible()
                self.computer_attack_type = None
                self.game_state = GameState.ROUND_ACTIVE
            elif GameState.GAME_OVER == self.game_state:
                self.player_score = 0
                self.computer_score = 0
                self.computer_attack_type = None
                self.game_state = GameState.NOT_STARTED

    def attack_visible(self):
        self.rock.visible = True
        self.paper.visible = True
        self.scissors.visible = True

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
       Méthode invoquée lorsque l'usager clique un bouton de la souris.
       Paramètres:
           - x, y: coordonnées où le bouton a été cliqué
           - button: le bouton de la souris appuyé
           - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
       """

        # Test de collision pour le type d'attaque (self.player_attack_type).
        # Rappel que si le joueur choisi une attaque, self.player_attack_chosen = True
        if self.game_state != GameState.ROUND_ACTIVE or self.player_attack_chosen:
            return
        if self.rock.collides_with_point((x, y)):
            self.player_attack_type = AttackType.ROCK
            self.player_attack_chosen = True
            self.paper.visible = False
            self.scissors.visible = False
        elif self.paper.collides_with_point((x, y)):
            self.player_attack_type = AttackType.PAPER
            self.player_attack_chosen = True
            self.rock.visible = False
            self.scissors.visible = False
        elif self.scissors.collides_with_point((x, y)):
            self.player_attack_type = AttackType.SCISSORS
            self.player_attack_chosen = True
            self.rock.visible = False
            self.paper.visible = False

def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
