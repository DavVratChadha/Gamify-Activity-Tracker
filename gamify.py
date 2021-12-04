#Project 1: Gamification
#By Dav Vrat Chadha and Mehul Bhardwaj

def initialize():
    """Initialize all the global variable"""
    global total_health_points
    total_health_points = 0
    global temp_points #temporary points
                        #useful for most_fun_activity_minute()
    temp_points = 0
    global total_hedons
    total_hedons = 0
    global run_minutes #minutes user runs without changing activity
    run_minutes = 0
    global prev_act
    prev_act = "" #Activity has started now and not earlier
    global prev_points
    prev_points = 0 #Points for previous activity
    global rest_time #time for which the user rested before starting another activity
    rest_time = 0
    global timeline #For recording time at which stars were offered
    timeline = list()
    global curr_time #current time that has just passed
    curr_time = 0
    global star_available
    star_available = False #No star available at start
    global star_activity #Activity for which star has been offered
    star_activity = ""
    global bored
    bored = False #User not bored in the beginning
    global temp_hedons #temporary hedons
                        #useful for most_fun_activity_minute()
    temp_hedons = 0
    global num_act #number of activities performed
    num_act = 0
    global r_num #number of times user has rested
                #useful in check_tired()
    r_num = 0
    return



def perform_activity(activity, duration):
    """Simulate the user’s performing activity activity for the duration"""
    global curr_time
    global star_available
    global star_activity
    global temp_hedons
    global total_hedons
    global prev_act
    global total_health_points
    global temp_points
    global prev_points
    global rest_time
    global num_act
    global r_num


    if activity == "running":#if the person ran
        curr_time += duration
        run(duration)
        rest_time = 0
        if prev_act == "running":
            prev_points += temp_points
        else:
            prev_points = temp_points
        star_available = False
        #Star no longer available as activity has ended
        star_activity = ""
        total_hedons += temp_hedons
        temp_hedons = 0
        total_health_points += temp_points
        temp_points = 0
        prev_act = activity
        num_act += 1

    elif activity == "textbooks":
        curr_time += duration
        carry_books(duration)
        prev_points = temp_points
        rest_time = 0
        star_available = False
        #Star no longer available as activity has ended
        star_activity = ""
        total_hedons += temp_hedons
        temp_hedons = 0
        total_health_points += temp_points
        temp_points = 0
        prev_act = activity
        num_act += 1

    elif activity == "resting":
        curr_time += duration
        rest(duration)
        prev_points = 0
        rest_time += duration
        star_available = False
        #Star no longer available as activity has ended
        star_activity = ""
        total_hedons += temp_hedons
        temp_hedons = 0
        total_health_points += temp_points
        temp_points = 0
        prev_act = activity
        r_num += 1
        num_act += 1

    return

def run(duration):
    """Reward points based upon the duration of running."""
    #global because value is being altered
    global run_minutes
    global temp_points
    global prev_act
    global prev_points
    global temp_hedons
    global star_available
    global star_activity
    global bored

    if bored == False:
        if star_available == True and star_activity == "running":
            if duration <= 10:
                temp_hedons += 3 * duration
            else:
                temp_hedons += 3 * 10

    tired = check_tired()
    if tired == True: #User tired
        temp_hedons += -2 * duration

    elif tired == False:#User not tired
        if duration <= 10:
            temp_hedons += 2 * duration
        else:
            temp_hedons += 2 * 10 - 2 * (duration - 10)


    if prev_act == "running": #Same activity has been done
        run_minutes += duration #run_minutes adding up
        already_given_points = prev_points
        if run_minutes <= 180:
            temp_points += 3 * run_minutes - already_given_points
            #Subtracting already_given_points because they had been awarded last time
        elif run_minutes > 180:
            temp_points += 3 * 180 + 1 * (run_minutes - 180) - already_given_points

    else: #Different activity was done last time
        already_given_points = 0 #for running
        run_minutes = duration

        if run_minutes <= 180:
            temp_points += 3 * run_minutes - already_given_points
            #Subtracting already_given_points because they had been awarded last time
        elif run_minutes > 180:
            temp_points += 3 * 180 + 1 * (run_minutes - 180) - already_given_points

    return

def carry_books(duration):
    """Reward points based upon the duration of carrying textbooks."""
    #global because value is being altered
    global temp_points
    global temp_hedons
    global star_available
    global star_activity
    global bored

    if bored == False:
        if star_available == True and star_activity == "textbooks":
            if duration <= 10:
                temp_hedons += 3 * duration
            else:
                temp_hedons += 3 * 10


    tired = check_tired()
    if tired == True: #User tired
        temp_hedons += -2 * duration

    elif tired == False:#User not tired
        if duration <= 20:
            temp_hedons += 1 * duration
        else:
            temp_hedons += 1 * 20 - 1 * (duration - 20)

    temp_points = 2 * duration
    return

def rest(duration):
    """Reward points based upon the duration of resting."""
    global temp_points
    global temp_hedons

    temp_points = 0 * duration
    temp_hedons = 0 * duration
    return

def check_tired():
    """Return True if the user is tired"""
    global prev_act
    global rest_time
    global num_act
    global r_num

    if prev_act == "resting" and (rest_time >= 120 or num_act == r_num):
        return False #User not tired
    elif prev_act == "":
        return False #User not tired
    else:
        return True #User is tired

def get_cur_hedons():
    """Return the number of hedons that the user has gained so far."""
    global total_hedons
    return total_hedons

def get_cur_health():
    """Return the number of health points that the user has gained so far."""
    global total_health_points
    return total_health_points

def offer_star(activity):
    """Simulate an offer to the user, a star, for engaging in the exercise activity"""
    global timeline
    global star_available
    global curr_time
    global star_activity
    global bored

    star_available = True
    timeline.append(curr_time) #star was offered just now
    star_activity = activity

    if len(timeline) >= 3 and bored == False:
        #2 stars have been previously offered
        time_passed = curr_time - timeline[-3]
        if time_passed < 120:
            bored = True #3 Stars have been offered in two hours
        elif time_passed >= 120:
            bored = False
    return


def star_can_be_taken(activity):
    """Return True iff a star can be used to get more hedons for the activity."""
    global star_available
    global star_activity
    global bored

    if star_available == False or bored == True:#No star has been offered
        return False
    else: #Star has been offered
        if activity == star_activity:
            return True
        else: #star was not offered for this activity
            return False

def most_fun_activity_minute():
    """Return the activity that would give the maximum number of hedons if the person performed it for one minute at the current time."""
    global temp_hedons
    global run_minutes
    global temp_points

    #To find the number of hedons that would be awarded by a\
    #activity, we call the three activity functions with\
    #duration = 1 run_minutes as parameter
    temp_hedons = 0
    run(1)
    hedon_from_running = temp_hedons
    temp_hedons = 0
    carry_books(1)
    hedon_from_textbooks = temp_hedons
    temp_hedons = 0
    rest(1)
    hedon_from_resting = temp_hedons
    temp_hedons = 0
    temp_points = 0
    run_minutes -= 1
    #because calling the run(1) increases run_minutes value by 1
    if hedon_from_running >= hedon_from_textbooks:
        if hedon_from_running >= hedon_from_resting:
            return "running"
        else:
            return "resting"
    elif hedon_from_textbooks >= hedon_from_resting:
        return "textbooks"
    else:
        return "resting"