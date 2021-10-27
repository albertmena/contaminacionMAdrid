# cellModel

**Steps in a cell:**
    1/ refresh skills:
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
            

