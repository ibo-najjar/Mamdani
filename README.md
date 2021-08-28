# Mamdani



ANKARA UNIVERSITY FUZZY LOGIC PROJECT



## CONSTRUCTIONS


The rules and their ranges were already given. Therefore, no analysis were performed to form rules. The given rules were simply incorporated into the code in tuple form.
Below, the incorporation of pressure fuzzy sets is given.
### PRESSURRE TRIANGULAR MEMBERSHIP FUNCTION
```
p_vb = (1.75, 1.75, 2.25)
p_b = (1.75, 2.25, 2.5)
p_n = (2.25, 2.75, 3.25)
p_g = (2.5, 3.25, 3.5)
p_vg = (2.75, 4, 4)
```
Then, input values which are temperature and pressure are taken from the user.
After taking the input, the membership values of these input are found. By doing this fuzzification was completed.
Below, the function developed to find the membership of a crisp value to a triangular fuzzy set is given.
```
def membership(memb_func, value):
    if value < memb_func[0]:
        return 0
    elif value > memb_func[2]:
        return 0
    elif value == memb_func[1]:
        return 1
    elif value < memb_func[1]:
        return (value-memb_func[0]) / (memb_func[1]-memb_func[0])
    elif value > memb_func[1]:
        return 1 - ((value-memb_func[1]) / (memb_func[2]-memb_func[1]))
```
Then, the rule matrix was constructed. To do this minimum of membership value of the two inputs was picked as the firing degree of consequent. Then, the maximum values these minimum values for each CO2 concentration set were found. These maximum values show the firing degree of each rule. By doing this Mamdani fuzzy inference was done.
For defuzzification, the center of area method was selected. Instead of an approximate method, the exact centroid of the area was found.In order to find the centroid, firstly the critical points were needed to be found. This was done as follows:
1-The intersection points of adjacent sub-areas(areas bounded by the membership value,x-axis and the membership function) were found. 
2-The α-cuts of consequents were found. Then these two lists of points were merged. 
3-Duplicated points were removed.
4-Among the points with the same x-value and differing µ values, other than the point with the highest µ were removed.
5-The points were sorted in increasing order with respect to x-values.
6-Intersection points previously found which lies beneath(has lower µ than the member points of the line) the lines of other points were removed.
With these steps all critical points of the area was obrained. Since every sub-area is convex
 in itself, their areas, centroids and centroids multiplied by area can be calculated. The centroid of the total area is found by the operation:(∑▒〖A×(x ) ̅ 〗)/(∑▒A) The result is the concentration of CO2
Below, the functions used for defuzzification are given:

### Calculates  the mass and the moment  a portion of the final graph
```
def area_and_moment(start_x, start_y, finish_x, finish_y):

    base = finish_x - start_x
    cent_rect = (finish_x + start_x) / 2

    if finish_y > start_y:
        smaller_y = start_y
        larger_y = finish_y
        cent_tri = start_x + 2 / 3 * base
    else:
        smaller_y = finish_y
        larger_y = start_y
        cent_tri = start_x + 1 / 3 * base
    area = smaller_y * base + base * (larger_y - smaller_y) / 2
    area_moment = smaller_y * base * cent_rect + base * (larger_y - smaller_y) / 2 * cent_tri

    return area, area_moment

def defuzzification(points):
    in_func = list()
    for k in points:
        in_func.append(k)
    nominator = 0
    denominator = 0
    for m in range(len(in_func) - 1):
        temp_denom, temp_nom = area_and_moment(in_func[m][0], in_func[m][1], in_func[m + 1][0], in_func[m + 1][1])
        denominator += temp_denom
        nominator += temp_nom

    return nominator / denominator
```


 


