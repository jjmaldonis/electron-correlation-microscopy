from utilities import load_pixel_positions
pixel_positions = load_pixel_positions()

i = 1
count = 0
f = open("inputs{}.in".format(i), "w")
for x,y in pixel_positions:
    f.write("{} {}\n".format(x, y))
    count += 1
    if count >= 10000:
        print("Wrote to 'inputs{}.in'".format(i))
        i += 1; count = 0; f.close()
        f = open("inputs{}.in".format(i), "w")
f.close()
print("Wrote to 'inputs{}.in'".format(i))
