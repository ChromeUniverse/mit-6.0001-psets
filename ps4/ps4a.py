# Problem Set 4A
# Name: Lucca Rodrigues
# Collaborators: N/A
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    perms = []

    # base case: single-character sequence
    if (len(sequence) == 1):
        return [sequence]

    # recursive case
    for i in range(len(sequence)):
        # strip current character, run recursively
        char = sequence[i]
        spliced_sequence = sequence[:i] + sequence[i+1:]
        sub_perms = get_permutations(spliced_sequence)

        # add stripped character back in,
        # concatenate list of permutations
        perms += [(char + perm) for perm in sub_perms]

    return perms


def test_get_permutations(input, expected_output):
    '''
    Runs a test case for `get_permutations`.

    `input` (string): the input sequence.

    `expected_output` (list of string): the expected list of permutations for the input sequence.
    '''

    print('Input:', input)
    print('Expected Output:', expected_output)
    print('Actual Output:', get_permutations(input), '\n')

    return


if __name__ == '__main__':
    #    #EXAMPLE
    #    example_input = 'abc'
    #    print('Input:', example_input)
    #    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    #    print('Actual Output:', get_permutations(example_input))

    #    # Put three example test cases here (for your sanity, limit your inputs
    #    to be three characters or fewer as you will have n! permutations for a
    #    sequence of length n)

    # test cases
    input_1 = 'cat'
    expected_output_1 = ['cat', 'cta', 'act', 'atc', 'tca', 'tac']
    input_2 = 'dog'
    expected_output_2 = ['dog', 'dgo', 'odg', 'ogd', 'gdo', 'god']
    input_3 = 'mit'
    expected_output_3 = ['mit', 'mti', 'imt', 'itm', 'tmi', 'tim']

    # run test cases
    test_get_permutations(input_1, expected_output_1)
    test_get_permutations(input_2, expected_output_2)
    test_get_permutations(input_3, expected_output_3)
