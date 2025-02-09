import numpy as np


def create_test_data():
    np_array = np.zeros([100, 500, 5000])
    return np_array


def main():
    test_data = create_test_data()
    print(test_data.shape)
    print(test_data[0, :, :].shape)


if __name__ == "__main__":
    main()
