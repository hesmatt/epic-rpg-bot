import globals_


def get_count_of_item_in_inventory(item):
    count = 0
    if item in globals_.items:
        count = int(globals_.items[item])
        return count

    return count


def get_count_of_consumables_in_inventory(consumable):
    count = 0
    if consumable in globals_.consumables:
        count = int(globals_.consumables[consumable])
        return count

    return count
