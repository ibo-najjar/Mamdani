
# Finds where two membership functions intersect
def finish_point(memb1, highest_point1, memb2, highest_point2):
    inter_x = 0
    inter_mu = 0
    if memb1 >= 0.5 and memb2 >= 0.5:
        inter_x = (highest_point1 + highest_point2) / 2
        inter_mu = 0.5
    elif memb1 >= memb2:
        inter_x = highest_point2 + memb1 - 1
        inter_mu = memb2
    elif memb1 < memb2:
        inter_x = highest_point2 + memb1 - 1
        inter_mu = memb1
    return inter_x, inter_mu


# Calculates  the mass and the moment  a portion of the final graph
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


# Finds the cut-off points for alpha_cuts
def alpha_cuts(memb_func, mu):
    if memb_func[0] == memb_func[1]:
        val1 = memb_func[0]
    else:
        val1 = memb_func[0] + mu
    if memb_func[1] == memb_func[2]:
        val2 = memb_func[2]
    else:
        val2 = memb_func[1] + 1 - mu
    return val1, val2


# Finds the membership value of a x value for a specific membership function.
# For example temperature has a membership value of 0.5 for very high etc.
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


# Takes the all critical points of the area. Then, sends them to the function  "area_and_moment" step by step
# where the sub-areas and their effect to the location of the centroid of the general shape are found.
# Finally returns the x value of the centroid. This x value is the concentration of Carbon Dioxide.
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


# Triangular membership functions for temperature
t_vc = (7, 7, 9)
t_c = (7, 9, 11)
t_n = (10, 12, 14)
t_h = (12, 14, 16)
t_vh = (13, 16, 16)

t_combined = [t_vc,
              t_c,
              t_n,
              t_h,
              t_vh]

# Triangular membership functions for pressure
p_vb = (1.75, 1.75, 2.25)
p_b = (1.75, 2.25, 2.5)
p_n = (2.25, 2.75, 3.25)
p_g = (2.5, 3.25, 3.5)
p_vg = (2.75, 4, 4)

p_combined = [p_vb,
              p_b,
              p_n,
              p_g,
              p_vg]

# Triangular membership functions for CO2

c_vb = (2, 2, 3)
c_b = (2, 3, 4)
c_n = (3, 4, 5)
c_g = (4, 5, 6)
c_vg = (5, 6, 6)

# Input is taken here
degree_sign = u"\N{DEGREE SIGN}"

while True:
    temperature = -100
    pressure = -100
    while temperature < 7 or temperature > 16 or pressure < 1.75 or pressure > 4:
        print("Please enter the temperature(It must be between 7{degree}C and 16{degree}C)".format(degree=degree_sign))
        try:
            temperature = float(input())
        except:
            print("You need to write the numbers correctly. Please try again.")
            continue
        if temperature < 7 or temperature > 16:
            print("The temperature value is out of acceptable range. Please try again.")
            continue
        print("Please enter the pressure(It must be between 1.75 bars and 4 bars)")
        try:
            pressure = float(input())

        except:
            print("You need to write the numbers correctly. Please try again.")
            continue
        if pressure < 1.75 or pressure > 4:
            print("The pressure value is out of acceptable range. Please try again.")
            continue

    # memberships of axes
    temp_memberships = list()
    press_memberships = list()

    # Count of rules
    no_temp_rules = 5
    no_press_rules = 5

    # Membership values of the input
    for i in range(no_temp_rules):
        temp_memberships.append(membership(t_combined[i], temperature))

    for i in range(no_press_rules):
        press_memberships.append(membership(p_combined[i], pressure))

    # CO2 rule matrix
    co_rule_matrix = list()
    for i in range(no_temp_rules):
        co_rule_matrix.append([])

    for i in range(no_temp_rules):
        for j in range(no_press_rules):
            co_rule_matrix[i].append(min(press_memberships[i], temp_memberships[j]))

    # CO2 membership values

    co_membership = list()

    co_very_bad = co_rule_matrix[0][4]
    co_membership.append(co_very_bad)

    co_bad_first_row = max(co_rule_matrix[0][1:3])
    co_bad_second_row = max(co_rule_matrix[1][3:])
    co_bad_absolute = max(co_bad_first_row, co_bad_second_row)
    co_membership.append(co_bad_absolute)

    co_normal_first_row = co_rule_matrix[0][0]
    co_normal_second_row = max(co_rule_matrix[1][0], co_rule_matrix[1][2])
    co_normal_third_row = max(co_rule_matrix[2][2:])
    co_normal_fourth_row = max(co_rule_matrix[3][3:])
    co_normal_absolute = max(co_normal_first_row, co_normal_second_row, co_normal_third_row, co_normal_fourth_row)
    co_membership.append(co_normal_absolute)

    co_good_second_row = co_rule_matrix[1][1]
    co_good_third_row = max(co_rule_matrix[2][0:2])
    co_good_fourth_row = max(co_rule_matrix[3][1:3])
    co_good_fifth_row = max(co_rule_matrix[4][3:])
    co_good_absolute = max(co_good_second_row, co_good_third_row, co_good_fourth_row, co_good_fifth_row)
    co_membership.append(co_good_absolute)

    co_very_good_fourth_row = co_rule_matrix[4][0]
    co_very_good_fifth_row = max(co_rule_matrix[4][:3])
    co_very_good_absolute = max(co_very_good_fourth_row, co_very_good_fifth_row)
    co_membership.append(co_very_good_absolute)

    # CO2 membership functions

    co_vb = (2, 2, 3)
    co_b = (2, 3, 4)
    co_n = (3, 4, 5)
    co_g = (4, 5, 6)
    co_vg = (5, 6, 6)

    co_combined = [
        co_vb,
        co_b,
        co_n,
        co_g,
        co_vg]

    # Here where two adjacent areas intersect is found for each intersection
    intersections = list()

    for i in range(len(co_combined) - 1):
        curr = finish_point(co_membership[i], co_combined[i][1], co_membership[i + 1], co_combined[i + 1][1])
        intersections.append(curr)

    # Here alpha-cuts are found.
    max_mu = list()

    for i in range(len(co_membership)):
        new_points = alpha_cuts(co_combined[i], co_membership[i])
        first_new_point = (new_points[0], co_membership[i])
        second_new_point = (new_points[1], co_membership[i])
        max_mu.append(first_new_point)
        max_mu.append(second_new_point)

    # Here alpha-cuts and intersections are merged.
    final_list_of_points = list()

    for i in intersections:
        final_list_of_points.append(i)

    for i in max_mu:
        final_list_of_points.append(i)

    # Here Duplicate points are removed.
    flag = 1

    while flag != 0:
        flag = 0
        for i in range(len(final_list_of_points) - 1):
            temp_list = final_list_of_points[:i] + final_list_of_points[i + 1:]
            temp_element = final_list_of_points[i]
            if temp_element in temp_list:
                final_list_of_points.pop(i)
                flag = 1
                break

    # Here among the points which have the same x value only the point with the highest membership
    # function remains and the rest is removed.
    flag = 1
    while flag != 0:
        flag = 0
        for i in range(len(final_list_of_points) - 1):
            for j in range(i + 1, len(final_list_of_points)):
                if final_list_of_points[i][0] == final_list_of_points[j][0]:
                    if final_list_of_points[i][1] >= final_list_of_points[j][1]:

                        final_list_of_points.pop(j)
                        flag = 1
                        break

                    else:
                        final_list_of_points.pop(i)
                        flag = 1
                        break
            if flag == 1:
                break
    # Here the points are sorted.
    for i in range(len(final_list_of_points) - 1):
        for j in range(i + 1, len(final_list_of_points)):
            if final_list_of_points[i][0] > final_list_of_points[j][0]:
                hold = final_list_of_points[j]
                final_list_of_points[j] = final_list_of_points[i]
                final_list_of_points[i] = hold

    # Here previous intersection points which are beneath current alpha-cuts are removed.
    flag = 1
    while flag != 0:
        flag = 0

        for i in range(len(final_list_of_points) - 2):
            for j in range(i+2, len(final_list_of_points)):
                if final_list_of_points[i][1] == final_list_of_points[j][1] and final_list_of_points[i][1] > 0:
                    if final_list_of_points[i+1][1] == 0:
                        final_list_of_points.pop(i+1)
                        flag = 1
                        break

    # Here the concentration is found.
    concentration = defuzzification(final_list_of_points)
    print("The concentration of Carbon Dioxide is {:.3f}%".format(concentration))
    print("Press q to quit.")
    print("Press any other key to continue")
    will_quit = input()
    # The user decides whether he/she wants to quit the program or not
    if will_quit == 'q' or will_quit == 'Q':
        break
