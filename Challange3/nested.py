# Usage : python metadata.py <key>
import sys

def main(obj, key ):
    object = obj
    ks = key
    #loop to traverse to key
    if isinstance(object, dict):
        while True:
            for k, v in object.items():
                if k != ks:
                    if isinstance(v, dict):
                        object = v
            if k == ks:
                break
    #print value of key passed as argument to python pogram.
    print (object.get(ks))

# trigger to main
if __name__ == '__main__':
    key = sys.argv[1]
    object = {"x":{"y":{"z":"a"}}}
    main(object, key)