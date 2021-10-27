import time
import numpy as np
import matplotlib.pyplot as plt #tutorial: http://pybonacci.org/2012/05/19/manual-de-introduccion-a-matplotlib-pyplot-ii-creando-y-manejando-ventanas-y-configurando-la-sesion/
import threading
from random import shuffle


T = 1
eps = 0.000000001
agilityMin = 1/T

'''------------GOVERMENT'''
class Goverment:
    ''' manage population '''
    def __init__(self ):
        self.listID = []
        self.listCells = []
        self.globalTime = 0

    def createPopulation(self, position, map, agility, smellInstinct):
        if  map.createCell(position) == False:
            return False
        else:
            IDx = len(self.listID)
            self.listID.append(IDx)
            self.listCells.append(MotherCell(IDx, goverment_i.globalTime, position, agility, smellInstinct, 5, 5, [10, 10], 5))
                        #(ID, time, positio n, agility, smellInstinct, reproduction, mutability, feeds, mortality)
            return True

    def retirePopulation (self, IDx):
        self.listID[IDx] = 0 #instancia cell no esta borrada creo

    def clock(self):
        self.globalTime += T


'''------------MAP'''
class Map:
    '''manage map(x,y); collision, edges, plot...
     map as 3dim matrix, (row, col, feeds (numfeeds + 1/0 if cell in position)
     cell in position: [N][[N][pos, feed1, feed2, feed3, feed4, feed5]
     '''
    def __init__(self,  size, num_feeds):
        self.size = size
        self.map_cells = np.zeros((self.size,  self.size)) #ncluye posicion celula

    def available(self, position):
        #position as row/col
        #return True if occupy
        row = position[0]
        col = position[1]
        if row < 0 or row > (self.size - 1) or col < 0 or col > (self.size - 1):
            return False
        elif self.map_cells[row, col] == 1:
            return False
        else:
            return True

    def moveInMap(self, actual_position, position):
        if actual_position == position:
            return True
        if self.available(position):
            self.map_cells[position[0]][position[1]] = 1
            self.map_cells[actual_position[0]][actual_position[1]] = 0
            return True
        else:
            return False

    def createCell(self, pos):
        if self.map_cells[pos[0]][pos[1]] == 1:
            return False
        else:
            self.map_cells[pos[0]][pos[1]] = 1
            return True

    def ploting(self):
        plt.ion()
        plt.figure()
        #plt.matshow(nature_i.map_feeds[0], fignum=1, cmap=plt.cm.gray)
        while True:
            f1 = plt.subplot2grid((2, 2), (0, 0))
            f2 = plt.subplot2grid((2, 2), (0, 1))
            f3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)
            f1.matshow(nature_i.map_feeds[0], cmap=plt.cm.gray, vmin=0, vmax=nature_i.abundance)
            f2.matshow(nature_i.map_feeds[1], cmap=plt.cm.gray, vmin=0, vmax=nature_i.abundance)
            f3.matshow(self.map_cells, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
            plt.draw()
            plt.pause(0.05)

'''------------NATURE'''
class Nature:
    '''manage feed seeds, delete feeds (eat by cells)'''
    def __init__(self, abundance, num_feeds, size):
        self.abundance = abundance
        self.num_feeds = num_feeds
        self.feeds = 0
        self.size = size
        map_feed_size = np.zeros((self.num_feeds, self.size,  self.size))#incluye recusros de celda
        self.map_size = map_feed_size.shape
        self.map_feeds = np.random.randint(0, self.abundance, size = self.map_size)

    def deleteFeed(self, position, feed):
        map_i.map_feeds[feed][position[0]][position[1]] =\
            map_i.map_feeds[feed][position[0]][position[1]] - 1#lo ultimo la columna siempre

    def createFeed(self, position, feed):
        map_i.map_feeds[feed][position[0]][position[1]] = \
            map_i.map_feeds[feed][position[0]][position[1]] + 1


'''------------CELLS'''
class MotherCell:
    '''
    Steps in a cell:
        1/ update skills:
            - hungry(feeds)
            - mutability(feeds)
            - reproductibility(feeds, time)
            - mortality (feeds, time)
        2/ check reproduction:
                True: create cell with actual mutability skill, use feeds
                False: pass
        3/ check food:
                check hungry:
                    True: calculate distance with smell:
                        distance = 0: eat(feeds)
                        distance > 0: move (x, y time) use feeds
        4/ check dead(feeds, time):
                True: dead
                False: pass

    '''
    def __init__(self,ID, time, position, agility, smellInstinct, reproduction, mutability, feeds, mortality):
        self.ID = ID
        self.localTime = goverment_i.globalTime - time
        self.position = position
        #Skills
        self.agility = agilityMin *  agility# agility 0--5
        self.smellInstinct = smellInstinct # from 0 to 10, radious of smeelled cels
        self.mutability = mutability # from 0 to 10
        self.mortality = mortality # from 0 to 10
        self.reproduction = reproduction
        self.feeds = feeds #[0, 0] from 0 to 10
        self.sweep = self.sweep()# created the sweep list with smellInstinct radious
        self.moving = False
        self.virtualPos = self.position

    '''------------------------'''
    def updateStates(self):
        #states
        self.liveBar = sum(self.feeds) / len(self.feeds)#if liveBar - mortality == 0 => dead
        self.hungry = self.liveBar - self.mortality
        self.burnFood()
        self.food(self.feeds, self.instinct, self.hungry)
        self.reproduction(self.mutability, self.feeds)
        self.dead(self.liveBar, self.mortality, self.ID)

    def reproduction(self):
        #mutability, feeds, time?
        pass

    def food(self):
        #feeds, instinct
        if self.hungry >= 4:
            self.smell()
        else:
            pass

    def burnFood(self):
        if self.localTime % 1 == 0:
            for i, x in enumerate(self.feeds):
                self.feeds[i] = x - 1

    def dead(self):
        #mortality
        if self.liveBar - self.mortality == 0:
            goverment_i.retirePopulation(self.ID)

    '''------------------------'''
    def smell(self):
        for smellingPos in self.sweep:
            pos = (self.position[0] + smellingPos[0], self.position[1] + smellingPos[1])
            if not (pos[0] < 0 or pos[1] < 0 or pos[0] >= map_i.size or pos[1] >= map_i.size):
                for i in range(len(self.feeds)):
                    feeds = nature_i.map_feeds[i][int(pos[0])][int(pos[1])]
                    if feeds != 0:
                        self.move(pos)
                        if map_i.moveInMap(self.position, self.virtualPos) is not True:
                            return
                        else:
                            self.eat((i, pos[0], pos[1]), nature_i)
                            self.position = self.virtualPos
                            # print('position: {}, virtualPos: {}feed({}) remain: {}. sweep: {}'.format(
                            #     self.position,self.virtualPos, i, feeds, smellingPos))
                        time.sleep(0.0005)
                        return


    def move(self, position_smelled):
        #manage agility
        direct = (position_smelled[0] - self.position[0], position_smelled[1] - self.position[1])
        self.virtualPos = (self.position[0] + (T * self.agility)* direct[0],
                           self.position[1] + (T * self.agility)* direct[1])
        self.virtualPos = int(round(self.virtualPos[0],0)), int(round(self.virtualPos[1],0))


    def eat(self, food, nature_i):#food = (feed, pos, pos)
        self.feeds[food[0]] += 1
        nature_i.map_feeds[food[0]][food[1]][food[2]] -= 1


    def sweep(self):
        sweep = []
        signo = 1;
        SW = (0, 1);
        j = 1;
        sweep = [(0, 0), (0, 1)]
        iterations = (self.smellInstinct*2) + 1
        iterations = (iterations * 2) + ((iterations - 2) * 2)
        for i in range(1, iterations):
            if i % 2 != 0:
                signo = signo * (-1)
                row = 1;
                col = 0
                row = row * signo;
                col = col * signo
                for x in range(j):
                    SW = (SW[0] + row, SW[1] + col)
                    sweep.append(SW)
            if i % 2 == 0:
                j = j + 1
                row = 0;
                col = 1;
                row = row * signo;
                col = col * signo
                for x in range(j):
                    SW = (SW[0] + row, SW[1] + col)
                    sweep.append((SW))

        shuff = sweep[1:8]
        shuffle(shuff)
        sweep = [sweep[0]] + shuff + sweep[8:]
        return sweep


'''-----------MAIN'''
if __name__ == '__main__':

    goverment_i = Goverment()
    num_feeds = 2
    size = 70
    abundance = 3
    nature_i = Nature(3, num_feeds, size)#abundance and number of feeds
    map_i = Map(size, num_feeds)#size, num of feeds
    goverment_i.clock()

    goverment_i.createPopulation((5, 5), map_i, 1, 5)#position, map, agility, smellInstict
    goverment_i.createPopulation((20, 20), map_i, 2, 2)
    goverment_i.createPopulation((40, 40), map_i, 3, 4)

    t_map_feeds = threading.Thread(target=map_i.ploting)
    print ("Iniciada la vida")
    print ("Cell position: ", goverment_i.listCells[0].position)
    print ("Cell position: ", goverment_i.listCells[1].position)
    print ("Cell position: ", goverment_i.listCells[2].position)

    t_map_feeds.start()
    time.sleep(1)
    for x in range(30000):
        goverment_i.listCells[0].smell()
        goverment_i.listCells[1].smell()
        goverment_i.listCells[2].smell()
        time.sleep(0.005)
