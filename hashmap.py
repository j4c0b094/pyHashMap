# Import pre-written DynamicArray and LinkedList classes
from ds import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    # === HELPER METHOD(S) ===
    def hash_get_index(self, hash_function, capacity, key):
        """
        Computes the hash via the passed hash function and returns the index
        :param hash_function: A hash function
        :param key: the key to be hashed
        :return: index where the hashed key would reside
        """
        hash = hash_function(key)
        index = hash % capacity
        return index

    def put_modded(self, arr_to_put_in, capacity, key, value):
        # Computing hash and index
        index = self.hash_get_index(self.hash_function, capacity, key)
        linked_list_at_index = arr_to_put_in[index]  # Linked List @ index
        # If the linked list is just the head --> Add new key:val pair
        if linked_list_at_index.length() == 0:
            linked_list_at_index.insert(key, value)
            return 1
        else:
            # Grab a pointer to node that contains key if exists
            key_in = linked_list_at_index.contains(key)
            # If key already in linked list --> Update Value
            if key_in is not None:
                key_in.value = value
                return 0
            # Otherwise collision resolution by chaining to prev node
            else:
                self.size += 1
                size = linked_list_at_index.length()
                size += 1
                linked_list_at_index.insert(key, value)
                return 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change the underlying hash table
        capacity. Returns nothing.
        """
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(LinkedList())
        self.size = 0

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        index = self.hash_get_index(self.hash_function, self.capacity, key)
        linked_list_at_idx = self.buckets[index]
        node_of_interest = linked_list_at_idx.contains(key)
        return None if node_of_interest is None else node_of_interest.value

    def put(self, key: str, value: object) -> None:
        """
        Updates the key / value pair in the hash map. If the key exists then the value of the key
        is updated with new value. If the key is not in the hash map a new key/value pair is added.
        """
        # Computing hash and index
        index = self.hash_get_index(self.hash_function, self.capacity, key)
        linked_list_at_index = self.buckets[index]  # Linked List @ index
        # If the linked list is just the head --> Add new key:val pair
        if linked_list_at_index.length() == 0:
            linked_list_at_index.insert(key, value)
            self.size += 1
        else:
            # Grab a pointer to node that contains key if exists
            key_in = linked_list_at_index.contains(key)
            # If key already in linked list --> Update Value
            if key_in is not None:
                key_in.value = value
            # Otherwise collision resolution by chaining
            else:
                self.size += 1
                # linked_list_at_index.size += 1 # Changed
                size = linked_list_at_index.length()
                size += 1
                linked_list_at_index.insert(key, value)

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If a given
        key is not in the hash map, the method does nothing.
        """
        index = self.hash_get_index(self.hash_function, self.capacity, key)
        linked_list_at_index = self.buckets[index]
        remove_node = linked_list_at_index.contains(key)
        if remove_node is None:
            return
        else:
            linked_list_at_index.remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        index = self.hash_get_index(self.hash_function, self.capacity, key)
        linked_list_at_index = self.buckets[index]  # Linked List @ index

        if linked_list_at_index.contains(key) is not None:
            return True
        else:
            return False

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hashmap
        """
        empty_counter = 0
        for i in range(self.capacity):
            if self.buckets[i].length() == 0:
                empty_counter += 1
        return empty_counter

    def table_load(self) -> float:
        """
        Returns the table load float value ie lambda value of lambda = m/n
        """
        lf = self.size / self.capacity
        return lf

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key / value pairs remain in the new hash
        map and all hash table links are be rehashed. If new_capacity is less than 1, this method does nothing.
        """

        # Do nothing if capacity is < 1
        if new_capacity < 1:
            return

        # New Buckets Array initialized to new capacity
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())

        # Update key/val pair hash index
        new_size_counter = 0
        for _ in range(self.capacity):
            # Iterate through the current buckets array
            linked_list = self.buckets[_]
            # If there is nothing in the bucket -> Do nothing
            if linked_list.length() == 0:
                continue

            for node in linked_list:
                new_size_counter += self.put_modded(
                    new_buckets, new_capacity, node.key, node.value)
        self.buckets = new_buckets
        self.size = new_size_counter
        self.capacity = new_capacity

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray that contains all keys stored in your hash map. Theorder of the keys in the DA does not
        matter.
        """
        key_da = DynamicArray()

        for _ in range(self.buckets.length()):
            linked_list_at_iter = self.buckets[_]
            if linked_list_at_iter.length() == 0:
                continue
            else:
                for node in linked_list_at_iter:
                    key_da.append(node.key)
        return key_da


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    print("emp lf size cap")
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print("emp lf key contains")
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
