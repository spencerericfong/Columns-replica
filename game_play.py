#Spencer Fong (45162908)
#run this one
import game_logic
import pygame

class GameBoard:
    
    def __init__(self):
        self._running = True
        self._size = (450, 900)
        self._game = game_logic.GameLogic()
        
        self.BLACK = (0, 0, 0)
        self.GREY = (110, 110, 110)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (255, 0, 255)
        self.SKY = (0, 255, 255)
        self.ORANGE = (255, 127, 0)
        self.PINK = (255, 0, 127)
        self.LIME = (0, 255, 127)
        self.BROWN = (165, 42, 42)
        

    def run(self) -> None:
        '''Runs the game'''
        pygame.init()
        
        self._game.create_blank_field()
        self._resize_surface(self._size)
        
        clock = pygame.time.Clock()
        game_over_clock = pygame.time.Clock()
        update_counter = 0
        game_end_counter = 0

        while self._running:
            clock.tick(30)
            update_counter += 1
            self._handle_events()
            
            if update_counter == 15:
                self._make_faller()
                self._game.change_field(self._game.time_pass())
                update_counter = 0

            self._redraw()

            if self._game._game_over:
                game_over_clock.tick(30)
                game_end_counter += 1
                if game_end_counter == 60:
                    self._redraw()
                    self._running = False
      
        pygame.quit()


    def _handle_events(self) -> None:
        '''Handles resizing and valid keypresses, otherwise keeps the game
            functioning'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == 'space':
                    self._space_key()
                elif (pygame.key.name(event.key) == 'left' or
                          pygame.key.name(event.key) == 'right'):
                    self._arrow_key(pygame.key.name(event.key))


    def _redraw(self) -> None:
        '''Redraws the game board with each update of time'''
        surface = pygame.display.get_surface()

        surface.fill(self.BLACK)

        self._draw_grid(surface)

        self._draw_jewels()

        pygame.display.flip()


    def _draw_grid(self, surface) -> None:
        '''Draws the game grid'''
        for column_markers in range(1, 7):
            pygame.draw.line(surface, self.GREY, [(self._size[0] / 6)
                                * column_markers, 0], [(self._size[0] / 6)
                                        * column_markers, self._size[1]], 2)
        for row_markers in range(1, 13):
            pygame.draw.line(surface, self.GREY, [0, (self._size[1] / 12)
                                * row_markers], [self._size[0],
                                    (self._size[1] / 12) * row_markers], 2)


    def _draw_jewels(self) -> None:
        '''Draws all the jewels on the board'''
        surface = pygame.display.get_surface()
        color = None
        field = self._game._field

        if self._game._game_over:
            self._draw_end_game()

        else:
            for row in range(self._game._num_rows):
                for column in range(self._game._num_columns):
                    jewel = field[row][column]
                    piece = list(jewel)
                        
                    if piece[1] == 'A':
                        color = self.RED
                    elif piece[1] == 'B':
                        color = self.GREEN
                    elif piece[1] == 'C':
                        color = self.BLUE
                    elif piece[1] == 'D':
                        color = self.YELLOW
                    elif piece[1] == 'E':
                        color = self.PURPLE
                    elif piece[1] == 'F':
                        color = self.SKY
                    elif piece[1] == 'G':
                        color = self.ORANGE
                    elif piece[1] == 'H':
                        color = self.PINK
                    elif piece[1] == 'I':
                        color = self.LIME
                    elif piece[1] == 'J':
                        color = self.BROWN

                    if jewel != '   ':
                        self._draw_jewel(surface, color, row, column)
                    if piece[0] == '[':
                        self._draw_faller_dot(surface, row, column)
                    elif piece[0] == '|':
                        self._draw_landed_dot(surface, row, column)
                    elif piece[0] == '*':
                        self._draw_matched_dot(surface, row, column)
            

    def _draw_jewel (self, surface: pygame.Surface, color: pygame.Color,
                         row: int, column: int) -> None:
        '''Draws each individual jewel'''
        pygame.draw.rect(surface, color, (self._size[0]
                                         / 6 * column + 13, self._size[1] / 12
                                            * row + 13, self._size[0] / 6 - 24
                                            , self._size[1] / 12 - 24))


    def _draw_faller_dot (self, surface: pygame.Surface, row: int,
                              column: int) -> None:
        '''Draws a white dot on a jewel that is part of a still-falling faller'''
        pygame.draw.circle(surface, self.WHITE, (int(self._size[0] / 6 *
                                column + 38), int(self._size[1] / 12 *
                                    row + 38)), 10)


    def _draw_landed_dot (self, surface: pygame.Surface, row: int,
                              column: int) -> None:
        '''Draws a grey dot on a jewel that is part of a faller that has landed'''
        pygame.draw.circle(surface, self.GREY, (int(self._size[0] / 6 *
                                column + 38), int(self._size[1] / 12 *
                                    row + 38)), 10)


    def _draw_matched_dot (self, surface: pygame.Surface, row: int,
                               column: int) -> None:
        '''Draws a black dot on a jewel that is part of a matched set'''
        pygame.draw.circle(surface, self.BLACK, (int(self._size[0] / 6 *
                                column + 38), int(self._size[1] / 12 *
                                    row + 38)), 10)


    def _draw_end_game (self):
        '''If the game is over, makes all jewels white'''
        surface = pygame.display.get_surface()
        field = self._game._field[:]
        for row in range(self._game._num_rows):
            for column in range(self._game._num_columns):
                jewel = field[row][column]

                if jewel != '   ':
                    pygame.draw.rect(surface, self.WHITE, (self._size[0]
                                         / 6 * column + 13, self._size[1] / 12
                                            * row + 13, self._size[0] / 6 - 24
                                            , self._size[1] / 12 - 24))


    def _make_faller(self) -> None:
        '''Makes a random faller'''
        if self._game.existing_faller() == False:
            self._game.create_faller()


    def _end_game(self) -> None:
        '''Ends the game'''
        self._running = False


    def _resize_surface(self, size: (int, int)) -> None:
        '''Enables the game window to be resized'''
        pygame.display.set_mode(size, pygame.RESIZABLE)
        self._size = size
        

    def _space_key(self) -> None:
        '''Handles event if space key is pressed'''
        self._game.change_field(self._game.rotate_faller())


    def _arrow_key(self, name: str) -> None:
        '''Handles event if the side arrow keys are pressed'''
        if name == 'left':
            self._game.change_field(self._game.move_faller('<'))
        elif name == 'right':
            self._game.change_field(self._game.move_faller('>'))



if __name__ == '__main__':
    GameBoard().run()
