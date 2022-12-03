#!/usr/bin/env python3.8
# https://adventofcode.com/2022/day/2

from sys import argv

class Move:
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'

class Result:
    WIN = 6
    DRAW = 3
    LOSE = 0

class MoveQ1:
    def __init__(self, label):
        map = {
            'A': Move.ROCK,
            'X': Move.ROCK,
            'B': Move.PAPER,
            'Y': Move.PAPER,
            'C': Move.SCISSORS,
            'Z': Move.SCISSORS,
        }
        self.move = map[label]

    def result(self, them):
        if them.move == self.move:
            return Result.DRAW

        if them.move == Move.ROCK:
            if self.move == Move.PAPER:
                return Result.WIN
            return Result.LOSE

        if them.move == Move.PAPER:
            if self.move == Move.SCISSORS:
                return Result.WIN
            return Result.LOSE

        if self.move == Move.ROCK:
            return Result.WIN
        return Result.LOSE

    def points(self, them):
        move_point = {Move.ROCK: 1, Move.PAPER: 2, Move.SCISSORS: 3}[self.move]
        return self.result(them) + move_point

    def __repr__(self):
        return self.move


class GameQ2:
    def __init__(self, them, result):
        self.them = {
            'A': Move.ROCK,
            'B': Move.PAPER,
            'C': Move.SCISSORS,
        }[them]
        self.desiredResult = {
            'X': Result.LOSE,
            'Y': Result.DRAW,
            'Z': Result.WIN,
        }[result]

    def correctMove(self):
        if self.desiredResult == Result.DRAW:
            return self.them

        if self.them == Move.ROCK:
            if self.desiredResult == Result.WIN:
                return Move.PAPER
            return Move.SCISSORS

        if self.them == Move.PAPER:
            if self.desiredResult == Result.WIN:
                return Move.SCISSORS
            return Move.ROCK

        if self.desiredResult == Result.WIN:
            return Move.ROCK
        return Move.PAPER

    def points(self):
        move = self.correctMove()
        move_point = {Move.ROCK: 1, Move.PAPER: 2, Move.SCISSORS: 3}[move]
        return self.desiredResult + move_point

    def __repr__(self):
        return self.move


def parse(input):
    games = []
    for line in input:
        games.append(line.split(' '))
    return games


def q1(input):
    games = [(MoveQ1(game[0]), MoveQ1(game[1])) for game in parse(input)]
    results = [game[1].points(game[0]) for game in games]
    return sum(results)


def q2(input):
    games = [GameQ2(game[0], game[1]) for game in parse(input)]
    results = [game.points() for game in games]
    return sum(results)

with open(argv[1], 'r') as f:
    print(q2([l.strip() for l in f]))
