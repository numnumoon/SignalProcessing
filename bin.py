import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input_file", type=str, default="C:\\Users\\takum\\Desktop\\SignalProcessing\\output_16bit_le.bin")
    parser.add_argument("--output_file", type=str, default="C:\\Users\\takum\\Desktop\\SignalProcessing\\output2.bin")
    
    return parser.parse_args()


def overwrite(args):
    new_array = []
    with open(args.input_file, "rb") as file:
        for _ in range(3):
            header = file.read(16)
            
            binary_data = file.read(100)
            # 2バイトずつリトルエンディアンで整数を読む
            data = [int.from_bytes(binary_data[i:i+2], byteorder='little')
                    for i in range(0, 100, 2)]
            # 値が5未満のものを5に書き換える
            data = [max(value, 5) for value in data]
            
            footer = file.read(8)
            
            new_array.append({
                "header": header,
                "data": data,
                "footer": footer
            })
    return new_array

def write_binary_file(args, new_array):
    with open(args.output_file, 'wb') as file:
        for data in new_array:
            file.write(data["header"])
            for value in data["data"]:
                file.write(value.to_bytes(2, byteorder='little', signed=False))
            file.write(data["footer"])

        
def main():
    args = parse_arguments()
    new_array = overwrite(args)
    #print(new_array)
    write_binary_file(args, new_array)

if __name__ == "__main__":
    main()