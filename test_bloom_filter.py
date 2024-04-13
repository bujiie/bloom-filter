import unittest

from bloom_filter import calculate_signature, build_bloom_filter, bit_array_to_bin, coalesce_bloom_filters

k = 5


class TestBloomFilter(unittest.TestCase):

    def test_empty_signature_returned_if_k_eq_0(self):
        subject = "subjectA"
        signature = calculate_signature(subject, k=0, bits_set=[])
        self.assertTrue(len(signature) == 0)

    def test_deterministic_signature_can_be_calculated(self):
        subject = "subjectA"
        signature_a = calculate_signature(subject, k, [])
        signature_b = calculate_signature(subject, k, [])
        self.assertEqual(signature_a, signature_b)

    def test_unique_signature_can_be_calculated(self):
        subject_a = "subjectA"
        subject_b = "subjectB"
        signature_a = calculate_signature(subject_a, k, [])
        signature_b = calculate_signature(subject_b, k, [])
        self.assertNotEquals(signature_a, signature_b)

    def test_building_bloom_filter_from_signature(self):
        signature = [1, 3, 5]
        bloom_filter = build_bloom_filter(signature)
        self.assertTrue(bloom_filter[signature[0]])
        self.assertTrue(bloom_filter[signature[1]])
        self.assertTrue(bloom_filter[signature[2]])
        bloom_filter[signature[0]] = 0
        bloom_filter[signature[1]] = 0
        bloom_filter[signature[2]] = 0
        self.assertEqual(0, bit_array_to_bin(bloom_filter))

    def test_bit_array_can_be_converted_to_binary(self):
        bit_arrays = [
            ([0, 0, 0], 0),
            ([0, 1, 0], 2),
            ([1, 0, 1], 5)
        ]
        for bit_array in bit_arrays:
            value = bit_array_to_bin(bit_array[0])
            self.assertEqual(bit_array[1], value)

    def test_coalesce_bloom_filters(self):
        signature_a = [1]
        signature_b = [3, 5]
        bloom_filter = coalesce_bloom_filters([signature_a, signature_b])
        self.assertTrue(bloom_filter[signature_a[0]])
        self.assertTrue(bloom_filter[signature_b[0]])
        self.assertTrue(bloom_filter[signature_b[1]])
        bloom_filter[signature_a[0]] = 0
        bloom_filter[signature_b[0]] = 0
        bloom_filter[signature_b[1]] = 0
        self.assertEqual(0, bit_array_to_bin(bloom_filter))


if __name__ == '__main__':
    unittest.main()

