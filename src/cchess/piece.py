# -*- coding: utf-8 -*-
'''
Copyright (C) 2014  walker li <walker8088@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys

#from sets import *
from enum import *

#-----------------------------------------------------#
#todo 英文全角半角统一识别
h_level_index = (
  (),
  ("九","八","七","六","五","四","三","二","一"),
  ("１","２","３","４","５","６","７","８","９")
)

v_change_index = (
  (), 
  ("错", "一", "二", "三", "四", "五", "六", "七", "八", "九"),
  ("误", "１", "２", "３", "４", "５", "６", "７", "８", "９")
)

#-----------------------------------------------------#
advisor_pos = ((),
    ((3, 0), (5, 0), (4, 1), (3, 2), (5, 2)),
    ((3, 9), (5, 9), (4, 8), (3, 7), (5, 7)) 
    )

bishop_pos = ((),
    ((2, 0), (6, 0), (0, 2), (4, 2), (9, 2), (2, 4), (6, 4)),
    ((2, 9), (6, 9), (0, 7), (4, 7), (9, 7), (2, 5), (6, 5)) 
    )

#-----------------------------------------------------#
class ChessSide(IntEnum):
    NO_SIDE = 0
    RED = 1
    BLACK = 2

    @staticmethod
    def next_side(side):
        if side == ChessSide.NO_SIDE : return ChessSide.NO_SIDE
        return ChessSide.RED if side == ChessSide.BLACK else ChessSide.BLACK
        
#-----------------------------------------------------#
'''
class PieceT(IntEnum):
    KING = 1
    ADVISOR = 2
    BISHOP = 3
    KNIGHT = 4
    ROOK = 5
    CANNON = 6
    PAWN = 7
'''
#-----------------------------------------------------#
'''
fench_species_dict = {
    'k': PieceT.KING,
    'a': PieceT.ADVISOR,
    'b': PieceT.BISHOP,
    'n': PieceT.KNIGHT,
    'r': PieceT.ROOK,
    'c': PieceT.CANNON,
    'p': PieceT.PAWN
}
'''
#-----------------------------------------------------#
fench_name_dict = {
    'K': "帅",
    'k': "将",
    'A': "仕",
    'a': "士",
    'B': "相",
    'b': "象",
    'N': "马",
    'n': "马",
    'R': "车",
    'r': "车",
    'C': "炮",
    'c': "炮",
    'P': "兵",
    'p': "卒"
}

#-----------------------------------------------------#
name_fench_dict = {
    "帅":'K',
    "将":'k',
    "仕":'A',
    "士":'a',
    "相":'B',
    "象":'b',
    "马":'n',
    "车":'r',
    "炮":'c',
    "兵":'P',
    "卒":'p'
}

_fench_txt_name_dict = {
    'K': u"帅",
    'k': u"将",
    'A': u"仕",
    'a': u"士",
    'B': u"相",
    'b': u"象",
    'N': u"马",
    'n': u"碼",
    'R': u"车",
    'r': u"砗",
    'C': u"炮",
    'c': u"砲",
    'P': u"兵",
    'p': u"卒"
}


def _fench_to_txt_name(fench):
    return _fench_txt_name_dict[fench]
    
#-----------------------------------------------------#
'''
species_fench_dict = {
    PieceT.KING: ('K', 'k'),
    PieceT.ADVISOR: ('A', 'a'),
    PieceT.BISHOP: ('B', 'b'),
    PieceT.KNIGHT: ('N', 'n'),
    PieceT.ROOK: ('R', 'r'),
    PieceT.CANNON: ('C', 'c'),
    PieceT.PAWN: ('P', 'p')
}
'''
#-----------------------------------------------------#
def fench_to_chinese(fench):
    return fench_name_dict[fench]

def chinese_to_fench(chinese, side):
    fench = name_fench_dict[chinese]
    return fench.lower() if side == ChessSide.BLACK else fench.upper()
    
def fench_to_species(fen_ch):
    return fen_ch.lower(), ChessSide.BLACK if fen_ch.islower() else ChessSide.RED

def species_to_fench(species, side):
    return species_fench_dict[species][side]

    
#-----------------------------------------------------#
#KING, ADVISOR, BISHOP, KNIGHT, ROOK, CANNON, PAWN
'''
chessman_show_name_dict = {
    PieceT.KING: ("帅", "将"),
    PieceT.ADVISOR: ("仕", "士"),
    PieceT.BISHOP: ("相", "象"),
    PieceT.KNIGHT: ("马", "碼"),
    PieceT.ROOK: ("车", "砗"),
    PieceT.CANNON: ("炮", "砲"),
    PieceT.PAWN: ("兵", "卒")
}

def get_show_name(species, side):
    return chessman_show_name_dict[species][side]
'''
#-----------------------------------------------------#
def abs_diff(x, y):
     return (abs(x[0]-y[0]), abs(x[1]-y[1]))

def middle_p(x,y):
    return ((x[0]+y[0])//2, (x[1]+y[1])//2) 
    
#-----------------------------------------------------#
class Piece(object):
    def __init__(self, board, fench, pos):

        self.board = board
        self.fench = fench

        self.species, self.side = fench_to_species(fench)

        self.x, self.y = pos

    def is_valid_pos(self, pos):
        return True if (0 <= pos[0] < 9) and (0 <= pos[1] <=9) else False 

    def is_valid_move(self, pos):
        return True

    @staticmethod
    def create(board, fench, pos):
        if fench == None: 
            return None
        p_type = fench.lower()
        if p_type == 'k':
            return King(board, fench, pos)
        if p_type == 'a':
            return Advisor(board, fench, pos)
        if p_type == 'b':
            return Bishop(board, fench, pos)
        if p_type == 'r':
            return Rook(board, fench, pos)
        if p_type == 'c':
            return Cannon(board, fench, pos)
        if p_type == 'n':
            return Knight(board, fench, pos)
        if p_type == 'p':
            return Pawn(board, fench, pos)
     
#-----------------------------------------------------#
#王
class King(Piece):
    def is_valid_pos(self, pos):
        if not super().is_valid_pos(pos):
            return False
            
        if pos[0] < 3 or pos[0] > 5:
            return False

        if (self.side == ChessSide.RED) and pos[1] > 2:
            return False

        if (self.side == ChessSide.BLACK) and pos[1] < 7:
            return False

        return True

    def is_valid_move(self, pos):

        #face to face
        k2 = self.board.get_king(ChessSide.next_side(self.side))
        if self.x == k2.x and (self.board.count_y_line_in(self.x, self.y, k2.y) == 0):
           return True

        if not self.is_valid_pos(pos):
            return False

        diff = abs_diff(pos,(self.x, self.y))

        return True if ((diff[0] + diff[1]) == 1) else False

    def create_moves(self):
        poss = [
            (self.x + 1, self.y),
            (self.x - 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1), 
        ]
        
        k2 = self.board.get_king(ChessSide.next_side(self.side))
        poss.append((k2.x, k2.y))
        
        curr_pos = (self.x, self.y)
        moves = [(curr_pos, to_pos) for to_pos in poss]
        return filter(self.board.is_valid_move_t, moves)


#-----------------------------------------------------#
#士
class Advisor(Piece):
    def is_valid_pos(self, pos):
        if not super().is_valid_pos(pos):
            return False
        return True if pos in advisor_pos[self.side] else False

    def is_valid_move(self, pos):
         
        if not self.is_valid_pos(pos):
            return False

        if abs_diff((self.x, self.y), pos) == (1, 1):
            return True

        return False

    def create_moves(self):
        poss = [
            (self.x + 1, self.y + 1),
            (self.x + 1, self.y - 1),
            (self.x - 1, self.y + 1),
            (self.x - 1, self.y - 1)
        ]
        curr_pos = (self.x, self.y)
        moves = [(curr_pos, to_pos) for to_pos in poss]
        return filter(self.board.is_valid_move_t, moves)


#-----------------------------------------------------#
#象
class Bishop(Piece):
    def is_valid_pos(self, pos):
        if not super().is_valid_pos(pos):
            return False
        
        return True if pos in bishop_pos[self.side] else False

    def is_valid_move(self, pos):
        if abs_diff((self.x, self.y), (pos)) != (2, 2):
            return False

        #塞象眼检查
        if self.board.get_fench(middle_p((self.x, self.y), pos)) != None:
            return False
        
        #象过河检查
        if (self.side == ChessSide.RED) and (pos[1] > 4):
            return False
        if (self.side == ChessSide.BLACK) and (pos[1] < 5):
            return False

        return True

    def create_moves(self):
        poss = [
            (self.x + 2, self.y + 2),
            (self.x + 2, self.y - 2),
            (self.x - 2, self.y + 2),
            (self.x - 2, self.y - 2)
        ]
        curr_pos = (self.x, self.y)
        moves = [(curr_pos, to_pos) for to_pos in poss]
        return filter(self.board.is_valid_move_t, moves)


#-----------------------------------------------------#
#马
class Knight(Piece):
    def is_valid_move(self, pos):
        if (abs(self.x - pos[0]) == 2) and (abs(self.y - pos[1]) == 1):
            m_x = (self.x + pos[0]) // 2
            m_y = self.y
            
            #别马腿检查
            if self.board.get_fench((m_x, m_y)) != None:
                return False
            else:
                return True
                
        if (abs(self.x - pos[0]) == 1) and (abs(self.y - pos[1]) == 2):
            m_x = self.x
            m_y = (self.y + pos[1]) // 2
            #别马腿检查
            if self.board.get_fench((m_x, m_y)) != None:
                return False
            else:
                return True
        return False

    def create_moves(self):
        poss = [
            (self.x + 1, self.y + 2),
            (self.x + 1, self.y - 2),
            (self.x - 1, self.y + 2),
            (self.x - 1, self.y - 2),
            (self.x + 2, self.y + 1),
            (self.x + 2, self.y - 1),
            (self.x - 2, self.y + 1),
            (self.x - 2, self.y - 1),
        ]
        curr_pos = (self.x, self.y)
        moves = [(curr_pos, to_pos) for to_pos in poss]
        return filter(self.board.is_valid_move_t, moves)


#-----------------------------------------------------#
#车
class Rook(Piece):
    def is_valid_move(self, pos):
        if self.x != pos[0]:
            #斜向移动是非法的
            if self.y != pos[1]:
                return False

            #水平移动
            if self.board.count_x_line_in(self.y, self.x, pos[0]) == 0:
                return True

        else:
            #垂直移动
            if self.board.count_y_line_in(self.x, self.y, pos[1]) == 0:
                return True

        return False

    def create_moves(self):
        moves = []
        curr_pos = (self.x, self.y)
        for x in range(9):
            for y in range(10):
                if self.x == x and self.y == y:
                    continue
                moves.append((curr_pos, (x, y)))
        return filter(self.board.is_valid_move_t, moves)


#-----------------------------------------------------#
#炮
class Cannon(Piece):
    def is_valid_move(self, pos):

        if self.x != pos[0]:
            #斜向移动是非法的
            if self.y != pos[1]:
                return False

            #水平移动
            count = self.board.count_x_line_in(self.y, self.x, pos[0])
            if (count == 0) and (self.board.get_fench(pos) == None):
                return True
            if (count == 1) and (self.board.get_fench(pos) != None):
                return True
        else:
            #垂直移动
            count = self.board.count_y_line_in(self.x, self.y, pos[1])
            if (count == 0) and (self.board.get_fench(pos) == None):
                return True
            if (count == 1) and (self.board.get_fench(pos) != None):
                return True

        return False

    def create_moves(self):
        moves = []
        curr_pos = (self.x, self.y)
        for x in range(9):
            for y in range(10):
                if self.x == x and self.y == y:
                    continue
                moves.append((curr_pos, (x, y)))
        return filter(self.board.is_valid_move_t, moves)


#-----------------------------------------------------#
#兵/卒
class Pawn(Piece):
    def is_valid_pos(self, pos):
        
        if not super().is_valid_pos(pos):
            return False
        
        if (self.side == ChessSide.RED) and pos[1] < 3:
            return False

        if (self.side == ChessSide.BLACK) and pos[1] > 6:
            return False

        return True

    def is_valid_move(self, pos):

        not_crossed_river_step = ((),(0, 1), (0, -1))
        crossed_river_step = ((),((-1, 0), (1, 0), (0, 1)), ((-1, 0), (1, 0), (0,
                                                                         -1)))

        step = (pos[0] - self.x, pos[1] - self.y)

        crossed_river = self.is_crossed_river()

        if (not crossed_river) and (step == not_crossed_river_step[self.side]):
            return True

        if crossed_river and (step in crossed_river_step[self.side]):
            return True

        return False

    def is_crossed_river(self):
        if (self.side == ChessSide.RED) and (self.y > 4):
            return True

        if (self.side == ChessSide.BLACK) and (self.y < 5):
            return True

        return False

    def create_moves(self):
        moves = []
        curr_pos = (self.x, self.y)
        for x in range(9):
            for y in range(10):
                if self.x == x and self.y == y:
                    continue
                moves.append((curr_pos, (x, y)))
        return filter(self.board.is_valid_move_t, moves)
