# testr

if 0:
    foods = [1,2,3,4,5,6,7,8,9]

    print(foods)

    food_del = [3,5,7]
    for idx in sorted(food_del, reverse=True):
        del foods[idx]

    print(foods)

if 0:
    elitism_num = int(math.floor(params['elitism'] * params['pop_size']))
    new_orgs = params['pop_size'] - elitism_num

    stats = defaultdict(int)
    for org in past_agents:
        if org.fitness > stats['BEST'] or stats['BEST'] == 0:
            stats['BEST'] = org.fitness

        if org.fitness < stats['WORST'] or stats['WORST'] == 0:
            stats['WORST'] = org.fitness

        stats['SUM'] += org.fitness
        stats['COUNT'] += 1

    stats['AVG'] = stats['SUM'] / stats['COUNT']
