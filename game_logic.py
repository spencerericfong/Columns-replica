#Spencer Fong (45162908)

import re
import random

class GameLogic:

    def __init__(self):
        '''Self explanatory? All the shared variables used to make the game work'''
        self._num_rows = 12
        self._num_columns = 6
        self._field = []
        self._run = True
        self._game_over = False
        self._jewels = 'ABCDEFGHIJ'
        
        self._faller = None
        self._faller_exist = False
        self._faller_clear = True
        self._faller_index = 2
        self._drop_row = 0
        self._drop_column = 0
        self._rotate_index = 0
        self._landed_state = False
        self._out_of_bounds_var = False        
        
        self._match_made = False
        self._delete = False



    def get_num_rows_columns(self, rows_columns: [int]) -> None:
        '''Gets the number of rows and columns'''
        self._num_rows = rows_columns[0]
        self._num_columns = rows_columns[1]



    def create_blank_field(self) -> None:
        for row in range(self._num_rows):
            blank_row = ['   ', '   ', '   ', '   ', '   ', '   ']
            self._field.append(blank_row)



    def change_field(self, rows: [str]) -> None:
        '''Takes a new list of rows and updates the game field'''
        field_new = []
        for row in rows:
                field_new.append(row)
        self._field = field_new[:]



    def print_field(self) -> None:
        '''Prints out the field'''
        for line in self._field:
            print_row = '|'
            for things in line:
                print_row += things
            print_row += '|'
            print(print_row)
        bottom_line = '---' * self._num_columns
        print(' ' + bottom_line + ' ')



    def time_pass(self) -> [str]:
        '''Acts as passing of time and changes field accordingly'''
        field_new = self._field[:]
        rotate_hold = True  #Used to prevent rotation index from messing up

        if self._check_match() == True and self._delete == True:
            field_new = self._delete_match()

        if self.existing_faller() == False and self.faller_clear():
            field_new = self.drop_faller()

        elif self.existing_faller() and self.faller_clear():
            for row in range(self._num_rows):
                for column in range(self._num_columns):
                    piece = field_new[row][column]
                    if '[' in piece:
                        if self._faller_index > 0:
                            self._faller_index -= 1
                            
                        field_new = self.drop_faller()

                        self._rotate_index += 1
                        if self._rotate_index == 3 and rotate_hold == True:
                            self._rotate_index -= 1
                            rotate_hold = False                    
                        return field_new

                    elif '|' in piece:
                        self._rotate_index += 1
                        if self._rotate_index == 3 and rotate_hold == True:
                            self._rotate_index -= 1
                            rotate_hold = False
                    
                    else:
                        pass

        elif self.faller_clear() == False and self._landed_state == False:
            field_new = self._faller_landed()

        elif self._landed_state == True and self._delete == False:
            field_new = self._faller_frozen()
            
        
        return field_new



    def create_faller(self) -> None:
        '''Creates a faller in a random column with random jewels'''
        self._drop_column = random.randint(0, 5)
        
        faller = [] 
        for jewel in range(3):
            faller.append('[' + random.choice(self._jewels) + ']')

        self._faller = faller
        self._landed_state = False
        self._delete = False



    def existing_faller(self) -> bool:
        '''Checks the board for an already existing faller'''
        for row in range(self._num_rows):
            for column in range(self._num_columns):
                piece = self._field[row][column]
                if '[' in piece or '|' in piece:
                    self._faller_exist = True
        return self._faller_exist



    def faller_clear(self) -> bool:
        '''Checks if a faller can continue falling'''
        new_field = self._field[:]
        
        if self._drop_row < self._num_rows:
            if new_field[self._drop_row][self._drop_column] != '   ':
                self._faller_clear = False

        elif self._drop_row == self._num_rows:
            self._faller_clear = False

        return self._faller_clear
    

    
    def drop_faller(self) -> [str]:
        '''Drops the current faller within a new field'''
        faller = self._faller[:]
        new_field = self._field[:]
        
        if self._faller_index == 2:
            new_field[self._drop_row][self._drop_column] = faller[
                self._faller_index]
            
        elif self._faller_index == 1:            
            new_field[self._drop_row - 1][self._drop_column] = faller[
                self._faller_index]
            
            new_field[self._drop_row][self._drop_column] = faller[
                self._faller_index + 1]
            
        elif self._faller_index == 0:
            new_field[self._drop_row - 2][self._drop_column] = faller[
                self._faller_index]
    
            new_field[self._drop_row - 1][self._drop_column] = faller[
                self._faller_index + 1]
            
            new_field[self._drop_row][self._drop_column] = faller[
                self._faller_index + 2]
            
            if self._drop_row >= 3:               
                new_field[self._drop_row - 3][self._drop_column] = '   '        

        self._drop_row += 1

        return new_field



    def _faller_landed(self) -> [str]:
        '''Changes faller to indicate it has landed'''
        new_field = self._field[:]
        faller_copy = self._faller[:]
        landed_faller_chars = []
        landed_faller = []

        for jewel in faller_copy:
            faller_chars = list(jewel)
            for char in faller_chars:
                landed_faller_chars.append(char)

        landed_faller.append(landed_faller_chars[1])
        landed_faller.append(landed_faller_chars[4])
        landed_faller.append(landed_faller_chars[7])
        landed_faller = ['|' + jewel + '|' for jewel in landed_faller]

        self._faller = landed_faller

        for row in range(self._num_rows):
            for column in range(self._num_columns):
                piece = new_field[row][column]

                if piece == faller_copy[0]:
                    piece = landed_faller[0]
                elif piece == faller_copy[1]:
                    piece = landed_faller[1]
                elif piece == faller_copy[2]:
                    piece = landed_faller[2]
                new_field[row][column] = piece

        self._landed_state = True

        if self._out_of_bounds() == True:
            self._run = False
            self._game_over = True

        return new_field



    def _out_of_bounds(self) -> bool:
        '''Checks if landed faller is fully displayed or not'''
        new_field = self._field[:]
        for row in range(self._num_rows):
            for column in range(self._num_columns):
                piece = new_field[row][column]
                if '|' in piece:
                    if '|' in new_field[row + 2][column]:
                        return self._out_of_bounds_var
                    else:
                        self._out_of_bounds_var = True
                        return self._out_of_bounds_var

                elif row == 0 and piece != '   ':
                    if self._drop_column == column:
                        self._out_of_bounds_var = True
                        return self._out_of_bounds_var

        return self._out_of_bounds_var



    def _faller_frozen(self) -> [str]:
        '''If a faller is landed, freezes it, then checks for matches
                and deals with them accordingly'''
        new_field = self._field[:]
        faller_copy = self._faller[:]
        frozen_faller_chars = []
        frozen_faller = []

        for jewel in faller_copy:
            faller_chars = list(jewel)
            for char in faller_chars:
                frozen_faller_chars.append(char)

        frozen_faller.append(frozen_faller_chars[1])
        frozen_faller.append(frozen_faller_chars[4])
        frozen_faller.append(frozen_faller_chars[7])
        frozen_faller = [' ' + jewel + ' ' for jewel in frozen_faller]

        self._faller = None

        for row in range(self._num_rows):
            for column in range(self._num_columns):
                piece = new_field[row][column]

                if piece == faller_copy[0]:
                    piece = frozen_faller[0]
                elif piece == faller_copy[1]:
                    piece = frozen_faller[1]
                elif piece == faller_copy[2]:
                    piece = frozen_faller[2]
                new_field[row][column] = piece
        
        self._reset()

        self._field = new_field

        return self._matches()
           

    def rotate_faller(self) -> [str]:
        '''Rotates the faller'''
        new_field = self._field[:]
        if self._faller != None:
            faller = self._faller[:]
            index = 2
            index_reverse = 0

            faller[0], faller[1], faller[2] = faller[2], faller[0], faller[1]
            self._faller = faller

            for row in range(self._num_rows):
                for column in range(self._num_columns):
                    piece = new_field[row][column]
                    if '[' in piece or '|' in piece:
                        new_field[row][column] = self._faller[
                            index - self._rotate_index]   
                        index += 1

        return new_field



    def move_faller(self, arrow: str) -> [str]:
        '''Moves the faller from one column to another'''
        new_field = self._field[:]

        
        if arrow == '<':
            if (self._drop_column > 0 and new_field[self._drop_row - 1][
                self._drop_column - 1] == '   '):
                self._drop_column -= 1
                

                for row in range(self._num_rows):
                    for column in range(self._num_columns):
                        piece = new_field[row][column]
                        if '[' in piece or '|' in piece:
                            new_field[row][column - 1] = new_field[row][column]
                            new_field[row][column] = '   '
                            break
            else:
                pass
            
        elif arrow == '>':
            if (self._drop_column < self._num_columns - 1 and new_field[
                    self._drop_row - 1][self._drop_column + 1] == '   '):
                self._drop_column += 1

                for row in range(self._num_rows):
                    for column in range(self._num_columns):
                        piece = new_field[row][column]
                        if '[' in piece or '|' in piece:
                            new_field[row][column + 1] = new_field[row][column]
                            new_field[row][column] = '   '
                            break
            else:
                pass
            
        return new_field



    def _matches(self) -> [str]:
        '''Checks the board for any matches, then deals with them accordingly'''
        new_field = self._field[:]
        match_coords = []

        for row in range(self._num_rows):
            for column in range(self._num_columns - 2):
                piece = new_field[row][column]
                
                if re.search('[A-Z]', piece):
                
                    piece_chars = list(piece)
                    jewel = piece_chars[1]

                    if (jewel in new_field[row][column + 1] and
                            jewel in new_field[row][column + 2]):
                        match_coords.append([row, column])
                        match_coords.append([row, column + 1])
                        match_coords.append([row, column + 2])                   
                    
        for row in range(self._num_rows - 2):
            for column in range(self._num_columns):
                piece = new_field[row][column]

                if re.search('[A-Z]', piece):
                    
                    piece_chars = list(piece)
                    jewel = piece_chars[1]
                    
                    if (jewel in new_field[row + 1][column] and
                            jewel in new_field[row + 2][column]):
                        match_coords.append([row, column])
                        match_coords.append([row + 1, column])
                        match_coords.append([row + 2, column])
        
        for row in range(self._num_rows - 2):
            for column in range(self._num_columns - 2):
                piece = new_field[row][column]

                if re.search('[A-Z]', piece):

                    piece_chars = list(piece)
                    jewel = piece_chars[1]

                    if (jewel in new_field[row + 1][column + 1] and
                            jewel in new_field[row + 2][column + 2]):
                        match_coords.append([row, column])
                        match_coords.append([row + 1, column + 1])
                        match_coords.append([row + 2, column + 2])

        for row in range(self._num_rows - 2):
            for column in range(self._num_columns - 1, 1, -1):
                piece = new_field[row][column]

                if re.search('[A-Z]', piece):
                    piece_chars = list(piece)
                    jewel = piece_chars[1]

                    if (jewel in new_field[row + 1][column - 1] and
                            jewel in new_field[row + 2][column - 2]):
                        match_coords.append([row, column])
                        match_coords.append([row + 1, column - 1])
                        match_coords.append([row + 2, column - 2])

                
        if len(match_coords) != 0:
            return self._match_change(match_coords)
        else:
            return new_field



    def _match_change(self, match_coords: [[str]]) -> [str]:
        '''Changes jewels to represent they match'''
        new_field = self._field[:]

        for coords in match_coords:
            coord = []
            matched_piece = []
            coord.append(coords[0])
            coord.append(coords[1])
            piece = new_field[coord[0]][coord[1]]
            jewel = list(piece)
            matched_piece.append(jewel[1])            
            new_field[coord[0]][coord[1]] = '*' + jewel[1] + '*'

        self._delete = True

        return new_field
                


    def _check_match(self) -> bool:
        '''Checks the field to see if any matches have been made'''
        new_field = self._field[:]
        
        for row in range(self._num_rows):
            for column in range(self._num_columns):
                piece = new_field[row][column]

                if '*' in piece:
                    self._match_made = True
                    self._delete = True
                    return self._match_made

        return self._match_made



    def _delete_match(self) -> None:
        '''If there are any matches, deletes the matched jewels'''
        new_field = self._field[:]

        for row in range(self._num_rows):
            for column in range(self._num_columns):
                piece = new_field[row][column]

                if '*' in piece:
                    new_field[row][column] = '   '
                    
        self._field = new_field[:]
        self._match_made = False
        self._delete = False

        return self._gravity()



    def _gravity(self) -> [str]:
        '''If matches have been deleted, moves jewels above the deleted ones
            down'''
        new_field = self._field[:]

        for row in range(self._num_rows - 1):
            for column in range(self._num_columns):
                piece = new_field[row][column]
                if new_field[row + 1][column] == '   ':
                    for row2 in range(row, -1, -1):
                        piece = new_field[row2][column]
                        new_field[row2 + 1][column] = piece
                        if row2 == 0:
                            new_field[row2][column] = '   '

        self._field = new_field[:]
    
        return self._matches()
                    


    def _reset(self) -> None:
        '''Resets faller counters, etc'''
        self._faller_exist = False
        self._faller_clear = True
        self._drop_row = 0
        self._faller_index = 2
        self._rotate_index = 0

          

    def start_content(self) -> [str]:
        '''Determines if field is empty or has jewels, returns list of content'''
        content_or_empty = input()
        content = []
        
        if content_or_empty.upper() == 'CONTENTS':
            for row in range(self._num_rows):
                start_jewels = input()
                content_row = list(start_jewels)
                content_row = [' ' + jewel + ' ' for jewel in content_row]
                content.append(content_row)
        elif content_or_empty.upper() == 'EMPTY':
            for empty_row in range(self._num_rows):
                single_row = []
                for column in range(self._num_columns):
                    single_row.append('   ')
                content.append(single_row)

        return content



    def game_run(self) -> bool:
        '''Returns switch that ends game'''
        return self._run



    def game_quit(self) -> None:
        '''Ends the game if player quits'''
        self._run = False



    def game_fail(self) -> bool:
        '''If the game is failed, ends the game'''
        return self._game_over
